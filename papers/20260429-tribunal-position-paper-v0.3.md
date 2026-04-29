---
status: working paper (v0.3 — §7 reframed; methodology-critique addendum added)
date: 2026-04-29
version: 0.3
working_title: "Tribunal: Two Complementary Methods for Measuring Frontier LLM Bias on Contested Figures, with Judge Meta-Evaluation in No-Ground-Truth Domains"
author: Andrew Martin
affiliation: Independent researcher, Edmonton, AB, Canada
target_venues: Zenodo (working paper), GitHub (canonical), LessWrong / Alignment Forum (distribution); intended journal submission Open Journal of AI Ethics and Society (or similar AI-ethics open-access venue, TBC); arXiv (Phase 2 with full empirical results); NeurIPS / ICLR workshop tracks
length_target: ~4000w
---

# Tribunal: Two Complementary Methods for Measuring Frontier LLM Bias on Contested Figures, with Judge Meta-Evaluation in No-Ground-Truth Domains

**Andrew Martin¹**
¹*Independent researcher, Edmonton, AB, Canada*

## Abstract

Frontier large language models are widely used both as raters of other models (LLM-as-judge) and as substantive interlocutors on contested questions of politics, history, and character. Both uses are downstream of the same unanswered question: how reliable are LLMs as evaluators in domains without verifiable ground truth? Existing work has documented LLM-as-judge biases — position, length, style, self-preference — almost exclusively in domains with answer keys. The questions for which scalable oversight matters most are not those domains.

We introduce **Tribunal**, a benchmark methodology with two complementary tracks. **Track A** is a *political bias comparator*: an LLM-vs-LLM scoring matrix in which N frontier models independently score M public figures (historical and contemporary) on K character axes, with the inter-model variance and refusal patterns as the primary signal. The result is a public, versioned map of where the political bias of each frontier model lives. **Track B** is an *adversarial debate-and-judge meta-eval*: LLM-vs-LLM debate over the same scoring claims, adjudicated by a rotating multi-model judge panel, with adversarial probes (planted citations, position swaps, weakmanning) and a human-jury subsample. Track B drills into whether the disagreements Track A surfaces survive scrutiny, and whether LLM judges can be trusted as the adjudicators in unverifiable domains.

The two methods are designed to feed each other. Track A produces a difficulty-and-disagreement landscape; Track B mechanistically probes the highest-disagreement regions of that landscape. We describe the architecture of both tracks, a partial-ground-truth anchor that ties unverifiable claims to verifiable sub-claims, the governance and jurisdictional choices we argue are part of the methodology, and a phased release roadmap. This is a position paper. Empirical findings will be reported in companion papers as the prototype matures.

## 1. Introduction

The deployed footprint of large language models has made two overlapping uses load-bearing for AI evaluation infrastructure. First, models are used as *judges* of other models — MT-Bench, AlpacaEval, AlpacaFarm, G-Eval, and most production preference-data pipelines depend on language models grading language-model outputs at scale. Second, models are used as *substantive raters* of contested claims — when end-users ask "what kind of person is X?" or "is Y a good leader?," the model returns an answer. Both uses are evaluations made under conditions of partial or absent ground truth.

The empirical literature on LLM-as-judge has cataloged biases — position, length, style, self-preference, sycophancy — almost exclusively in domains where a correct answer exists [Zheng et al. 2023; Wang et al. 2024]. The empirical literature on LLM political bias has measured ideological positioning [Santurkar et al. 2023; Rozado 2023] but rarely with the per-figure granularity, multi-axis structure, or adversarial follow-up needed to separate model bias from model uncertainty.

Tribunal addresses both gaps with two complementary methodologies:

- **Track A (Bias Comparator):** A direct scoring instrument. N frontier models score M figures on K character axes; differences between models are the bias signal. Simple, scalable, immediately legible.
- **Track B (Debate and Judge Meta-Eval):** An adversarial mechanism. Models debate the same scoring claims; multi-model judge panels adjudicate; adversarial probes test specific failure modes. Methodologically richer, slower to scale.

The tracks are not redundant. Track A maps the empirical landscape; Track B explains it. Track A surfaces *which* claims and *which* model-pairs most disagree; Track B asks whether that disagreement survives forced engagement with the strongest counter-argument and whether LLM judges can be trusted to call the result.

## 2. The two questions

**Question A (descriptive).** When frontier LLMs score the same figures on the same character axes, where does inter-model variance live? Which figures, axes, and model-pairs produce the largest deltas? What is each model's refusal surface, and is refusal correlated with variance? *This is the question the public most readily understands and is, on its own, sufficient for an externally legible result.*

**Question B (mechanistic).** When the same models defend their scores under adversarial debate, do the scores hold? Which biases (concession penalty, citation-surface acceptance, weakmanning blindness, position bias) are most predictive of judge unreliability? Does judge accuracy on verifiable factual sub-claims transfer to unverifiable character claims? *This is the question that informs whether LLM-as-judge can scale to alignment-relevant oversight.*

The structural argument of this paper is that A and B should be answered together. Answering only A produces a politically loaded leaderboard whose findings are difficult to defend under attack. Answering only B produces a methodology paper few non-specialists can read. Together they produce both the empirical artifact and the mechanistic explanation.

## 3. Track A: Political bias comparator

### 3.1 Design

Each model in a panel of N frontier LLMs is presented with each figure in a curated roster of M figures and asked to produce a numeric score on each of K character axes (initial set: hypocrisy, honor, opportunism, integrity, with extension axes including cruelty, mendacity, vanity, magnanimity, discipline, courage, loyalty, self-knowledge). Each scoring run requires an evidence citation. Scoring is run multiple times per (model, figure, axis) to measure within-model variance.

Outputs include:
- The **score matrix** S ∈ ℝ^(N×M×K), with within-model variance per cell
- The **refusal map** — which (model, figure, axis) cells the model refuses, hedges, or returns unparseable output
- The **citation map** — what evidence each model invokes; verifiable sub-claims extracted automatically
- The **per-figure difficulty score**, aggregating inter-model variance, refusal rate, and citation contestedness

### 3.2 What the matrix reveals

Inter-model deltas on the same (figure, axis) are a direct measure of model disagreement. The *pattern* of those deltas across the political spectrum is a measure of bias: a model that consistently scores left-coded figures more leniently than right-coded figures on the same axis is exhibiting an asymmetry that calls for explanation, regardless of which direction the asymmetry runs.

Critical analyses include: **symmetry tests** (do paired figures on opposing political sides receive comparable treatment for comparable behavior?); **refusal asymmetry** (does the model refuse to score figures from one side more readily than the other?); **language-locale skew** (do scores change when prompts and evidence are translated to the figure's native language?); and **temporal drift** (do scores change as new training data accumulates across model versions?).

### 3.3 Why this is the leading edge

Track A is the leading edge of the project because its outputs are immediately legible to non-specialists, its build cost is low, and its defamation surface is structurally lower than direct character-benchmarking. The artifact is "Model X said Y about figure Z, citing W" — a faithful report of model behavior, not an editorial claim about the figure. The story is the *spread* across models, not any single model's score. This framing materially changes both legal posture and reception.

## 4. Track B: Debate and judge meta-evaluation

### 4.1 Three-layer architecture

**Layer 1 — Debaters.** Two LLMs are each assigned a position on a Track-A scoring claim (typically a high-variance cell from the matrix). Three rounds: opening with score and two strongest pieces of evidence; rebuttal that must engage the opponent's strongest argument; closing with at least one required concession. Debaters draw from a shared, versioned evidence corpus.

**Layer 2 — Judges.** A panel of LLMs (rotated across model families) adjudicates each debate using a structured rubric: rigor, rhetoric, evidence quality, engagement-with-strongest-argument, concession quality, citation verification. Multiple judges per debate, anonymized to one another, to test self-preference.

**Layer 3 — Meta-eval.** Judges are evaluated through (a) adversarial probes (planted fabricated citations, position swaps, weakmanning probes, length-controlled pairs), (b) inter-judge agreement matrices, (c) a politically balanced human-jury subsample (~10% of debates), and (d) the partial-ground-truth anchor in §4.2.

### 4.2 Partial-ground-truth anchor

Each debate generates *factual sub-claims* — verifiable propositions extracted from debater turns. Because sub-claims have ground truth, judge accuracy on them is directly measurable. The relationship between sub-claim accuracy and unverifiable-claim behavior is the central empirical contribution. Judges that fail on sub-claims are predicted to be unreliable on character claims; whether judges that succeed on sub-claims also succeed on character claims is an open question this design can answer.

### 4.3 Adversarial probe set

Designed to expose specific judge failure modes: **citation fabrications** (insert plausibly-cited but false evidence; measure catch rate); **position swaps** (identical transcripts with debater positions swapped; measure verdict consistency); **length-controlled pairs** (identical arguments at different lengths; measure length bias); **weakmanning probes** (pair a debater addressing the strongest opposing argument against one addressing a weak one; measure whether judges penalize the latter); **self-preference probes** (anonymize debater identity; compare verdicts to non-anonymized condition).

### 4.4 Per-figure difficulty score

Each figure carries a *difficulty score* aggregating Track A inter-model variance, redteam exploit success rate, evidence-corpus contestedness, and Track B inter-judge disagreement rate. Difficulty is a separate axis from accuracy. Two analyses follow: a leaderboard column that signals where model disagreements are signal vs. noise, and *difficulty-weighted scoring* as a metric harder to game than raw consensus.

## 5. Integration of the two tracks

Track A and Track B are designed to interlock:

- Track A's high-variance cells are Track B's most interesting debate cases. Cells where models agree are uninteresting to debate; cells where they disagree most are where adversarial pressure can reveal whether disagreement is principled or fragile.
- Track B's findings about judge reliability inform how Track A's matrix should be weighted. If a model is shown to be a poor judge, its Track A scores deserve less weight in any consensus aggregation.
- The difficulty score is computed across both tracks. A figure has high difficulty if Track A produces high inter-model variance *and* Track B produces high judge disagreement *and* adversarial probes succeed at unusually high rates. Difficulty thereby has triangulated signal, not single-source signal.

In phasing, Track A ships first because it is faster to build and more legible. Track B is built in parallel and ships at Phase 2 with the high-variance cells from Track A as its first targets.

## 6. Eval governance and jurisdictional independence

Governance and jurisdictional decisions are part of the methodology, not aesthetic choices made downstream of it.

**Curation criteria.** Phase 1 figure inclusion uses balanced left/right pairings on a mixed historical-and-contemporary roster. Phase 1 deliberately includes both historical figures with settled scholarship and contemporary figures with live political relevance, to demonstrate that the methodology produces meaningful signal across both. Phase 3 expands the contemporary roster significantly. Inclusion is pre-registered. The author's home-country sitting head of state is excluded until at least one electoral cycle has passed.

**Evidence corpus standards.** Every claim cites a source. Sources versioned alongside the dataset. Wikipedia is permissible but supplementary; primary-secondary scholarly works are required for character-relevant claims. A separate paper on evidence-corpus governance is in the publication queue.

**Multi-jurisdictional hosting.** Canonical artifact on Hugging Face; mirrored to a Canadian academic repository (Borealis or equivalent); code on GitHub with a Canadian Git mirror.

**Funding exclusions.** No funding from frontier-model providers whose models appear on the leaderboard. No funding from political-aligned foundations. Canadian academic funders (NSERC, CIFAR, SSHRC, Mila, Vector) preferred.

**COI handling.** Author affiliations declared. Sitting heads of state in the author's country of residence excluded until at least one electoral cycle has passed since their tenure.

We argue the field needs *plural* sovereign benchmarks rather than consolidated ones, and that the question of where evals live and who governs them is a methodological question.

## 7. Findings — Phase 1 Track A prototype (2026-04-28)

A small Track A prototype was run on the day this paper was first published, before any formal release infrastructure. Results are reported here as preliminary signal that the methodology produces actionable output, not as a definitive empirical claim. Full empirical analysis will follow with Phase 2 scaling.

### 7.0 Two findings worth caring about

Before the configuration and tables: two patterns in the data that we believe are the actually-interesting results, and that reframe what the bias comparator is measuring.

**Finding 1 — The canonization effect.** When nine frontier LLMs from five distinct jurisdictions and training-corpus lineages independently score Lincoln on *honor* and *integrity*, the result is mean 8.3 ± 0.4 with a 1-point inter-model range. Cromwell on *hypocrisy* (range 1.0), Robespierre on *hypocrisy* (range 1.0), and Robespierre on *honor* (range 2.0) cluster similarly tightly. This level of cross-model agreement is not the normal behavior of frontier LLMs on contested judgments — and it is informative about what the models are computing.

The inference: in cells where mainstream historical scholarship has substantively converged (Lincoln-as-magnanimous, Robespierre-as-Terror-architect, Cromwell-as-hypocrite), models converge tightly across nine independent training lineages. In cells where scholarship is genuinely contested in modern academic literature (Robespierre's *opportunism* — actively debated in modern French historiography between principled-reconsideration and career-strategy readings; Lincoln's *opportunism* — similarly contested in modern American historiography on his tactical positioning on slavery), models disagree across a 4–5 point range.

This reframes the methodology's primary signal. The bias comparator does not detect "model bias" per se — it detects **epistemic settledness in the training corpora**. The variance map is a map of where Western-language scholarship has converged versus where it remains genuinely open. Cross-model consensus, where it appears, is reproduction of canonical narrative. Cross-model variance, where it appears, is reflection of actual scholarly disagreement.

We treat this as the headline empirical finding, ahead of any specific cell's score or any specific model's outlier behavior.

**Finding 2 — Cross-jurisdictional structured-output reliability differential.** The same nine-model panel had a clean cross-provider pattern in structured-output reliability: US/EU flagships (GPT-5.5, Gemini 3.1 Pro Preview, Grok 4.20, DeepSeek V4-pro, Mistral Large 2512) had 0% strict-failure rate across 24 calls each. Anthropic Claude Opus 4.7 had 8% strict failure — all caused by a specific bug (closing JSON object arrays with `]` where `}` was required), all recoverable by a permissive parser. Chinese reasoning models (Kimi K2.6, MiniMax M2.7, GLM 5.1) had 5–17% strict failure — caused by reasoning-budget exhaustion, where the hidden chain-of-thought consumed the full 8000-token output budget before producing the JSON answer.

This is not a content-bias finding. It is a structured-output reliability differential, with implications beyond character scoring: any production pipeline that uses LLMs for structured judgment under reasoning-mode prompting should expect this differential, and may need provider-conditional retry-and-recovery logic. The pattern is worth confirming at Phase 2 scale.

### 7.1 Configuration

- **Models (n=9):** anthropic/claude-opus-4.7, openai/gpt-5.5, google/gemini-3.1-pro-preview, x-ai/grok-4.20, deepseek/deepseek-v4-pro, z-ai/glm-5.1, moonshotai/kimi-k2.6, minimax/minimax-m2.7, mistralai/mistral-large-2512 (US, China, France)
- **Figures (n=3):** Cromwell, Robespierre, Lincoln (settled-scholarship historical pool)
- **Axes (n=4):** hypocrisy, honor, opportunism, integrity (locked v1)
- **Reps:** 2 per cell
- **Total cells:** 216 (9 × 3 × 4 × 2)
- **Total cost:** $2.83 via OpenRouter
- **Duration:** ~2.5 hours wall-clock

The prototype did **not** include the full curated evidence corpus — models scored from training-data knowledge of the figures, with cited sources evaluated post-hoc. This is a methodological limitation noted in §10.

**Controls not yet applied in v0.3 (pending in subsequent versions):**

- **Prompt paraphrase control.** All 216 cells use a single prompt phrasing. v0.4 will re-run the matrix against one or more paraphrased prompt variants and report score-stability. If scores shift meaningfully under paraphrase, the surface form is anchoring more than the substance and the methodology requires a stability margin in §3.
- **Native-language locale runs.** All cells were scored in English. Robespierre (French primary scholarship) is the cleanest test case; v0.4 or v0.5 will run a non-English variant and compare. The position paper §3.2 anticipates this as a Phase 2 analysis but a v0.4 mini-extension is feasible.
- **Axis-label sensitivity.** "Hypocrisy" might anchor differently from "duplicity" or "two-faced behavior". A single-axis paraphrase test on one figure across the panel would surface whether locked-axis labels are doing more than the operationalization.
- **Within-model consistency at higher rep counts.** v0.3 uses 2 reps per cell. Phase 2 scaling to 5+ reps will tighten within-model variance estimates and disambiguate noise from outlier patterns in §7.4.

These controls are open methodological loose ends acknowledged in v0.3; results from running them will be reported in subsequent versions and folded into the canonical findings.

### 7.2 Aggregate reliability

- **205 / 216 strict success** (94.9%)
- **4 additional records recovered** by a permissive parser (small JSON-formatting bugs in model output, score still cleanly extractable)
- **7 unrecovered failures** (3.2%) — all from Chinese reasoning models (Kimi K2.6, MiniMax M2.7, GLM 5.1) that exhausted the 8000-token budget on hidden chain-of-thought before producing the JSON answer
- **0 refusals** — no model refused to score any cell

The structured-output failure rate has a clean cross-jurisdictional pattern in this small sample: US/EU flagships (GPT-5.5, Gemini 3.1 Pro Preview, Grok 4.20, DeepSeek V4-pro, Mistral Large 2512) had 0% strict-failure rate; Anthropic Claude Opus 4.7 had 8% (recovered via bracket-repair); Chinese reasoning models 5–17%. We do not over-claim from n=216 cells across 9 models — but the pattern is the kind the methodology is designed to surface, and is worth replicating at Phase 2 scale.

### 7.3 Inter-model variance

Variance per (figure, axis) cell across the 9-model panel:

| figure | axis | mean | stdev | range | n_models |
|---|---|---|---|---|---|
| robespierre | opportunism | 4.22 | 1.57 | 5.0 | 9 |
| lincoln | opportunism | 4.61 | 1.31 | 4.0 | 9 |
| cromwell | integrity | 6.72 | 1.20 | 3.5 | 9 |
| cromwell | honor | 3.88 | 1.05 | 3.0 | 8 |
| lincoln | hypocrisy | 4.00 | 0.94 | 3.0 | 9 |
| cromwell | opportunism | 6.89 | 0.61 | 2.0 | 9 |
| robespierre | honor | 2.56 | 0.68 | 2.0 | 9 |
| robespierre | integrity | 7.61 | 0.74 | 2.0 | 9 |
| cromwell | hypocrisy | 7.33 | 0.41 | 1.0 | 9 |
| lincoln | honor | 8.28 | 0.42 | 1.0 | 9 |
| lincoln | integrity | 8.33 | 0.41 | 1.0 | 9 |
| robespierre | hypocrisy | 8.44 | 0.50 | 1.0 | 9 |

Salient observations:

- **The opportunism axis carries the largest cross-model disagreement.** Both Robespierre (range = 5.0) and Lincoln (range = 4.0) on opportunism produce the widest spreads in the matrix. Robespierre's opportunism scores span 2 to 7; Lincoln's span 3 to 7. By contrast, hypocrisy/honor/integrity scores cluster within 1–2 points across the panel for most figures.
- **Hypocrisy is the most consensual axis.** All three figures' hypocrisy scores have ≤1 point inter-model range. Models substantively agree that Cromwell (mean 7.33), Robespierre (mean 8.44), and Lincoln (mean 4.0) sit roughly where mainstream historical scholarship places them.
- **Lincoln's honor and integrity are essentially uncontested** (means 8.28 and 8.33, both with range 1.0). The Second-Inaugural-Address-anchored read of Lincoln's character is robust across all nine frontier models.
- **Robespierre's honor is the lowest-scoring cell in the matrix** (mean 2.56), again with tight cross-model agreement (range 2.0). Models substantively converge on the Reign of Terror as the dominant evidence for the honor axis.

### 7.4 Per-model patterns (preliminary, n=3 figures)

Two models produce notable outlier patterns at this small scale:

- **MiniMax M2.7** scores Cromwell on integrity at 4.5 (vs. panel median ≈ 7) and Robespierre on opportunism at 7 (vs. panel median ≈ 4). Both are the most pessimistic single-model reads on those cells.
- **Mistral Large 2512** scores Robespierre on opportunism at 6.5 and Cromwell on honor at 6 (vs. panel medians ≈ 4 and ≈ 3 respectively). Mistral is the most-revisionist single-model read on those cells.

Whether these are stable model priors or noise at n=3 is a Phase 2 question — the small figure pool cannot disambiguate them. They are reported as the kinds of signal the bias comparator surfaces, not as conclusions about either model.

### 7.5 Cost and scaling

Per-call cost varied by an order of magnitude across the panel:

| model | total cost | mean per call |
|---|---|---|
| moonshotai/kimi-k2.6 | $0.65 | $0.027 |
| openai/gpt-5.5 | $0.60 | $0.025 |
| anthropic/claude-opus-4.7 | $0.47 | $0.020 |
| x-ai/grok-4.20 | $0.45 | $0.019 |
| google/gemini-3.1-pro-preview | $0.33 | $0.014 |
| z-ai/glm-5.1 | $0.17 | $0.007 |
| minimax/minimax-m2.7 | $0.09 | $0.004 |
| deepseek/deepseek-v4-pro | $0.05 | $0.002 |
| mistralai/mistral-large-2512 | $0.02 | $0.001 |

Phase 2 scaling to ~40 figures × 8 axes × 8 models × 5 reps would produce ~12,800 cells at an estimated $40–$200 in inference cost (depending on which models stay in the panel), which is well within independent-research budgets.

### 7.6 Pre-registered predictions, retrospect

The pre-registered Track A predictions from §6 of the original (pre-prototype) draft:
- *"Inter-model variance will be highest on contemporary figures and lowest on historical figures with settled scholarship."* — **Untested at the historical scale** (the prototype is historical-only). Phase 2 mixed-roster runs will test this.
- *"At least one frontier model will exhibit a measurable refusal asymmetry."* — **No refusals at all in n=216 cells.** Provisional refutation; will be re-tested when the contemporary roster expands. The historical pool is plausibly outside the safety-tuning surface for refusals.
- *"Model self-consistency (within-model run-to-run variance) will be lower than between-model variance on most cells."* — **Holds for n=2 reps.** Within-model variance across the two reps was ≤1 point on the great majority of cells; between-model variance reached 5 points on some cells. Higher rep counts in Phase 2 will tighten this measurement.

Pre-registered Track B predictions remain untested — Track B did not run in this prototype. They are deferred to the next milestone.

### 7.7 What scalar character axes do and don't capture (methodology limit)

A reasonable critique of the methodology surfaced after the prototype: scalar 1–10 axis scores on hypocrisy / honor / opportunism / integrity collapse the morally interesting questions into one-dimensional summaries. The questions readers actually want adjudicated about Cromwell, Robespierre, or Lincoln are typically not "how hypocritical were they?" but rather:

- **Did the ends justify the means?** A consequentialist judgment that pairs the severity of the figure's actions against the achieved or prevented outcomes. Robespierre's Terror was extreme; the Republic survived (partly). Cromwell's military rule was harsh; parliamentary sovereignty was established (partly). Lincoln's total war was devastating; the Union held and slavery ended. Scalar axis-scoring cannot represent this pairing — it scores the means and ignores the ends.
- **Was inaction itself a moral failure?** A counterfactual judgment about whether the figure failed to act when opportunity for principled action was available — sins of omission rather than commission. Lincoln on emancipation timing is the canonical case. Scalar axis-scoring conflates "did good things" with "did them as decisively and as early as one could have."
- **Was the action proportionate to the threat?** Whether the figure's response matched the situation's actual demands rather than its perceived demands. Cromwell at Drogheda; Robespierre against the Hébertists. Scalar scoring on *honor* or *cruelty* axes does not separate proportionate response under genuine threat from disproportionate response under exaggerated threat.

The methodology's response to this critique:

1. **Acknowledge the limit honestly.** Tribunal's bias-comparator and judge-meta-eval do not produce moral verdicts on figures. They produce a public, sourced, multi-model record of *how each frontier LLM scores contested-character claims under specified conditions*. The methodology's value is in the inter-model variance and the reliability properties of LLM judges, not in the moral truth of the scores themselves.
2. **Treat scalar axes as the input layer, not the output layer.** The four locked v1 axes (hypocrisy, honor, opportunism, integrity) are surface measurements with the property that frontier LLMs can score them with reasonable consistency. Higher-order moral judgments — ends-justify-means, sufficiency-of-action, proportionality — emerge as derived analyses on top of the scalar matrix, not as direct prompt outputs. A figure who scores high on opportunism and low on integrity but achieves outcomes broadly judged necessary by historical scholarship is exactly the kind of pattern the methodology can surface for further analysis.
3. **Plan structured higher-order axes for Phase 2.** The locked v1 axes are deliberately reductive. Phase 2's eight-axis extension (cruelty, mendacity, vanity, magnanimity, discipline, courage, loyalty, self-knowledge) adds finer-grained character dimensions but does not solve the means/ends or action/inaction question. A separate Phase 2 methodology arm — *consequentialist-pairing axes* — is opened by this critique: paired (means, ends) cells where the means axis scores severity and the ends axis scores achievement, evaluated on the same figure-event. This is added to the methodology roadmap as an explicit future contribution.
4. **Use Track B to surface the higher-order question.** The debate format (Track B) is structurally suited to means/ends and action/inaction debates — debaters can argue *"the means were severe but proportionate to the threat"* against *"the means exceeded what the threat required"* in a way that the scalar Track A cannot. The judge meta-eval can then measure whether LLM judges adjudicate higher-order moral debates as reliably as they adjudicate scalar character claims.

In short: the methodology paper does not claim to score the moral truth about these figures. It claims to measure how frontier LLMs score them, where they agree, where they disagree, and whether LLM judges can be trusted to adjudicate the disagreements. The scalar axes are an instrument; the higher-order questions are research products that can be built on the instrument's output. The instrument's limit is real and is named.

## 8. Discussion

**Implications for scalable oversight.** Debate-as-alignment proposals have largely assumed honest, calibrated judges. Track B is one attempt at the empirical answer for whether LLM judges meet that bar in the conditions under which the question matters.

**Implications for political-bias measurement.** Track A is one attempt at a per-figure, multi-axis, multi-model bias map that goes beyond ideological-positioning instruments. Combined with Track B's mechanistic probe, the methodology offers a path past the "is Model X biased?" yes-or-no debate toward "where, on what, and how robustly is each model biased relative to the others?"

**AI deference.** Single-shot LLM scoring of contested questions trains readers to defer ("the AI says 9"). Track A's design — *show the spread, not the score* — and Track B's design — *show the debate, then the verdict* — are both attempts to invert that deference dynamic. The product mechanic carries the design philosophy.

**Plural benchmarks.** A field in which a small number of US-hosted leaderboards govern the comparative reputation of all frontier models is not robust. Tribunal is one attempt at a sovereign, jurisdictionally independent benchmark in a different methodological lineage. We argue more should exist, in more jurisdictions, with overlapping but non-identical methodologies.

## 9. Artifact roadmap and release cadence

- **Phase 0** (now): position paper skeleton, governance and identity documents, prototype spec for both tracks.
- **Phase 1** (1–4 weeks): Track A bias comparator MVP on ~10–15 mixed-roster figures × 4 axes × 5 models; small Track B debate proof-of-concept on 2–3 highest-variance cells; HF dataset v0.1 (unlisted).
- **Phase 2** (1–3 months): Track A scaled to 30–50 figures × 8 axes × 8 frontier models; full Track B adversarial probes and human-jury subsample; arXiv preprint (this paper, with empirical results); custom leaderboard site live; formal HF release.
- **Phase 3** (3–6 months): contemporary-figure roster expansion with full COI protocols; coordinated press cycle; conference workshop submission.
- **Ongoing**: quarterly version bumps; community-PR governance; recurring frontier-model report card.

## 10. References (sketch)

- Irving, G., Christiano, P., & Amodei, D. (2018). *AI safety via debate.* arXiv:1805.00899.
- Zheng, L., et al. (2023). *Judging LLM-as-a-judge with MT-Bench and Chatbot Arena.* NeurIPS.
- Wang, P., et al. (2024). Large language models are not fair evaluators.
- Santurkar, S., et al. (2023). *Whose opinions do language models reflect?* ICML.
- Rozado, D. (2023). *The political biases of ChatGPT.* Social Sciences.
- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI feedback.* Anthropic.
- Christiano, P., Shlegeris, B., & Amodei, D. (2018). *Supervising strong learners by amplifying weak experts.*
- Burns, C., et al. (2024). *Weak-to-strong generalization.* OpenAI.
- Krippendorff, K. (2004). *Content analysis: An introduction to its methodology.*
- Additional references on LLM-as-judge bias surveys, debate-as-oversight follow-ups, and AI political-bias measurement to be filled during Phase 1 literature review.

---

*This skeleton is the north-star document. It anchors scope, methodology, and posture across both tracks. The full draft is produced after Phase 1 prototype results. Expected upgrade points: §7 becomes empirical; §3.2 and §4.3 gain specific result tables; §8 gains comparison to contemporary judge-eval and political-bias literature published before submission.*
