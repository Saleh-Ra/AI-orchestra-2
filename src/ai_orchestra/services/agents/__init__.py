"""Debate agents (Pro, Con, Judge)."""

from ai_orchestra.services.agents.base import DebateAgent
from ai_orchestra.services.agents.con_agent import create_con_agent
from ai_orchestra.services.agents.judge_agent import JudgeAgent
from ai_orchestra.services.agents.pro_agent import create_pro_agent

__all__ = [
    "DebateAgent",
    "JudgeAgent",
    "create_con_agent",
    "create_pro_agent",
]
