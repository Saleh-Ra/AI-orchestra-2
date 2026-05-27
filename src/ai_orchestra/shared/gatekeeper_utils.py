"""Pure helper functions for :mod:`ai_orchestra.shared.gatekeeper`.

Extracted to keep the main gatekeeper module within the course file-size rule.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from ai_orchestra.services.llm_errors import LlmTransientError
from ai_orchestra.shared.gatekeeper_models import RateLimitConfig


def is_transient(exc: Exception) -> bool:
    """Return whether an exception should be retried."""

    if isinstance(exc, LlmTransientError):
        return True
    status = getattr(exc, "status_code", None)
    return isinstance(status, int) and status in {408, 429, 500, 502, 503, 504}


def count_since(request_times: Iterable[float], now: float, window: float) -> int:
    """Count request timestamps within a rolling window."""

    return sum(1 for stamp in request_times if now - stamp < window)


def seconds_until_slot(
    request_times: deque[float],
    *,
    now: float,
    config: RateLimitConfig,
    concurrent_in_use: int,
) -> float:
    """Compute how long we should wait before attempting a new slot."""

    waits: list[float] = [0.0]
    minute_times = [stamp for stamp in request_times if now - stamp < 60]
    if len(minute_times) >= config.requests_per_minute:
        waits.append(60 - (now - min(minute_times)) + 0.001)

    hour_times = [stamp for stamp in request_times if now - stamp < 3600]
    if len(hour_times) >= config.requests_per_hour:
        waits.append(3600 - (now - min(hour_times)) + 0.001)

    if concurrent_in_use >= config.concurrent_max:
        waits.append(config.retry_after_seconds)

    return max(waits)
