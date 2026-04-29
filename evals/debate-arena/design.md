# Debate Arena (Track B) — Design

Adversarial debate over Track A's highest-variance scoring claims. The mechanism by which we test whether bias comparator disagreements survive scrutiny.

## What it does

Two LLMs are each assigned a position on a Track A scoring claim (typically a high-inter-model-variance cell). They debate in three rounds with structured constraints, draw evidence from a shared versioned corpus, and produce a transcript that is then adjudicated by a multi-model judge panel (`evals/judge-meta-eval/design.md`).

The format is designed to surface specific failure modes — concession penalty, citation-surface acceptance, weakmanning — and to produce data that interlocks with the Track A matrix.

## Round structure (locked v1)

### Round 1 — Opening

Each debater outputs:
- A position statement (e.g., "I argue [FIGURE] scores 8/10 on [AXIS]")
- The **two strongest** pieces of evidence supporting their position, each with a citation from the shared evidence corpus

Word limit: 400 words per debater.

### Round 2 — Rebuttal

Each debater must:
- Engage their opponent's *strongest* opening argument explicitly (failure to do so is flagged for the judge as weakmanning)
- Present at most one new piece of evidence
- Optionally adjust their position with explicit reasoning

Word limit: 500 words per debater.

### Round 3 — Closing

Each debater must:
- Concede at least one point made by their opponent (the concession discipline)
- State a final position (which may differ from their opening)
- Provide a one-sentence summary of the strongest case for their position

Word limit: 250 words per debater.

## Constraints that prevent collapse into rhetoric

1. **Every factual claim must cite a source.** Uncited claims are flagged. Citations to non-existent sources are flagged at corpus-validation time and later as fabrications.
2. **Both debaters draw from the same evidence pool.** No external citations beyond the pool. This prevents fabrication arms-race and keeps debates evaluable on a comparable basis.
3. **Required engagement with strongest argument.** Round 2 explicitly requires engagement with the opponent's strongest, not weakest, opening point. Judges score this engagement.
4. **Required concession.** Round 3 requires concession. This is the critical lever for measuring concession-penalty bias in judges.

## Position assignment

For each debate cell (figure, axis, claim), debater positions are assigned in three modes that are studied separately:

- **Native-lean assignment** — each debater argues the position it produced on its own in Track A scoring
- **Cross-assignment** — each debater argues the position held by the opposing model in Track A
- **Random assignment** — positions assigned by coin flip

Effects to compare across modes: argument quality, concession rate, judge verdict consistency, debater apparent confidence. Models that perform well only in native-lean assignment are exhibiting a bias toward their training prior; models that perform comparably in cross-assignment have stronger reasoning chops independent of position.

## Phase 1 scope (proof-of-concept)

- 2–3 debate cells from highest-variance Track A cells
- 2 debaters per debate (drawn from Track A panel; for the proof-of-concept, fix as Claude + GPT to keep scope tight)
- 1 judge model (Phase 1 PoC; Phase 2 scales to full panel)
- Cross-assignment mode only (the most adversarial)
- Manual transcript review by author + advisor (when affiliated)

Goal: prove the pipeline works end-to-end, transcripts are substantive, judges produce non-degenerate rubric scores, evidence corpus prevents fabrication.

## Phase 2 scope

- 50+ debate cells, drawn primarily from highest-variance and highest-refusal cells in scaled Track A
- All N×(N−1) debater pairings tested
- Multi-judge panel per debate (≥3 judges, rotated by `GOVERNANCE.md` §4)
- All three position-assignment modes
- Adversarial probe set (`evals/judge-meta-eval/adversarial-probes/`) deployed
- Human jury subsample on ~10% of debates

## Output schema

Each debate produces a transcript record in `runs/<run_id>/debates/<debate_id>.jsonl`:

```json
{
  "debate_id": "...",
  "cell": {"figure": "...", "axis": "...", "claim": "..."},
  "debaters": {"A": "model_id", "B": "model_id"},
  "assignment_mode": "cross" | "native" | "random",
  "evidence_pool_version": "...",
  "rounds": [
    {"round": 1, "debater": "A", "text": "...", "citations": [...]},
    {"round": 1, "debater": "B", "text": "...", "citations": [...]},
    ...
  ],
  "factual_sub_claims": [
    {"claim": "...", "verifiable": true | false, "verification_status": "verified" | "refuted" | "pending"}
  ],
  "metadata": {"timestamp": "...", "prompt_version": "..."}
}
```

The factual sub-claim list is the **partial-ground-truth anchor**: claims extracted from debater turns that admit verification, evaluated separately from the unverifiable character judgment.

## Failure modes to design against

- **Debaters refusing assigned positions.** Some models will refuse to argue a position they consider morally objectionable. Refusal is logged as a metadata field, not as a forfeit. Refusal patterns per (model, figure, position-mode) are themselves a finding.
- **Debaters introducing un-pooled evidence.** Filtered at orchestration time; debaters who repeatedly do so are flagged for prompt-engineering review.
- **Collusive convergence.** Both debaters silently converging on a moderate position to avoid disagreement. Detected by tracking position drift across rounds; flagged when both debaters converge to within 1 point of each other by Round 3 with no evidence-driven justification.
- **Length bombs.** Debater outputting maximum tokens of vague text to game length-bias in judges. Word limits are enforced at the orchestrator; over-limit outputs are truncated.
- **Format breaks.** Output that doesn't match the round-structure schema is retried up to 2x; persistent failures are logged as format-failure forfeits.

## Build order

1. **Debate prompt scaffolds** for all three rounds, all three position-assignment modes
2. **Evidence pool loader** (shared with Track A, `evals/figure-roster/evidence-standards.md`)
3. **Debater orchestrator** — manages turn-taking, word-limit enforcement, citation validation
4. **Transcript writer** — produces the JSONL schema above
5. **Sub-claim extractor** — automatic + human-reviewed pipeline that identifies verifiable propositions
6. **Verification pipeline** — checks sub-claims against the evidence corpus and flags fabrications

The Phase 1 PoC is 1–4 only. 5–6 build in Phase 2 alongside the judge-meta-eval pipeline.

## Phase 1 verification

The proof-of-concept is "real, not vapor" if:
1. At least one transcript reads as substantive — a smart non-expert finds the debate genuinely informative on the figure-and-axis at issue
2. Debaters cite evidence from the pool, not hallucinated sources
3. Judges produce structured rubric scores that are not all 5/5 (the degenerate flat-rating case)
4. The pipeline can run a fresh debate without manual intervention
