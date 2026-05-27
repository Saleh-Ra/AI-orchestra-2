"""Configuration error types."""


class ConfigError(Exception):
    """Base error for configuration problems."""


class ConfigNotFoundError(ConfigError, FileNotFoundError):
    """Raised when a required config file is missing."""


class SecretInConfigError(ConfigError, ValueError):
    """Raised when config JSON appears to contain secrets."""
