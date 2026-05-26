from ai_orchestra.services.llm_client import build_llm_client
from ai_orchestra.shared.gatekeeper import ApiGatekeeper
from ai_orchestra.shared.gatekeeper_models import RateLimitConfig


def test_gatekeeper_wraps_mock_llm_client() -> None:
    client = build_llm_client(
        model="gpt-4o-mini",
        mock=True,
        mock_response="debate argument text",
    )
    gatekeeper = ApiGatekeeper(
        RateLimitConfig(60, 1000, 5, 0, 2, 50),
    )
    result = gatekeeper.execute(
        client.chat,
        [{"role": "user", "content": "Argue pro."}],
        temperature=0.7,
    )
    assert result == "debate argument text"
