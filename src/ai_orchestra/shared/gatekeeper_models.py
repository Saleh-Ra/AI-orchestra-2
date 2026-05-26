"""Models and errors for the API gatekeeper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_orchestra.shared.config_models import RateLimitServiceSettings


@dataclass(frozen=True)
class RateLimitConfig:
    """Runtime rate-limit settings for a single service."""

    requests_per_minute: int
    requests_per_hour: int
    concurrent_max: int
    retry_after_seconds: int
    max_retries: int
    queue_max_depth: int

    @classmethod
    def from_service(cls, service: RateLimitServiceSettings) -> RateLimitConfig:
        return cls(
            requests_per_minute=service.requests_per_minute,
            requests_per_hour=service.requests_per_hour,
            concurrent_max=service.concurrent_max,
            retry_after_seconds=service.retry_after_seconds,
            max_retries=service.max_retries,
            queue_max_depth=service.queue_max_depth,
        )


@dataclass(frozen=True)
class QueueStatus:
    """Snapshot of gatekeeper queue and usage."""

    queue_depth: int
    concurrent_in_use: int
    requests_last_minute: int
    requests_last_hour: int
    total_calls: int
    total_retries: int


class GatekeeperError(Exception):
    """Base gatekeeper error."""


class GatekeeperQueueFullError(GatekeeperError):
    """Raised when the wait queue exceeds configured depth."""
