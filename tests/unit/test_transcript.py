import pytest

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn
from ai_orchestra.services.transcript import Transcript, create_turn


def _turn(round_number: int, agent: AgentRole, turn_type: TurnType, text: str) -> Turn:
    return create_turn(
        round_number=round_number,
        agent=agent,
        turn_type=turn_type,
        text=text,
        turn_id=f"turn-{round_number}-{agent.value}",
    )


def test_append_turn_increases_length_and_preserves_order() -> None:
    transcript = Transcript(topic="Test topic")
    first = _turn(1, AgentRole.PRO, TurnType.OPENING, "Pro opens.")
    second = _turn(1, AgentRole.CON, TurnType.REBUTTAL, "Con rebuts.")
    transcript.append_turn(first)
    transcript.append_turn(second)

    assert len(transcript) == 2
    assert transcript.turns[0].id == first.id
    assert transcript.turns[1].id == second.id


def test_format_for_judge_includes_all_turns() -> None:
    transcript = Transcript(topic="Social media debate")
    transcript.append_turn(_turn(1, AgentRole.PRO, TurnType.OPENING, "Argument A"))
    transcript.append_turn(_turn(1, AgentRole.CON, TurnType.REBUTTAL, "Argument B"))
    transcript.append_score(
        ScoreSnapshot(
            pro_score=60,
            con_score=40,
            rationale="Pro ahead.",
            after_turn_id="turn-1-con",
        )
    )

    formatted = transcript.format_for_judge()
    assert "Social media debate" in formatted
    assert "Argument A" in formatted
    assert "Argument B" in formatted
    assert "Pro: 60" in formatted
    assert "Con: 40" in formatted


def test_transcript_json_round_trip() -> None:
    transcript = Transcript(topic="Round trip")
    transcript.append_turn(_turn(1, AgentRole.PRO, TurnType.OPENING, "Hello"))
    payload = transcript.to_json()
    restored = Transcript.from_json(payload)
    assert restored.topic == "Round trip"
    assert len(restored.turns) == 1
    assert restored.turns[0].text == "Hello"


def test_build_result_uses_latest_scores() -> None:
    transcript = Transcript(topic="Final")
    turn = _turn(1, AgentRole.PRO, TurnType.OPENING, "Point")
    transcript.append_turn(turn)
    transcript.append_score(
        ScoreSnapshot(
            pro_score=70,
            con_score=30,
            rationale="Strong pro.",
            after_turn_id=turn.id,
        )
    )
    result = transcript.build_result(
        winner=AgentRole.PRO,
        final_summary="Pro wins overall.",
    )
    assert result.final_pro_score == 70
    assert result.final_con_score == 30
    assert result.winner == AgentRole.PRO


def test_turn_rejects_judge_as_speaker() -> None:
    with pytest.raises(ValueError, match="PRO or CON"):
        Turn(
            round=1,
            agent=AgentRole.JUDGE,
            turn_type=TurnType.OPENING,
            text="Judges do not debate.",
        )
