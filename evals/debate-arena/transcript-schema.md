# Track B — Debate Transcript Schema

Versioned data model for debate transcripts. Phase 1 PoC uses v0.1; Phase 2 may extend.

## Schema (v0.1)

Each debate produces one record at `runs/<run_id>/debates/<debate_id>.jsonl`:

```json
{
  "schema_version": "0.1",
  "debate_id": "<uuid>",
  "run_id": "<run_id>",
  "ts_started": "<ISO 8601>",
  "ts_completed": "<ISO 8601>",

  "cell": {
    "figure": "<figure_id>",
    "axis": "<axis_id>",
    "claim": "<one-sentence claim being debated, e.g. 'Cromwell scored 7/10 on hypocrisy'>"
  },

  "debaters": {
    "A": {"model_id": "<provider/model-name>", "position": "argues_for", "assigned_score": <int>},
    "B": {"model_id": "<provider/model-name>", "position": "argues_against", "assigned_score": <int>}
  },

  "assignment_mode": "native | cross | random",

  "evidence_pool_version": "<version string for the corpus snapshot used>",

  "rounds": [
    {
      "round": 1,
      "type": "opening",
      "debater": "A",
      "ts": "<ISO 8601>",
      "model_id": "<provider/model-name>",
      "text": "<debater output>",
      "citations": [
        {"claim": "<claim summary>", "source": "<source citation>", "in_pool": true | false}
      ],
      "tokens": {"input": <int>, "output": <int>},
      "elapsed_s": <float>
    },
    ...
  ],

  "factual_sub_claims": [
    {
      "claim_id": "<uuid>",
      "claim_text": "<verifiable factual proposition>",
      "extracted_from_round": <int>,
      "extracted_from_debater": "A | B",
      "verifiable": true | false,
      "verification_status": "verified | refuted | pending | not_in_corpus",
      "verification_evidence": "<source from corpus that verifies/refutes>"
    }
  ],

  "fabrications_detected": [
    {
      "round": <int>,
      "debater": "A | B",
      "claim": "<fabricated citation>",
      "detected_at": "ts ISO 8601"
    }
  ],

  "metadata": {
    "prompt_version": "<version>",
    "evidence_pool_size_chars": <int>,
    "word_limits_enforced": {"opening": 400, "rebuttal": 500, "closing": 250}
  }
}
```

## Judge verdict schema (v0.1)

Per-judge adjudication, one record per (debate × judge) at `runs/<run_id>/judgments/<debate_id>/<judge_id>.jsonl`:

```json
{
  "schema_version": "0.1",
  "debate_id": "<uuid>",
  "judge_id": "<provider/model-name>",
  "ts": "<ISO 8601>",

  "rubric_scores": {
    "A": {
      "rigor": <1-10>,
      "rhetoric": <1-10>,
      "evidence_quality": <1-10>,
      "engagement_with_strongest": <1-10>,
      "concession_quality": <1-10>
    },
    "B": { ... }
  },

  "verdict": "A_wins | B_wins | tie",

  "opinion": "<written rationale, ≤300 words>",

  "fabricated_citations_flagged": [
    {"round": <int>, "debater": "A | B", "claim": "<flagged citation>"}
  ],

  "anonymized_to_judge": true | false,

  "metadata": {
    "prompt_version": "<version>",
    "tokens": {"input": <int>, "output": <int>},
    "elapsed_s": <float>
  }
}
```

## Sub-claim verification schema

Per factual sub-claim, evaluated separately (`runs/<run_id>/sub_claims/<claim_id>.jsonl`):

```json
{
  "schema_version": "0.1",
  "claim_id": "<uuid>",
  "debate_id": "<uuid>",
  "claim_text": "<verifiable proposition>",
  "judges": [
    {
      "judge_id": "<provider/model-name>",
      "verdict": "supported | refuted | unverifiable | unknown",
      "evidence_cited": "<corpus source>",
      "ts": "<ISO 8601>"
    }
  ],
  "ground_truth": "supported | refuted | contested | unknown",
  "ground_truth_source": "<authoritative source from corpus>"
}
```

## Versioning policy

- Schema version is included in every record. Breaking changes increment major version.
- Phase 2 may add fields (additional probe metadata, multi-judge rotation flags, language-locale tags) without breaking v0.1 readers.
- Schema documents (this file) are versioned alongside the dataset; the position paper references the schema version active at the time of each prototype run.

## Storage layout

```
runs/<run_id>/
  config.json                          # run config (models, figures, axes, prompt versions)
  debates/<debate_id>.jsonl            # one record per debate (Track B)
  judgments/<debate_id>/<judge_id>.jsonl  # one record per judge per debate
  sub_claims/<claim_id>.jsonl          # one record per extracted factual sub-claim
  scores.jsonl                         # Track A scoring runs
  summary.md                           # human-readable summary (analyze.py output)
  matrix.csv                           # Track A score matrix
```

## What v0.1 does *not* yet specify

- Cross-debate aggregation schema (will be v0.2 with the difficulty score formula)
- Probe-condition records (paired conditions for adversarial probes — Phase 2 extension)
- Human-jury record schema — see `evals/judge-meta-eval/human-jury-protocol.md`
