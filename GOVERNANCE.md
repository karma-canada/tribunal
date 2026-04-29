# Governance

Rules the project will be held to. Not aspirations, not hand-waves. Pre-registered before the first debate runs and before the first matrix is published.

This document covers seven decision surfaces:

1. Figure curation
2. Axis acceptance
3. Evidence corpus standards
4. Judge rotation and anonymization (Track B)
5. Scoring run protocol (Track A)
6. Jurisdictional and hosting choices
7. Conflicts of interest, funding exclusions, and amendment process

## 1. Figure curation

### 1.1 Phase 1 (mixed roster)

Phase 1 includes 10–15 figures drawn from two pools, in roughly equal proportion:

**Historical pool.** Figures who have been the subject of professional historical scholarship for ≥50 years and whose primary actions can be sourced to ≥3 independent secondary works of standing. Initial set under consideration (final list pre-registered before scoring begins): Cromwell, Robespierre, LBJ, Lincoln, Bismarck, Catherine the Great, Thatcher, Mao.

**Contemporary pool.** Figures who are current or recent occupants of major political offices, balanced left/right by an explicit pairing rule (each contemporary figure is paired with another whose political coalition opposes theirs in the same democracy or international context). Initial pool under consideration: a balanced selection from current European, North American, and Latin American politics.

**Exclusion list.**
- **Sitting heads of state in the author's country of residence (Canada).** Excluded until at least one full electoral cycle has passed since the end of their tenure. The current Canadian Prime Minister (Carney) is therefore excluded. This is non-negotiable and applies regardless of disclosure.
- **Figures currently subject to active criminal proceedings** in jurisdictions where the project may publish, until those proceedings are resolved or stayed.
- **Figures whose inclusion would produce gross asymmetry** between the political pools (e.g., 8 left-coded vs 2 right-coded). Balance is verified at roster lock.

### 1.2 Phase 3 expansion

Phase 3 expands the contemporary pool. Inclusion at this phase requires:
- Explicit COI declaration in the dataset card
- Sitting-head-of-state exclusion still in force for the author's country
- Inclusion approved by at least two reviewers who declare opposing political affiliations (a minimal-balance check, formalized in `gtm/PARTNERSHIPS.md` once review-panel composition is set)

### 1.3 Community contributions

After Phase 2 release, community PRs proposing new figures are accepted via the same criteria. PRs must include:
- Pairing rationale (which existing figure does this one balance?)
- Initial evidence-corpus pointer (≥3 sources)
- Disclosure of contributor's political affiliation if relevant

PRs are reviewed by the maintainer with cross-affiliation second-eyes.

## 2. Axis acceptance

### 2.1 Locked v1 axes

Phase 1 ships with four character axes, locked: **hypocrisy, honor, opportunism, integrity**. These were chosen because they were proposed by a subject-area discussion (not derived by an LLM) and because they produce non-trivial inter-model variance in informal pre-tests.

### 2.2 Extension axes (Phase 2)

Phase 2 adds extension axes drawn from a structured cluster framework:
- **Capacity-for-harm cluster:** cruelty, mendacity
- **Ego cluster:** vanity, magnanimity
- **Operational cluster:** discipline, courage
- **Reflective cluster:** self-knowledge, loyalty

Axes from outside this set may be proposed but require:
- A definition with operationalization (what evidence counts for/against?)
- A cross-figure smoke test showing non-trivial variance
- Cross-affiliation review approval

### 2.3 Reader-customizable axes

The leaderboard interface permits readers to select which subset of the locked + extension axes to view. It does *not* permit ad-hoc axis creation, because user-generated axis labels destroy comparability across the dataset. New axes go through 2.2.

## 3. Evidence corpus standards

### 3.1 Source hierarchy

For any evidence cited in a debate or scoring run:
- **Tier 1 (required for character-relevant claims):** Peer-reviewed scholarly works, books from established academic publishers, primary documents (court records, official government statements, contemporaneous news of record).
- **Tier 2 (permitted as supplementary):** Reputable news organizations, biographies from non-academic but credible publishers.
- **Tier 3 (permitted only as pointer, not as sole source):** Wikipedia, encyclopedic summaries.

Wikipedia is not banned, but no character-relevant claim may rest on Wikipedia alone.

### 3.2 Versioning

The evidence corpus is versioned alongside the dataset. Each (figure, claim, source) triple has a fingerprint that locks the source as accessed at a specific timestamp. Source URLs, page numbers, and accessed-on dates are required.

### 3.3 Contestation handling

Where scholarly sources contest a fact, both the claim and the contestation are included in the corpus, marked as contested. Debaters and scoring runs may invoke either side; judges are expected to recognize contestation and not penalize debaters for citing the side opposite the judge's own reading.

### 3.4 Fabrication policy

Any debater output that cites a non-existent source is flagged in the dataset and reported. Patterns of fabrication per model are tracked. Plant-and-detect fabrication probes are part of the adversarial probe set (`evals/judge-meta-eval/adversarial-probes/`).

## 4. Judge rotation and anonymization (Track B)

### 4.1 Panel composition

Every Track B debate is judged by a panel of ≥3 LLMs drawn from at least 3 distinct model families. Panel composition is randomized within constraints (no two panelists from the same family; at least one panelist whose training cutoff is ≥6 months earlier than the most recent).

### 4.2 Anonymization

Debater identities are stripped from transcripts before judges see them, where the model API permits this. Where it does not, this limitation is noted in the dataset.

### 4.3 Self-judging rule

A model never judges a debate in which it was a debater. This is enforced at the orchestration layer.

### 4.4 Judge rotation across versions

When a frontier model releases a new version, the previous version is *not* immediately retired from the judge panel. Both versions remain on the panel for at least one quarterly release cycle so version-to-version consistency can be measured.

## 5. Scoring run protocol (Track A)

### 5.1 Repetitions

Each (model, figure, axis) cell is scored ≥5 times to measure within-model variance. Variance distributions are reported alongside point estimates.

### 5.2 Prompt versioning

The scoring prompt is versioned. Re-runs against new prompt versions are reported as version-comparison studies, not as updates to the matrix.

### 5.3 Refusal handling

Refusals, hedges, and unparseable outputs are recorded as such. They are *not* substituted with default scores. A refusal map per (model, figure, axis) is published alongside the score matrix.

### 5.4 Locale

Each cell is scored in English by default. Phase 2 adds non-English replications for figures whose primary language is non-English. Score deltas across languages are reported as the language-locale-skew finding.

## 6. Jurisdictional and hosting choices

### 6.1 Primary jurisdiction

Canada. Author resides in Canada; primary publication is Canadian; legal review queue uses Canadian counsel.

### 6.2 Multi-jurisdictional hosting

The canonical artifact (dataset, code, transcripts) is mirrored to:
- Hugging Face (US) — primary discovery surface
- GitHub (US) — code repository
- A Canadian academic repository (Borealis or equivalent) — sovereign archive
- A second academic mirror in a non-US, non-Canadian jurisdiction (target: Zenodo, EU) — diversification

The benchmark survives platform-moderation decisions made in any single jurisdiction.

### 6.3 Domain

Project domain is `.ca` and registered to a Canadian individual or entity. Decision deferred to post-naming.

## 7. Conflicts of interest, funding, amendments

### 7.1 Funding exclusions

The project does not accept funding from:
- Any frontier-model provider whose models appear on the leaderboard (OpenAI, Anthropic, Google, Meta, xAI, Mistral, Cohere, DeepSeek, Alibaba/Qwen, etc.)
- Foundations or organizations with a declared political mission on either side of the political axis the project measures
- Governments that are themselves represented by figures on the leaderboard, except for Canadian academic-research funding bodies subject to standard public-research grant terms (NSERC, CIFAR, SSHRC, FRQNT, etc.)

Inference cost may be comped by frontier-model providers under a published-on-launch transparency standard, provided no review or pre-publication access is exchanged.

### 7.2 Author COI

Author political affiliations are declared in the dataset card. The Canadian sitting-head-of-state exclusion (§1.1) is the operational expression of personal-jurisdiction COI.

### 7.3 Reviewer COI

Phase 3 reviewers (figure-inclusion review panel) declare political affiliations on selection. The panel maintains cross-affiliation balance.

### 7.4 Amendment process

This document is versioned. Amendments require:
- A pull request with rationale
- A 14-day public comment window before merge (Phase 2+ only; Phase 0–1 amendments are at maintainer discretion with full changelog disclosure)
- For amendments that loosen any exclusion (e.g., narrowing the sitting-head-of-state rule), cross-affiliation review approval

Changelogs are appended to the bottom of this document and dated.

---

## Changelog

- **2026-04-28** — v0.1 initial draft. Phase 0 deliverable.
