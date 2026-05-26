"""Configuration loader (stub for Phase 1)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Minimal config model for Phase 1."""

    app_name: str = "AI Orchestra 2"


def load_setup_config(config_path: str | Path | None = None) -> AppConfig:
    """Load debate setup config (Phase 1 stub)."""

    _ = config_path
    return AppConfig()

