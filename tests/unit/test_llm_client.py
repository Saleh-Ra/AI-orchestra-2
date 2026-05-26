import pytest

from ai_orchestra.services.llm_client import LlmClient, build_llm_client
from ai_orchestra.services.llm_errors import LlmTransientError


def test_mock_llm_client_returns_fixed_response() -> None:
    client = build_llm_client(
        model="gpt-4o-mini",
        mock=True,
        mock_response='{"pro_score": 60, "con_score": 40, "rationale": "mock"}',
    )
    text = client.chat([{"role": "user", "content": "Hello"}], temperature=0.5)
    assert "pro_score" in text


def test_mock_client_does_not_open_network() -> None:
    client = LlmClient(model="gpt-4o-mini", mock=True)
    with pytest.raises(RuntimeError, match="Mock LlmClient"):
        client._ensure_client()


def test_map_openai_rate_limit_error() -> None:
    from ai_orchestra.services import llm_client as module

    class FakeRateLimitError(Exception):
        status_code = 429

    mapped = module._map_openai_error(FakeRateLimitError("limit"))
    assert isinstance(mapped, LlmTransientError)


def test_map_openai_server_error_by_status_code() -> None:
    from ai_orchestra.services import llm_client as module

    class FakeServerError(Exception):
        status_code = 503

    mapped = module._map_openai_error(FakeServerError("down"))
    assert isinstance(mapped, LlmTransientError)
