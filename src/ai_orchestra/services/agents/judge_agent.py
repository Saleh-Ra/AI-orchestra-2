"""Judge agent — scores the debate after each turn."""

from __future__ import annotations

from ai_orchestra.services.agents.judge_parser import parse_judge_response
from ai_orchestra.services.llm_client import LlmClient, Message
from ai_orchestra.services.models.scores import ScoreSnapshot
from ai_orchestra.services.models.turn import Turn
from ai_orchestra.services.prompts.loader import load_prompt
from ai_orchestra.services.transcript import Transcript
from ai_orchestra.shared.gatekeeper import ApiGatekeeper


class JudgeAgent:
    """Evaluate persuasion and return structured scores."""

    def __init__(
        self,
        *,
        topic: str,
        gatekeeper: ApiGatekeeper,
        llm_client: LlmClient,
        temperature: float,
    ) -> None:
        self.topic = topic
        self.system_prompt = load_prompt("judge", topic=topic)
        self._gatekeeper = gatekeeper
        self._llm = llm_client
        self._temperature = temperature

    def score_after_turn(
        self,
        transcript: Transcript,
        latest_turn: Turn,
    ) -> ScoreSnapshot:
        """Score the debate after the latest agent turn."""

        messages = self._build_messages(transcript, latest_turn)
        raw = self._gatekeeper.execute(
            self._llm.chat,
            messages,
            temperature=self._temperature,
        )
        fallback = transcript.score_history[-1] if transcript.score_history else None
        return parse_judge_response(
            raw,
            after_turn_id=latest_turn.id,
            fallback=fallback,
        )

    def _build_messages(self, transcript: Transcript, latest_turn: Turn) -> list[Message]:
        user_content = (
            f"Latest turn (score after this turn):\n"
            f"Round {latest_turn.round} | {latest_turn.agent.value} | "
            f"{latest_turn.turn_type.value}\n"
            f"{latest_turn.text}\n\n"
            f"Full transcript:\n{transcript.format_for_judge()}"
        )
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]
