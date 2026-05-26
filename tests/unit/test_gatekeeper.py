from ai_orchestra.shared.gatekeeper import ApiGatekeeper


def test_gatekeeper_execute_calls_callable() -> None:
    gatekeeper = ApiGatekeeper()

    def api_call(x: int, y: int) -> int:
        return x + y

    assert gatekeeper.execute(api_call, 2, 3) == 5

