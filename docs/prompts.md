# Prompt Engineering Log

Track system prompts for Pro, Con, and Judge. Update this file when prompts change.

## Version history

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | (pending) | Initial prompts — not yet implemented |

## Pro Agent (system)

_To be added in Phase 5. Must include: topic, role (defend), one argument per turn, engage opponent on rebuttal._

## Con Agent (system)

_To be added in Phase 5. Must include: topic, role (oppose), rebuttal must address Pro’s latest argument._

## Judge Agent (system)

_To be added in Phase 5. Must include: rubric, full transcript in user message, JSON-only response matching [PRD_judge_scoring.md](PRD_judge_scoring.md)._

## Notes

- Debater temperature: TBD in `config/setup.json`
- Judge temperature: lower than debaters (TBD)
- Avoid asking Judge for markdown fences around JSON if parser expects raw JSON
