import json

import pytest
from pydantic import ValidationError

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.debate import DebateResult, DebateState
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn


def test_score_snapshot_bounds() -> None:
    snapshot = ScoreSnapshot(
        pro_score=0,
        con_score=100,
        rationale="Edge values allowed.",
        after_turn_id="t1",
    )
    assert snapshot.pro_score == 0
    assert snapshot.con_score == 100


def test_score_snapshot_rejects_out_of_range() -> None:
    with pytest.raises(ValidationError):
        ScoreSnapshot(
            pro_score=101,
            con_score=50,
            rationale="Too high.",
            after_turn_id="t1",
        )
    with pytest.raises(ValidationError):
        ScoreSnapshot(
            pro_score=50,
            con_score=-1,
            rationale="Too low.",
            after_turn_id="t1",
        )


def test_debate_state_dict_json_round_trip() -> None:
    state = DebateState(
        topic="Topic",
        turns=[
            Turn(
                id="t1",
                round=1,
                agent=AgentRole.PRO,
                turn_type=TurnType.OPENING,
                text="Hi",
            )
        ],
        score_history=[
            ScoreSnapshot(
                pro_score=55,
                con_score=45,
                rationale="Close.",
                after_turn_id="t1",
            )
        ],
    )
    restored = DebateState.from_dict(state.to_dict())
    assert json.loads(state.to_json()) == json.loads(restored.to_json())


def test_debate_result_dict_json_round_trip() -> None:
    result = DebateResult(
        topic="Topic",
        turns=[
            Turn(
                id="t1",
                round=1,
                agent=AgentRole.CON,
                turn_type=TurnType.REBUTTAL,
                text="No",
            )
        ],
        score_history=[
            ScoreSnapshot(
                pro_score=40,
                con_score=60,
                rationale="Con leads.",
                after_turn_id="t1",
            )
        ],
        winner=AgentRole.CON,
        final_pro_score=40,
        final_con_score=60,
        final_summary="Con wins.",
    )
    payload = result.to_dict()
    restored = DebateResult.from_dict(payload)
    assert restored.winner == AgentRole.CON
    assert restored.final_summary == "Con wins."
