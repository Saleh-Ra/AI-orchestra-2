"""Load system prompt templates from disk."""

from __future__ import annotations

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent
PROMPT_VERSION = "0.1.0"


def load_prompt(name: str, *, topic: str) -> str:
    """Load and format a system prompt template (e.g. ``pro``, ``con``, ``judge``)."""

    path = PROMPTS_DIR / f"{name}_system.txt"
    if not path.is_file():
        msg = f"Prompt template not found: {path}"
        raise FileNotFoundError(msg)
    template = path.read_text(encoding="utf-8")
    return template.format(topic=topic)
