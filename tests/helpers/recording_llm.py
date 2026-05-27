"""Test doubles for LLM client."""

from __future__ import annotations

from ai_orchestra.services.llm_client import Message


class RecordingLlmClient:
    """Records ``chat`` calls and returns a fixed or queued response."""

    def __init__(self, response: str = "Sample argument.") -> None:
        self.response = response
        self.calls: list[dict] = []

    def chat(self, messages: list[Message], *, temperature: float) -> str:
        self.calls.append({"messages": messages, "temperature": temperature})
        return self.response

    @property
    def last_messages(self) -> list[Message]:
        return self.calls[-1]["messages"]

    @property
    def last_user_content(self) -> str:
        return self.last_messages[-1]["content"]
