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
