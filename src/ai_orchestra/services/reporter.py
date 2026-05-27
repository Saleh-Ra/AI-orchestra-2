"""Terminal reporter for AI Orchestra 2 debates."""

from __future__ import annotations

import datetime as dt
from collections.abc import Iterable
from pathlib import Path

from ai_orchestra.constants import AgentRole
from ai_orchestra.services.models.debate import DebateResult


def _header(turn_no: int, role: AgentRole) -> str:
    return f"Turn {turn_no}: {role.value.upper()}"


def format_debate(result: DebateResult) -> str:
    """Create a human-readable terminal report."""

    parts: list[str] = []
    parts.append(f"Debate topic: {result.topic}")
    parts.append("")

    for i, turn in enumerate(result.turns):
        snapshot = result.score_history[i] if i < len(result.score_history) else None
        parts.append(
            f"Round {turn.round} | Agent {turn.agent.value.upper()} | {turn.turn_type.value.upper()}"
        )
        parts.append(turn.text)
        if snapshot is not None:
            parts.append(f"Current scores — Pro: {snapshot.pro_score}, Con: {snapshot.con_score}")
        parts.append("")

    parts.append(
        f"Final Winner: {result.winner.value.upper()} "
        f"(Pro {result.final_pro_score} / Con {result.final_con_score})"
    )
    parts.append(f"Judge Summary: {result.final_summary}")
    return "\n".join(parts).strip() + "\n"


def print_debate(result: DebateResult) -> None:
    """Print the debate report to stdout."""

    print(format_debate(result), end="")


def save_debate_json(result: DebateResult, *, results_dir: str | Path) -> Path:
    """Save debate result JSON under `results_dir/` and return the path."""

    path_dir = Path(results_dir)
    path_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = path_dir / f"debate_{ts}.json"
    path.write_text(result.to_json(indent=2), encoding="utf-8")
    return path


def print_score_timeline(result: DebateResult) -> None:
    """Print scores after each turn (useful for debugging)."""

    for i, snapshot in enumerate(result.score_history, start=1):
        print(f"After turn {i}: Pro={snapshot.pro_score}, Con={snapshot.con_score}")


def iter_turn_lines(result: DebateResult) -> Iterable[str]:
    """Yield formatted lines for each turn (useful for tests)."""

    for i, turn in enumerate(result.turns):
        yield f"Round {turn.round} | Agent {turn.agent.value.upper()} | {turn.turn_type.value.upper()}"
        yield turn.text
        if i < len(result.score_history):
            s = result.score_history[i]
            yield f"Current scores — Pro: {s.pro_score}, Con: {s.con_score}"

