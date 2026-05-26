from ai_orchestra.constants import AgentRole, OpenerPolicy, TurnType


def test_turn_type_values() -> None:
    assert TurnType.OPENING.value == "opening"
    assert TurnType.REBUTTAL.value == "rebuttal"


def test_agent_role_values() -> None:
    assert AgentRole.PRO.value == "pro"
    assert AgentRole.CON.value == "con"
    assert AgentRole.JUDGE.value == "judge"


def test_opener_policy_values() -> None:
    assert OpenerPolicy.ALTERNATE.value == "alternate"
    assert OpenerPolicy.FIXED_PRO.value == "fixed_pro"
