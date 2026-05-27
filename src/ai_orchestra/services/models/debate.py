"""Debate state and final result models."""

from __future__ import annotations

import json

from pydantic import BaseModel, Field, model_validator

from ai_orchestra.constants import AgentRole
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn


class DebateState(BaseModel):
    """Running debate: transcript turns and score history."""

    topic: str = Field(min_length=1)
    turns: list[Turn] = Field(default_factory=list)
    score_history: list[ScoreSnapshot] = Field(default_factory=list)

    def latest_scores(self) -> ScoreSnapshot | None:
        if not self.score_history:
            return None
        return self.score_history[-1]

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> DebateState:
        return cls.model_validate(data)


class DebateResult(BaseModel):
    """Final output after all rounds complete."""

    topic: str
    turns: list[Turn]
    score_history: list[ScoreSnapshot]
    winner: AgentRole
    final_pro_score: int = Field(ge=0, le=100)
    final_con_score: int = Field(ge=0, le=100)
    final_summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def winner_must_be_debater(self) -> DebateResult:
        if self.winner not in {AgentRole.PRO, AgentRole.CON}:
            msg = "Winner must be PRO or CON."
            raise ValueError(msg)
        return self

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> DebateResult:
        return cls.model_validate(data)
