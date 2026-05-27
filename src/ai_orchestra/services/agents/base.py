"""Base debater agent (Pro / Con)."""

from __future__ import annotations

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.llm_client import LlmClient, Message
from ai_orchestra.services.transcript import Transcript
from ai_orchestra.shared.gatekeeper import ApiGatekeeper

OPPONENT = {
    AgentRole.PRO: AgentRole.CON,
    AgentRole.CON: AgentRole.PRO,
}


class DebateAgent:
    """Generate opening or rebuttal arguments through the API gatekeeper."""

    def __init__(
        self,
        *,
        role: AgentRole,
        topic: str,
        system_prompt: str,
        gatekeeper: ApiGatekeeper,
        llm_client: LlmClient,
        temperature: float,
    ) -> None:
        if role not in {AgentRole.PRO, AgentRole.CON}:
            msg = "DebateAgent role must be PRO or CON."
            raise ValueError(msg)
        self.role = role
        self.topic = topic
        self.system_prompt = system_prompt
        self._gatekeeper = gatekeeper
        self._llm = llm_client
        self._temperature = temperature

    def generate_argument(
        self,
        transcript: Transcript,
        turn_type: TurnType,
        *,
        round_number: int,
    ) -> str:
        """Return one debate argument for the given round and turn type."""

        messages = self._build_messages(transcript, turn_type, round_number)
        text = self._gatekeeper.execute(
            self._llm.chat,
            messages,
            temperature=self._temperature,
        )
        return text.strip()

    def _build_messages(
        self,
        transcript: Transcript,
        turn_type: TurnType,
        round_number: int,
    ) -> list[Message]:
        user_prompt = self._build_user_prompt(transcript, turn_type, round_number)
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _build_user_prompt(
        self,
        transcript: Transcript,
        turn_type: TurnType,
        round_number: int,
    ) -> str:
        history = transcript.format_for_judge()
        if turn_type == TurnType.OPENING:
            return (
                f"Round {round_number} — deliver your OPENING argument.\n\n"
                f"Transcript so far:\n{history}"
            )
        opponent = OPPONENT[self.role]
        last_opponent = _last_turn_for_agent(transcript, opponent)
        opponent_block = (
            f"Opponent's latest argument (Round {last_opponent.round}):\n{last_opponent.text}"
            if last_opponent
            else "No opponent turn found yet."
        )
        return (
            f"Round {round_number} — deliver your REBUTTAL.\n\n"
            f"{opponent_block}\n\n"
            f"Full transcript:\n{history}"
        )


def _last_turn_for_agent(transcript: Transcript, agent: AgentRole):
    for turn in reversed(transcript.turns):
        if turn.agent == agent:
            return turn
    return None
