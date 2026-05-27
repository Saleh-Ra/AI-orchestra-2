"""Centralized API gatekeeper with rate limits, queueing, and retries."""

from __future__ import annotations

import logging
import threading
import time
from collections import deque
from collections.abc import Callable
from typing import Any, TypeVar

from ai_orchestra.shared.config import load_rate_limits_config
from ai_orchestra.shared.config_models import RateLimitServiceSettings
from ai_orchestra.shared.gatekeeper_models import (
    GatekeeperQueueFullError,
    QueueStatus,
    RateLimitConfig,
)
from ai_orchestra.shared.gatekeeper_utils import count_since, is_transient, seconds_until_slot

T = TypeVar("T")
Clock = Callable[[], float]
Sleeper = Callable[[float], None]


class ApiGatekeeper:
    """Execute external API calls with rate limiting and retries."""

    def __init__(
        self,
        config: RateLimitConfig | RateLimitServiceSettings,
        *,
        logger: logging.Logger | None = None,
        clock: Clock | None = None,
        sleeper: Sleeper | None = None,
    ) -> None:
        if isinstance(config, RateLimitServiceSettings):
            config = RateLimitConfig.from_service(config)
        self.config = config
        self._logger = logger or logging.getLogger(__name__)
        self._clock = clock or time.monotonic
        self._sleeper = sleeper or time.sleep
        self._lock = threading.Lock()
        self._request_times: deque[float] = deque()
        self._concurrent = 0
        self._waiting = 0
        self._total_calls = 0
        self._total_retries = 0

    @classmethod
    def from_config_file(cls, path: str | None = None, **kwargs: Any) -> ApiGatekeeper:
        """Build gatekeeper using ``config/rate_limits.json`` (or override path)."""

        limits = load_rate_limits_config(path)
        return cls(limits.default_service(), **kwargs)

    def execute(self, api_callable: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Run ``api_callable`` through rate limits with retries."""

        self._acquire_slot()
        try:
            return self._execute_with_retry(api_callable, *args, **kwargs)
        finally:
            self._release_slot()

    def get_queue_status(self) -> QueueStatus:
        """Return current queue depth and usage counters."""

        with self._lock:
            now = self._clock()
            return QueueStatus(
                queue_depth=self._waiting,
                concurrent_in_use=self._concurrent,
                requests_last_minute=count_since(self._request_times, now, 60),
                requests_last_hour=count_since(self._request_times, now, 3600),
                total_calls=self._total_calls,
                total_retries=self._total_retries,
            )

    def _execute_with_retry(self, api_callable: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        attempts = 0
        while True:
            try:
                self._logger.info(
                    "Gatekeeper executing %s", getattr(api_callable, "__name__", "call")
                )
                result = api_callable(*args, **kwargs)
                with self._lock:
                    self._total_calls += 1
                self._logger.info("Gatekeeper call succeeded")
                return result
            except Exception as exc:
                if not is_transient(exc) or attempts >= self.config.max_retries:
                    self._logger.error("Gatekeeper call failed: %s", exc)
                    raise
                attempts += 1
                with self._lock:
                    self._total_retries += 1
                self._logger.warning(
                    "Gatekeeper retry %d/%d after transient error",
                    attempts,
                    self.config.max_retries,
                )
                self._sleeper(self.config.retry_after_seconds)

    def _acquire_slot(self) -> None:
        while True:
            with self._lock:
                now = self._clock()
                if self._can_proceed(now):
                    self._request_times.append(now)
                    self._concurrent += 1
                    return
                if self._waiting >= self.config.queue_max_depth:
                    raise GatekeeperQueueFullError(
                        f"Queue full (max depth {self.config.queue_max_depth})."
                    )
                self._waiting += 1
            wait_seconds = seconds_until_slot(
                self._request_times,
                now=now,
                config=self.config,
                concurrent_in_use=self._concurrent,
            )
            self._sleeper(max(wait_seconds, 0.001))
            with self._lock:
                self._waiting = max(self._waiting - 1, 0)

    def _release_slot(self) -> None:
        with self._lock:
            self._concurrent = max(self._concurrent - 1, 0)

    def _can_proceed(self, now: float) -> bool:
        if self._concurrent >= self.config.concurrent_max:
            return False
        return (
            count_since(self._request_times, now, 60) < self.config.requests_per_minute
            and count_since(self._request_times, now, 3600) < self.config.requests_per_hour
        )
