from pathlib import Path

from ai_orchestra.constants import AgentRole
from ai_orchestra.services.debate_factory import create_debate_engine
from ai_orchestra.shared.config import load_app_config


def test_full_debate_with_test_config(sample_config) -> None:
    engine = create_debate_engine(sample_config)
    result = engine.run()
    assert len(result.turns) == 4
    assert len(result.score_history) == 4
    assert result.winner in {AgentRole.PRO, AgentRole.CON}
    assert result.final_summary


def test_run_debate_from_test_fixtures(setup_test_path: Path, rate_limits_test_path: Path) -> None:
    app_config = load_app_config(setup_test_path, rate_limits_test_path)
    engine = create_debate_engine(app_config)
    result = engine.run()
    assert result.topic == "Test debate topic."
    assert len(result.turns) == 2 * app_config.setup.debate.round_count
