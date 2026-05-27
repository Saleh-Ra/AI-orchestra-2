"""Low-level helpers for loading and validating configuration JSON."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ai_orchestra.shared.config_errors import ConfigError, ConfigNotFoundError, SecretInConfigError
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


def read_json(path: Path) -> dict[str, Any]:
    """Read JSON from disk with consistent errors."""

    if not path.is_file():
        raise ConfigNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_file_version(raw: dict[str, Any], *, source: str) -> None:
    """Ensure config files include a version matching CONFIG_VERSION."""

    version = raw.get("version")
    if version is None:
        msg = f"{source} must include a 'version' field"
        raise ConfigError(msg)
    validate_config_version(str(version), source=source)


def reject_secrets_in_payload(payload: Any, *, path: str = "root") -> None:
    """Reject config trees that embed credential-like keys."""

    if isinstance(payload, dict):
        for key, value in payload.items():
            key_lower = str(key).lower()
            if any(fragment in key_lower for fragment in FORBIDDEN_CONFIG_KEY_FRAGMENTS):
                raise SecretInConfigError(
                    f"Forbidden config key {key!r} at {path}; use environment variables."
                )
            reject_secrets_in_payload(value, path=f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            reject_secrets_in_payload(item, path=f"{path}[{index}]")


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

