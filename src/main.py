"""Thin CLI entry point for AI Orchestra 2 (stub for Phase 1)."""

from ai_orchestra.sdk import DebateSDK


def main() -> None:
    sdk = DebateSDK()
    _ = sdk.run_debate()
    print("AI Orchestra 2 scaffold created. Implement the debate in later phases.")


if __name__ == "__main__":
    main()

