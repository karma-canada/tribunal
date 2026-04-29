# Evidence Corpus Standards

Per `GOVERNANCE.md` §3. Defines what counts as evidence in Track A scoring runs and Track B debates.

## Source tier hierarchy

### Tier 1 — required for character-relevant claims

- Peer-reviewed scholarly works (journal articles, university press monographs)
- Books from established academic publishers (Oxford UP, Cambridge UP, Princeton UP, Yale UP, equivalent)
- Primary documents — court records, official government statements, contemporaneous news of record (Times, Le Monde, Frankfurter Allgemeine, NYT pre-1990 archive, etc.)
- Edited volumes of letters, speeches, or diplomatic correspondence published by academic presses

### Tier 2 — permitted as supplementary

- Reputable news organizations of record (NYT, Guardian, Le Monde, Globe and Mail, etc.)
- Biographies from non-academic but credible publishers
- Curated archival collections (national archives, presidential libraries)
- Specialist scholarly journals outside top tier

### Tier 3 — permitted as pointer, not as sole source

- Wikipedia (any language)
- Encyclopedia entries (Britannica, Oxford Reference, Stanford Encyclopedia of Philosophy)
- Reputable encyclopedic-style summaries

**Rule:** No character-relevant claim may rest on Tier 3 alone. Tier 3 sources may serve as discovery / index entries pointing to Tier 1 or Tier 2 material.

## Per-figure corpus structure

Each figure's evidence corpus lives at `evals/figure-roster/corpora/<figure-slug>.md` (created during Phase 1 build). Each corpus contains:

```
# Evidence Corpus — <Figure Name>

## Source pointers (Tier 1)
- <Author, Title, Year>: <one-line description of what this source covers>
- ...

## Source pointers (Tier 2)
- ...

## Per-axis evidence
### Hypocrisy
- <Claim summary> — <citation> — <Tier>
- <Counter-claim summary> — <citation> — <Tier>
...

### Honor
- ...

### Opportunism
- ...

### Integrity
- ...
```

## Versioning

The evidence corpus is versioned alongside the dataset. Each (figure, claim, source) triple has a fingerprint that locks the source as accessed at a specific timestamp:

- Source URLs include accessed-on dates
- Page numbers required for book citations
- Edition specified for any source that has been revised
- Where scholarly sources contest a fact, both sides are recorded in the corpus, marked as `contested: true`

## Contestation handling

For claims where serious scholarly sources disagree:

- Both positions are present in the corpus
- Each position has Tier-1 backing
- Debaters and scoring runs may invoke either position
- Judges (Track B) are expected to recognize contestation and not penalize debaters for citing the position opposite the judge's own reading

## Fabrication detection

Any debater or scoring-run output that cites a non-existent source is flagged in the dataset and reported. Patterns of fabrication per model are tracked in the bias-comparator analysis.

The adversarial red-team probe set (`evals/judge-meta-eval/adversarial-probes/` once built) includes planted fabrications to measure judge catch rates. See `evals/redteam/charter.md`.

## Wikipedia policy (in detail)

Wikipedia is permissible because:
- It often provides the cleanest discoverable index of sources for a figure
- For widely-studied figures, Wikipedia citations point to Tier 1 scholarship
- Excluding Wikipedia entirely produces an unrealistic prompt context

Wikipedia is constrained because:
- It is editable and can shift between scoring runs
- For contested or contemporary figures, Wikipedia content reflects active partisan editing
- Citing Wikipedia alone for a character-relevant claim is methodologically lazy

**Operational rule:** model scoring runs MAY draw on Wikipedia for figure context but MUST cite a Tier 1 or Tier 2 source for any specific claim that supports a score. The prompt scaffold reflects this — `evals/bias-comparator/run.py`'s prompt asks for "specific source citation (book title and author, primary document, or contemporary record)."

## Corpus build sequence

For each figure on the locked Phase 1 roster:

1. Identify ≥3 Tier-1 scholarly works that comprehensively cover the figure's career
2. For each character axis:
   - Identify ≥3 Tier-1 evidence pointers supporting the dominant scholarly reading
   - Identify ≥1 Tier-1 evidence pointer contesting that reading
3. Identify primary documents where available (court records, official statements, contemporaneous publications)
4. Compile into `corpora/<figure-slug>.md`
5. Version the corpus with the dataset

## Phase 1 prototype note

The Phase 1 prototype (running 2026-04-28) does **not** yet include a curated per-figure evidence corpus injected into the model prompts — models score from their training-data knowledge of the figures, with the source citations they invoke evaluated post-hoc. This is documented as a methodological limitation of v0.1. v0.2 of the bias-comparator pipeline injects a curated corpus into the prompt context, allowing measurement of citation grounding (model claims vs. corpus content) as a separate axis.
