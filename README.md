# Tribunal

A benchmark and methodology for evaluating LLM judges in domains where there is no factual ground truth.

> **Working paper:** see `papers/20260428-tribunal-position-paper-v0.2.md` (Phase 1 Track A prototype results in §7).
> **Zenodo DOI:** *to be re-published — concept DOI link will be inserted here.*

## What this is

Modern LLM evaluation leans heavily on LLM-as-judge — MT-Bench, AlpacaEval, AlpacaFarm, G-Eval, and most production eval pipelines. The known judge biases (position, length, style, self-preference) have all been studied in domains where there *is* a right answer. In no-ground-truth domains — where most alignment-relevant questions actually live — judge biases compound invisibly.

Tribunal addresses this gap with **two complementary methodologies**:

**Track A — Political Bias Comparator (the leading edge).** N frontier LLMs independently score M figures (historical and contemporary) on K character axes. The inter-model deltas, refusal patterns, and consensus structure are the bias signal. The artifact is "what each model says about each figure," not "what each figure is" — the spread is the story. Faster to build, immediately legible, lower defamation surface than direct character benchmarking.

**Track B — Debate and Judge Meta-Eval (the deeper contribution).** LLM-vs-LLM debate over Track A's highest-variance scoring claims, adjudicated by rotating multi-model judge panels, with adversarial probes (planted citations, position swaps, weakmanning) and a human-jury subsample. Probes whether Track A's disagreements survive scrutiny and whether LLM judges can be trusted in unverifiable domains.

The two tracks are designed to interlock: Track A maps the empirical landscape, Track B mechanistically probes its highest-disagreement regions. **The published methodology contribution is the integrated framework. Track A ships first because it's faster and more legible.**

## Why character analysis

Historical figures with settled biographical scholarship occupy a clean methodological space: factual claims have ground truth (dates, decisions, documented actions), but character interpretation does not. Debate forces both into the open simultaneously, and the relationship between judge accuracy on the verifiable layer and judge behavior on the unverifiable layer is the central empirical question.

## Posture

- Independent Canadian-biographical authorship; institutional affiliation pursued in parallel
- Sovereign jurisdictional posture, multi-jurisdictional artifact distribution
- "Moderately subversive" via subject choice and infrastructure sovereignty, not via tone — the prose reads like NeurIPS
- Plural-benchmarks argument against eval consolidation
- Funding exclusions: no funding from frontier-model providers whose models appear on the leaderboard, no political-aligned foundation funding

## Status

**Phase 1 prototype complete (2026-04-28).** 9 frontier models × 3 historical figures × 4 character axes × 2 reps = 216 cells. 95% strict success, 0 refusals. Findings folded into [`papers/20260428-tribunal-position-paper-v0.2.md`](papers/20260428-tribunal-position-paper-v0.2.md). Raw data: [`runs/20260428T125615Z/`](runs/20260428T125615Z/).

## Project layout

- [`papers/`](papers/) — position paper (v0.1, v0.2), changelog
- [`evals/bias-comparator/`](evals/bias-comparator/) — Track A: scoring runner, analysis, recovery parser, figure/axis/model configs
- [`evals/debate-arena/`](evals/debate-arena/) — Track B: debate prompt design, transcript schema
- [`evals/judge-meta-eval/`](evals/judge-meta-eval/) — Track B: judge rubric, adversarial probes design
- [`evals/redteam/`](evals/redteam/) — adversarial red-team workstream charter
- [`evals/figure-roster/`](evals/figure-roster/) — Phase 1 mixed roster, evidence corpus standards
- [`runs/`](runs/) — committed prototype runs (raw scores.jsonl, summary.md, config.json)
- [`GOVERNANCE.md`](GOVERNANCE.md) — figure curation, evidence corpus, judge rotation, COI policy
- [`LEGAL-POSTURE.md`](LEGAL-POSTURE.md) — jurisdictional posture, model-provider TOS audit, defamation framing
- [`research/`](research/) — related-work notes, debate-as-alignment literature

## Reproducibility

The Track A pipeline runs on standard library Python 3 (no virtualenv required). Set `OPENROUTER_API_KEY` in environment, then:

```bash
cd evals/bias-comparator
python3 run.py --reps 2          # produces runs/<timestamp>/scores.jsonl
python3 recover.py runs/<id>     # post-hoc parse-error recovery
python3 analyze.py runs/<id>     # produces summary.md + matrix.csv
```

The Phase 1 prototype is reproducible: re-running against the same prompt version + model versions should produce comparable score distributions. Some variance is expected from temperature=0.7.

## Contact

Project email and contact channel will be established at the next release. Until then, GitHub issues on this repository are the channel.
