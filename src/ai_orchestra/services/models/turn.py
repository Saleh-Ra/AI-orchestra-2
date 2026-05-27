"""Debate turn model."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from ai_orchestra.constants import AgentRole, TurnType

DEBATER_ROLES = {AgentRole.PRO, AgentRole.CON}


def new_turn_id() -> str:
    """Generate a unique turn identifier."""

    return str(uuid4())


class Turn(BaseModel):
    """One agent utterance in the debate."""

    id: str = Field(default_factory=new_turn_id)
    round: int = Field(ge=1)
    agent: AgentRole
    turn_type: TurnType
    text: str = Field(min_length=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @field_validator("agent")
    @classmethod
    def agent_must_be_debater(cls, value: AgentRole) -> AgentRole:
        if value not in DEBATER_ROLES:
            msg = "Turn agent must be PRO or CON, not JUDGE."
            raise ValueError(msg)
        return value
