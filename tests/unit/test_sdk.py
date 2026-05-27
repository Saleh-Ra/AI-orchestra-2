import pytest

from ai_orchestra.constants import AgentRole
from ai_orchestra.sdk import DebateSDK


def test_sdk_run_debate_with_fixture_config(setup_test_path) -> None:
    sdk = DebateSDK()
    result = sdk.run_debate(setup_test_path)
    assert result.topic == "Test debate topic."
    assert len(result.turns) == 4
    assert len(result.score_history) == 4
    assert result.winner == AgentRole.PRO
    assert result.final_pro_score == 55
    assert result.final_con_score == 45


def test_sdk_does_not_require_api_key_when_mock(monkeypatch: pytest.MonkeyPatch, setup_test_path) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    sdk = DebateSDK()
    result = sdk.run_debate(setup_test_path)
    assert result.winner in {AgentRole.PRO, AgentRole.CON}

