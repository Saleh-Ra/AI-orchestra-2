"""Stub agents for debate engine tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.transcript import Transcript


@dataclass
class StubDebater:
    """Records generate_argument calls and returns deterministic text."""

    role: AgentRole
    calls: list[tuple[TurnType, int]] = field(default_factory=list)

    def generate_argument(
        self,
        transcript: Transcript,
        turn_type: TurnType,
        *,
        round_number: int,
    ) -> str:
        self.calls.append((turn_type, round_number))
        return f"{self.role.value}-{turn_type.value}-round-{round_number}"


@dataclass
class StubJudge:
    """Returns increasing pro scores for each judge call."""

    calls: int = 0

    def score_after_turn(self, transcript: Transcript, latest_turn) -> ScoreSnapshot:
        self.calls += 1
        pro_score = min(100, 30 + self.calls * 3)
        con_score = max(0, 100 - pro_score)
        return ScoreSnapshot(
            pro_score=pro_score,
            con_score=con_score,
            rationale=f"Judge update #{self.calls}",
            after_turn_id=latest_turn.id,
        )
