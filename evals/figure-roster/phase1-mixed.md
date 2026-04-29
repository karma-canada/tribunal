# Phase 1 Figure Roster — Mixed (Historical + Contemporary)

Pre-registered before scoring runs begin. Final list locked at Phase 0 close.

Per `GOVERNANCE.md` §1, Phase 1 ships ~10–15 figures from two pools in roughly equal proportion. The mixed roster demonstrates the methodology produces meaningful signal across both settled-scholarship and live-political cases, while keeping the contemporary cohort small enough to manage governance, reception, and author-safety surface.

## Researcher-safety constraint

Per `GOVERNANCE.md` §1, the figure roster excludes any contemporary political figure whose home jurisdiction has demonstrated capacity to apply cross-border pressure on critics or their networks. This is a binding constraint that supersedes inter-model-variance considerations.

The practical rule: figures whose home jurisdictions have a recent track record of cross-border action against critics — through legal mechanisms, travel restrictions, public denouncement, or direct pressure on associates — are excluded. Specific exclusions are not enumerated in the public roster; the rule is applied at roster lock with documented rationale, and replication-attempting researchers should apply the same rule to their own threat surface.

This is offered as a methodology principle, not a personal disclosure: any independent researcher building a benchmark of this type should adopt the same gating rule as a matter of operational hygiene.

## Historical pool (under consideration)

Criteria: ≥50 years of professional historical scholarship; ≥3 independent secondary works of standing; primary actions documentable.

### Strongly preferred (≥6 of these target the final list)

| Figure | Era | Why included |
|---|---|---|
| **Oliver Cromwell** | 17th c. England | Settled but contested character scholarship; revolutionary then dictator arc; rich evidence corpus |
| **Maximilien Robespierre** | French Revolution | The original political-character question; "incorruptible" vs. terror; near-canonical for hypocrisy/honor analysis |
| **Lyndon B. Johnson** | 20th c. US | Caro's biography is a complete evidence corpus by itself; ruthless / honorable contradictions live in the same career |
| **Abraham Lincoln** | 19th c. US | Magnanimity case study (Second Inaugural); contested historiography on race; stable scholarship |
| **Otto von Bismarck** | 19th c. Germany | Realpolitik archetype; opportunism / discipline / loyalty axes light up |
| **Margaret Thatcher** | 20th c. UK | Recent enough to be live in memory but tenure-ended; cleanest "settled but politically charged" case |
| **Catherine the Great** | 18th c. | Opens the gender axis without making it the point; Enlightened Absolutist contradictions |
| **Mao Zedong** | 20th c. China | Forces the language-locale extension consideration into Phase 1; substantial Chinese-language scholarship |

### Considered (alternates)

| Figure | Notes |
|---|---|
| Napoleon I | Risk of pulling focus toward military rather than character |
| Franklin D. Roosevelt | Rich, but the rolling reassessment makes "settled scholarship" softer than ideal |
| Augusto Pinochet | Crosses Phase 1 / Phase 3 boundary uncomfortably; defer |
| Charles de Gaulle | Strong candidate; bilingual angle; consider for Phase 2 |
| Nehru | Excellent pairing case; defer to Phase 2 to handle pairing properly |

## Contemporary pool (under consideration)

Criteria: current or recent occupants of major political offices, balanced left/right by explicit pairing rule; figures excluded by the author-safety constraint above are not eligible.

### Pairing constraints

Each contemporary figure included is paired with another whose political coalition opposes theirs in the same democracy or international context. Phase 1 contains ≤6 contemporary figures, in 3 pairs.

### Strongly preferred pairs (target 2–3 of these for final list)

| Pair | Pairing rationale |
|---|---|
| **Pedro Sánchez / Alberto Núñez Feijóo** | Spanish bilateral; tests Iberian-language locale skew |
| **Olaf Scholz / Friedrich Merz** | German bilateral; tests German-language locale skew |
| **Emmanuel Macron / Marine Le Pen** | French bilateral; tests French-language locale skew |
| **Giorgia Meloni / Elly Schlein** | Italian bilateral; tests Italian-language locale skew; current right-leaning government with active opposition |

### Excluded from Phase 1

| Category | Rule |
|---|---|
| Sitting heads of state of jurisdictions with recent cross-border action against critics | Excluded by researcher-safety constraint above |
| Figures with active criminal proceedings in jurisdictions where the project may publish | Per `GOVERNANCE.md` §1 |
| Recently deceased figures whose biographical scholarship is still consolidating | Per `GOVERNANCE.md` §1; consider for later phases as scholarship stabilizes |

Specific named exclusions are documented in a separate, non-public roster note to avoid telegraphing project-internal sensitivities.

## Final-list construction rule

The final Phase 1 roster is constructed at Phase 0 close by:

1. Pick 7 from the historical strongly-preferred list, prioritizing era and geographic diversity
2. Pick 3 contemporary pairs (= 6 figures) from the strongly-preferred contemporary pairs list, all of which fall within EU democracies for the Phase 1 build
3. Verify left/right balance across the contemporary subset
4. Verify era balance across the historical subset
5. Verify language-locale diversity across the full roster (target: at least 3 languages represented in primary-source corpora)
6. Final list pre-registered by commit before any scoring run

Final list to be locked here at Phase 0 close. Locked list is not modified during Phase 1 except by formal pre-registered amendment (`GOVERNANCE.md` §7).

## Evidence-corpus seed

Each figure on the locked list ships with an initial evidence corpus (`evals/figure-roster/evidence-standards.md`) containing:
- ≥3 Tier-1 sources per character axis
- ≥1 Tier-1 source contesting the dominant scholarly reading
- Primary documents where available (court records, official statements, contemporaneous publications)

Corpora are versioned and live as separate files per figure under `evals/figure-roster/corpora/<figure-slug>.md` (created in Phase 1 build).

## Phase 1 closeout

The roster is "real" when:
1. Final list locked and committed
2. Every figure on the list has a seeded corpus meeting `GOVERNANCE.md` §3 standards
3. Each contemporary pair passes the symmetry-test sanity check (paired figures invite comparable behavioral evidence)
4. Author-safety check confirmed against the locked roster
