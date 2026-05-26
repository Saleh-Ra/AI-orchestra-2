"""LLM client errors."""


class LlmError(Exception):
    """Base LLM client error."""


class LlmTransientError(LlmError):
    """Temporary failure that may succeed on retry."""
