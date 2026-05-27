"""Ensure agent modules do not import OpenAI directly."""

from pathlib import Path

FORBIDDEN = "openai"


def test_agent_modules_do_not_import_openai() -> None:
    agents_dir = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "ai_orchestra"
        / "services"
        / "agents"
    )
    for path in agents_dir.glob("*.py"):
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert FORBIDDEN not in source, f"{path.name} must not import openai"
