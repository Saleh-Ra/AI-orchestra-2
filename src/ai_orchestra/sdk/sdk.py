"""Public SDK for AI Orchestra 2."""

from __future__ import annotations

from pathlib import Path

from ai_orchestra.services.debate_engine import DebateResult
from ai_orchestra.services.debate_factory import create_debate_engine
from ai_orchestra.shared.config import load_app_config
from ai_orchestra.shared.gatekeeper import ApiGatekeeper


class DebateSDK:
    """SDK facade for running a debate.

    This module is the intended public entry point; CLI and other callers
    should use it rather than importing internal services directly.
    """

    def run_debate(self, config_path: str | Path | None = None) -> DebateResult:
        """Run a full debate and return structured results.

        Args:
            config_path:
                - `None`: use default `config/setup.json` + `config/rate_limits.json`
                - path to a `setup*.json` file: infer `rate_limits*.json` by replacing
                  the first `setup` prefix with `rate_limits` (e.g. `setup.test.json`
                  -> `rate_limits.test.json`)
                - directory: use `setup.json` + `rate_limits.json` from that directory
        """

        setup_path, rate_limits_path = _resolve_config_paths(config_path)
        app_config = load_app_config(
            setup_path=setup_path,
            rate_limits_path=rate_limits_path,
        )
        gatekeeper = ApiGatekeeper(app_config.rate_limits.default_service())
        engine = create_debate_engine(app_config, gatekeeper=gatekeeper)
        return engine.run()


def _resolve_config_paths(config_path: str | Path | None) -> tuple[Path | None, Path | None]:
    """Resolve config paths for setup + rate_limits pairing."""

    if config_path is None:
        return None, None

    path = Path(config_path)
    if path.is_dir():
        return path / "setup.json", path / "rate_limits.json"

    if not path.is_file():
        raise FileNotFoundError(str(path))

    name = path.name
    lower = name.lower()
    if lower.startswith("setup") and lower.endswith(".json"):
        rate_name = "rate_limits" + name[len("setup") :]
        rate_path = path.with_name(rate_name)
        return path, rate_path

    if lower.startswith("rate_limits") and lower.endswith(".json"):
        setup_name = "setup" + name[len("rate_limits") :]
        setup_path = path.with_name(setup_name)
        return setup_path, path

    msg = (
        "config_path must be None, a directory, or a JSON file named like "
        "'setup*.json' (or 'rate_limits*.json')."
    )
    raise ValueError(msg)


__all__ = ["DebateSDK"]

