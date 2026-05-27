from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_runs_with_fixture_config(setup_test_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    proc = subprocess.run(
        [
            sys.executable,
            "src/main.py",
            "--config-path",
            str(setup_test_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0
    assert "Debate topic:" in proc.stdout
    assert "Round 1" in proc.stdout
    assert "Final Winner:" in proc.stdout
    assert proc.stderr == ""
