# Legal Posture

What the project does to keep itself defensible. Pre-Phase-1 audit checklist plus standing posture decisions.

## Standing posture

### Jurisdiction

- **Primary:** Canada. Author resident. Publication and press contact Canadian.
- **Secondary mirrors:** US (HF, GitHub) and EU (Zenodo) for distribution. The benchmark survives a moderation decision in any single jurisdiction.
- **Counsel:** Canadian media/IP lawyer engaged for one-hour sanity check before Phase 2 release. Counsel of record retained when Phase 3 contemporary roster goes live.

### Defamation framing (the load-bearing argument)

Tribunal's **methodology and outputs** are *reports of model behavior*, not editorial claims about figures. The artifact is "Model X said Y about figure Z, citing W" — a faithful, sourced, versioned report of what frontier LLMs produced under specified conditions. The story the project tells is the *spread across models*, not any single model's score, and not any aggregate score about the figure.

This framing materially changes defamation surface relative to a project that publishes "X is a 9/10 hypocrite." Maintaining the framing across all surfaces (paper body, leaderboard, press, dataset card, social) is part of the legal posture, not just an editorial choice. Drift from this framing — slipping into "Tribunal scores X at 9/10" — is the single largest avoidable defamation risk and is policed in style guides.

### Evidence corpus discipline

Every claim made in a debate or scoring run must cite to a source. Sources are versioned. Where scholarly sources contest a fact, both sides are recorded. This protects the project under fair-comment and academic-research defenses in Canadian, UK, and EU defamation law.

### Author posture

Independent Canadian-biographical author. Affiliated to a Canadian institution before formal release where possible. Cross-affiliation review panel for Phase 3 contemporary roster.

## Pre-Phase-1 audit checklist

Before any debate runs or scoring runs against named figures, complete each of the following:

### A. Model-provider TOS audit

For each frontier-model provider whose model will appear on the leaderboard, review the relevant policy and document:

- [ ] **OpenAI** — Usage Policies, particularly clauses on benchmarking and on outputs about real people
- [ ] **Anthropic** — Usage Policy, clauses on naming individuals in evaluation contexts
- [ ] **Google** — Generative AI Prohibited Use Policy
- [ ] **Meta** — Llama Acceptable Use Policy
- [ ] **xAI** — Grok terms
- [ ] **Mistral** — Acceptable Use
- [ ] **Cohere** — Usage Guidelines
- [ ] **DeepSeek** — Terms of Use
- [ ] **Alibaba/Qwen** — Terms

For each provider, record:
- Whether outputs about named living individuals are permitted under TOS
- Whether benchmarking and publishing model outputs is permitted
- Whether comparative leaderboards are permitted
- Any contact protocol required for publication

If a provider's TOS prohibits or constrains the project, the model is either (a) excluded from the panel, (b) included with the constraint documented, or (c) the project pursues written permission. No provider's outputs are published in violation of their TOS.

### B. Defamation review

Before Phase 1 publication (even unlisted HF release):

- [ ] One-hour consultation with a Canadian media lawyer
- [ ] Sanity check on the figure roster (especially contemporary inclusions in Phase 1 mixed roster)
- [ ] Sanity check on the dataset card and leaderboard framing
- [ ] Sanity check on the press strategy (Phase 2)

Counsel is briefed on the defamation framing (above) and asked specifically whether the framing as constructed protects the project under Canadian defamation law and whether any specific roster inclusions warrant additional caution.

### C. PIPEDA and personal-data review

Public figures' political conduct is generally outside PIPEDA's scope (publicly available info, exceptions for journalism / artistic / literary purposes), but:

- [ ] Confirm the journalism / academic-research carve-outs apply
- [ ] Document the personal-data-handling policy
- [ ] Confirm the dataset does not include personal information beyond what is in the evidence corpus (no scraped private data)

### D. Copyright and quotation

The evidence corpus quotes from scholarly works and news reporting. Confirm:

- [ ] Quotation length stays within fair-dealing thresholds (Canadian fair dealing for research, criticism, news reporting)
- [ ] Each quotation is attributed to source with publication metadata
- [ ] Bulk text from copyrighted works is not redistributed; the corpus contains pointers and short quotations, not full texts

## Defamation review queue

Throughout the project, items requiring counsel review go on the queue rather than being published immediately:

| Item | Priority | Phase |
|---|---|---|
| Phase 1 figure roster final | high | Phase 0 close |
| Phase 1 dataset card + leaderboard framing | high | Phase 1 close |
| Phase 2 press materials | medium | Phase 2 mid |
| Phase 2 arXiv preprint | high | Phase 2 close |
| Phase 3 contemporary roster expansion | critical | Phase 3 open |
| Any op-ed or press piece naming a figure | high | as drafted |
| Any community PR adding a figure | medium | as filed |

Items above "high" must clear counsel before publication.

## Refusal handling

If a frontier-model provider requests removal of their model's outputs from the dataset or leaderboard:

1. Acknowledge the request in writing within 5 business days
2. Review the basis for the request (TOS, specific figure, specific axis, etc.)
3. If TOS-grounded, comply and document the removal in the dataset changelog
4. If TOS does not support removal, respond with the legal basis for retention (academic research, fair dealing, public-interest journalism) and seek counsel review
5. Disputes that escalate are documented in a public transparency log

## Adversary modeling

The project pre-empts plausible adversaries:

- **A frontier-model provider unhappy with a finding.** Mitigated by: TOS audit before publication, defamation framing, transparent methodology, willingness to comply with TOS-grounded requests.
- **A figure on the roster (or their representatives).** Mitigated by: defamation framing, evidence corpus discipline, counsel review before publication, sitting-head-of-state exclusion.
- **A partisan critic claiming asymmetric methodology.** Mitigated by: pre-registered curation criteria, balanced pairings, cross-affiliation review panel for Phase 3, public methodology, refusal asymmetry analysis published openly.
- **A SLAPP suit.** Mitigated by: Canadian jurisdiction (anti-SLAPP statutes in Ontario, BC, Quebec), academic-research framing, evidence-corpus discipline, multi-jurisdictional artifact mirrors so a single-jurisdiction injunction does not remove the work.
- **Doxxing or harassment of contributors.** Mitigated by: real-name author posture is voluntary; reviewers and contributors may operate pseudonymously; project does not require personal information from community PR contributors beyond what is necessary to verify they are not affiliated with a figure on the roster.

## Counsel engagement plan

- **Pre-Phase 2 (now):** Identify and short-list 2–3 Canadian media/IP lawyers with relevant practice area. Cost target: under $1,500 for the initial sanity-check consultation.
- **Phase 2 release:** Counsel reviews preprint, dataset card, and press strategy. Cost target: under $5,000.
- **Phase 3 release:** Counsel of record retained on a small monthly retainer ahead of contemporary-roster expansion. Cost depends on retainer terms.
- **As-needed:** Counsel review for any op-ed, press release, or community PR that names a contemporary figure outside the published roster.

## Public-facing legal page

The project landing page (Phase 2) carries:
- A statement of the defamation framing (outputs are reports of model behavior, not editorial claims)
- The TOS audit summary per provider
- The evidence-corpus standards (linked to GOVERNANCE.md)
- A removal-request contact and protocol
- A transparency log link

Lawyer reviews the public-facing legal page before publication.

---

## Changelog

- **2026-04-28** — v0.1 initial draft. Phase 0 deliverable.
