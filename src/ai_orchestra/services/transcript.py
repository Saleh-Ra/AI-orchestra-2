"""Mutable debate transcript with judge formatting helpers."""

from __future__ import annotations

import json

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.debate import DebateResult, DebateState
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn


class Transcript:
    """Stores debate turns and score history for one run."""

    def __init__(self, topic: str) -> None:
        self._state = DebateState(topic=topic)

    @property
    def topic(self) -> str:
        return self._state.topic

    @property
    def turns(self) -> list[Turn]:
        return list(self._state.turns)

    @property
    def score_history(self) -> list[ScoreSnapshot]:
        return list(self._state.score_history)

    def __len__(self) -> int:
        return len(self._state.turns)

    def append_turn(self, turn: Turn) -> None:
        """Add a turn in chronological order."""

        self._state.turns.append(turn)

    def append_score(self, snapshot: ScoreSnapshot) -> None:
        """Record judge scores after a turn."""

        self._state.score_history.append(snapshot)

    def last_turn(self) -> Turn | None:
        if not self._state.turns:
            return None
        return self._state.turns[-1]

    def format_for_judge(self) -> str:
        """Format full transcript for the judge agent."""

        lines = [f"Debate topic: {self._state.topic}", ""]
        for turn in self._state.turns:
            lines.extend(_format_turn_block(turn))
        if self._state.score_history:
            latest = self._state.score_history[-1]
            lines.append(f"Current scores — Pro: {latest.pro_score}, Con: {latest.con_score}")
        return "\n".join(lines).strip()

    def to_state(self) -> DebateState:
        """Return an immutable snapshot of current state."""

        return DebateState.model_validate(self._state.model_dump())

    def to_dict(self) -> dict:
        return self._state.to_dict()

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> Transcript:
        state = DebateState.from_dict(data)
        transcript = cls(topic=state.topic)
        transcript._state = state
        return transcript

    @classmethod
    def from_json(cls, payload: str) -> Transcript:
        return cls.from_dict(json.loads(payload))

    def build_result(
        self,
        *,
        winner: AgentRole,
        final_summary: str,
        final_pro_score: int | None = None,
        final_con_score: int | None = None,
    ) -> DebateResult:
        """Construct final debate result from current transcript."""

        latest = self._state.latest_scores()
        pro = (
            final_pro_score if final_pro_score is not None else (latest.pro_score if latest else 0)
        )
        con = (
            final_con_score if final_con_score is not None else (latest.con_score if latest else 0)
        )
        return DebateResult(
            topic=self._state.topic,
            turns=self.turns,
            score_history=self.score_history,
            winner=winner,
            final_pro_score=pro,
            final_con_score=con,
            final_summary=final_summary,
        )


def _format_turn_block(turn: Turn) -> list[str]:
    agent_label = turn.agent.value.upper()
    type_label = turn.turn_type.value
    return [
        f"--- Round {turn.round} | {agent_label} | {type_label} (id: {turn.id}) ---",
        turn.text,
        "",
    ]


def create_turn(
    *,
    round_number: int,
    agent: AgentRole,
    turn_type: TurnType,
    text: str,
    turn_id: str | None = None,
) -> Turn:
    """Helper to build a validated turn."""

    data = {
        "round": round_number,
        "agent": agent,
        "turn_type": turn_type,
        "text": text,
    }
    if turn_id is not None:
        data["id"] = turn_id
    return Turn.model_validate(data)
