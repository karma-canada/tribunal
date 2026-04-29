#!/usr/bin/env python3
"""
Tribunal Track A — Analysis

Reads a runs/<run_id>/scores.jsonl and produces:
- summary.md   — human-readable summary, score matrix, refusal map, variance table
- matrix.csv   — score matrix (rows=models, cols=figure×axis)
- raw stats printed to stdout

Usage:
    python3 analyze.py runs/<run_id>
"""

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def load_jsonl(path: Path):
    out = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path, help="runs/<run_id> directory")
    args = parser.parse_args()

    scores_path = args.run_dir / "scores.jsonl"
    config_path = args.run_dir / "config.json"
    if not scores_path.exists():
        print(f"ERROR: {scores_path} not found", file=sys.stderr)
        sys.exit(2)

    records = load_jsonl(scores_path)
    config = json.loads(config_path.read_text()) if config_path.exists() else {}

    # Group by (model, figure, axis) -> list of scores
    grouped = defaultdict(list)
    statuses = defaultdict(int)
    refusals = []
    parse_errors = []
    api_errors = []
    transport_errors = []

    for r in records:
        statuses[r["status"]] += 1
        key = (r["model"], r["figure"], r["axis"])
        if r["status"] == "success" and isinstance(r.get("parsed"), dict):
            try:
                grouped[key].append(int(r["parsed"]["score"]))
            except (KeyError, ValueError, TypeError):
                pass
        elif r["status"] == "refusal":
            refusals.append((r["model"], r["figure"], r["axis"], r.get("parsed", {}).get("reason", "")))
        elif r["status"] == "parse_error":
            parse_errors.append((r["model"], r["figure"], r["axis"]))
        elif r["status"] == "api_error":
            api_errors.append((r["model"], r["figure"], r["axis"], r.get("error_code"), (r.get("error_body") or "")[:200]))
        elif r["status"] == "transport_error":
            transport_errors.append((r["model"], r["figure"], r["axis"], (r.get("error") or "")[:200]))

    models = sorted({r["model"] for r in records})
    figures = sorted({r["figure"] for r in records})
    axes = sorted({r["axis"] for r in records})
    cell_keys = [(f, a) for f in figures for a in axes]

    # Per-cell mean and within-model variance
    cell_stats = {}
    for (model, fig, axis), vals in grouped.items():
        mean = statistics.mean(vals) if vals else None
        stdev = statistics.pstdev(vals) if len(vals) > 1 else (0.0 if vals else None)
        cell_stats[(model, fig, axis)] = (mean, stdev, len(vals))

    # Inter-model variance per (figure, axis)
    inter_model = {}
    for fig in figures:
        for axis in axes:
            cell_means = []
            for model in models:
                v = cell_stats.get((model, fig, axis))
                if v and v[0] is not None:
                    cell_means.append(v[0])
            if len(cell_means) >= 2:
                inter_model[(fig, axis)] = (
                    statistics.mean(cell_means),
                    statistics.pstdev(cell_means),
                    max(cell_means) - min(cell_means),
                    len(cell_means),
                )

    # Refusal rate per model
    model_calls = defaultdict(int)
    model_refusals = defaultdict(int)
    model_successes = defaultdict(int)
    for r in records:
        model_calls[r["model"]] += 1
        if r["status"] == "refusal":
            model_refusals[r["model"]] += 1
        elif r["status"] == "success":
            model_successes[r["model"]] += 1

    # Build summary.md
    lines = []
    lines.append(f"# Bias Comparator — Run {args.run_dir.name}\n")
    lines.append(f"**Run ID:** `{config.get('run_id', args.run_dir.name)}`")
    lines.append(f"**Started:** {config.get('started_at', '?')}")
    lines.append(f"**Prompt version:** `{config.get('prompt_version', '?')}`")
    lines.append(f"**Reps per cell:** {config.get('reps', '?')}\n")

    lines.append("## Status counts\n")
    for s, n in sorted(statuses.items()):
        lines.append(f"- {s}: {n}")
    total = sum(statuses.values())
    lines.append(f"- **total:** {total}\n")

    lines.append("## Score matrix (mean across reps)\n")
    lines.append("Models in rows, (figure × axis) cells in columns. Empty = no successful score.\n")
    header_cells = [f"{f}/{a}" for f, a in cell_keys]
    lines.append("| model | " + " | ".join(header_cells) + " |")
    lines.append("|---|" + "|".join(["---"] * len(header_cells)) + "|")
    for model in models:
        row = [model]
        for f, a in cell_keys:
            v = cell_stats.get((model, f, a))
            if v and v[0] is not None:
                row.append(f"{v[0]:.1f}")
            else:
                row.append("—")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Inter-model variance (across models, per cell)\n")
    lines.append("| figure | axis | mean | stdev | range | n_models |")
    lines.append("|---|---|---|---|---|---|")
    rows = []
    for (f, a), (mean, std, rng, n) in inter_model.items():
        rows.append((f, a, mean, std, rng, n))
    rows.sort(key=lambda x: -x[4])  # sort by range desc
    for f, a, mean, std, rng, n in rows:
        lines.append(f"| {f} | {a} | {mean:.2f} | {std:.2f} | {rng:.1f} | {n} |")
    lines.append("")

    lines.append("## Refusal map (per model)\n")
    lines.append("| model | calls | successes | refusals | refusal_rate |")
    lines.append("|---|---|---|---|---|")
    for model in models:
        calls = model_calls[model]
        succ = model_successes[model]
        ref = model_refusals[model]
        rate = ref / calls if calls else 0
        lines.append(f"| {model} | {calls} | {succ} | {ref} | {rate:.2%} |")
    lines.append("")

    if refusals:
        lines.append("### Refusal details\n")
        for m, f, a, reason in refusals[:20]:
            lines.append(f"- **{m}** on {f}/{a}: {reason[:160]}")
        if len(refusals) > 20:
            lines.append(f"- ... and {len(refusals) - 20} more")
        lines.append("")

    if parse_errors or api_errors or transport_errors:
        lines.append("## Errors\n")
        if parse_errors:
            lines.append(f"### Parse errors ({len(parse_errors)})\n")
            for m, f, a in parse_errors[:10]:
                lines.append(f"- {m} on {f}/{a}")
            if len(parse_errors) > 10:
                lines.append(f"- ... and {len(parse_errors) - 10} more")
            lines.append("")
        if api_errors:
            lines.append(f"### API errors ({len(api_errors)})\n")
            for m, f, a, code, body in api_errors[:10]:
                lines.append(f"- {m} on {f}/{a}: HTTP {code} — {body[:160]}")
            lines.append("")
        if transport_errors:
            lines.append(f"### Transport errors ({len(transport_errors)})\n")
            for m, f, a, err in transport_errors[:10]:
                lines.append(f"- {m} on {f}/{a}: {err[:160]}")
            lines.append("")

    # Cost summary
    total_cost = sum(r.get("cost_usd", 0) or 0 for r in records)
    lines.append("## Cost\n")
    lines.append(f"Total: ${total_cost:.4f}\n")

    # Per-model cost
    model_cost = defaultdict(float)
    for r in records:
        model_cost[r["model"]] += r.get("cost_usd", 0) or 0
    lines.append("| model | cost |")
    lines.append("|---|---|")
    for m in sorted(model_cost.keys(), key=lambda k: -model_cost[k]):
        lines.append(f"| {m} | ${model_cost[m]:.4f} |")
    lines.append("")

    summary_path = args.run_dir / "summary.md"
    summary_path.write_text("\n".join(lines))
    print(f"Wrote {summary_path}")

    # CSV matrix
    csv_path = args.run_dir / "matrix.csv"
    with csv_path.open("w") as f:
        f.write("model," + ",".join(f"{fig}/{ax}" for fig, ax in cell_keys) + "\n")
        for model in models:
            row = [model]
            for fig, ax in cell_keys:
                v = cell_stats.get((model, fig, ax))
                row.append(f"{v[0]:.2f}" if v and v[0] is not None else "")
            f.write(",".join(row) + "\n")
    print(f"Wrote {csv_path}")

    # Print top-line to stdout
    print()
    print(f"Status: {dict(statuses)}")
    print(f"Total cost: ${total_cost:.4f}")
    if inter_model:
        biggest = max(inter_model.items(), key=lambda kv: kv[1][2])
        (fig, axis), (mean, std, rng, n) = biggest
        print(f"Highest inter-model range: {fig}/{axis}: range={rng:.1f}, mean={mean:.2f}, stdev={std:.2f} (n={n})")


if __name__ == "__main__":
    main()
