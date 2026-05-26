# PRD — Debate Engine

## Purpose

Orchestrate 10 rounds of structured debate: opener turn, rebuttal turn, judge scoring after each agent turn, transcript growth.

## Inputs

| Input | Source | Notes |
|-------|--------|-------|
| `round_count` | `config/setup.json` | Default 10 |
| `opener_policy` | config | `alternate` (default), `fixed_pro`, `fixed_con`, `random` |
| `topic` | config | Fixed string for v1 |
| Agent callables | services | Mocked in tests |

## Outputs

| Output | Type | Notes |
|--------|------|-------|
| `DebateResult` | object | transcript, score_history, winner, final_summary |
| Per-turn events | internal | For reporter |

## Behavior

1. Initialize empty `Transcript` and `DebateState`.
2. For `round` in `1..round_count`:
   - Determine opener (Pro or Con) from policy.
   - Opener generates **opening** turn → append → call Judge.
   - Other side generates **rebuttal** → append → call Judge.
3. After round 10, set winner by higher final score; attach judge’s last rationale as summary tie-in.

## Opener policy — alternate (default)

| Round | Opener |
|-------|--------|
| 1, 3, 5, 7, 9 | Pro |
| 2, 4, 6, 8, 10 | Con |

## Acceptance criteria

- [ ] Engine produces exactly `2 × round_count` agent turns.
- [ ] Judge called exactly `2 × round_count` times per run.
- [ ] `score_history` length equals judge call count.
- [ ] Unit tests use mocks; no network.
- [ ] `debate_engine.py` (and helpers) ≤ 150 lines each.

## Edge cases

| Case | Expected behavior |
|------|-------------------|
| Agent raises exception | Propagate or wrap with clear message; debate aborts |
| Judge raises exception | Same; partial transcript preserved in error if feasible |
| `round_count` &lt; 1 | Reject at config validation |

## Dependencies

- [PRD_judge_scoring.md](PRD_judge_scoring.md)
- [PRD_llm_integration.md](PRD_llm_integration.md)
