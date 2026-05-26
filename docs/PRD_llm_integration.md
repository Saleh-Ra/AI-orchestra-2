# PRD — LLM Integration & API Gatekeeper

## Purpose

Centralize all calls to external LLM APIs: rate limiting, retries, logging, and testability.

## Requirements

| ID | Requirement |
|----|-------------|
| GK-1 | No provider SDK usage outside `shared/gatekeeper.py` and its dedicated client adapter. |
| GK-2 | Rate limits read from `config/rate_limits.json`, not hardcoded. |
| GK-3 | Secrets from `os.environ` (e.g. `OPENAI_API_KEY`), never from source or JSON config. |
| GK-4 | All tests mock the gatekeeper or underlying client—no live API in CI/local test runs. |
| GK-5 | `execute(callable, *args, **kwargs)` (or equivalent) is the public gatekeeper entry. |

## Configuration

`config/rate_limits.json` (versioned):

- `requests_per_minute`, `requests_per_hour`
- `concurrent_max`, `retry_after_seconds`, `max_retries`

Aligned with course template; values tuned for debate (~40+ calls per full run).

## Flow

```
Agent → Gatekeeper.execute → LlmClient.chat(messages, ...) → Provider HTTP API
```

## Mock mode

- CLI flag or config: `mock_llm: true`
- Returns deterministic canned text / judge JSON for integration tests and offline demos.

## Acceptance criteria

- [ ] Unit tests: rate limit blocks or queues (mock clock/counter).
- [ ] Unit tests: retry on transient failure up to `max_retries`.
- [ ] Grep/check: no `openai` import in `services/agents/`.
- [ ] Gatekeeper module(s) ≤ 150 lines each.

## Errors

- Missing API key when mock disabled → clear message pointing to `.env.example`
- Provider 429/5xx → retry per config, then fail with logged context
