# Technical Plan — AI Orchestra 2

Canonical architecture and behavior spec. Product requirements: [PRD.md](PRD.md).

## Overview

Python debate system: **Pro**, **Con**, and **Judge** agents driven by LLMs. Goal: evaluate persuasion and debate performance, not objective truth.

**Topic (v1):** *Social media improves human communication.*

## Agents

| Role | Name | Responsibility |
|------|------|----------------|
| Supporting | Pro | Defends the claim. |
| Opposing | Con | Argues against the claim. |
| Referee | Judge | Full-transcript view; updates scores after every turn; declares winner. |

No live internet search in v1.

## Argument & interaction rules

- One **human-style** argument per turn (thesis, evidence, study reference, conclusion—focused, not a mandatory template).
- Agents may argue persuasively without strict factual correctness; Con exposing weak reasoning should influence Judge scores.
- Rebuttals must engage the opponent’s latest turn.

## Debate structure

- **10 rounds** × (opening + rebuttal).
- **Opener policy (v1 default):** Pro opens odd rounds, Con opens even rounds (configurable later).
- After **each** agent turn → Judge updates Pro/Con scores (0–100) and rationale.

See [PRD_judge_scoring.md](PRD_judge_scoring.md) for scoring example and JSON contract.

## System outputs

1. Full transcript (round, agent, opening/rebuttal)
2. Per-round breakdown
3. Score history after each turn
4. Final scores, winner, judge summary
5. Optional JSON in `results/` when enabled in config

## Target repository layout

```
src/
  main.py                 # thin CLI → SDK
  ai_orchestra/
    sdk/sdk.py            # public API
    services/             # engine, agents, transcript, reporter
    shared/               # config, gatekeeper, version
    constants.py
tests/unit/, tests/integration/
config/setup.json, config/rate_limits.json
docs/                     # PRD, PLAN, mechanism PRDs
```

## Layered architecture

```
CLI (main.py)
    → SDK (DebateSDK.run_debate)
        → DebateEngine
            → ProAgent / ConAgent / JudgeAgent
            → Transcript
        → Reporter (stdout)
    → ApiGatekeeper → LlmClient → Provider API
```

**Rules:** No business logic in CLI. No direct provider calls outside gatekeeper.

## C4-style context

| Element | Description |
|---------|-------------|
| **User** | Runs CLI locally |
| **System** | AI Orchestra 2 |
| **External** | LLM API (e.g. OpenAI) |

## Key modules (implementation)

| Module | Responsibility |
|--------|----------------|
| `debate_engine` | Round loop, opener policy, orchestration |
| `agents/*` | Role prompts + generation |
| `judge_parser` | JSON validation |
| `transcript` | Turn storage, judge formatting |
| `gatekeeper` | Rate limits, retries, logging |
| `reporter` | Terminal formatting |

## LLM (v1)

- Single provider/model acceptable; roles differ by system prompts and temperature (in config).
- Prompt versions tracked in [prompts.md](prompts.md).

## Non-goals (v1)

- Web search, GUI, truth verdict

## ADR-001: SDK as single entry point

**Decision:** All consumers call `ai_orchestra.sdk`, not internal services.  
**Rationale:** Course standard + testable boundary.  
**Tradeoff:** Thin wrapper file required.

## ADR-002: Judge returns JSON

**Decision:** Judge must return parseable JSON `{ "pro_score", "con_score", "rationale" }`.  
**Rationale:** Reliable score history and tests.  
**Tradeoff:** Parser + fallback needed for malformed output.

## ADR-003: Alternate opener

**Decision:** Default alternate opener by round number.  
**Rationale:** Fairness without randomness in tests.  
**Tradeoff:** Config must document other modes if added.

## Project objective

Explore multi-agent debate: generation, rebuttal, dynamic scoring, and referee behavior in a structured environment.
