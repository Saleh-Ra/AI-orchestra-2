"""Factory helpers to build a configured debate engine."""

from __future__ import annotations

import random

from ai_orchestra.services.agents.con_agent import create_con_agent
from ai_orchestra.services.agents.judge_agent import JudgeAgent
from ai_orchestra.services.agents.pro_agent import create_pro_agent
from ai_orchestra.services.debate_engine import DebateEngine, DebateResult
from ai_orchestra.services.llm_client import build_llm_client
from ai_orchestra.shared.config import AppConfig, load_app_config
from ai_orchestra.shared.gatekeeper import ApiGatekeeper

DEFAULT_JUDGE_MOCK_JSON = (
    '{"pro_score": 55, "con_score": 45, "rationale": "Mock judge evaluation."}'
)


def create_debate_engine(
    app_config: AppConfig,
    *,
    gatekeeper: ApiGatekeeper | None = None,
    rng: random.Random | None = None,
) -> DebateEngine:
    """Wire Pro, Con, and Judge agents from application configuration."""

    setup = app_config.setup
    gatekeeper = gatekeeper or ApiGatekeeper.from_config_file()
    mock = setup.mock_llm
    topic = setup.debate.topic
    model = setup.llm.model
    pro_llm = build_llm_client(model=model, mock=mock, mock_response="Pro debater mock argument.")
    con_llm = build_llm_client(model=model, mock=mock, mock_response="Con debater mock argument.")
    judge_llm = build_llm_client(model=model, mock=mock, mock_response=DEFAULT_JUDGE_MOCK_JSON)
    return DebateEngine(
        setup,
        create_pro_agent(
            topic=topic,
            gatekeeper=gatekeeper,
            llm_client=pro_llm,
            temperature=setup.llm.temperature.pro,
        ),
        create_con_agent(
            topic=topic,
            gatekeeper=gatekeeper,
            llm_client=con_llm,
            temperature=setup.llm.temperature.con,
        ),
        JudgeAgent(
            topic=topic,
            gatekeeper=gatekeeper,
            llm_client=judge_llm,
            temperature=setup.llm.temperature.judge,
        ),
        rng=rng,
    )


def run_debate_from_config(
    setup_path: str | None = None,
    *,
    rng: random.Random | None = None,
) -> DebateResult:
    """Load config and run one full debate."""

    app_config = load_app_config(setup_path)
    return create_debate_engine(app_config, rng=rng).run()
