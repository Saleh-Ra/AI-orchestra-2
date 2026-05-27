"""CLI entry point for AI Orchestra 2."""

from __future__ import annotations

import argparse
import sys

from ai_orchestra.sdk import DebateSDK
from ai_orchestra.services.reporter import print_debate, save_debate_json


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Orchestra 2 — debate demo")
    parser.add_argument(
        "--config-path",
        default=None,
        help="Path to setup*.json, rate_limits*.json, or a directory containing both.",
    )
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save debate result JSON into the results directory.",
    )
    parser.add_argument("--results-dir", default="results", help="Directory for saved results.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sdk = DebateSDK()
    result = sdk.run_debate(args.config_path)

    if args.save_json:
        save_debate_json(result, results_dir=args.results_dir)
    print_debate(result)


if __name__ == "__main__":
    main(sys.argv[1:])

