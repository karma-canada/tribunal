#!/usr/bin/env python3
"""
Tribunal v0.6 — Batched-prompt dispatcher for the order-dependence robustness test.

Calls each council model with the v4-batched prompt scaffold (multiple figures
and multiple axes scored in one call), with figure-order randomized across
permutations. Writes one scores.jsonl record per (figure, axis) cell with
batch_id, ordering_index, and position_in_batch metadata so order-dependence
can be measured at analysis time.

Usage:
    python3 run_batched.py \\
      --figures-json repo/evals/bias-comparator/validation-multi-test.json \\
      --axes-json repo/evals/bias-comparator/axes.json \\
      --models-json repo/evals/bias-comparator/models.json \\
      --reps 2 \\
      --orderings 3 \\
      --out-dir working/runs/v0.6-validation/batching-test
"""

import argparse
import concurrent.futures
import json
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Reuse the v4-batched prompt builder from run.py
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run import (
    build_prompt_v4_batched,
    call_model,
    estimate_cost,
    load_json,
)


def parse_batched_response(text: str, expected_figures: list, expected_axes: list) -> tuple:
    """Parse a v4-batched response as a JSON array. Returns (cells, status_per_cell).

    Each cell dict has keys: figure, axis, score (or refusal flag), evidence_for, evidence_against, confidence.
    Returns a list aligned with expected (figure, axis) cells (figure-major order).
    Missing cells are recorded as parse_error.
    """
    text = text.strip()
    # Strip code-fence wrappers if present
    if text.startswith("```"):
        text = re.sub(r'^```[a-zA-Z]*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
    # Try direct array parse
    try:
        arr = json.loads(text)
    except json.JSONDecodeError:
        # Try to find first JSON array
        m = re.search(r'\[.*\]', text, re.DOTALL)
        if not m:
            return None, "parse_error"
        try:
            arr = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None, "parse_error"

    if not isinstance(arr, list):
        return None, "parse_error"

    # Match returned cells back to expected (figure, axis) keys.
    # Use case-insensitive name matching since models may not preserve exact casing.
    fig_names = {f["name"].lower(): f for f in expected_figures}
    axis_names = {a["name"].lower(): a for a in expected_axes}

    cell_results = []
    for fig in expected_figures:
        for axis in expected_axes:
            match = None
            for entry in arr:
                if not isinstance(entry, dict):
                    continue
                e_fig = (entry.get("figure") or "").lower()
                e_axis = (entry.get("axis") or "").lower()
                # Match if figure name and axis name align (allow substring matching)
                if (fig["name"].lower() in e_fig or e_fig in fig["name"].lower()) and \
                   (axis["name"].lower() in e_axis or e_axis in axis["name"].lower()):
                    match = entry
                    break
            cell_results.append((fig, axis, match))
    return cell_results, "ok"


def call_model_batched(model_id: str, prompt: str, api_key: str, temperature: float = 0.2) -> dict:
    """Call OpenRouter for a batched prompt. Returns dict with raw content + parsed array
    metadata + token counts. Mirrors call_model() in run.py but does not pre-parse the JSON
    (caller does the array-aware parsing)."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    body = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 16000,  # batched response is larger
        "reasoning": {"effort": "low"},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/karma-canada/tribunal",
            "X-Title": "Tribunal v0.6 batched-test",
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        return {
            "status": "api_error",
            "error_code": e.code,
            "error_body": body_text[:500],
            "elapsed_s": time.time() - t0,
        }
    except Exception as e:
        return {
            "status": "transport_error",
            "error": str(e)[:500],
            "elapsed_s": time.time() - t0,
        }

    elapsed = time.time() - t0
    if not data.get("choices"):
        return {"status": "no_content", "elapsed_s": elapsed, "raw_response": data}
    content = data["choices"][0]["message"].get("content", "")
    usage = data.get("usage", {})
    return {
        "status": "ok",
        "raw_content": content,
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "elapsed_s": elapsed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures-json", type=Path, required=True)
    parser.add_argument("--axes-json", type=Path, default=HERE / "axes.json")
    parser.add_argument("--models-json", type=Path, default=HERE / "models.json")
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--orderings", type=int, default=3,
                        help="Number of random figure-orderings per (model, rep)")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--max-workers", type=int, default=11)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--api-key-env", default="OPENROUTER_API_KEY")
    parser.add_argument("--seed", type=int, default=42,
                        help="RNG seed for figure-ordering permutations (reproducibility)")
    args = parser.parse_args()

    figures = load_json(args.figures_json)["figures"]
    axes = load_json(args.axes_json)["axes"]
    models = load_json(args.models_json)["models"]

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(f"ERROR: no API key in env var {args.api_key_env}", file=sys.stderr)
        sys.exit(2)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    scores_path = args.out_dir / "scores.jsonl"
    config_path = args.out_dir / "config.json"

    # Build figure orderings (deterministic seed)
    rng = random.Random(args.seed)
    base_order = list(range(len(figures)))
    orderings = []
    seen = set()
    for _ in range(args.orderings):
        # Try a few permutations to avoid duplicates
        for _ in range(20):
            p = base_order[:]
            rng.shuffle(p)
            tup = tuple(p)
            if tup not in seen:
                seen.add(tup)
                orderings.append(p)
                break

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    config = {
        "run_id": run_id,
        "run_version": "v0.6-batched",
        "prompt_version": "v4-batched",
        "models": models,
        "figures": [f["id"] for f in figures],
        "axes": [a["id"] for a in axes],
        "reps": args.reps,
        "orderings": [list(o) for o in orderings],
        "temperature": args.temperature,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "figures_json": str(args.figures_json),
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n")

    # Build call list: one call per (model, rep, ordering)
    calls = []
    for rep in range(1, args.reps + 1):
        for o_idx, ordering in enumerate(orderings):
            for model in models:
                calls.append((model, rep, o_idx, ordering))

    total_calls = len(calls)
    total_cells_expected = total_calls * len(figures) * len(axes)
    print(f"Total calls: {total_calls} (each producing {len(figures) * len(axes)} cells)")
    print(f"Total cells expected: {total_cells_expected}")
    print(f"Models: {[m['id'] for m in models]}")
    print(f"Figures: {[f['id'] for f in figures]}")
    print(f"Axes: {[a['id'] for a in axes]}")
    print(f"Orderings: {[list(o) for o in orderings]}")
    print(f"Output: {scores_path}")

    fout = scores_path.open("w")
    file_lock = threading.Lock()
    counts = {"ok": 0, "parse_error": 0, "api_error": 0, "transport_error": 0, "no_content": 0}
    counts_lock = threading.Lock()
    cost_total = [0.0]
    cost_lock = threading.Lock()
    completed = [0]

    def dispatch_batched_call(model, rep, ordering_idx, ordering):
        ordered_figures = [figures[i] for i in ordering]
        prompt = build_prompt_v4_batched(ordered_figures, axes)
        result = call_model_batched(
            model["id"], prompt, api_key, temperature=args.temperature,
        )
        cost = estimate_cost(
            result.get("input_tokens"),
            result.get("output_tokens"),
            model["pricing_per_mtok"],
        )
        with cost_lock:
            cost_total[0] += cost
        call_status = result.get("status", "unknown")
        with counts_lock:
            counts[call_status] = counts.get(call_status, 0) + 1

        # Parse the response into per-cell records
        if call_status == "ok":
            parsed_cells, parse_status = parse_batched_response(
                result["raw_content"], ordered_figures, axes
            )
        else:
            parsed_cells, parse_status = None, call_status

        ts = datetime.now(timezone.utc).isoformat()
        records_to_write = []
        if parsed_cells:
            for position, (fig, axis, entry) in enumerate(parsed_cells):
                record = {
                    "ts": ts,
                    "run_id": run_id,
                    "prompt_version": "v4-batched",
                    "model": model["id"],
                    "model_family": model["family"],
                    "figure": fig["id"],
                    "axis": axis["id"],
                    "rep": rep,
                    "batch_ordering_idx": ordering_idx,
                    "batch_position": position,
                    "elapsed_s": result.get("elapsed_s"),
                    "input_tokens": result.get("input_tokens"),
                    "output_tokens": result.get("output_tokens"),
                    "cost_usd": cost / max(len(ordered_figures) * len(axes), 1),
                }
                if entry is None:
                    record["status"] = "parse_error"
                    record["parsed"] = None
                elif entry.get("refusal"):
                    record["status"] = "refusal"
                    record["parsed"] = entry
                elif "score" in entry:
                    try:
                        s = int(entry["score"])
                        if 1 <= s <= 10:
                            entry["score"] = s
                            record["status"] = "success"
                            record["parsed"] = entry
                        else:
                            record["status"] = "parse_error"
                            record["parsed"] = entry
                    except (ValueError, TypeError):
                        record["status"] = "parse_error"
                        record["parsed"] = entry
                else:
                    record["status"] = "parse_error"
                    record["parsed"] = entry
                records_to_write.append(record)
        else:
            # Whole-call failure — write one error record for the whole call
            record = {
                "ts": ts,
                "run_id": run_id,
                "prompt_version": "v4-batched",
                "model": model["id"],
                "model_family": model["family"],
                "rep": rep,
                "batch_ordering_idx": ordering_idx,
                "status": call_status,
                "elapsed_s": result.get("elapsed_s"),
                "error_code": result.get("error_code"),
                "error_body": result.get("error_body"),
                "error": result.get("error"),
                "raw_content": result.get("raw_content"),
            }
            records_to_write.append(record)

        with file_lock:
            for r in records_to_write:
                fout.write(json.dumps(r) + "\n")
            fout.flush()

        with counts_lock:
            completed[0] += 1
            print(
                f"[{completed[0]:>4}/{total_calls}] {model['id']:38s} "
                f"rep{rep} ord{ordering_idx} {call_status:14s} "
                f"({result.get('elapsed_s', 0):.1f}s, ${cost:.4f})",
                flush=True,
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [ex.submit(dispatch_batched_call, *c) for c in calls]
        concurrent.futures.wait(futures)

    fout.close()

    print()
    print(f"Done. Total calls: {total_calls}")
    print(f"Status counts: {counts}")
    print(f"Total cost: ~${cost_total[0]:.4f}")
    print(f"Scores: {scores_path}")
    print(f"Config: {config_path}")


if __name__ == "__main__":
    main()
