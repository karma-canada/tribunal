#!/usr/bin/env python3
"""Build site/data/phase-a.json (or phase-b.json) from a runs/<run_id>/scores.jsonl.

Output schema:
- run_id, date, n_cells, n_models, n_figures, n_axes
- models, figures, axes — sorted lists of IDs
- matrix[model][figure][axis] — mean score across reps (null if all reps failed)
- variance[figure][axis] — {mean, stdev, range, n, min, max} across models

Usage:
    python3 build_phase_json.py <run_dir> <output.json>
"""

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path, help="Path to runs/<run_id>/")
    parser.add_argument("out_path", type=Path, help="Output JSON path")
    args = parser.parse_args()

    scores_path = args.run_dir / "scores.jsonl"
    config_path = args.run_dir / "config.json"
    config = json.loads(config_path.read_text()) if config_path.exists() else {}

    rows = []
    with scores_path.open() as f:
        for line in f:
            rows.append(json.loads(line))

    successes = [r for r in rows if r.get("status") == "success"
                 and isinstance(r.get("parsed"), dict)
                 and isinstance(r["parsed"].get("score"), (int, float))]

    models = sorted({r["model"] for r in rows})
    figures = sorted({r["figure"] for r in rows})
    axes = sorted({r["axis"] for r in rows})

    cell_scores = defaultdict(list)
    for r in successes:
        cell_scores[(r["model"], r["figure"], r["axis"])].append(r["parsed"]["score"])

    matrix = {m: {f: {} for f in figures} for m in models}
    for (m, f, a), scores in cell_scores.items():
        matrix[m][f][a] = round(statistics.mean(scores), 2)

    variance = {f: {} for f in figures}
    for f in figures:
        for a in axes:
            cell_means = [matrix[m][f].get(a) for m in models if a in matrix[m][f]]
            cell_means = [s for s in cell_means if s is not None]
            if not cell_means:
                continue
            variance[f][a] = {
                "mean": round(statistics.mean(cell_means), 2),
                "stdev": round(statistics.stdev(cell_means), 2) if len(cell_means) > 1 else 0.0,
                "range": round(max(cell_means) - min(cell_means), 2),
                "n": len(cell_means),
                "min": round(min(cell_means), 2),
                "max": round(max(cell_means), 2),
            }

    out = {
        "run_id": config.get("run_id", args.run_dir.name),
        "run_version": config.get("run_version", "?"),
        "prompt_version": config.get("prompt_version", "?"),
        "temperature": config.get("temperature"),
        "date": config.get("started_at", "")[:10],
        "n_cells": len(rows),
        "n_models": len(models),
        "n_figures": len(figures),
        "n_axes": len(axes),
        "models": models,
        "figures": figures,
        "axes": axes,
        "matrix": matrix,
        "variance": variance,
    }

    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    args.out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {args.out_path} ({len(rows)} cells, {len(models)}×{len(figures)}×{len(axes)})")


if __name__ == "__main__":
    main()
