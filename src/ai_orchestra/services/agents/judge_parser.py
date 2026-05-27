"""Parse and validate judge LLM JSON output."""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from ai_orchestra.services.models.scores import ScoreSnapshot

_JSON_BLOCK = re.compile(r"\{[^{}]*\}", re.DOTALL)


class JudgeParseError(ValueError):
    """Raised when judge output cannot be parsed and no fallback is allowed."""


def parse_judge_response(
    raw: str,
    *,
    after_turn_id: str,
    fallback: ScoreSnapshot | None = None,
) -> ScoreSnapshot:
    """Parse judge JSON; on failure return fallback or equal split scores."""

    try:
        payload = _extract_payload(raw)
        data = {
            "pro_score": payload["pro_score"],
            "con_score": payload["con_score"],
            "rationale": payload["rationale"],
            "after_turn_id": after_turn_id,
        }
        return ScoreSnapshot.model_validate(data)
    except ValidationError:
        raise
    except (KeyError, json.JSONDecodeError, TypeError, ValueError):
        if fallback is not None:
            return ScoreSnapshot(
                pro_score=fallback.pro_score,
                con_score=fallback.con_score,
                rationale=_fallback_rationale(raw, kept_previous=True),
                after_turn_id=after_turn_id,
            )
        return ScoreSnapshot(
            pro_score=50,
            con_score=50,
            rationale=_fallback_rationale(raw, kept_previous=False),
            after_turn_id=after_turn_id,
        )


def _extract_payload(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```").strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = _JSON_BLOCK.search(text)
        if not match:
            raise
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        msg = "Judge output must be a JSON object."
        raise TypeError(msg)
    return parsed


def _fallback_rationale(raw: str, *, kept_previous: bool) -> str:
    snippet = raw.strip().replace("\n", " ")[:180]
    if kept_previous:
        return f"Judge output was invalid; previous scores kept. Raw snippet: {snippet}"
    return f"Judge output was invalid; neutral scores assigned. Raw snippet: {snippet}"
