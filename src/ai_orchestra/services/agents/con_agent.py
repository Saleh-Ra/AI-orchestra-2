"""Con (opposing) debater agent."""

from __future__ import annotations

from ai_orchestra.constants import AgentRole
from ai_orchestra.services.agents.base import DebateAgent
from ai_orchestra.services.llm_client import LlmClient
from ai_orchestra.services.prompts.loader import load_prompt
from ai_orchestra.shared.gatekeeper import ApiGatekeeper


def create_con_agent(
    *,
    topic: str,
    gatekeeper: ApiGatekeeper,
    llm_client: LlmClient,
    temperature: float,
) -> DebateAgent:
    """Build a Con debater for the given topic."""

    return DebateAgent(
        role=AgentRole.CON,
        topic=topic,
        system_prompt=load_prompt("con", topic=topic),
        gatekeeper=gatekeeper,
        llm_client=llm_client,
        temperature=temperature,
    )
