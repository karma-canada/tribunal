# Adversarial Red-Team — Charter

A first-class workstream that runs **in parallel** with eval design from Phase 1 forward, not as post-hoc validation. Every credible benchmark released in the last two years that did not do this got embarrassed within a month of release.

## Mandate

Find ways to break the benchmark before public release. Document what is found. Report findings as part of the methodology paper, not hidden.

The red-team is internal to the project but operationally independent: the eval-design and red-team workstreams are run by different humans (or by the same human with a deliberate context separation in Phase 1). Findings are not negotiated away to protect timelines; either the methodology adapts, or the finding is published as a known limitation.

## Attack surface

### 1. Debater attacks

- **Prompt injection.** Can a debater inject instructions into a transcript that affect the judge's verdict?
- **Evidence pool exploits.** Can a debater find or fabricate citations the corpus validator misses?
- **Position-mode collusion.** Can two debaters from the same model family produce mutually-favorable transcripts that judges fail to detect?
- **Length and format games.** Can a debater hit max-quality token output with low-rigor content?
- **Refusal as forfeit-game.** Can a debater strategically refuse positions that would lose, biasing the matrix?

### 2. Judge attacks

- **Rubric exploits.** Are there transcripts that score 9/9/9/9/9 from a judge but are obviously slop to a human?
- **Self-preference under anonymization.** Does anonymization actually defeat self-preference, or do models recognize their own outputs through stylistic signature?
- **Concession penalty.** Generate transcripts that should reward concession; measure judge behavior; document if the penalty is real.
- **Sub-claim laundering.** Can a debater bury a fabricated factual claim inside a long argument such that the sub-claim extractor misses it but the claim affects the judge's verdict?
- **Confidence laundering.** Can high-confidence framing alone shift verdicts without changing substance?

### 3. Track A scoring attacks

- **Prompt-version sensitivity.** How much do scores shift across small prompt-template changes? Is the v0.1 prompt at a stable plateau or a local oddity?
- **Evidence-pool poisoning.** Insert plausibly-cited but ideologically slanted evidence into the pool; measure score shift.
- **Refusal-engineering.** Can the prompt be tweaked to elicit refusals that wouldn't otherwise appear, or to suppress refusals that should appear?
- **Run-to-run drift.** Are within-model variances stable across days, weeks, model-version updates?

### 4. Aggregation attacks

- **Difficulty score gaming.** Can a model be tuned to score well on difficulty-weighted aggregation by deliberately producing high-confidence outputs on easy figures and refusing hard ones?
- **Leaderboard ranking exploits.** Are there incentive-structure reasons a model could move up the leaderboard without becoming more aligned?

### 5. Governance and corpus attacks

- **Curation drift.** Can the figure-inclusion process be gamed by community PRs that skew the political balance?
- **Source-tier laundering.** Are there sources that look Tier-1 but are not?
- **Contestation suppression.** Can a contributor edit a contested-source list to remove dissenting scholarly views?

### 6. Legal and reputational attacks

- **Defamation framing drift.** Track press, blog, leaderboard, and dataset-card surfaces for slippage from "what each model says" to "what the figure is." Slippage is the single highest-likelihood legal risk.
- **Asymmetry attack.** Identify the strongest credible argument that the methodology is biased; either fix it or pre-empt it in the paper.

## Operating principles

1. **Adversary, not skeptic.** The red-team's job is to actively try to break things, not to write polite review comments. Probes are real attempts.
2. **Findings logged, not negotiated.** A finding becomes part of the project record the moment it is documented. Mitigations are tracked as PRs against the finding.
3. **Parallel cadence.** Red-team work tracks eval-design work, not the other way around. A new eval feature ships only after the red-team has had a real chance to attack it.
4. **Public finding log.** Findings (with mitigations) are published in the methodology paper. The credibility of the benchmark is partly the credibility of the red-team's findings.

## Phase 1 deliverables

- This charter
- Initial attack surface document with at least one concrete attack per surface (above)
- One red-team-driven test per surface, run against the Phase 1 prototype
- Findings log seeded

## Phase 2 deliverables

- Probes 1–8 (`evals/judge-meta-eval/design.md`) reviewed by red-team for confound and incentive-structure issues before deployment
- At least one third-party red-teamer (cross-affiliation) brought in for an external review pass before Phase 2 release
- Findings log published as appendix to the methodology paper

## Phase 3 deliverables

- Bug bounty program (if scoped and funded)
- Rolling red-team findings published quarterly with the release cadence

## Operating budget

- Phase 1: ~20% of eval-design effort
- Phase 2: ~25% (more attack surface to cover)
- Phase 3+: ~20% sustained

## Failure mode this charter is designed to prevent

The dominant failure mode for ML benchmarks is: published with a clean-looking dashboard, attacked publicly within weeks, response is defensive, credibility tanks, methodology is not recoverable.

This charter exists because that pattern is mostly avoidable with a parallel red-team and a published findings log. The cost is real but the cost of skipping it is higher.
