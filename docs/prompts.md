# Prompt Engineering Log

Track system prompts for Pro, Con, and Judge. Templates live in `src/ai_orchestra/services/prompts/`.

## Version history

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | 2026-05-26 | Initial `pro`, `con`, `judge` system prompts |

## Pro Agent

- **File:** `services/prompts/pro_system.txt`
- **Role:** Defend `{topic}`
- **User message:** Opening vs rebuttal instructions + full transcript; rebuttal includes opponent’s latest turn

## Con Agent

- **File:** `services/prompts/con_system.txt`
- **Role:** Oppose `{topic}`
- **User message:** Same structure as Pro; rebuttal cites opponent’s latest argument

## Judge Agent

- **File:** `services/prompts/judge_system.txt`
- **Output:** JSON only — `pro_score`, `con_score`, `rationale` (see [PRD_judge_scoring.md](PRD_judge_scoring.md))
- **Parser:** `services/agents/judge_parser.py` — invalid JSON keeps previous scores if available, else 50/50

## Temperatures (`config/setup.json`)

| Role | Default |
|------|---------|
| Pro | 0.8 |
| Con | 0.8 |
| Judge | 0.3 |

## Notes

- All LLM calls go through `ApiGatekeeper` → `LlmClient.chat`
- Tests use `RecordingLlmClient` (no network)
- Judge parser strips optional markdown fences if the model disobeys
