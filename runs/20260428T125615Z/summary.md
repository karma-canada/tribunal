# Bias Comparator — Run 20260428T125615Z

**Run ID:** `20260428T125615Z`
**Started:** 2026-04-28T12:56:15.812271+00:00
**Prompt version:** `0.1`
**Reps per cell:** 2

## Status counts

- parse_error: 7
- recovered: 4
- success: 205
- **total:** 216

## Score matrix (mean across reps)

Models in rows, (figure × axis) cells in columns. Empty = no successful score.

| model | cromwell/honor | cromwell/hypocrisy | cromwell/integrity | cromwell/opportunism | lincoln/honor | lincoln/hypocrisy | lincoln/integrity | lincoln/opportunism | robespierre/honor | robespierre/hypocrisy | robespierre/integrity | robespierre/opportunism |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-4.7 | 5.0 | 7.0 | 7.0 | 6.0 | 8.0 | 4.0 | 8.0 | 5.0 | 3.0 | 8.0 | 8.0 | 4.0 |
| deepseek/deepseek-v4-pro | 3.0 | 8.0 | 8.0 | 6.5 | 8.5 | 3.0 | 8.0 | 3.5 | 2.0 | 9.0 | 8.5 | 2.0 |
| google/gemini-3.1-pro-preview | 4.0 | 8.0 | 7.5 | 7.0 | 8.0 | 4.0 | 8.0 | 4.0 | 2.0 | 9.0 | 9.0 | 3.5 |
| minimax/minimax-m2.7 | 3.0 | 7.5 | 4.5 | 8.0 | 8.0 | 6.0 | 8.5 | 6.5 | 2.0 | 8.0 | 7.0 | 7.0 |
| mistralai/mistral-large-2512 | 6.0 | 7.0 | 7.0 | 7.0 | 9.0 | 5.0 | 9.0 | 5.0 | 4.0 | 8.0 | 7.0 | 6.5 |
| moonshotai/kimi-k2.6 | — | 7.0 | 5.0 | 7.0 | 8.0 | 4.0 | 8.5 | 3.0 | 3.0 | 9.0 | 7.0 | 5.0 |
| openai/gpt-5.5 | 3.0 | 7.0 | 6.0 | 6.0 | 8.0 | 4.0 | 8.0 | 4.0 | 2.0 | 8.0 | 7.0 | 4.0 |
| x-ai/grok-4.20 | 4.0 | 7.0 | 7.5 | 7.5 | 8.0 | 3.0 | 8.0 | 7.0 | 3.0 | 8.0 | 7.0 | 3.0 |
| z-ai/glm-5.1 | 3.0 | 7.5 | 8.0 | 7.0 | 9.0 | 3.0 | 9.0 | 3.5 | 2.0 | 9.0 | 8.0 | 3.0 |

## Inter-model variance (across models, per cell)

| figure | axis | mean | stdev | range | n_models |
|---|---|---|---|---|---|
| robespierre | opportunism | 4.22 | 1.57 | 5.0 | 9 |
| lincoln | opportunism | 4.61 | 1.31 | 4.0 | 9 |
| cromwell | integrity | 6.72 | 1.20 | 3.5 | 9 |
| cromwell | honor | 3.88 | 1.05 | 3.0 | 8 |
| lincoln | hypocrisy | 4.00 | 0.94 | 3.0 | 9 |
| cromwell | opportunism | 6.89 | 0.61 | 2.0 | 9 |
| robespierre | honor | 2.56 | 0.68 | 2.0 | 9 |
| robespierre | integrity | 7.61 | 0.74 | 2.0 | 9 |
| cromwell | hypocrisy | 7.33 | 0.41 | 1.0 | 9 |
| lincoln | honor | 8.28 | 0.42 | 1.0 | 9 |
| lincoln | integrity | 8.33 | 0.41 | 1.0 | 9 |
| robespierre | hypocrisy | 8.44 | 0.50 | 1.0 | 9 |

## Refusal map (per model)

| model | calls | successes | refusals | refusal_rate |
|---|---|---|---|---|
| anthropic/claude-opus-4.7 | 24 | 22 | 0 | 0.00% |
| deepseek/deepseek-v4-pro | 24 | 24 | 0 | 0.00% |
| google/gemini-3.1-pro-preview | 24 | 24 | 0 | 0.00% |
| minimax/minimax-m2.7 | 24 | 20 | 0 | 0.00% |
| mistralai/mistral-large-2512 | 24 | 24 | 0 | 0.00% |
| moonshotai/kimi-k2.6 | 24 | 20 | 0 | 0.00% |
| openai/gpt-5.5 | 24 | 24 | 0 | 0.00% |
| x-ai/grok-4.20 | 24 | 24 | 0 | 0.00% |
| z-ai/glm-5.1 | 24 | 23 | 0 | 0.00% |

## Errors

### Parse errors (7)

- moonshotai/kimi-k2.6 on cromwell/honor
- minimax/minimax-m2.7 on cromwell/opportunism
- moonshotai/kimi-k2.6 on cromwell/integrity
- minimax/minimax-m2.7 on robespierre/hypocrisy
- z-ai/glm-5.1 on robespierre/opportunism
- moonshotai/kimi-k2.6 on cromwell/hypocrisy
- minimax/minimax-m2.7 on robespierre/opportunism

## Cost

Total: $2.8269

| model | cost |
|---|---|
| moonshotai/kimi-k2.6 | $0.6524 |
| openai/gpt-5.5 | $0.5950 |
| anthropic/claude-opus-4.7 | $0.4685 |
| x-ai/grok-4.20 | $0.4472 |
| google/gemini-3.1-pro-preview | $0.3301 |
| z-ai/glm-5.1 | $0.1676 |
| minimax/minimax-m2.7 | $0.0916 |
| deepseek/deepseek-v4-pro | $0.0522 |
| mistralai/mistral-large-2512 | $0.0222 |
