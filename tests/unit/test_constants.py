from ai_orchestra.constants import TurnType


def test_turn_type_values() -> None:
    assert TurnType.OPENING.value == "opening"
    assert TurnType.REBUTTAL.value == "rebuttal"

