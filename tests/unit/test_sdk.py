from ai_orchestra.sdk import DebateSDK


def test_sdk_run_debate_returns_stub_dict() -> None:
    sdk = DebateSDK()
    result = sdk.run_debate()
    assert isinstance(result, dict)
    assert result["status"] == "not_implemented_yet"

