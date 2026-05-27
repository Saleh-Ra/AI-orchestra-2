import pytest

from ai_orchestra.constants import AgentRole, OpenerPolicy
from ai_orchestra.services.debate_engine import DebateEngine, DebateEngineError
from ai_orchestra.shared.config_models import (
    DebateSettings,
    LlmSettings,
    LlmTemperatureSettings,
    SetupConfig,
)
from tests.helpers.stub_agents import StubDebater, StubJudge


def _setup(*, round_count: int = 10) -> SetupConfig:
    return SetupConfig(
        version="1.00",
        debate=DebateSettings(
            topic="Social media improves human communication.",
            round_count=round_count,
            opener_policy=OpenerPolicy.ALTERNATE,
        ),
        llm=LlmSettings(
            model="gpt-4o-mini",
            temperature=LlmTemperatureSettings(pro=0.8, con=0.8, judge=0.3),
        ),
        mock_llm=True,
    )


def _engine(*, round_count: int = 10) -> tuple[DebateEngine, StubJudge]:
    judge = StubJudge()
    engine = DebateEngine(
        _setup(round_count=round_count),
        StubDebater(AgentRole.PRO),
        StubDebater(AgentRole.CON),
        judge,
    )
    return engine, judge


def test_ten_rounds_produce_twenty_turns() -> None:
    engine, _ = _engine(round_count=10)
    result = engine.run()
    assert len(result.turns) == 20


def test_judge_called_after_every_turn() -> None:
    engine, judge = _engine(round_count=10)
    result = engine.run()
    assert judge.calls == 20
    assert len(result.score_history) == 20


def test_score_history_matches_judge_calls() -> None:
    engine, judge = _engine(round_count=3)
    result = engine.run()
    assert len(result.score_history) == judge.calls == 6


def test_winner_from_final_scores() -> None:
    engine, _ = _engine(round_count=2)
    result = engine.run()
    latest = result.score_history[-1]
    expected = AgentRole.PRO if latest.pro_score >= latest.con_score else AgentRole.CON
    assert result.winner == expected


def test_engine_wraps_unexpected_errors() -> None:
    class FailingDebater(StubDebater):
        def generate_argument(self, transcript, turn_type, *, round_number):
            raise RuntimeError("agent failure")

    judge = StubJudge()
    engine = DebateEngine(
        _setup(round_count=1),
        FailingDebater(AgentRole.PRO),
        StubDebater(AgentRole.CON),
        judge,
    )
    with pytest.raises(DebateEngineError, match="aborted"):
        engine.run()
