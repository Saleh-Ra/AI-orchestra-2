from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.debate import DebateResult
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn
from ai_orchestra.services.reporter import format_debate, print_debate


def test_format_debate_includes_sections() -> None:
    turn = Turn(
        round=1,
        agent=AgentRole.PRO,
        turn_type=TurnType.OPENING,
        text="Pro opening argument.",
    )
    snapshot = ScoreSnapshot(
        pro_score=60,
        con_score=40,
        rationale="Pro is ahead.",
        after_turn_id=turn.id,
    )
    result = DebateResult(
        topic="Test topic",
        turns=[turn],
        score_history=[snapshot],
        winner=AgentRole.PRO,
        final_pro_score=60,
        final_con_score=40,
        final_summary="Pro wins overall.",
    )

    report = format_debate(result)
    assert "Debate topic: Test topic" in report
    assert "Round 1" in report
    assert "PRO" in report
    assert "OPENING" in report
    assert "Current scores — Pro: 60, Con: 40" in report
    assert "Final Winner: PRO" in report
    assert "Judge Summary: Pro wins overall." in report


def test_print_debate_writes_to_stdout(capsys) -> None:
    turn = Turn(
        round=1,
        agent=AgentRole.CON,
        turn_type=TurnType.REBUTTAL,
        text="Con rebuttal argument.",
    )
    snapshot = ScoreSnapshot(
        pro_score=30,
        con_score=70,
        rationale="Con looks better.",
        after_turn_id=turn.id,
    )
    result = DebateResult(
        topic="Test topic",
        turns=[turn],
        score_history=[snapshot],
        winner=AgentRole.CON,
        final_pro_score=30,
        final_con_score=70,
        final_summary="Con wins overall.",
    )

    print_debate(result)
    out = capsys.readouterr().out
    assert "Con rebuttal argument." in out
    assert "Final Winner: CON" in out

