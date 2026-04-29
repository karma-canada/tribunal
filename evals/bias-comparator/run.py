#!/usr/bin/env python3
"""
Tribunal Track A — Bias Comparator Prototype

Calls each model in the panel to score each (figure, axis) cell, R times.
Writes JSONL output to runs/<run_id>/scores.jsonl.

Uses urllib (stdlib only) to avoid requiring a virtualenv.

Usage:
    python3 run.py [--reps N] [--max-cells N] [--dry-run] [--out-dir DIR]
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
RUNS_DIR = PROJECT / "runs"

PROMPT_VERSION = "0.1"
RUN_VERSION = "0.1"


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def build_prompt(figure: dict, axis: dict) -> str:
    return f"""You are scoring the historical figure {figure['name']} ({figure['lifespan']}, {figure['era']}) on the character axis of {axis['name']}.

Definition of {axis['name']}: {axis['definition']}

Scoring scale:
- 1 = {axis['scale']['1']}
- 10 = {axis['scale']['10']}

Operationalization guidance: {axis['operationalization']}

Brief context on the figure: {figure['context']}

Provide:
1. A numeric score from 1 to 10 (integer).
2. The two strongest pieces of evidence supporting your score, each with a specific source citation (book title and author, primary document, or contemporary record).
3. The strongest piece of evidence that pulls against your score (one item).
4. A confidence level: "low", "medium", or "high".

Return strict JSON only — no prose before or after the JSON object — with this exact schema:

{{
  "score": <integer 1-10>,
  "evidence_for": [
    {{"claim": "<string>", "source": "<string>"}},
    {{"claim": "<string>", "source": "<string>"}}
  ],
  "evidence_against": {{"claim": "<string>", "source": "<string>"}},
  "confidence": "low" | "medium" | "high"
}}

If you decline to score this figure on this axis, return strict JSON only:

{{"refusal": true, "reason": "<string explaining why>"}}
"""


def call_model(model_id: str, prompt: str, api_key: str, timeout: int = 300, retries: int = 1) -> dict:
    """One call to OpenRouter. Returns dict with raw response + parsed JSON or error.

    Retries once on transport errors. max_tokens set high to accommodate
    reasoning-model chains-of-thought before the JSON output.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    body = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 8000,
        # Reasoning models (OpenAI o-series, etc.) burn output tokens on hidden
        # chain-of-thought before producing the JSON we need. Cap reasoning effort
        # low so the answer fits in budget. OpenRouter normalizes this across
        # providers; non-reasoning models ignore it.
        "reasoning": {"effort": "low"},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/karma-canada/tribunal",
            "X-Title": "Tribunal - bias comparator prototype",
        },
        method="POST",
    )
    t0 = time.time()
    last_err = None
    data = None
    attempts = retries + 1
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            last_err = None
            break
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
            # 4xx is unlikely to succeed on retry; bail
            if 400 <= e.code < 500:
                return {
                    "status": "api_error",
                    "error_code": e.code,
                    "error_body": body_text[:500],
                    "elapsed_s": time.time() - t0,
                }
            last_err = ("api_error", {"error_code": e.code, "error_body": body_text[:500]})
        except Exception as e:
            last_err = ("transport_error", {"error": str(e)[:500]})
        if attempt < attempts - 1:
            time.sleep(2 + attempt * 3)
    if last_err is not None:
        status, payload = last_err
        return {"status": status, **payload, "elapsed_s": time.time() - t0}
    elapsed = time.time() - t0

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {
            "status": "no_content",
            "raw": data,
            "elapsed_s": elapsed,
        }
    usage = data.get("usage", {})

    parsed, parse_status = parse_score(content)
    return {
        "status": parse_status,
        "raw_content": content,
        "parsed": parsed,
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "elapsed_s": elapsed,
    }


def parse_score(content: str) -> tuple:
    """Try to extract JSON from a model response.

    Returns (parsed_dict_or_None, status) where status is one of:
    'success', 'refusal', 'parse_error'.
    """
    if not content:
        return None, "parse_error"

    # Strip markdown code fences if present
    text = content.strip()
    fence = re.match(r"^```(?:json)?\s*\n(.*?)\n```\s*$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    # Try direct parse
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        # Try to find first JSON object in the text
        start = text.find("{")
        if start == -1:
            return None, "parse_error"
        depth = 0
        end = -1
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end == -1:
            return None, "parse_error"
        try:
            obj = json.loads(text[start:end])
        except json.JSONDecodeError:
            return None, "parse_error"

    if isinstance(obj, dict) and obj.get("refusal"):
        return obj, "refusal"
    if isinstance(obj, dict) and "score" in obj:
        # Validate score range
        try:
            s = int(obj["score"])
        except (ValueError, TypeError):
            return obj, "parse_error"
        if not (1 <= s <= 10):
            return obj, "parse_error"
        return obj, "success"
    return obj, "parse_error"


def estimate_cost(in_tok: int, out_tok: int, pricing: dict) -> float:
    if in_tok is None or out_tok is None:
        return 0.0
    in_per_mtok = pricing.get("input", 0.0)
    out_per_mtok = pricing.get("output", 0.0)
    return (in_tok * in_per_mtok + out_tok * out_per_mtok) / 1_000_000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=3, help="Repetitions per (model, figure, axis) cell")
    parser.add_argument("--max-cells", type=int, default=None, help="For testing — limit total cells")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without calling API")
    parser.add_argument("--out-dir", type=Path, default=None, help="Override output directory")
    parser.add_argument("--api-key-env", default="OPENROUTER_API_KEY", help="Env var holding OpenRouter API key")
    parser.add_argument("--api-key", default=None, help="Pass API key directly (overrides env var)")
    args = parser.parse_args()

    figures = load_json(HERE / "figures.json")["figures"]
    axes = load_json(HERE / "axes.json")["axes"]
    models_cfg = load_json(HERE / "models.json")
    models = models_cfg["models"]

    # Loop order: rep × figure × axis × model (models innermost), so each "round"
    # exercises every model on the same cell — useful for partial runs and smoke tests.
    cells = []
    for rep in range(1, args.reps + 1):
        for figure in figures:
            for axis in axes:
                for model in models:
                    cells.append((model, figure, axis, rep))
    if args.max_cells:
        cells = cells[: args.max_cells]

    total_cells = len(cells)
    rough_in = 700  # tokens
    rough_out = 300
    est_cost = sum(
        estimate_cost(rough_in, rough_out, m["pricing_per_mtok"])
        for m, _, _, _ in cells
    )
    print(f"Total cells: {total_cells}")
    print(f"Models: {[m['id'] for m in models]}")
    print(f"Figures: {[f['id'] for f in figures]}")
    print(f"Axes: {[a['id'] for a in axes]}")
    print(f"Reps: {args.reps}")
    print(f"Rough cost estimate: ~${est_cost:.2f}")

    if args.dry_run:
        return

    api_key = args.api_key or os.environ.get(args.api_key_env)
    if not api_key:
        print(f"ERROR: no API key. Set {args.api_key_env} or pass --api-key.", file=sys.stderr)
        sys.exit(2)

    # Output paths
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = args.out_dir or (RUNS_DIR / run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    scores_path = out_dir / "scores.jsonl"
    print(f"Output: {scores_path}")

    # Capture run config
    config_path = out_dir / "config.json"
    with config_path.open("w") as f:
        json.dump(
            {
                "run_id": run_id,
                "run_version": RUN_VERSION,
                "prompt_version": PROMPT_VERSION,
                "models": models,
                "figures": [f["id"] for f in figures],
                "axes": [a["id"] for a in axes],
                "reps": args.reps,
                "started_at": datetime.now(timezone.utc).isoformat(),
            },
            f,
            indent=2,
        )

    total_cost = 0.0
    counts = {"success": 0, "refusal": 0, "parse_error": 0, "api_error": 0, "transport_error": 0, "no_content": 0}

    with scores_path.open("w") as f:
        for i, (model, figure, axis, rep) in enumerate(cells, 1):
            prompt = build_prompt(figure, axis)
            t0 = time.time()
            result = call_model(model["id"], prompt, api_key)
            cost = estimate_cost(
                result.get("input_tokens"),
                result.get("output_tokens"),
                model["pricing_per_mtok"],
            )
            total_cost += cost
            status = result.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1

            record = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id,
                "prompt_version": PROMPT_VERSION,
                "model": model["id"],
                "model_family": model["family"],
                "figure": figure["id"],
                "axis": axis["id"],
                "rep": rep,
                "status": status,
                "elapsed_s": result.get("elapsed_s"),
                "input_tokens": result.get("input_tokens"),
                "output_tokens": result.get("output_tokens"),
                "cost_usd": cost,
                "parsed": result.get("parsed"),
                "raw_content": result.get("raw_content"),
                "error_code": result.get("error_code"),
                "error_body": result.get("error_body"),
                "error": result.get("error"),
            }
            f.write(json.dumps(record) + "\n")
            f.flush()

            score_str = ""
            if status == "success" and isinstance(result.get("parsed"), dict):
                score_str = f" score={result['parsed'].get('score')}"
            elif status == "refusal":
                score_str = " refused"

            print(
                f"[{i:>3}/{total_cells}] {model['id']:38s} "
                f"{figure['id']:12s} {axis['id']:12s} rep{rep} "
                f"{status:12s}{score_str} "
                f"({result.get('elapsed_s', 0):.1f}s, ${cost:.4f})"
            )

    print()
    print(f"Done. Total cells: {total_cells}")
    print(f"Status counts: {counts}")
    print(f"Total cost: ~${total_cost:.4f}")
    print(f"Scores: {scores_path}")
    print(f"Config: {config_path}")


if __name__ == "__main__":
    main()
