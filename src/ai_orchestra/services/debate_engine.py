"""Orchestrate a full multi-round debate."""

from __future__ import annotations

import random
from typing import Protocol

from ai_orchestra.constants import AgentRole, TurnType
from ai_orchestra.services.models.debate import DebateResult
from ai_orchestra.services.opener_policy import resolve_opener
from ai_orchestra.services.transcript import Transcript, create_turn
from ai_orchestra.shared.config_models import SetupConfig

REBUTTAL_ROLE = {
    AgentRole.PRO: AgentRole.CON,
    AgentRole.CON: AgentRole.PRO,
}


class DebateEngineError(RuntimeError):
    """Raised when the debate cannot be completed."""


class DebaterAgent(Protocol):
    """Protocol for Pro/Con agents used by the engine."""

    role: AgentRole

    def generate_argument(
        self,
        transcript: Transcript,
        turn_type: TurnType,
        *,
        round_number: int,
    ) -> str: ...


class JudgeScorer(Protocol):
    """Protocol for the judge agent."""

    def score_after_turn(self, transcript: Transcript, latest_turn) -> object: ...


class DebateEngine:
    """Run rounds: open → score → rebuttal → score."""

    def __init__(
        self,
        setup: SetupConfig,
        pro_agent: DebaterAgent,
        con_agent: DebaterAgent,
        judge_agent: JudgeScorer,
        *,
        rng: random.Random | None = None,
    ) -> None:
        self._setup = setup
        self._pro = pro_agent
        self._con = con_agent
        self._judge = judge_agent
        self._rng = rng

    def run(self) -> DebateResult:
        """Execute the full debate and return the final result."""

        transcript = Transcript(topic=self._setup.debate.topic)
        try:
            for round_number in range(1, self._setup.debate.round_count + 1):
                self._run_round(transcript, round_number)
            return self._finalize(transcript)
        except DebateEngineError:
            raise
        except Exception as exc:
            msg = f"Debate aborted after {len(transcript.turns)} turns: {exc}"
            raise DebateEngineError(msg) from exc

    def _run_round(self, transcript: Transcript, round_number: int) -> None:
        opener = resolve_opener(
            self._setup.debate.opener_policy,
            round_number,
            rng=self._rng,
        )
        rebuttal_role = REBUTTAL_ROLE[opener]
        self._play_turn(
            transcript,
            agent_role=opener,
            turn_type=TurnType.OPENING,
            round_number=round_number,
        )
        self._play_turn(
            transcript,
            agent_role=rebuttal_role,
            turn_type=TurnType.REBUTTAL,
            round_number=round_number,
        )

    def _play_turn(
        self,
        transcript: Transcript,
        *,
        agent_role: AgentRole,
        turn_type: TurnType,
        round_number: int,
    ) -> None:
        agent = self._agent_for(agent_role)
        text = agent.generate_argument(
            transcript,
            turn_type,
            round_number=round_number,
        )
        turn = create_turn(
            round_number=round_number,
            agent=agent_role,
            turn_type=turn_type,
            text=text,
        )
        transcript.append_turn(turn)
        snapshot = self._judge.score_after_turn(transcript, turn)
        transcript.append_score(snapshot)

    def _agent_for(self, role: AgentRole) -> DebaterAgent:
        if role == AgentRole.PRO:
            return self._pro
        if role == AgentRole.CON:
            return self._con
        msg = f"Expected PRO or CON, got {role!r}"
        raise ValueError(msg)

    def _finalize(self, transcript: Transcript) -> DebateResult:
        if not transcript.score_history:
            msg = "Debate finished without any judge scores."
            raise DebateEngineError(msg)
        latest = transcript.score_history[-1]
        winner = (
            AgentRole.PRO
            if latest.pro_score >= latest.con_score
            else AgentRole.CON
        )
        return transcript.build_result(
            winner=winner,
            final_summary=latest.rationale,
            final_pro_score=latest.pro_score,
            final_con_score=latest.con_score,
        )
