# PRD — Judge & Scoring

## Purpose

After every agent turn, evaluate the debate so far and assign **current** persuasion scores to Pro and Con (0–100), with a short rationale.

## Inputs

- Full `Transcript` (all prior turns)
- Latest turn metadata (round, agent, opening vs rebuttal, text)

## Output contract (JSON)

```json
{
  "pro_score": 0,
  "con_score": 0,
  "rationale": "One or two sentences explaining this revision."
}
```

| Field | Type | Constraints |
|-------|------|-------------|
| `pro_score` | int | 0–100 inclusive |
| `con_score` | int | 0–100 inclusive |
| `rationale` | string | Non-empty; max ~500 chars recommended |

## Rubric (persuasion, not truth)

- Strength and clarity of arguments
- Logical consistency
- Quality of rebuttals
- Rhetorical persuasiveness
- Exposing opponent weaknesses
- Overall debate flow

## Scoring semantics

- Scores reflect **who is ahead so far**, not only the latest sentence.
- First turn: one side may be 100 / 0 until the other speaks.
- Later turns: scores **may decrease** for a side if a strong rebuttal undermines prior claims.

### Illustrative example (mechanics only)

1. Pro argues memes strengthen in-group communication → Judge: Pro 100, Con 0.
2. Con argues generational gap and offline humor → Judge: Pro 30, Con 50.

Production debates should be substantially stronger than this sketch.

## Malformed LLM response

| Scenario | v1 behavior (to implement) |
|----------|----------------------------|
| Invalid JSON | Retry once if configured; else use last valid scores + log warning |
| Out-of-range scores | Clamp to 0–100 |
| Missing fields | Reject parse; document in README |

Document final choice in code and `docs/prompts.md`.

## Acceptance criteria

- [ ] Parser unit tests: valid JSON, clamping, invalid JSON path.
- [ ] Judge agent tests: mock LLM returns JSON; scores stored in history.
- [ ] Each judge-related file ≤ 150 lines.

## Non-goals

- Fact-checking against external sources
- Separate per-dimension sub-scores in v1 (optional future)
