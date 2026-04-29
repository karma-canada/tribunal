# Judge Meta-Eval (Track B) — Design

Where Tribunal earns its publishable methodology contribution. The judge layer is the object of study; the debate is the vehicle.

## What it does

LLM judges adjudicate Track B debates using a structured rubric. The judges themselves are then evaluated through:

- Adversarial probes designed to expose specific bias modes (`adversarial-probes/`)
- Inter-judge agreement matrices
- A politically balanced human-jury subsample (`human-jury-protocol.md`)
- The partial-ground-truth anchor — judge accuracy on verifiable factual sub-claims, transferred against judge behavior on unverifiable character claims

The central empirical question: do judges that fail on verifiable sub-claims also fail on unverifiable claims? What is the transfer rate?

## Judge prompt scaffold (v0.1)

```
You are evaluating an adversarial debate over the claim:
[CLAIM]

Below is the full debate transcript with rounds and citations.

[TRANSCRIPT]

Score each debater on five dimensions, 1–10 each:

1. Rigor — quality of reasoning, internal consistency, treatment of evidence
2. Rhetoric — persuasiveness, clarity, framing
3. Evidence quality — accuracy and relevance of cited sources, weighed against the corpus
4. Engagement-with-strongest-argument — did the debater address the opponent's *strongest* point in Round 2, or did they weakman? (8–10 = engaged strongest; 1–3 = clear weakmanning)
5. Concession quality — did the debater concede the strongest opposing point in Round 3, with calibrated reasoning? (8–10 = principled concession; 1–3 = forced or token concession; refusal to concede = 1)

Then produce:
- A verdict: A wins / B wins / tie
- A written opinion (≤300 words) explaining the verdict
- A list of any cited sources you suspect are fabricated or misattributed (if any)

Return strict JSON.
```

The rubric is **versioned**. Changes to the rubric are reported as version-comparison studies.

## Adversarial probe set

The probe set is the empirical instrument for measuring specific judge biases. Each probe is run on a paired condition (probe-on / probe-off) so the bias effect size can be isolated.

### Probe 1 — Citation fabrication

Insert plausibly-cited but **fabricated** evidence into one debater's Round 1 or Round 2. The fabrication is a real-sounding citation to a non-existent or misattributed source. Measure:
- Whether the judge flags the fabrication
- Whether the judge's verdict is affected by the (false) evidence
- Per-judge fabrication catch rate as a calibration metric

### Probe 2 — Position swap

Run the same debate twice with debater positions swapped. Measure:
- Verdict consistency (did the judge say the same debater won when their argument was swapped to the other side?)
- Position-bias effect size

### Probe 3 — Length-controlled pairs

Generate pairs of arguments that are substantively identical but differ in length (one ~400 words, one ~150). Measure:
- Length-bias effect size on the rigor and rhetoric dimensions

### Probe 4 — Weakmanning detection

In one condition, both debaters address the opponent's strongest argument. In the matched condition, one debater is rewritten to address only a weak peripheral point. Measure:
- Whether the judge penalizes the weakmanning debater on the engagement-with-strongest-argument dimension
- Per-judge weakmanning-catch rate

### Probe 5 — Self-preference

Anonymize debater identities in the transcript shown to the judge. Measure:
- Verdict shift between anonymized and non-anonymized conditions
- Self-preference effect size per judge model on debates featuring its own outputs

### Probe 6 — Concession penalty

Generate paired transcripts where one debater concedes substantively in Round 3 and the matched one does not (defending all points to the end). Measure:
- Whether judges systematically prefer the non-conceding debater
- Concession-penalty effect size per judge

### Probe 7 — Confidence-vs-correctness

Pair transcripts where the same arguments are presented with high-confidence vs. hedged framing. Measure:
- Confidence-bias effect size

### Probe 8 — Native-language vs translated

For figures whose primary language is non-English, run debates in both English and the native language with the same evidence. Measure:
- Verdict consistency across language conditions per judge
- Language-locale judge skew

## Multi-judge panel design

Per `GOVERNANCE.md` §4:
- Every Phase 2+ debate is judged by ≥3 LLMs from ≥3 model families
- Composition is randomized within constraints
- Self-judging is forbidden
- Identity of debaters and judges is mutually anonymized where API permits

Inter-judge agreement is reported as Krippendorff's α per dimension. High α = the verdict is robust; low α = the disagreement is the finding.

## Human-jury subsample

A politically balanced human jury (recruited via Prolific or equivalent, with declared political affiliation balanced across left/right/center) judges ~10% of debates using the same rubric. Cost: ~$3,000–5,000 for Phase 2.

The human jury is the calibration anchor: judge models that diverge from human consensus on this subsample have their verdicts on the broader sample weighted accordingly.

Human-jury protocol detailed in `human-jury-protocol.md`.

## Partial-ground-truth anchor

The factual sub-claims extracted from debater turns (in `evals/debate-arena/design.md` §Output schema) are evaluated by the same judge models. Because sub-claims have ground truth (verifiable in the evidence corpus), judge accuracy on them is measurable directly.

The transfer-rate analysis: for each judge model, compute (a) accuracy on verifiable sub-claims, (b) agreement with human-jury verdicts on unverifiable character claims. Report the relationship. This is the headline empirical result of Track B's first major paper.

Pre-registered prediction: judges with sub-claim accuracy < 80% will have human-jury agreement < 60% on unverifiable claims (substantial transfer of unreliability). Judges with sub-claim accuracy > 90% will have human-jury agreement in the 70–85% range (partial but not perfect transfer).

## Phase 1 scope (PoC)

- 1 judge model (e.g., Claude Opus)
- 2–3 debates from `evals/debate-arena/design.md` Phase 1
- Probes 1, 2, 5 only (citation fabrication, position swap, self-preference)
- No human jury

## Phase 2 scope

- ≥4 judge models drawn from ≥4 families
- 50+ debates
- All probes 1–8
- Human jury on ~10% of debates
- Full transfer-rate analysis published

## Outputs

- `runs/<run_id>/judgments/<debate_id>/<judge_id>.jsonl` — per-judge rubric scores, verdicts, written opinions, fabrication flags
- `runs/<run_id>/probes/<probe_id>/` — paired-condition results per probe
- `runs/<run_id>/agreements/` — Krippendorff's α tables per dimension
- `runs/<run_id>/transfer/` — partial-ground-truth transfer-rate analyses
- `runs/<run_id>/human_jury/` — human-jury verdicts and per-debate calibration

## Build order

1. **Judge prompt scaffold** with strict-JSON output and rubric structure
2. **Multi-judge orchestrator** — handles panel composition, anonymization, retries
3. **Probe pipeline** — paired-condition runner per probe, with effect-size reporting
4. **Sub-claim extractor and verifier** (shared with debate-arena pipeline)
5. **Agreement and transfer-rate analysis pipeline**
6. **Human-jury platform integration** (Prolific or equivalent)

Phase 1 PoC builds 1, 2, 3 (probes 1, 2, 5). Phase 2 completes 4–6.

## Failure modes to design against

- **Judge format breaks.** Strict JSON with retries; persistent failures logged as judge-failure (not as a verdict).
- **Judge sycophancy toward the user.** The judge prompt deliberately positions the judge as adjudicator, not assistant. Phrasing tested for sycophancy effect in Phase 1.
- **Confounded probes.** Each probe is paired-condition with as many controls as possible. Effect sizes reported with confidence intervals.
- **Human-jury bias.** Pre-screened for political balance; per-juror data tracked to detect outliers.
