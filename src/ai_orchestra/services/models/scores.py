"""Persuasion score snapshots."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

MIN_SCORE = 0
MAX_SCORE = 100


class ScoreSnapshot(BaseModel):
    """Judge scores immediately after a debate turn."""

    pro_score: int = Field(ge=MIN_SCORE, le=MAX_SCORE)
    con_score: int = Field(ge=MIN_SCORE, le=MAX_SCORE)
    rationale: str = Field(min_length=1)
    after_turn_id: str = Field(min_length=1)

    @field_validator("pro_score", "con_score", mode="before")
    @classmethod
    def coerce_score(cls, value: int | float | str) -> int:
        return int(value)
