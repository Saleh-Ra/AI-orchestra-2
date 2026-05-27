from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.agents.con_agent import create_con_agent
from ai_orchestra.services.transcript import Transcript, create_turn
from ai_orchestra.shared.gatekeeper import ApiGatekeeper
from ai_orchestra.shared.gatekeeper_models import RateLimitConfig
from tests.helpers.recording_llm import RecordingLlmClient

TOPIC = "Social media improves human communication."


def _agent(llm: RecordingLlmClient):
    limits = RateLimitConfig(60, 1000, 5, 0, 2, 50)
    return create_con_agent(
        topic=TOPIC,
        gatekeeper=ApiGatekeeper(limits),
        llm_client=llm,
        temperature=0.8,
    )


def test_con_rebuttal_references_opponent_last_turn() -> None:
    llm = RecordingLlmClient("Con rebuttal.")
    agent = _agent(llm)
    transcript = Transcript(topic=TOPIC)
    transcript.append_turn(
        create_turn(
            round_number=1,
            agent=AgentRole.PRO,
            turn_type=TurnType.OPENING,
            text="Pro claims memes help groups bond.",
        )
    )
    agent.generate_argument(transcript, TurnType.REBUTTAL, round_number=1)
    user_prompt = llm.last_user_content
    assert "REBUTTAL" in user_prompt
    assert "memes help groups bond" in user_prompt
    assert "Opponent" in user_prompt
