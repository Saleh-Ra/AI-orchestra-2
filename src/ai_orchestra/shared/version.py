"""Package and configuration version helpers."""

from __future__ import annotations

__version__ = "0.1.0"

# Config file version expected by this codebase (course standard: 1.00).
CONFIG_VERSION = "1.00"


class ConfigVersionError(ValueError):
    """Raised when a config file version does not match CONFIG_VERSION."""


def validate_config_version(version: str, *, source: str = "config") -> None:
    """Ensure config version matches the version supported by this release."""

    if version != CONFIG_VERSION:
        msg = f"{source} version {version!r} is unsupported; expected {CONFIG_VERSION!r}."
        raise ConfigVersionError(msg)
