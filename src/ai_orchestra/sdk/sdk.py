"""Public SDK for AI Orchestra 2.

Phase 1 provides a minimal, testable boundary without LLM integration yet.
"""

from __future__ import annotations


class DebateSDK:
    """SDK facade for running a debate."""

    def run_debate(self, *args, **kwargs) -> dict:
        """Run a debate (stub for Phase 1)."""

        return {"status": "not_implemented_yet"}

