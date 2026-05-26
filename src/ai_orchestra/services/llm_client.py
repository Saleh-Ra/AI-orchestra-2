"""OpenAI-compatible LLM client (used only via ApiGatekeeper)."""

from __future__ import annotations

import logging
from typing import Any

from ai_orchestra.services.llm_errors import LlmTransientError
from ai_orchestra.shared.config import get_openai_api_key, get_openai_base_url

logger = logging.getLogger(__name__)

Message = dict[str, str]


class LlmClient:
    """Thin adapter around the OpenAI chat completions API."""

    def __init__(
        self,
        *,
        model: str,
        mock: bool = False,
        mock_response: str = "Mock LLM response.",
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.model = model
        self.mock = mock
        self.mock_response = mock_response
        self._api_key = api_key
        self._base_url = base_url
        self._client: Any | None = None

    def _ensure_client(self) -> Any:
        if self.mock:
            msg = "Mock LlmClient does not open a network connection."
            raise RuntimeError(msg)
        if self._client is None:
            from openai import OpenAI

            key = self._api_key or get_openai_api_key()
            url = self._base_url if self._base_url is not None else get_openai_base_url()
            self._client = OpenAI(api_key=key, base_url=url)
        return self._client

    def chat(self, messages: list[Message], *, temperature: float) -> str:
        """Return assistant text for the given chat messages."""

        if self.mock:
            logger.debug("LlmClient mock chat (%d messages)", len(messages))
            return self.mock_response

        try:
            client = self._ensure_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as exc:  # noqa: BLE001 — mapped below
            raise _map_openai_error(exc) from exc

        choice = response.choices[0].message
        return (choice.content or "").strip()


def build_llm_client(
    *,
    model: str,
    mock: bool = False,
    mock_response: str = "Mock LLM response.",
) -> LlmClient:
    """Factory for a configured ``LlmClient``."""

    return LlmClient(model=model, mock=mock, mock_response=mock_response)


def _map_openai_error(exc: Exception) -> Exception:
    """Map provider errors to transient vs permanent failures."""

    status = getattr(exc, "status_code", None)
    if isinstance(status, int) and status in {408, 429, 500, 502, 503, 504}:
        return LlmTransientError(str(exc))
    name = exc.__class__.__name__
    if name in {"RateLimitError", "APITimeoutError", "APIConnectionError"}:
        return LlmTransientError(str(exc))
    return exc
