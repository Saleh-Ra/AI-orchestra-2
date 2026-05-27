from pathlib import Path

import pytest

from ai_orchestra.constants import AgentRole
from ai_orchestra.sdk import DebateSDK
from ai_orchestra.sdk.sdk import _resolve_config_paths


def test_sdk_run_debate_with_fixture_config(setup_test_path) -> None:
    sdk = DebateSDK()
    result = sdk.run_debate(setup_test_path)
    assert result.topic == "Test debate topic."
    assert len(result.turns) == 4
    assert len(result.score_history) == 4
    assert result.winner == AgentRole.PRO
    assert result.final_pro_score == 55
    assert result.final_con_score == 45


def test_sdk_does_not_require_api_key_when_mock(
    monkeypatch: pytest.MonkeyPatch, setup_test_path
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    sdk = DebateSDK()
    result = sdk.run_debate(setup_test_path)
    assert result.winner in {AgentRole.PRO, AgentRole.CON}


def test_resolve_config_paths_none() -> None:
    assert _resolve_config_paths(None) == (None, None)


def test_resolve_config_paths_from_setup_file(setup_test_path, rate_limits_test_path) -> None:
    setup, rate = _resolve_config_paths(setup_test_path)
    assert setup == setup_test_path
    assert rate == rate_limits_test_path


def test_resolve_config_paths_from_rate_limits_file(setup_test_path, rate_limits_test_path) -> None:
    setup, rate = _resolve_config_paths(rate_limits_test_path)
    assert setup == setup_test_path
    assert rate == rate_limits_test_path


def test_resolve_config_paths_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        _resolve_config_paths("definitely_missing_setup.test.json")


def test_resolve_config_paths_invalid_filename(tmp_path: Path) -> None:
    bad = tmp_path / "not_a_setup_file.json"
    bad.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="setup"):
        _resolve_config_paths(bad)
