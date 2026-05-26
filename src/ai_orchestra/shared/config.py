"""Load JSON configuration and environment secrets."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ai_orchestra.shared.config_models import (
    AppConfig,
    LoggingConfig,
    RateLimitsConfig,
    SetupConfig,
)
from ai_orchestra.shared.version import validate_config_version

FORBIDDEN_CONFIG_KEY_FRAGMENTS = (
    "api_key",
    "apikey",
    "secret",
    "password",
    "token",
)

SETUP_FILENAME = "setup.json"
RATE_LIMITS_FILENAME = "rate_limits.json"
LOGGING_FILENAME = "logging_config.json"


class ConfigError(Exception):
    """Base error for configuration problems."""


class ConfigNotFoundError(ConfigError, FileNotFoundError):
    """Raised when a required config file is missing."""


class SecretInConfigError(ConfigError, ValueError):
    """Raised when config JSON appears to contain secrets."""


def project_root() -> Path:
    """Resolve repository root (directory containing pyproject.toml)."""

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


def config_dir() -> Path:
    """Default config directory under project root."""

    return project_root() / "config"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _validate_file_version(raw: dict[str, Any], *, source: str) -> None:
    version = raw.get("version")
    if version is None:
        msg = f"{source} must include a 'version' field"
        raise ConfigError(msg)
    validate_config_version(str(version), source=source)


def _reject_secrets_in_payload(payload: Any, *, path: str = "root") -> None:
    """Reject config trees that embed credential-like keys."""

    if isinstance(payload, dict):
        for key, value in payload.items():
            key_lower = str(key).lower()
            if any(fragment in key_lower for fragment in FORBIDDEN_CONFIG_KEY_FRAGMENTS):
                raise SecretInConfigError(
                    f"Forbidden config key {key!r} at {path}; use environment variables."
                )
            _reject_secrets_in_payload(value, path=f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            _reject_secrets_in_payload(item, path=f"{path}[{index}]")


def load_setup_config(config_path: str | Path | None = None) -> SetupConfig:
    """Load and validate setup.json."""

    path = Path(config_path) if config_path else config_dir() / SETUP_FILENAME
    raw = _read_json(path)
    _reject_secrets_in_payload(raw)
    _validate_file_version(raw, source="setup.json")
    return SetupConfig.model_validate(raw)


def load_rate_limits_config(config_path: str | Path | None = None) -> RateLimitsConfig:
    """Load and validate rate_limits.json."""

    path = Path(config_path) if config_path else config_dir() / RATE_LIMITS_FILENAME
    raw = _read_json(path)
    _reject_secrets_in_payload(raw)
    _validate_file_version(raw, source="rate_limits.json")
    return RateLimitsConfig.model_validate(raw)


def load_logging_config(
    config_path: str | Path | None = None,
    *,
    required: bool = False,
) -> LoggingConfig | None:
    """Load logging_config.json when present."""

    path = Path(config_path) if config_path else config_dir() / LOGGING_FILENAME
    if not path.is_file():
        if required:
            raise ConfigNotFoundError(f"Config file not found: {path}")
        return None
    raw = _read_json(path)
    _reject_secrets_in_payload(raw)
    _validate_file_version(raw, source="logging_config.json")
    return LoggingConfig.model_validate(raw)


def load_app_config(
    setup_path: str | Path | None = None,
    rate_limits_path: str | Path | None = None,
) -> AppConfig:
    """Load setup, rate limits, and optional logging config."""

    return AppConfig(
        setup=load_setup_config(setup_path),
        rate_limits=load_rate_limits_config(rate_limits_path),
        logging=load_logging_config(),
    )


def get_openai_api_key() -> str:
    """Read OpenAI API key from environment (never from JSON config)."""

    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        msg = "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
        raise ConfigError(msg)
    return key


def get_openai_base_url() -> str | None:
    """Optional custom API base URL from environment."""

    value = os.environ.get("OPENAI_BASE_URL", "").strip()
    return value or None
