"""Public configuration API for AI Orchestra 2.

Internals were split into smaller helper modules to keep each file within the
course guideline limits.
"""

from ai_orchestra.shared.config_errors import (
    ConfigError,
    ConfigNotFoundError,
    SecretInConfigError,
)
from ai_orchestra.shared.config_loader import (
    get_openai_api_key,
    get_openai_base_url,
    load_app_config,
    load_logging_config,
    load_rate_limits_config,
    load_setup_config,
)
from ai_orchestra.shared.config_models import (
    AppConfig,
    LoggingConfig,
    RateLimitsConfig,
    SetupConfig,
)

__all__ = [
    "AppConfig",
    "ConfigError",
    "ConfigNotFoundError",
    "LoggingConfig",
    "RateLimitsConfig",
    "SecretInConfigError",
    "SetupConfig",
    "get_openai_api_key",
    "get_openai_base_url",
    "load_app_config",
    "load_logging_config",
    "load_rate_limits_config",
    "load_setup_config",
]
