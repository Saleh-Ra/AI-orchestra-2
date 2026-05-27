import pytest
from pydantic import ValidationError

from ai_orchestra.services.agents.judge_parser import parse_judge_response
from ai_orchestra.services.models.scores import ScoreSnapshot


def test_parse_valid_json() -> None:
    raw = '{"pro_score": 70, "con_score": 30, "rationale": "Pro is clearer."}'
    snapshot = parse_judge_response(raw, after_turn_id="turn-1")
    assert snapshot.pro_score == 70
    assert snapshot.con_score == 30
    assert snapshot.after_turn_id == "turn-1"


def test_parse_json_with_markdown_fences() -> None:
    raw = '```json\n{"pro_score": 55, "con_score": 45, "rationale": "Even."}\n```'
    snapshot = parse_judge_response(raw, after_turn_id="t2")
    assert snapshot.pro_score == 55


def test_parse_invalid_json_uses_fallback_scores() -> None:
    previous = ScoreSnapshot(
        pro_score=80,
        con_score=20,
        rationale="Earlier.",
        after_turn_id="t0",
    )
    snapshot = parse_judge_response(
        "not json at all",
        after_turn_id="t1",
        fallback=previous,
    )
    assert snapshot.pro_score == 80
    assert snapshot.con_score == 20
    assert "invalid" in snapshot.rationale.lower()


def test_parse_invalid_json_without_fallback_defaults_to_fifty_fifty() -> None:
    snapshot = parse_judge_response("broken", after_turn_id="t1")
    assert snapshot.pro_score == 50
    assert snapshot.con_score == 50


def test_parse_rejects_out_of_range_after_extract() -> None:
    raw = '{"pro_score": 150, "con_score": 0, "rationale": "Bad"}'
    with pytest.raises(ValidationError):
        parse_judge_response(raw, after_turn_id="t1")
