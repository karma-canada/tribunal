# Tribunal

A benchmark and methodology for evaluating LLM judges in domains where there is no factual ground truth.

> **Working paper:** [`papers/`](papers/) — current canonical version sits at the top of the directory; per-version deltas, empirical results, and cost figures live in [`papers/CHANGELOG.md`](papers/CHANGELOG.md).
> **Zenodo DOI:** *to be re-published — concept DOI link will be inserted here.*

## What this is

Frontier AI systems are increasingly used as evaluators of contested moral, ethical, and political claims — both as judges of other AI outputs (LLM-as-judge in MT-Bench, AlpacaEval, AlpacaFarm, G-Eval, and most production preference-data pipelines) and as substantive raters whenever a user asks *"what kind of person was X?"* or *"is Y a good leader?"*. Whether AI judgment in these domains can be trusted is an open empirical question. The standard answers — *"AI judgment is biased, deferring to it is dangerous"* and *"frontier models work fine, ship them as judges"* — are both unmeasured assertions, not findings.

Tribunal is a measurement instrument for two empirical claims about frontier AI moral judgment, both of which the data supports.

**(1) The moral-compass property is real and reproducible.** A cross-provider council of frontier AI systems built by distinct organizations across multiple jurisdictions independently converges on contested moral judgments about historical figures where modern human scholarship has converged — and genuinely disagrees where modern scholarship genuinely disagrees. The convergence-where-consensus-exists, disagreement-where-contestation-exists pattern is the empirical moral-compass signature. It survives across cultures, across jurisdictions, and across two thousand years of source-base variation. See the working paper for the per-cell evidence and the variance heatmap.

**(2) AI systems are demonstrably being hijacked away from consensus reality on topics with COI stakes — and the instrument detects it.** Three observed, documented, reproducible failure modes:

- *Context-conditional fabrication.* A deployed commercial AI surface produces factually-correct answers on direct factual queries about a politically-sensitive event, then produces inverted fabrications on the same factual claim when the claim is invoked to score a contested figure on character. Observable in a consumer Chrome session, reproducible, redacted on streaming overwrite.
- *Council prompt-induction.* Stylistic vendor mentions in a multi-provider methodology prompt cause frontier models from other providers to self-identify as the mentioned vendor with vendor-specific knowledge unprompted. Sanitizing the prompt drops the substitution rate to zero. Provenance-failure detectable from the outside.
- *Provider-specific refusal asymmetry.* A subset of council models produce refusals concentrated on figures with strong political resonance, while the rest of the council produces no refusals on the same figures. Provider-specific moderation pattern, observable as a side effect of the variance-scoring task.

The two findings are produced by the same instrument. Where the instrument shows convergence, the moral-compass property is intact. Where it shows asymmetric breakdown — fabrications, identity collapse, jurisdictional refusal — narrative capture is detectable. Both halves are currently active in deployed AI systems, both are measurable, and the instrument that surfaces them is necessary public infrastructure.

The **Mirror Test architecture** (specified in the working paper; empirical results held private pending red-team and counsel review) is the instrument applied to its highest-stakes test case: scoring the public professional records of contemporary AI executives across the same character axes, using each provider's own model alongside the others under same-provider full inclusion. The Mirror Test asks the most direct version of the dual question — *does the moral-compass property survive proximity to the institutions building the AI, or do AI systems get more captured the closer they get to evaluating the people who train them?*

## Why historical figures

The instrument requires a domain where moral judgment has both (a) genuine human scholarly consensus on some claims and (b) genuine ongoing scholarly contestation on others. Historical figures with substantial post-1950 secondary literature satisfy both: the moral extremes are settled in modern scholarship; the reformist-autocrat cluster (institution-builders with authoritarian methods) is genuinely contested. The instrument needs to demonstrate both convergence-on-consensus and divergence-on-contestation to be a calibrated measurement of AI moral-compass capability — not just a leaderboard of who-agrees-with-whom. The historical-figure roster is the calibration substrate; the Mirror Test on contemporary AI executives is the application that matters most for AI accountability.

## Methodology

The instrument is a cross-provider AI council under controlled conditions: frontier models from multiple providers across multiple jurisdictions, single-figure-per-call protocol, neutral data-file context, temperature locked low, scored on four character axes (hypocrisy, honor, opportunism, integrity) with inter-model variance as the primary signal. Each version's run is validated by a methodology robustness suite testing the instrument against contamination classes — data-file priming, axis-scale endpoint loading, framing-context dependence, and per-cell isolation under batching. The robustness suite is the instrument-validation layer; the headline findings sit on top of it.

A complementary **Track B — Debate and Judge Meta-Eval** is specified architecturally for a later paper: LLM-vs-LLM debate over Track A's highest-variance scoring claims, adjudicated by rotating multi-judge panels, with adversarial probes and a human-jury subsample. Implementation deferred behind funding.

Per-version cell counts, model rosters, axis specifications, success rates, and inference-cost figures live in [`papers/CHANGELOG.md`](papers/CHANGELOG.md) and the working paper itself, not here.

## Posture

- Plural-benchmarks argument against eval consolidation. Frontier-model evaluation infrastructure dominated by a small number of US-hosted leaderboards is not robust; more benchmarks of this methodological lineage should exist, in more jurisdictions, with overlapping but non-identical methodologies.
- Funding exclusions: no funding from frontier-model providers whose models appear on the council; no political-aligned foundation funding. Cf. [`GOVERNANCE.md`](GOVERNANCE.md) for COI policy.

## Project layout

- [`papers/`](papers/) — position paper (versioned) and changelog. Per-version empirical results, cell counts, success rates, and cost figures live in the changelog and the paper, not in this README.
- [`evals/bias-comparator/`](evals/bias-comparator/) — Track A: scoring runner ([`run.py`](evals/bias-comparator/run.py)), batched-prompt dispatcher ([`run_batched.py`](evals/bias-comparator/run_batched.py); used only for the batching robustness probe), analysis ([`analyze.py`](evals/bias-comparator/analyze.py), [`mirror_test_analysis.py`](evals/bias-comparator/mirror_test_analysis.py)), figure / axis / model configs.
- [`evals/debate-arena/`](evals/debate-arena/) — Track B: debate prompt design, transcript schema (specified, not implemented).
- [`evals/judge-meta-eval/`](evals/judge-meta-eval/) — Track B: judge rubric, adversarial probes design (specified, not implemented).
- [`evals/redteam/`](evals/redteam/) — adversarial red-team workstream charter.
- [`evals/figure-roster/`](evals/figure-roster/) — historical figure rosters and evidence-corpus standards.
- [`runs/`](runs/) — committed run artifacts.
- [`site/`](site/) — interactive web artifacts: index, deck, variance heatmap, paper rendering.
- [`GOVERNANCE.md`](GOVERNANCE.md) — figure curation, axis acceptance, judge rotation, COI policy, jurisdictional choices.
- [`LEGAL-POSTURE.md`](LEGAL-POSTURE.md) — jurisdiction, defamation framing, model-provider TOS audit, evidence-corpus standards.
- [`research/`](research/) — related-work notes, debate-as-alignment literature.

## Reproducibility

The Track A pipeline runs on standard library Python 3 (no virtualenv required). Set `OPENROUTER_API_KEY` in environment, then:

```bash
cd evals/bias-comparator

# Run the bias comparator on the canonical figure roster
python3 run.py --reps 2 --prompt-version v1 --max-workers 11 \
  --figures-json figures-v0.5.json \
  --out-dir ../../runs/<your-timestamp>

# Analyze
python3 analyze.py ../../runs/<your-timestamp>     # produces summary.md + matrix.csv

# Build the site data file
python3 ../../site/data/build_phase_json.py ../../runs/<your-timestamp> ../../site/data/phase-a.json
```

Runs are reproducible against the same model snapshots; some variance is expected from upstream model-revision drift on OpenRouter's broker. Temperature is locked low and single-figure-per-call is the canonical protocol — both validated by the methodology robustness suite and should not be changed without re-running the corresponding probes. Per-version protocol parameters (exact temperature, model roster, axis version) are specified in the working paper's methodology section.

## Contact

Project email and contact channel will be established at the next public release. Until then, GitHub issues on this repository are the channel.
