"""Command-line entry point; task execution will be added in Phase 1."""

import argparse
from collections.abc import Sequence

from repopilot import __version__


def main(argv: Sequence[str] | None = None) -> int:
    """Show available commands without requiring credentials or Docker."""
    parser = argparse.ArgumentParser(
        prog="repopilot",
        description="RepoPilot - repository-aware coding agent (Phase 0 scaffold).",
        epilog="Task execution is not implemented yet. See docs/roadmap.md for next steps.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    parser.print_help()
    return 0
