from __future__ import annotations

from pathlib import Path


def test_src_python_files_are_within_line_limit() -> None:
    src_dir = Path(__file__).resolve().parents[2] / "src"
    py_files = list(src_dir.rglob("*.py"))

    offenders: list[str] = []
    for path in py_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 150:
            offenders.append(f"{path.relative_to(Path.cwd())}: {len(lines)} lines")

    assert offenders == [], "Files exceed 150 lines:\n" + "\n".join(offenders)
