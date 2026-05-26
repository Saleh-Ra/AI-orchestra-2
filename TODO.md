# AI Orchestra 2 — TODO

Phased checklist for building the debate system ([PLAN.md](PLAN.md)) to course standards (structure, ≤150 lines/file, tests, README, `uv`).  
Work **one phase per GitHub push** when possible; mark items `[x]` as you finish them.

**Status:** `⬜ not started` · `🔄 in progress` · `✅ done`

| Phase | Focus | Status |
|-------|--------|--------|
| 0 | Documentation & repo baseline | ✅ |
| 1 | Tooling & project scaffold | ✅ |
| 2 | Configuration & constants | ✅ |
| 3 | API gatekeeper & LLM client | ⬜ |
| 4 | Domain models & transcript | ⬜ |
| 5 | Agent prompts & agent classes | ⬜ |
| 6 | Debate engine & turn order | ⬜ |
| 7 | SDK & public API | ⬜ |
| 8 | CLI, reporter & end-to-end flow | ⬜ |
| 9 | README, docs polish & quality gate | ⬜ |
| 10 | Final verification & submission prep | ⬜ |

---

## Phase 0 — Documentation & repo baseline

**Goal:** Formal docs exist before major code; repo is safe to push.

**Definition of done:** `docs/PRD.md` and `docs/PLAN.md` exist; `.gitignore` blocks secrets; root `PLAN.md` still valid or points to `docs/`.

### Docs

- [x] Create `docs/` directory
- [x] Write `docs/PRD.md` — product summary, user stories, acceptance criteria, non-goals (no web search, CLI v1)
- [x] Copy or sync technical content into `docs/PLAN.md` (from root `PLAN.md`; keep architecture tables)
- [x] Add `docs/PRD_debate_engine.md` — rounds, turns, opener rule, transcript contract
- [x] Add `docs/PRD_judge_scoring.md` — continuous 0–100 scores, JSON output shape, rubric
- [x] Add `docs/PRD_llm_integration.md` — gatekeeper-only LLM access, mocks in tests
- [x] Add `docs/prompts.md` (or `docs/prompt_log.md`) — placeholder for Pro / Con / Judge prompt versions

### Repo hygiene

- [x] Update `.gitignore` — `.env`, `__pycache__/`, `.pytest_cache/`, `.coverage`, `htmlcov/`, `.venv/`, `results/` (if local-only outputs)
- [x] Ensure no API keys or secrets are committed
- [x] Remove or relocate PyCharm sample `main.py` content (note in commit message)

### Tests (phase 0)

- [ ] N/A — documentation only

---

## Phase 1 — Tooling & project scaffold

**Goal:** `uv` project runs; folders match layered layout; quality tools configured.

**Definition of done:** `uv run pytest` runs (even if 0 tests); `uv run ruff check` passes on empty/stub package.

### Package layout

- [x] Create `src/ai_orchestra/` package with `__init__.py` and `__version__`
- [x] Create `src/ai_orchestra/sdk/` — `sdk.py` stub
- [x] Create `src/ai_orchestra/services/` — empty `__init__.py`
- [x] Create `src/ai_orchestra/shared/` — `config.py`, `gatekeeper.py`, `version.py` stubs
- [x] Create `src/ai_orchestra/constants.py` stub
- [x] Create `src/main.py` — thin entry (imports SDK only)
- [x] Create `tests/unit/`, `tests/integration/`, `tests/conftest.py`
- [x] Create `config/`, `data/`, `results/` (with `.gitkeep` if outputs stay local)

### `uv` & `pyproject.toml`

- [x] Initialize `pyproject.toml` (name, version, Python ≥3.10, package discovery under `src/`)
- [x] Add dependencies — OpenAI SDK (or chosen provider), pydantic (if used), pytest, pytest-cov, ruff
- [x] Run `uv sync` and commit `uv.lock`
- [x] Document in README stub: use `uv run`, not `pip`

### Ruff & coverage

- [x] Configure `[tool.ruff]` — line length 100, target py310, rule set per course PDF
- [x] Configure `[tool.coverage.run]` — `source = ["src"]`, omit `src/main.py` if appropriate
- [x] Configure `[tool.coverage.report]` — `fail_under = 85`
- [x] Add `[tool.pytest.ini_options]` — `testpaths = ["tests"]`

### Tests (phase 1)

- [x] `tests/unit/test_version.py` — package `__version__` is defined and semver-shaped
- [x] `tests/unit/test_imports.py` — `ai_orchestra` and subpackages import without error
- [x] Verify `uv run pytest` exits 0

---

## Phase 2 — Configuration & constants

**Goal:** All tunables in config files; no magic numbers for limits, rounds, topic.

**Definition of done:** App reads `config/setup.json` and `config/rate_limits.json`; secrets only from environment.

### Config files

- [x] Add `config/setup.json` — `version`, debate topic, `round_count` (10), opener mode (`alternate` / `fixed` / `random`), model names, temperatures
- [x] Add `config/rate_limits.json` — `version`, per-service RPM/concurrency/retry (per PDF gatekeeper template)
- [x] Add `.env.example` — `OPENAI_API_KEY=`, optional `OPENAI_BASE_URL=`
- [x] Add `config/logging_config.json` (optional) or logging section in `setup.json`

### Code

- [x] Implement `shared/config.py` — load JSON, validate required keys, read env for secrets
- [x] Implement `constants.py` — enums/labels only (agent roles, turn types: `opening` / `rebuttal`)
- [x] Implement `shared/version.py` — code version `1.00`, config version check helper
- [x] Keep each file ≤150 lines

### Tests (phase 2)

- [x] `tests/unit/test_config.py` — loads valid `setup.json`; missing file raises clear error
- [x] `tests/unit/test_config.py` — rejects hardcoded API key patterns (smoke: config never returns raw key from JSON)
- [x] `tests/unit/test_version.py` — config version mismatch detected when versions differ
- [x] `tests/conftest.py` — fixture `sample_config` pointing at test config under `tests/fixtures/`
- [x] Add `tests/fixtures/setup.test.json` and `tests/fixtures/rate_limits.test.json`

---

## Phase 3 — API gatekeeper & LLM client

**Goal:** Every external LLM call goes through gatekeeper; tests use mocks.

**Definition of done:** No direct `openai` (or provider) calls outside `shared/gatekeeper.py` (and thin client it wraps).

### Implementation

- [ ] Define `RateLimitConfig` / `QueueStatus` dataclasses or models (small module if needed)
- [ ] Implement `shared/gatekeeper.py` — `ApiGatekeeper.execute()`, rate check, retry, logging hook
- [ ] Implement `services/llm_client.py` (or `shared/llm_client.py`) — provider adapter used only by gatekeeper
- [ ] Wire gatekeeper to read limits from `config/rate_limits.json`
- [ ] Split files if any exceed 150 lines

### Tests (phase 3)

- [ ] `tests/unit/test_gatekeeper.py` — blocks or queues when rate limit exceeded (mock clock/counter)
- [ ] `tests/unit/test_gatekeeper.py` — retries transient failure up to `max_retries`
- [ ] `tests/unit/test_gatekeeper.py` — logs / records call metadata (assert mock logger called)
- [ ] `tests/unit/test_gatekeeper.py` — successful call returns provider response
- [ ] `tests/conftest.py` — `mock_llm_client` fixture returning fixed string / JSON
- [ ] No tests call real API

---

## Phase 4 — Domain models & transcript

**Goal:** Typed structures for turns, scores, and full debate state.

**Definition of done:** Transcript can serialize to dict/JSON for judge input and final output.

### Implementation

- [ ] `services/models/turn.py` — `Turn` (round, agent, role, text, timestamp/id)
- [ ] `services/models/scores.py` — `ScoreSnapshot` (pro_score, con_score, rationale, after_turn_id)
- [ ] `services/models/debate.py` — `DebateState`, `DebateResult` (transcript, score_history, winner, final_summary)
- [ ] `services/transcript.py` — append turn, format for judge prompt, export full transcript
- [ ] Use Pydantic or dataclasses consistently; keep files ≤150 lines

### Tests (phase 4)

- [ ] `tests/unit/test_transcript.py` — append turn increases length; order preserved
- [ ] `tests/unit/test_transcript.py` — `format_for_judge()` includes all prior turns
- [ ] `tests/unit/test_models.py` — score bounds 0–100 validated
- [ ] `tests/unit/test_models.py` — serialization round-trip (dict/JSON)

---

## Phase 5 — Agent prompts & agent classes

**Goal:** Pro, Con, and Judge generate content via gatekeeper with role-specific prompts.

**Definition of done:** Judge returns parseable structured scores; debaters receive opponent context.

### Prompts

- [ ] `services/prompts/pro_system.txt` (or `.py` template module) — defends topic
- [ ] `services/prompts/con_system.txt` — opposes topic
- [ ] `services/prompts/judge_system.txt` — rubric + JSON schema instruction
- [ ] Document prompt versions in `docs/prompts.md`

### Agents

- [ ] `services/agents/base.py` — shared `generate_argument(transcript, role, turn_type)` via gatekeeper
- [ ] `services/agents/pro_agent.py` — Pro opening & rebuttal builders
- [ ] `services/agents/con_agent.py` — Con opening & rebuttal builders
- [ ] `services/agents/judge_agent.py` — full transcript + latest turn → `ScoreSnapshot`
- [ ] `services/agents/judge_parser.py` — parse/validate JSON; safe defaults on malformed response
- [ ] Each file ≤150 lines

### Tests (phase 5)

- [ ] `tests/unit/test_judge_parser.py` — valid JSON → correct scores
- [ ] `tests/unit/test_judge_parser.py` — invalid JSON → clear error or graceful fallback (document behavior)
- [ ] `tests/unit/test_pro_agent.py` — mock LLM; prompt contains topic and transcript snippet
- [ ] `tests/unit/test_con_agent.py` — mock LLM; rebuttal prompt references opponent last turn
- [ ] `tests/unit/test_judge_agent.py` — mock LLM returning JSON; scores in range
- [ ] Assert no agent module imports provider SDK directly (optional lint test / grep checklist)

---

## Phase 6 — Debate engine & turn order

**Goal:** Run 10 rounds (open → rebuttal); judge updates after every agent turn.

**Definition of done:** Single run produces 20 debater turns + 20 judge updates (or 20 judge calls after each of 20 turns — per PLAN).

### Implementation

- [ ] `services/opener_policy.py` — alternate / fixed / random (config-driven); document chosen default in code
- [ ] `services/debate_engine.py` — loop rounds 1–10, assign opener, call Pro/Con, call judge after each turn
- [ ] `services/debate_engine.py` — accumulate `score_history` on `DebateState`
- [ ] Handle engine errors with clear messages (per PDF error-handling)
- [ ] Keep engine ≤150 lines; extract helpers if needed

### Tests (phase 6)

- [ ] `tests/unit/test_opener_policy.py` — alternate: odd/even rounds correct opener
- [ ] `tests/unit/test_debate_engine.py` — 10 rounds → 20 turns recorded (mocked agents)
- [ ] `tests/unit/test_debate_engine.py` — judge invoked after every turn (mock call count == 20)
- [ ] `tests/unit/test_debate_engine.py` — score history length matches judge invocations
- [ ] `tests/integration/test_debate_flow.py` — full debate with all mocks; winner set from final scores

---

## Phase 7 — SDK & public API

**Goal:** CLI and future consumers use only `sdk` layer.

**Definition of done:** `from ai_orchestra.sdk import DebateSDK` (or similar) exposes `run_debate()` without importing services directly from `main`.

### Implementation

- [ ] `sdk/sdk.py` — `DebateSDK.run_debate(config_path=None) -> DebateResult`
- [ ] `sdk/sdk.py` — optional `run_debate_async` only if needed (YAGNI otherwise)
- [ ] `ai_orchestra/__init__.py` — export `__version__`, document public API in `__all__`
- [ ] SDK wires config → engine → result; no business logic in `main.py`

### Tests (phase 7)

- [ ] `tests/unit/test_sdk.py` — `run_debate` with test config + mocks returns `DebateResult`
- [ ] `tests/unit/test_sdk.py` — SDK does not require env var when mock mode/fixture flag set
- [ ] `tests/integration/test_sdk_integration.py` — end-to-end with fixture config under `tests/fixtures/`

---

## Phase 8 — CLI, reporter & end-to-end flow

**Goal:** Terminal UX prints debate step-by-step and final summary.

**Definition of done:** `uv run python src/main.py` runs a full mocked debate; optional real API run documented in README.

### Implementation

- [ ] `services/reporter.py` — print turn header (round, agent, role), argument text, current scores
- [ ] `services/reporter.py` — print final winner, scores, judge summary
- [ ] `src/main.py` — argparse if needed (`--config`, `--mock`); calls `DebateSDK` only
- [ ] Optional: write transcript JSON to `results/<timestamp>.json` (config flag)
- [ ] All files ≤150 lines

### Tests (phase 8)

- [ ] `tests/unit/test_reporter.py` — snapshot or assert key strings in output (capsys)
- [ ] `tests/integration/test_cli.py` — invoke main with mock mode; exit code 0
- [ ] `tests/integration/test_cli.py` — output contains round labels and final winner

---

## Phase 9 — README, docs polish & quality gate

**Goal:** Submission-ready documentation and automated quality bars.

**Definition of done:** README is a full user manual; `ruff` clean; coverage ≥85% on `src/`.

### README (`README.md`)

- [ ] Project title and description (debate system, three agents, persuasion focus)
- [ ] Features list aligned with PLAN.md
- [ ] Prerequisites — Python version, `uv` install link
- [ ] Installation — clone, `uv sync`, copy `.env.example` → `.env`
- [ ] Configuration — `config/setup.json`, `rate_limits.json`, env vars
- [ ] Usage — `uv run python src/main.py`, flags, example output snippet
- [ ] Running tests — `uv run pytest`, coverage command
- [ ] Project structure — tree of `src/`, `tests/`, `docs/`, `config/`
- [ ] Link to `PLAN.md` / `docs/PRD.md`
- [ ] License & credits section

### Docs sync

- [ ] `docs/TODO.md` — copy or link to root `TODO.md` (keep one source of truth; avoid drift)
- [ ] Update `docs/PRD.md` acceptance criteria — check off implemented items
- [ ] Update `docs/PLAN.md` — final module diagram and opener rule chosen

### Quality gate

- [ ] `uv run ruff check .` — 0 errors
- [ ] `uv run ruff format .` (if used) — consistent style
- [ ] `uv run pytest --cov=src --cov-report=term-missing` — ≥85%
- [ ] Review every `.py` under `src/` — each ≤150 lines of code (manual or script)
- [ ] Review test files — each ≤150 lines

### Tests (phase 9)

- [ ] Add any missing tests to reach 85% (focus `gatekeeper`, `debate_engine`, `judge_parser`)
- [ ] `tests/unit/test_line_limits.py` (optional) — fail if any `src/**/*.py` > 150 code lines

---

## Phase 10 — Final verification & submission prep

**Goal:** Confidence the submitted repo matches PLAN + course rules.

**Definition of done:** Manual checklist signed off; GitHub repo ready for grader clone-and-run.

### Manual smoke tests

- [ ] `uv sync` on clean machine / fresh venv
- [ ] `uv run pytest` — all green
- [ ] `uv run python src/main.py` with `--mock` (or test config) — full debate prints
- [ ] (Optional) One real API run with valid `.env` — topic and 10 rounds complete

### Submission checklist (PDF-aligned, submission scope)

- [ ] `README.md` complete
- [ ] `docs/PRD.md`, `docs/PLAN.md`, mechanism PRDs present
- [ ] `pyproject.toml` + `uv.lock` committed
- [ ] `.env.example` present; `.env` not committed
- [ ] SDK pattern — no business logic in CLI beyond SDK call
- [ ] Gatekeeper — no raw LLM calls outside gatekeeper
- [ ] Tests — unit + integration; coverage ≥85%
- [ ] Ruff — 0 errors
- [ ] File size — all Python files ≤150 lines of code
- [ ] Product — 10 rounds, Pro/Con/Judge, dynamic scoring, fixed topic per PLAN.md

### Git / GitHub

- [ ] Meaningful commit per phase (or logical group)
- [ ] Branch `main` (or `master`) reflects stable last phase
- [ ] Push to GitHub; verify clone instructions in README work

### Tests (phase 10)

- [ ] Full CI-style local run: `uv run ruff check . && uv run pytest --cov=src --cov-fail-under=85`
- [ ] Record pass date / commit hash in this file (optional): _______________

---

## Notes & decisions log

Record choices here so we do not reopen them mid-project.

| Decision | Choice | Date |
|----------|--------|------|
| Opener policy (alternate / fixed / random) | | |
| LLM provider & model | | |
| Mock mode flag name (`--mock` / env) | | |
| Judge malformed JSON behavior | | |

---

## Out of scope (v1 — do not block submission)

- Token usage dashboards and cost spreadsheets
- Jupyter research notebooks
- GUI / web interface
- Live web search / RAG evidence
- Multiple debate topics in config UI
