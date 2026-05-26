"""Pytest fixtures for AI Orchestra 2."""

from pathlib import Path

import pytest

from ai_orchestra.shared.config import AppConfig, load_app_config

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def setup_test_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "setup.test.json"


@pytest.fixture
def rate_limits_test_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "rate_limits.test.json"


@pytest.fixture
def sample_config(setup_test_path: Path, rate_limits_test_path: Path) -> AppConfig:
    return load_app_config(
        setup_path=setup_test_path,
        rate_limits_path=rate_limits_test_path,
    )


@pytest.fixture
def mock_llm_client():
    from ai_orchestra.services.llm_client import build_llm_client

    return build_llm_client(
        model="gpt-4o-mini",
        mock=True,
        mock_response='{"pro_score": 55, "con_score": 45, "rationale": "fixture"}',
    )


@pytest.fixture
def gatekeeper(rate_limits_test_path: Path):
    from ai_orchestra.shared.gatekeeper import ApiGatekeeper

    return ApiGatekeeper.from_config_file(rate_limits_test_path)
