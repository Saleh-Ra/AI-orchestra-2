# Product Requirements Document — AI Orchestra 2

## 1. Overview

**AI Orchestra 2** is a Python application that runs a structured debate between two LLM-powered agents (Pro and Con) on a fixed topic, with a third agent (Judge) scoring persuasiveness after every turn. The product goal is to demonstrate high-quality multi-agent interaction, rebuttal, and dynamic evaluation—not to establish objective truth.

## 2. Problem & audience

| Item | Description |
|------|-------------|
| **Problem** | Manual comparison of LLM argument quality is ad hoc; we need a repeatable, structured debate format. |
| **Primary user** | Developer or student running a local CLI demo and inspecting transcript + scores. |
| **Stakeholder** | Course grader evaluating architecture, tests, and documentation. |

## 3. Debate topic (v1)

> **Social media improves human communication.**

- **Pro** defends this claim.
- **Con** argues against it.

## 4. User stories

| ID | Story | Priority |
|----|--------|----------|
| US-1 | As a user, I run one command and see a 10-round debate printed in the terminal. | Must |
| US-2 | As a user, I see Pro/Con arguments that respond to the opponent’s previous turn. | Must |
| US-3 | As a user, I see persuasion scores (0–100) update after each agent turn. | Must |
| US-4 | As a user, I see a final winner and short judge summary. | Must |
| US-5 | As a user, I configure the LLM via environment variables and JSON config without editing code. | Must |
| US-6 | As a user, I run the app in mock mode without an API key for tests/demos. | Should |

## 5. Functional requirements

### Debate flow

- FR-1: Exactly **10 rounds** per run.
- FR-2: Each round has **two turns**: opening argument, then rebuttal.
- FR-3: Opener per round follows a **documented policy** (default: alternate Pro/Con by round).
- FR-4: Judge evaluates after **every** agent turn using the **full transcript** so far.
- FR-5: Scores are integers **0–100** for Pro and Con; history is retained.

### Agents

- FR-6: Pro and Con produce one focused human-style argument per turn (thesis, evidence, rhetoric—no fixed template).
- FR-7: Judge outputs **structured** scores plus a short rationale (JSON preferred).
- FR-8: No live web search or fact-check API in v1.

### Output

- FR-9: Terminal display includes round, agent, turn type (opening/rebuttal), text, and current scores.
- FR-10: Final output includes winner, final scores, and judge summary.
- FR-11: Optional JSON export of transcript and score history to `results/` (config flag).

## 6. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | Python ≥ 3.10; dependencies managed with **uv**. |
| NFR-2 | Each source file ≤ **150 lines** of code. |
| NFR-3 | Test coverage ≥ **85%** on `src/`. |
| NFR-4 | **Ruff** lint: zero errors. |
| NFR-5 | All LLM calls via **API gatekeeper**; secrets in `.env` only. |
| NFR-6 | Business logic exposed through **SDK**; CLI is thin. |

## 7. Acceptance criteria

- [x] Full debate completes for the fixed topic with 20 agent turns and 20 judge updates (production `round_count: 10`; verified in integration tests with stub/mock agents).
- [x] Rebuttal prompts include the opponent’s latest argument (verified in unit tests with recording mocks).
- [x] Judge JSON is parsed; invalid JSON handled without crashing (see `judge_parser.py` and [prompts.md](prompts.md)).
- [x] `uv run pytest` passes with coverage ≥ 85% on `src/`.
- [x] `uv run ruff check .` passes.
- [x] README explains install, config, usage, and test commands.

## 8. Out of scope (v1)

- Web or desktop GUI
- Live internet / RAG evidence
- Multiple selectable topics in UI
- Token cost dashboards and research notebooks
- Objective “truth” verdict on the topic

## 9. Assumptions & constraints

- User has an API key for the chosen LLM provider (e.g. OpenAI).
- Network available for real runs; mock mode works offline.
- Judge may exhibit LLM bias (length, recency); mitigated by rubric and full transcript, not eliminated.

## 10. References

- [PLAN.md](PLAN.md) — technical architecture
- [PRD_debate_engine.md](PRD_debate_engine.md), [PRD_judge_scoring.md](PRD_judge_scoring.md), [PRD_llm_integration.md](PRD_llm_integration.md)
- Root [PLAN.md](../PLAN.md) — product summary (pointer)
