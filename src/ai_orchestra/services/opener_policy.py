"""Resolve which agent opens each debate round."""

from __future__ import annotations

import random

from ai_orchestra.constants import AgentRole, OpenerPolicy

# Default for v1 (see docs/PLAN.md ADR-003): Pro opens odd rounds, Con opens even.


def resolve_opener(
    policy: OpenerPolicy,
    round_number: int,
    *,
    rng: random.Random | None = None,
) -> AgentRole:
    """Return the agent that delivers the opening turn for ``round_number``."""

    if round_number < 1:
        msg = f"round_number must be >= 1, got {round_number}"
        raise ValueError(msg)

    if policy == OpenerPolicy.ALTERNATE:
        return AgentRole.PRO if round_number % 2 == 1 else AgentRole.CON
    if policy == OpenerPolicy.FIXED_PRO:
        return AgentRole.PRO
    if policy == OpenerPolicy.FIXED_CON:
        return AgentRole.CON
    if policy == OpenerPolicy.RANDOM:
        random_source = rng or random.Random()
        return random_source.choice([AgentRole.PRO, AgentRole.CON])

    msg = f"Unsupported opener policy: {policy!r}"
    raise ValueError(msg)
