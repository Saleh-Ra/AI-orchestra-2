"""Load and validate configuration JSON from disk."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ai_orchestra.shared.config_errors import ConfigNotFoundError
from ai_orchestra.shared.config_helpers import (
    LOGGING_FILENAME,
    RATE_LIMITS_FILENAME,
    SETUP_FILENAME,
    config_dir,
    get_openai_api_key,
    get_openai_base_url,
    read_json,
    reject_secrets_in_payload,
    validate_file_version,
)
from ai_orchestra.shared.config_models import (
    AppConfig,
    LoggingConfig,
    RateLimitsConfig,
    SetupConfig,
)


def load_setup_config(config_path: str | Path | None = None) -> SetupConfig:
    """Load and validate setup.json."""

    path = Path(config_path) if config_path else config_dir() / SETUP_FILENAME
    raw: dict[str, Any] = read_json(path)
    reject_secrets_in_payload(raw)
    validate_file_version(raw, source="setup.json")
    return SetupConfig.model_validate(raw)


def load_rate_limits_config(config_path: str | Path | None = None) -> RateLimitsConfig:
    """Load and validate rate_limits.json."""

    path = Path(config_path) if config_path else config_dir() / RATE_LIMITS_FILENAME
    raw: dict[str, Any] = read_json(path)
    reject_secrets_in_payload(raw)
    validate_file_version(raw, source="rate_limits.json")
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
    raw = read_json(path)
    reject_secrets_in_payload(raw)
    validate_file_version(raw, source="logging_config.json")
    return LoggingConfig.model_validate(raw)


def load_app_config(
    setup_path: str | Path | None = None,
    rate_limits_path: str | Path | None = None,
) -> AppConfig:
    """Load setup, rate limits, and optional logging config."""

    # logging_config.json is optional by design in v1
    return AppConfig(
        setup=load_setup_config(setup_path),
        rate_limits=load_rate_limits_config(rate_limits_path),
        logging=load_logging_config(),
    )


__all__ = [
    "get_openai_api_key",
    "get_openai_base_url",
    "load_app_config",
    "load_logging_config",
    "load_rate_limits_config",
    "load_setup_config",
]

