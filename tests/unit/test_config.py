import json
from pathlib import Path

import pytest

from ai_orchestra.constants import OpenerPolicy
from ai_orchestra.shared.config import (
    ConfigError,
    ConfigNotFoundError,
    SecretInConfigError,
    get_openai_api_key,
    load_rate_limits_config,
    load_setup_config,
)
from ai_orchestra.shared.config_models import SetupConfig


def test_load_setup_config_from_fixture(setup_test_path: Path) -> None:
    cfg = load_setup_config(setup_test_path)
    assert cfg.app_name == "AI Orchestra 2 Test"
    assert cfg.debate.round_count == 2
    assert cfg.debate.opener_policy == OpenerPolicy.ALTERNATE
    assert cfg.mock_llm is True


def test_load_setup_config_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(ConfigNotFoundError, match="not found"):
        load_setup_config(missing)


def test_load_app_config_from_fixtures(sample_config) -> None:
    assert sample_config.setup.debate.topic == "Test debate topic."
    assert sample_config.rate_limits.default_service().requests_per_minute == 60


def test_setup_config_has_no_api_key_field() -> None:
    fields = set(SetupConfig.model_fields)
    assert "api_key" not in fields
    assert "openai_api_key" not in fields


def test_reject_secret_key_in_json(tmp_path: Path) -> None:
    bad = {
        "version": "1.00",
        "app_name": "Bad",
        "debate": {
            "topic": "x",
            "round_count": 1,
            "opener_policy": "alternate",
        },
        "llm": {"model": "gpt-4o-mini", "temperature": {"pro": 0.5, "con": 0.5, "judge": 0.1}},
        "api_key": "sk-should-not-be-here",
    }
    path = tmp_path / "bad_setup.json"
    path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(SecretInConfigError, match="Forbidden config key"):
        load_setup_config(path)


def test_get_openai_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
    assert get_openai_api_key() == "test-key-123"


def test_get_openai_api_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ConfigError, match="OPENAI_API_KEY"):
        get_openai_api_key()


def test_load_project_setup_json() -> None:
    cfg = load_setup_config()
    assert cfg.debate.round_count == 10
    assert "social media" in cfg.debate.topic.lower()


def test_load_project_rate_limits_json() -> None:
    limits = load_rate_limits_config()
    default = limits.default_service()
    assert default.max_retries == 3
