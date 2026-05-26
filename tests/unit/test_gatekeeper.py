import logging

import pytest

from ai_orchestra.services.llm_errors import LlmTransientError
from ai_orchestra.shared.gatekeeper import ApiGatekeeper
from ai_orchestra.shared.gatekeeper_models import (
    GatekeeperQueueFullError,
    RateLimitConfig,
)


def _limits(
    *,
    rpm: int = 60,
    rph: int = 1000,
    concurrent: int = 5,
    retries: int = 3,
    queue: int = 100,
) -> RateLimitConfig:
    return RateLimitConfig(
        requests_per_minute=rpm,
        requests_per_hour=rph,
        concurrent_max=concurrent,
        retry_after_seconds=0,
        max_retries=retries,
        queue_max_depth=queue,
    )


def test_gatekeeper_execute_returns_result() -> None:
    gatekeeper = ApiGatekeeper(_limits())

    def api_call(value: int) -> int:
        return value * 2

    assert gatekeeper.execute(api_call, 4) == 8
    status = gatekeeper.get_queue_status()
    assert status.total_calls == 1


def test_gatekeeper_retries_transient_errors() -> None:
    attempts: list[int] = []

    def flaky() -> str:
        attempts.append(1)
        if len(attempts) < 3:
            raise LlmTransientError("temporary outage")
        return "ok"

    gatekeeper = ApiGatekeeper(_limits(retries=3))
    assert gatekeeper.execute(flaky) == "ok"
    assert len(attempts) == 3
    assert gatekeeper.get_queue_status().total_retries == 2


def test_gatekeeper_logs_calls() -> None:
    records: list[logging.LogRecord] = []

    class ListHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    logger = logging.getLogger("test.gatekeeper")
    logger.handlers.clear()
    logger.addHandler(ListHandler())
    logger.setLevel(logging.INFO)

    gatekeeper = ApiGatekeeper(_limits(), logger=logger)
    gatekeeper.execute(lambda: "done")

    messages = [record.getMessage() for record in records]
    assert any("executing" in message for message in messages)
    assert any("succeeded" in message for message in messages)


def test_gatekeeper_waits_when_minute_limit_reached() -> None:
    times = [0.0]
    sleeps: list[float] = []

    def clock() -> float:
        return times[-1]

    def sleeper(seconds: float) -> None:
        sleeps.append(seconds)
        times.append(times[-1] + seconds)

    gatekeeper = ApiGatekeeper(
        _limits(rpm=1, rph=1000),
        clock=clock,
        sleeper=sleeper,
    )
    assert gatekeeper.execute(lambda: 1) == 1
    assert gatekeeper.execute(lambda: 2) == 2
    assert sleeps
    assert sleeps[0] > 0


def test_gatekeeper_queue_full_raises() -> None:
    gatekeeper = ApiGatekeeper(
        _limits(rpm=1, queue=0),
        clock=lambda: 0.0,
        sleeper=lambda _seconds: None,
    )
    assert gatekeeper.execute(lambda: 1) == 1
    with pytest.raises(GatekeeperQueueFullError):
        gatekeeper.execute(lambda: 2)


def test_gatekeeper_from_config_file(rate_limits_test_path) -> None:
    gatekeeper = ApiGatekeeper.from_config_file(rate_limits_test_path)
    assert gatekeeper.execute(lambda: "x") == "x"
