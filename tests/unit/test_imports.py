from ai_orchestra.sdk import DebateSDK


def test_sdk_import() -> None:
    sdk = DebateSDK()
    assert hasattr(sdk, "run_debate")
