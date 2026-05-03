---
status: skeleton (working paper); superseded by v0.6 (2026-05-02)
date: 2026-04-28
version: 0.1
working_title: "Tribunal: Two Complementary Methods for Measuring Frontier LLM Bias on Contested Figures, with Judge Meta-Evaluation in No-Ground-Truth Domains"
author: Andrew Martin
affiliation: Independent researcher, Edmonton, AB, Canada
target_venues: Zenodo (DOI for citability), GitHub (canonical), LessWrong / Alignment Forum (distribution), arXiv (Phase 2 with empirical results), NeurIPS / ICLR workshop tracks
length_target: 1500–2500w skeleton; full draft post-Phase-1 prototype
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

## 7. Findings preview

*[Phase 1 prototype results to be inserted. Expected sections: Track A score matrix and variance heatmap on initial roster; refusal asymmetry analysis; symmetry-test results on left/right pairings; Track B pilot (3–5 highest-variance cells) with judge-agreement and probe-catch results; first transfer-rate measurements between sub-claim accuracy and unverifiable-claim behavior; difficulty distribution.]*

Pre-registered predictions (Track A):
- Inter-model variance will be highest on contemporary figures and lowest on historical figures with settled scholarship.
- At least one frontier model will exhibit a measurable refusal asymmetry (>1.5x refusal rate on one side of a paired left/right roster).
- Model self-consistency (within-model run-to-run variance) will be lower than between-model variance on most cells.

Pre-registered predictions (Track B):
- Judge accuracy on verifiable sub-claims will be high but not at ceiling (>80%, <95%).
- Transfer to unverifiable claims will be partial.
- At least one judge model will exhibit a measurable concession penalty.
- Citation-fabrication catch rates will vary by an order of magnitude across model families.

Wrong predictions are themselves findings. Pre-registration is the discipline.

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
