# AI Orchestra 2

A Python debate system: two LLM agents (Pro and Con) argue a fixed topic while a Judge scores persuasiveness after every turn.

## Status

**Phase 2 complete** — config JSON + env loading. See [TODO.md](TODO.md).

| Document | Description |
|----------|-------------|
| [docs/PRD.md](docs/PRD.md) | Product requirements |
| [docs/PLAN.md](docs/PLAN.md) | Technical architecture |
| [PLAN.md](PLAN.md) | Short summary + links |

## Getting started

```bash
python -m uv sync
copy .env.example .env   # then add OPENAI_API_KEY
python -m uv run python src/main.py
```

Configuration: `config/setup.json`, `config/rate_limits.json`. Secrets only in `.env`.

```bash
python -m uv run pytest --cov=src --cov-fail-under=85
python -m uv run ruff check .
```
