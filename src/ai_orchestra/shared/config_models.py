"""Pydantic models for JSON configuration files."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from ai_orchestra.constants import OpenerPolicy


class DebateSettings(BaseModel):
    """Debate parameters from setup.json."""

    topic: str = Field(min_length=1)
    round_count: int = Field(ge=1, le=50)
    opener_policy: OpenerPolicy

    @field_validator("opener_policy", mode="before")
    @classmethod
    def parse_opener_policy(cls, value: str | OpenerPolicy) -> OpenerPolicy:
        if isinstance(value, OpenerPolicy):
            return value
        return OpenerPolicy(value)


class LlmTemperatureSettings(BaseModel):
    """Per-role LLM sampling temperatures."""

    pro: float = Field(ge=0.0, le=2.0)
    con: float = Field(ge=0.0, le=2.0)
    judge: float = Field(ge=0.0, le=2.0)


class LlmSettings(BaseModel):
    """LLM provider settings (model name only; keys from env)."""

    model: str = Field(min_length=1)
    temperature: LlmTemperatureSettings


class OutputSettings(BaseModel):
    """Output and persistence options."""

    save_results_json: bool = False
    results_dir: str = "results"


class SetupConfig(BaseModel):
    """Root setup.json schema."""

    version: str
    app_name: str = "AI Orchestra 2"
    debate: DebateSettings
    llm: LlmSettings
    output: OutputSettings = Field(default_factory=OutputSettings)
    mock_llm: bool = False


class RateLimitServiceSettings(BaseModel):
    """Rate limits for one named service."""

    requests_per_minute: int = Field(ge=1)
    requests_per_hour: int = Field(ge=1)
    concurrent_max: int = Field(ge=1)
    retry_after_seconds: int = Field(ge=0)
    max_retries: int = Field(ge=0)
    queue_max_depth: int = Field(ge=1)


class RateLimitsConfig(BaseModel):
    """Root rate_limits.json schema."""

    version: str
    rate_limits: dict[str, dict[str, RateLimitServiceSettings]]

    def default_service(self) -> RateLimitServiceSettings:
        services = self.rate_limits.get("services", {})
        if "default" not in services:
            msg = "rate_limits.json must define services.default"
            raise ValueError(msg)
        return services["default"]


class LoggingConfig(BaseModel):
    """logging_config.json schema."""

    version: str
    logging: dict[str, str]


class AppConfig(BaseModel):
    """Combined application configuration."""

    setup: SetupConfig
    rate_limits: RateLimitsConfig
    logging: LoggingConfig | None = None
