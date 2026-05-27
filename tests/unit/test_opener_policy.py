import random

import pytest

from ai_orchestra.constants import AgentRole, OpenerPolicy
from ai_orchestra.services.opener_policy import resolve_opener


def test_alternate_opener_odd_rounds_pro_even_con() -> None:
    assert resolve_opener(OpenerPolicy.ALTERNATE, 1) == AgentRole.PRO
    assert resolve_opener(OpenerPolicy.ALTERNATE, 2) == AgentRole.CON
    assert resolve_opener(OpenerPolicy.ALTERNATE, 9) == AgentRole.PRO
    assert resolve_opener(OpenerPolicy.ALTERNATE, 10) == AgentRole.CON


def test_fixed_pro_and_con() -> None:
    assert resolve_opener(OpenerPolicy.FIXED_PRO, 5) == AgentRole.PRO
    assert resolve_opener(OpenerPolicy.FIXED_CON, 5) == AgentRole.CON


def test_random_opener_uses_injected_rng() -> None:
    rng = random.Random(42)
    first = resolve_opener(OpenerPolicy.RANDOM, 1, rng=rng)
    second = resolve_opener(OpenerPolicy.RANDOM, 2, rng=rng)
    assert first in {AgentRole.PRO, AgentRole.CON}
    assert second in {AgentRole.PRO, AgentRole.CON}


def test_invalid_round_number() -> None:
    with pytest.raises(ValueError, match="round_number"):
        resolve_opener(OpenerPolicy.ALTERNATE, 0)
