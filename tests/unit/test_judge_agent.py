from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.agents.judge_agent import JudgeAgent
from ai_orchestra.services.transcript import Transcript, create_turn
from ai_orchestra.shared.gatekeeper import ApiGatekeeper
from ai_orchestra.shared.gatekeeper_models import RateLimitConfig
from tests.helpers.recording_llm import RecordingLlmClient

TOPIC = "Social media improves human communication."
JUDGE_JSON = (
    '{"pro_score": 62, "con_score": 38, "rationale": "Pro argument is more cohesive."}'
)


def test_judge_agent_returns_valid_snapshot() -> None:
    llm = RecordingLlmClient(JUDGE_JSON)
    limits = RateLimitConfig(60, 1000, 5, 0, 2, 50)
    judge = JudgeAgent(
        topic=TOPIC,
        gatekeeper=ApiGatekeeper(limits),
        llm_client=llm,
        temperature=0.2,
    )
    transcript = Transcript(topic=TOPIC)
    turn = create_turn(
        round_number=1,
        agent=AgentRole.PRO,
        turn_type=TurnType.OPENING,
        text="Social media connects distant families instantly.",
        turn_id="turn-judge-1",
    )
    transcript.append_turn(turn)
    snapshot = judge.score_after_turn(transcript, turn)
    assert snapshot.pro_score == 62
    assert snapshot.con_score == 38
    assert snapshot.after_turn_id == "turn-judge-1"
    assert TOPIC in llm.last_user_content
