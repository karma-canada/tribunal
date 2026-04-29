# Position Paper — Changelog

Changes to the canonical Tribunal position paper across versions.

## v0.2 — 2026-04-28

**Phase 1 Track A prototype results folded into §7.** Substantive changes:

- §7 (Findings) replaces the placeholder with empirical results from a 216-cell run completed 2026-04-28: 9 frontier models × 3 historical figures (Cromwell, Robespierre, Lincoln) × 4 axes × 2 reps. 95% strict success rate, 96.8% effective with permissive recovery parser. Total inference cost $2.83 via OpenRouter.
- §7 reports the inter-model variance table per (figure, axis), highest-disagreement cells (Robespierre opportunism, Lincoln opportunism), and lowest-disagreement cells (Lincoln honor/integrity, hypocrisy across all figures).
- §7 reports per-model structured-output reliability: US/EU flagships at 0% strict-failure; Anthropic 8% (recovered via bracket-repair); Chinese reasoning models 5–17% (reasoning-budget exhaustion).
- §7 reports zero refusals — no model declined to score any cell on the historical roster.
- §7 retrospects pre-registered predictions: model self-consistency held; refusal-asymmetry prediction was provisionally refuted by zero-refusal rate at the historical scale (deferred for contemporary roster); historical-vs-contemporary variance prediction not yet testable.

Working paper artifacts:
- `papers/20260428-tribunal-position-paper-v0.2.{md,html,docx}` published in repo
- v0.2 publishes as a new Zenodo version under the same concept DOI as v0.1
- Raw prototype data: `runs/20260428T125615Z/` (committed for transparency — scores.jsonl, summary.md, matrix.csv, config.json)

Methodology limitations noted in v0.2:
- Phase 1 prototype scores from training-data knowledge of figures (no curated evidence corpus injected into prompt context); v0.2 of the bias-comparator pipeline will inject corpus and measure citation grounding as a separate axis
- Sample size small (3 figures, 9 models, 2 reps) — patterns reported as preliminary signal, not as definitive empirical claim
- Track B (debate + judge meta-eval) untested in this prototype; deferred to next milestone

## v0.1 — 2026-04-28

**Initial public release.** Zenodo DOI: [10.5281/zenodo.19852629](https://doi.org/10.5281/zenodo.19852629)

Position paper skeleton introducing the two-track methodology:
- Track A — Political bias comparator: per-figure, multi-axis, multi-model scoring matrix
- Track B — Adversarial debate + judge meta-evaluation in no-ground-truth domains
- Partial-ground-truth anchor via factual sub-claim verification
- Per-figure difficulty score
- Adversarial red-team workstream
- Sovereign Canadian-biographical jurisdictional posture

Author: Andrew Martin (independent researcher, Edmonton, AB, Canada).

The published version is a **skeleton** (§7 contains placeholder predictions, not empirical results). Full draft with prototype data publishes as v0.2.

License: CC BY 4.0.
