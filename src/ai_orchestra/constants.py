"""Project-wide constants.

Phase 1 keeps this module intentionally small.
"""

from enum import Enum


class TurnType(str, Enum):
    OPENING = "opening"
    REBUTTAL = "rebuttal"

