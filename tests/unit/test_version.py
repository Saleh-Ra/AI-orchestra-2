import re
from pathlib import Path

import pytest

from ai_orchestra import __version__
from ai_orchestra.shared.version import (
    CONFIG_VERSION,
    ConfigVersionError,
    validate_config_version,
)


def test_version_is_semver_like() -> None:
    assert re.match(r"^\d+\.\d+\.\d+$", __version__) is not None


def test_config_version_constant() -> None:
    assert CONFIG_VERSION == "1.00"


def test_validate_config_version_accepts_current() -> None:
    validate_config_version("1.00", source="test.json")


def test_validate_config_version_rejects_mismatch() -> None:
    with pytest.raises(ConfigVersionError, match="unsupported"):
        validate_config_version("2.00", source="setup.json")


def test_setup_config_rejects_wrong_version(setup_test_path: Path, tmp_path: Path) -> None:
    from ai_orchestra.shared.config import load_setup_config

    raw = setup_test_path.read_text(encoding="utf-8").replace('"1.00"', '"9.99"', 1)
    bad_path = tmp_path / "bad_version.json"
    bad_path.write_text(raw, encoding="utf-8")
    with pytest.raises(ConfigVersionError):
        load_setup_config(bad_path)
