"""Project-wide constants and enums."""

from enum import Enum


class AgentRole(str, Enum):
    """Debate participant roles."""

    PRO = "pro"
    CON = "con"
    JUDGE = "judge"


class TurnType(str, Enum):
    """Type of turn within a debate round."""

    OPENING = "opening"
    REBUTTAL = "rebuttal"


class OpenerPolicy(str, Enum):
    """Who opens each round."""

    ALTERNATE = "alternate"
    FIXED_PRO = "fixed_pro"
    FIXED_CON = "fixed_con"
    RANDOM = "random"
