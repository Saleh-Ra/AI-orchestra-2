# AI Orchestra 2

A Python multi-agent debate system: **Pro** and **Con** LLM agents argue a fixed topic for 10 structured rounds while a **Judge** scores persuasiveness (0–100) after every turn using the full transcript. The goal is to demonstrate structured rebuttal and dynamic evaluation—not to declare objective truth.

**Topic (v1):** *Social media improves human communication.*

**Status:** Phases 0–10 complete — submission-ready locally (see [TODO.md](TODO.md)). Optional: one real 10-round API run with `mock_llm: false` and `.env`.

## Features

- Three specialized agents: Pro (defends), Con (opposes), Judge (scores + winner)
- 10 rounds × (opening + rebuttal) = 20 agent turns and 20 judge updates per full run
- **Alternate opener policy** (default): Pro opens odd rounds, Con opens even rounds
- Rebuttals include the opponent’s latest argument in the prompt
- All LLM traffic goes through an **API gatekeeper** (rate limits, retries, logging)
- **Mock LLM mode** for offline tests and demos (`mock_llm: true` in config)
- Thin **CLI** and public **SDK** (`DebateSDK.run_debate()`)
- Optional JSON export of transcript and scores to `results/`
- Course-aligned quality bar: Ruff lint, ≥85% test coverage, ≤150 lines per `.py` file

| Document | Description |
|----------|-------------|
| [docs/PRD.md](docs/PRD.md) | Product requirements and acceptance criteria |
| [docs/PLAN.md](docs/PLAN.md) | Technical architecture and ADRs |
| [PLAN.md](PLAN.md) | Short summary + links |
| [TODO.md](TODO.md) | Implementation checklist by phase |

## Prerequisites

- **Python** ≥ 3.10
- **[uv](https://docs.astral.sh/uv/)** — fast Python package and project manager  
  Install: `pip install uv` (or see the uv docs for your OS)
- **OpenAI API key** — only required when `mock_llm` is `false` in config

## Installation

```bash
git clone <your-repo-url>
cd AI-orchestra-2
python -m uv sync
```

Copy environment template and add your key (never commit `.env`):

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-...
# Optional: OPENAI_BASE_URL=https://api.openai.com/v1
```

## Configuration

### `config/setup.json`

| Field | Description |
|-------|-------------|
| `debate.topic` | Fixed debate statement |
| `debate.round_count` | Number of rounds (default `10`) |
| `debate.opener_policy` | `alternate` (default), `pro_first`, `con_first`, or `random` |
| `llm.model` | Provider model name (e.g. `gpt-4o-mini`) |
| `llm.temperature` | Per-role temperatures (`pro`, `con`, `judge`) |
| `mock_llm` | `true` = deterministic mock responses (no API key) |
| `output.save_results_json` | When `true`, SDK/engine may persist JSON (CLI uses `--save-json`) |
| `output.results_dir` | Directory for saved debate files |

### `config/rate_limits.json`

Rate limits and retry settings for the API gatekeeper (`requests_per_minute`, `max_retries`, etc.).

### Test fixtures

`tests/fixtures/setup.test.json` pairs with `rate_limits.test.json` — 2 rounds, `mock_llm: true` for fast CI and smoke runs.

### Pairing rule

Passing `setup.test.json` to the SDK or CLI automatically loads `rate_limits.test.json` from the same directory (replace the `setup` prefix with `rate_limits`).

## Usage

### CLI (recommended for demos)

Default config (`config/setup.json` + `config/rate_limits.json`):

```bash
python -m uv run python src/main.py
```

Fast mock run (no API key):

```bash
python -m uv run python src/main.py --config-path tests/fixtures/setup.test.json
```

Save result JSON:

```bash
python -m uv run python src/main.py --config-path tests/fixtures/setup.test.json --save-json --results-dir results
```

| Flag | Description |
|------|-------------|
| `--config-path` | Path to `setup*.json`, `rate_limits*.json`, or a directory containing both |
| `--save-json` | Write `debate_YYYYMMDD_HHMMSS.json` under `--results-dir` |
| `--results-dir` | Output directory (default `results`) |

### Example output (mock, 2-round fixture)

```
Debate topic: Test debate topic.

Round 1 | Agent PRO | OPENING
Pro debater mock argument.
Current scores — Pro: 55, Con: 45

Round 1 | Agent CON | REBUTTAL
Con debater mock argument.
...

Final Winner: PRO (Pro 55 / Con 45)
Judge Summary: Mock judge evaluation.
```

### SDK (programmatic)

```python
from ai_orchestra.sdk import DebateSDK

result = DebateSDK().run_debate("tests/fixtures/setup.test.json")
print(result.winner, result.final_pro_score, result.final_con_score)
```

Use `None` for default production config paths.

## Running tests

```bash
python -m uv run pytest
python -m uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=85
python -m uv run ruff check .
python -m uv run ruff format --check .
```

Apply formatting:

```bash
python -m uv run ruff format .
```

## Project structure

```
AI-orchestra-2/
├── config/
│   ├── setup.json
│   └── rate_limits.json
├── docs/                    # PRD, PLAN, mechanism PRDs, prompts log
├── results/                 # optional debate JSON exports
├── src/
│   ├── main.py              # thin CLI → DebateSDK + reporter
│   └── ai_orchestra/
│       ├── sdk/             # public API
│       ├── services/        # engine, agents, transcript, reporter, LLM
│       └── shared/          # config, gatekeeper
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── pyproject.toml
└── TODO.md
```

**Architecture (summary):** `CLI → DebateSDK → DebateEngine → agents + transcript → ApiGatekeeper → LlmClient`. Business logic stays out of `main.py`; external callers should use `ai_orchestra.sdk` only.

## Judge output and errors

The Judge must return JSON: `pro_score`, `con_score`, `rationale`. If parsing fails, `judge_parser` keeps the previous scores when available; otherwise it assigns 50/50 and records a short rationale snippet. The debate never crashes on malformed judge output.

## Development notes

- Prompt templates: `src/ai_orchestra/services/prompts/*.txt` — versions in [docs/prompts.md](docs/prompts.md)
- No live web search in v1
- Secrets only in `.env`; never in source or JSON config

## License and credits

Built for a multi-agent systems course project following professional software guidelines (modular layout, SDK boundary, high test coverage, Ruff, uv).

**Author:** *(add your name)*  
**Course / institution:** *(add as required)*

For requirements and grading criteria, see [docs/PRD.md](docs/PRD.md) and [docs/PLAN.md](docs/PLAN.md).
