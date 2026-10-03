#!/usr/bin/env python3
"""Emit native spawn_agent arguments; the host starts the twin and copies context."""

from __future__ import annotations

import argparse
import json
import re
import sys


DEFAULT_MESSAGE = (
    "You are the parent's twin. The parent continues in parallel. "
    "Use the context available to you to pursue useful complementary work "
    "toward the user's current goal. Return useful findings through native "
    "agent messaging or your final report."
)


def validate_task_name(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9_]+", value):
        raise argparse.ArgumentTypeError(
            "task_name must contain only lowercase letters, digits, and underscores"
        )
    return value


def validate_fork_turns(value: str) -> str:
    value = value.strip().lower()
    if value in {"all", "none"}:
        return value
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "fork_turns must be 'all', 'none', or a positive integer"
        ) from exc
    if count <= 0:
        raise argparse.ArgumentTypeError(
            "fork_turns must be 'all', 'none', or a positive integer"
        )
    return str(count)


def build_request(
    task_name: str = "context_twin",
    message: str = DEFAULT_MESSAGE,
    fork_turns: str = "all",
) -> dict[str, str]:
    return {
        "task_name": validate_task_name(task_name),
        "message": message,
        "fork_turns": validate_fork_turns(fork_turns),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task-name", default="context_twin", type=validate_task_name,
        help="Native agent task name (default: context_twin).",
    )
    parser.add_argument(
        "--message", default=DEFAULT_MESSAGE,
        help="Initial message, passed to the native agent unchanged.",
    )
    parser.add_argument(
        "--fork-turns", default="all", type=validate_fork_turns,
        help="Native context option: all, none, or a positive turn count (default: all).",
    )
    args = parser.parse_args(argv)
    request = build_request(args.task_name, args.message, args.fork_turns)
    # ASCII JSON also preserves non-ASCII messages on Windows legacy terminals.
    json.dump(request, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
