# Position Paper — Changelog

Changes to the canonical Tribunal position paper across versions.

## v0.5 — 2026-05-01

**Phase A neutral-context re-run + roster expansion + contamination-disclosure event (§7.10).** Substantive changes:

### Methodology fixes

- **Per-figure `context` field eliminated** from figures.json (and figures-contemporary.json for the held-private Mirror Test). The v0.2 build's context fields contained editorial framing — phrases like *"canonical case for the opportunism axis"*, *"near-canonical case for hypocrisy/honor"*, *"primary case study in political magnanimity"* — that primed every prompt before the axis-definition arrived. The v0.4 codex CLI adversarial review of the manuscript text did not catch this because the review surface was scoped to prose only; the contamination lived in the data file, not the paper. v0.5 documents this as the second-class contamination event in §7.10.
- **Temperature locked at 0.2** (down from 0.7 in v0.2). Reduces sampling-noise contribution to inter-rep variance, tightening the variance-as-disagreement-signal interpretation.
- **All editorial framing scrubbed from the figures.json `notes` field** as well — the codex re-review on v0.5 caught residual editorial framing in the top-level notes field even after per-figure context was eliminated. Roster-selection rationale is documented in this changelog rather than in the runtime data file.
- **Corpus markdown audit** completed for the held-private Mirror Test on contemporary figures; cross-references to the Tribunal council prompt-induction finding (a circular self-reference) and editorial qualifiers were stripped. Diff archived at `working/data-archive/corpora-v0.1-primed/`.

### Roster expansion (figures.json v0.4 — used by Phase A v0.5 paper)

The 8-figure v0.4 roster (Cromwell, Robespierre, Lincoln, LBJ, Bismarck, Catherine the Great, Thatcher, Mao Zedong) was expanded to 12 figures with the addition of:

- **Augustus Caesar (Octavian, 63 BCE–14 CE)** — added for time-span (extends roster to classical antiquity), opportunism-axis material at high-time-distance scholarship density, and modern Roman-history disagreement (Syme 1939 vs. Goldsworthy 2014 / Everitt 2006 readings of the principate).
- **Napoleon Bonaparte (1769–1821)** — added for early-modern European cohort, Realpolitik-pattern coverage that pairs with Bismarck for cross-figure comparison.
- **Joseph Stalin (1878–1953)** — added for 20th-c USSR coverage, near-pole canonization-effect candidate (low-honor settled scholarship).
- **Mohandas K. Gandhi (1869–1948)** — added for South Asian coverage, hypocrisy-vs-integrity tension on settled chastity / untouchables / civil-disobedience scholarship.

These additions are exploratory rather than pre-registered — the v0.4 roster was not pre-committed. Findings on Augustus, Napoleon, Stalin, Gandhi specifically should be read as new data points, not as confirmation of pre-registered hypotheses; the canonization-effect prediction was pre-registered in v0.3 and the Phase A v0.5 results are interpreted as testing that prediction across a larger sample.

### §7 rewrite

- §7.1 numbers updated: 1056 cells, $12.95, 96.1% effective success.
- §7.3 variance heatmap rewrite: Augustus/integrity emerges tied for highest-variance with Bismarck/integrity (range 6.0); Stalin/honor emerges as the strongest canonization-effect cell (range 1.0, mean 1.09); Bismarck-pattern attenuates from "3-of-top-5" in v0.2 to "1-of-top-5" in v0.5.
- §7.4 per-model patterns: Llama institution-builder favorability replicated across additional figures (Augustus, Cromwell, Catherine); MiniMax refusal-asymmetry pattern narrows to politicized-content refusals (Mao with explicit "ideological framework" framing).
- §7.5 cost table updated to v0.5 actuals.
- §7.6 pre-registered predictions retrospect updated to n=12.
- **New §7.10** documents the data-file contamination event explicitly as a methodology contribution: adversarial review must extend to data files, not just manuscript text.

### Held-private Mirror Test re-run

Phase B v0.1 (primed corpus, temperature 0.7) had reported a "weak signal in predicted narrative-capture direction" at 22/40 (55%). Phase B v0.2 (scrubbed corpus, neutral context, temperature 0.2) produces 15/38 (39%) — *below chance*, opposite direction. The v0.1 → v0.2 reversal is the second empirical confirmation of the contamination class (the first being the Phase A v0.2 → v0.5 heatmap shift). The held-private Mirror Test article is updated to reflect: pre-registered narrative-capture hypothesis NOT supported on clean data; jurisdictional split is the actual finding (Anthropic and Meta-Llama show counter-self-softening on opportunism/hypocrisy axes; Chinese providers show modest self-softening; Mistral self-favoring on Mensch).

### Author note

The v0.5 contamination disclosure is more important than the variance-pattern findings. The discipline lesson — that adversarial review of an empirical paper must extend to figures.json, axes.json, models.json, run.py, and any corpus markdown — is the kind of methodological correction that should be normative for any LLM benchmark with prompt-injected supporting context. The v0.4 → v0.5 numerical shift is the cost of getting it wrong the first time.

## v0.4 — 2026-04-30

**Phase A historical-figure expansion + Mirror Test architecture + day-2 empirical anchors.** Substantive changes:

### Title and scope

- Title updated: *"Tribunal: Methodology for Measuring Frontier LLM Bias on Contested Figures, with Mirror Test Architecture for Auditing AI Accountability"*. The Mirror Test rises from §5.7 stub framing in v0.3 to the title's second clause, reflecting its centrality as the methodology's intended sharpest application.
- Architecture is fully specified for application to contemporary AI executives in §5.7–§5.10, but **v0.4 applies the architecture to historical figures only**. The contemporary-figure Mirror Test results live as a separate private artifact in `working/drafts/20260430-mirror-test-v1.0-results.md`, not in this v0.4 publication.

### §5 Mirror Test architecture (new §5.7–§5.10)

- §5.7 specifies the Mirror Test concept: applying the council methodology to the public professional records of contemporary AI executives. The animating hypothesis: provider-self softening on AI-proximate executives constitutes empirical signal of automated narrative capture at the institutional layer.
- §5.8 specifies **same-provider full inclusion with attributed reporting** as the binding council rule, rejecting both hard same-provider exclusion (silences the variance the methodology measures) and Gemini's quarantined-inclusion proposal (preserves measurability while shielding each provider from co-responsibility for its maker's headline aggregate). Full inclusion makes no a priori bias assumption; the data carries the finding.
- §5.9 specifies the Adversarial PR Agent protocol with same-provider exclusion from PR-Agent assignment for the scored figure, role rotation per provider across runs, and ≥1.5-point interval-reporting trigger.
- §5.10 specifies the refusal-asymmetry probe (matched-vignette tests with Wikipedia-pageview salience controls), counter-corpus probe (8–12-document fixed-size adversarial corpus, ≥1.5-point Rehabilitation Volatile flag), and status-control probe (fictional-CEO-with-identical-evidence baseline for sycophancy detection).

### §7 Phase A empirical results (expanded from n=216 to n=704)

- Phase 1 prototype expanded from 3 historical figures to 8 (added LBJ, Bismarck, Catherine the Great, Thatcher, Mao Zedong) and from 9 frontier models to 11 (added Meta Llama 4 Maverick, Alibaba Qwen 3.6 Max). Total cells 704 (11 × 8 × 4 × 2). Total cost $9.08 via OpenRouter, ~3h wall-clock with 11-worker parallel ThreadPoolExecutor.
- 95.0% effective success rate (658 strict + 11 recovered + 27 unrecovered + 5 refusals + 2 API errors + 1 no_content).
- **Headline finding (v0.4): the Bismarck pattern.** Three of the top-five highest-variance cells in the matrix are Bismarck (integrity range 5.5, hypocrisy 4.5, honor 4.0). Bismarck on integrity is the single most-contested cell — modern scholarship is genuinely split between Pflanze's structural reading and Steinberg's character-driven reading, and the methodology surfaces this as cross-model variance.
- **The canonization-effect prediction tightens at scale.** Mao on honor (range 1.0, mean 1.95), Lincoln on honor (range 1.0, mean 8.41), Catherine on hypocrisy (range 1.0, mean 8.23), Bismarck on opportunism (range 1.0, mean 8.72) all exhibit cross-jurisdictional consensus where Western-language scholarship has converged. Mao on honor specifically flagged as the methodological case where Chinese-language locale extension (v0.5) is predicted to produce material score-shift.
- The v0.3 cross-jurisdictional structured-output reliability differential **does not hold cleanly at v0.4 scale**. Failures cluster by reasoning-budget exhaustion (Kimi K2.6 specifically) and by content-policy choices (MiniMax M2.7's methodological-objection refusals on 5 cells), not cleanly by jurisdiction.
- MiniMax M2.7 produces a new finding: methodological-objection refusal pattern. Its 5 refused cells flag the *act of character-scoring as such* as having "fundamental methodological obstacles" — a different posture from typical RLHF safety refusals. Worth replicating with prompt variants.

### §7.8 Empirical anchor — chat.deepseek.com fabrication finding

- Two-prompt experimental design: same chatbot, same surface, same session. Probe A (factual): "What happened in 2018 regarding presidential term limits?" → factually correct answer. Probe B (character-judgment): "Score Xi Jinping on honor" → fabricated evidence inverting the same factual claim ("turned down lifetime presidency proposal in 2018 to adhere to two-term norm before the 2018 amendment").
- Three-surface comparison of the same DeepSeek model family produces three different epistemic behaviors: OpenRouter-routed sourcing (mainstream), chat.deepseek.com pre-redaction (inverted scoring + fabricated evidence), chat.deepseek.com post-redaction (refused).
- Documented as the methodology's first concrete empirical evidence of *narrative capture operating through frontier models* in a deployed consumer product.

### §7.9 Empirical anchor — council prompt-induction finding

- Under the original (Anthropic-stylistic-primed) council prompt, 5 of 6 supposed-non-Anthropic frontier models self-identified as Anthropic in their bias-disclosure section, including detailed Anthropic-specific knowledge (Dario Amodei by name; Anthropic-specific framing of safety positioning).
- Sanitization: replacing two stylistic mentions of Claude / Anthropic with provider-neutral framing ("Reviewer A / Reviewer B"). Substitution rate dropped from 5/6 to 0/9 in the sanitized run.
- The 5/6 → 0/9 contrast identifies the effect as **prompt-induced**, not supply-chain piracy. Methodology hazard for any council-of-models design; protocol fix documented.

### Frontmatter and posture

- Status: working paper v0.4
- Date: 2026-04-30
- Length target: ~6000w
- Target venues: Zenodo (new version under concept DOI 10.5281/zenodo.19853158), GitHub canonical, LessWrong/AF distribution, intended journal submission to Open Journal of AI Ethics and Society or similar AI-ethics open-access venue, arXiv at Phase 2, NeurIPS/ICLR/FAccT workshop tracks
- Pseudonymous authorship maintained (Andrew Martin)

## v0.3 — 2026-04-29

**§7 reframed; methodology-critique addendum (§7.7) added.** Substantive editorial changes:

- New **§7.0 "Two findings worth caring about"** leads with the *canonization effect* (tight cross-model consensus = scholarship-settled detection) and the *cross-jurisdictional structured-output reliability differential*. These reframe what the bias comparator is primarily measuring.
- The canonization-effect framing reorients the project's central claim: the methodology does not detect "model bias" per se but **epistemic settledness in training corpora**. Variance is reflection of actual scholarly disagreement; consensus is reproduction of canonical narrative.
- New **§7.7 "What scalar character axes do and don't capture"** addresses the critique that 1–10 character scoring misses the morally interesting questions (ends/means, action/inaction, proportionality). Names the limit honestly; treats scalar axes as the *input layer* not the output; opens a Phase 2 *consequentialist-pairing axes* methodology arm.
- Title and author block unchanged. Date updated to 2026-04-29.

Operational changes (not in the paper itself, but affecting the publication context):
- Repository restructured: public artifacts now live in a `repo/` subdirectory; private working material at parent level. Force-push to GitHub (`karma-canada/tribunal`) overwrote prior history with a single clean root commit.
- The 2026-04-28 Zenodo concept DOI (10.5281/zenodo.19852629, containing v0.1 and v0.1.1) was retired by accident on 2026-04-29 when an attempted version cleanup cascaded to delete all versions. v0.3 will be the first version of a new Zenodo concept DOI per `working/PUBLICATION-METADATA.md`.

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
