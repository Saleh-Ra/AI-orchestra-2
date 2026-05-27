from __future__ import annotations

from pathlib import Path

from ai_orchestra.constants import AgentRole
from ai_orchestra.sdk import DebateSDK


def test_sdk_end_to_end_with_fixture_config(setup_test_path: Path) -> None:
    sdk = DebateSDK()
    result = sdk.run_debate(setup_test_path)
    assert result.topic == "Test debate topic."
    assert result.winner in {AgentRole.PRO, AgentRole.CON}
    assert result.final_summary
