from ai_orchestra.constants import TurnType
from ai_orchestra.services.agents.pro_agent import create_pro_agent
from ai_orchestra.services.transcript import Transcript
from ai_orchestra.shared.gatekeeper import ApiGatekeeper
from ai_orchestra.shared.gatekeeper_models import RateLimitConfig
from tests.helpers.recording_llm import RecordingLlmClient

TOPIC = "Social media improves human communication."


def _agent(llm: RecordingLlmClient):
    limits = RateLimitConfig(60, 1000, 5, 0, 2, 50)
    return create_pro_agent(
        topic=TOPIC,
        gatekeeper=ApiGatekeeper(limits),
        llm_client=llm,
        temperature=0.8,
    )


def test_pro_opening_prompt_contains_topic() -> None:
    llm = RecordingLlmClient("Pro opening argument.")
    agent = _agent(llm)
    transcript = Transcript(topic=TOPIC)
    text = agent.generate_argument(transcript, TurnType.OPENING, round_number=1)
    assert text == "Pro opening argument."
    combined = " ".join(message["content"] for message in llm.last_messages)
    assert TOPIC in combined
    assert "OPENING" in llm.last_user_content


def test_pro_system_prompt_defends_topic() -> None:
    llm = RecordingLlmClient()
    agent = _agent(llm)
    assert "PRO" in agent.system_prompt
    assert TOPIC in agent.system_prompt
