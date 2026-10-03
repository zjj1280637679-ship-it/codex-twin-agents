#!/usr/bin/env python3
"""Build a native Codex spawn_agent request for a same-context twin.

This helper does not copy conversation history itself. Codex owns the live
conversation state. The actual copy is performed by the host-native
`spawn_agent(..., fork_turns="all")` primitive.

The helper's job is to make the fork semantics explicit and deterministic:
- choose a twin mode;
- create a small branch-local Fork Handle;
- encode what is inherited, reset, and recomputed;
- emit the exact spawn_agent arguments for Codex to execute.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


SCHEMA = "codex-twin-agents/fork-request@1"


class TwinMode(str, Enum):
    OPEN = "open"
    DIRECTED = "directed"
    VERIFY = "verify"
    CONSOLIDATE = "consolidate"


@dataclass(frozen=True)
class InheritanceMatrix:
    root_goal: bool
    world_conditions: bool
    evidence_history: bool
    user_constraints: bool
    local_strategy: bool
    local_metrics: bool
    completion_pressure: bool


@dataclass(frozen=True)
class ForkHandle:
    fork_id: str
    role: str
    mode: str
    parent_role: str
    execution: str
    return_channel: str
    inheritance: InheritanceMatrix
    divergence_intent: str


MODE_POLICY: dict[TwinMode, tuple[InheritanceMatrix, str]] = {
    TwinMode.OPEN: (
        InheritanceMatrix(
            root_goal=True,
            world_conditions=True,
            evidence_history=True,
            user_constraints=True,
            local_strategy=False,
            local_metrics=False,
            completion_pressure=False,
        ),
        "first_principles_complement",
    ),
    TwinMode.DIRECTED: (
        InheritanceMatrix(
            root_goal=True,
            world_conditions=True,
            evidence_history=True,
            user_constraints=True,
            local_strategy=True,
            local_metrics=True,
            completion_pressure=False,
        ),
        "directed_same_context_execution",
    ),
    TwinMode.VERIFY: (
        InheritanceMatrix(
            root_goal=True,
            world_conditions=True,
            evidence_history=True,
            user_constraints=True,
            local_strategy=True,
            local_metrics=False,
            completion_pressure=False,
        ),
        "independent_verification",
    ),
    TwinMode.CONSOLIDATE: (
        InheritanceMatrix(
            root_goal=True,
            world_conditions=True,
            evidence_history=True,
            user_constraints=True,
            local_strategy=False,
            local_metrics=False,
            completion_pressure=False,
        ),
        "memory_and_knowledge_consolidation",
    ),
}


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


def make_handle(mode: TwinMode, fork_id: str | None = None) -> ForkHandle:
    matrix, intent = MODE_POLICY[mode]
    return ForkHandle(
        fork_id=fork_id or f"twin-{uuid.uuid4().hex[:10]}",
        role="TWIN",
        mode=mode.value.upper(),
        parent_role="MAIN",
        execution="ASYNC",
        return_channel="PARENT_MAILBOX",
        inheritance=matrix,
        divergence_intent=intent,
    )


def inheritance_text(matrix: InheritanceMatrix) -> str:
    inherited = []
    released = []
    for key, value in asdict(matrix).items():
        (inherited if value else released).append(key)
    return (
        "inherit=" + ",".join(inherited) + "\n"
        + "release=" + ",".join(released)
    )


def build_message(
    handle: ForkHandle,
    objective: str | None = None,
) -> str:
    common = f"""[TWIN HANDLE]
fork_id={handle.fork_id}
self_role={handle.role}
parent_role={handle.parent_role}
mode={handle.mode}
execution={handle.execution}
return_channel={handle.return_channel}
divergence_intent={handle.divergence_intent}
{inheritance_text(handle.inheritance)}

The inherited parent history is your own past, not a briefing. The parent
continues in parallel. Do not spend your first turn re-summarizing the shared
history.

Treat inherited facts, evidence, user constraints, and root intent as the
shared starting point. Treat any released local plan, metric, or completion
pressure as historical evidence rather than an obligation.
"""

    if handle.mode == "OPEN":
        mission = """
Mission:
Re-derive what is worth doing from the root goal and the shared evidence.
Look for important work the main branch may not say aloud or may leave
unfinished: closure gaps, unverified claims, false premises, regressions,
documentation/repository drift, knowledge hygiene, or a better success metric.

Do not differ merely for novelty. Preserve reality when evidence supports it.
If the shared conditions themselves look suspect, report the challenged
condition and evidence rather than silently pretending a new world model is
already true.

Complete only already-authorized, low-risk, reversible work. Send consequential
findings to the parent with concise evidence. Otherwise work independently and
finish with a short evidence-first report.
"""
    elif handle.mode == "DIRECTED":
        if not objective:
            raise ValueError("directed mode requires --objective")
        mission = f"""
Mission:
Execute this specific task from the inherited full context without rebuilding
the project from a briefing:

{objective}

Stay focused on that task. Use the shared history to preserve implicit
constraints and prior decisions. Report any discovered premise conflict that
would invalidate the requested task.
"""
    elif handle.mode == "VERIFY":
        target = objective or "the main branch's current claim of correctness/completion"
        mission = f"""
Mission:
Independently verify:

{target}

Do not treat the parent's current success metric as sufficient merely because
it already passed. Check whether the evidence actually proves the root goal.
Prefer direct evidence from files, tests, logs, runtime behavior, and
authoritative documentation. Report contradictions with evidence.
"""
    else:
        target = objective or "the shared work completed since the last meaningful checkpoint"
        mission = f"""
Mission:
Consolidate knowledge from:

{target}

Preserve raw evidence pointers and the history of failed hypotheses. Organize
reusable state, decisions, causes, unresolved uncertainty, and project
knowledge without interrupting or rewriting the main branch's active plan.
Do not delete evidence merely because a summary exists.
"""

    return (common + mission).strip()


def build_request(
    mode: TwinMode,
    task_name: str,
    objective: str | None,
    fork_turns: str,
    fork_id: str | None,
) -> dict[str, Any]:
    handle = make_handle(mode, fork_id=fork_id)
    message = build_message(handle, objective=objective)
    same_context = fork_turns != "none"

    warnings: list[str] = []
    if fork_turns == "none":
        warnings.append(
            "fork_turns='none' does not create a same-context twin; it creates a clean-context child."
        )
    elif fork_turns != "all":
        warnings.append(
            "A bounded fork preserves only recent turns; use 'all' when cognitive fidelity matters."
        )

    return {
        "schema": SCHEMA,
        "host_primitive": "spawn_agent",
        "host_executes_context_copy": True,
        "same_context": same_context,
        "fork_handle": {
            **asdict(handle),
            "inheritance": asdict(handle.inheritance),
        },
        "parent_note": (
            f"Fork {handle.fork_id}: MAIN continues the current task; "
            f"{handle.mode} twin runs asynchronously."
        ),
        "spawn_agent": {
            "task_name": task_name,
            "message": message,
            "fork_turns": fork_turns,
        },
        "warnings": warnings,
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build a Codex same-context twin spawn request."
    )
    p.add_argument(
        "mode",
        choices=[m.value for m in TwinMode],
        help="Twin mode: open, directed, verify, or consolidate.",
    )
    p.add_argument(
        "--task-name",
        default="context-twin",
        help="Native Codex subagent task name.",
    )
    p.add_argument(
        "--objective",
        help="Optional directed objective or verification/consolidation target.",
    )
    p.add_argument(
        "--fork-turns",
        default="all",
        type=validate_fork_turns,
        help="Codex fork_turns value. Default: all.",
    )
    p.add_argument(
        "--fork-id",
        help="Stable fork handle ID. Generated automatically when omitted.",
    )
    p.add_argument(
        "--spawn-args-only",
        action="store_true",
        help="Emit only the arguments to pass to native spawn_agent.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        request = build_request(
            mode=TwinMode(args.mode),
            task_name=args.task_name,
            objective=args.objective,
            fork_turns=args.fork_turns,
            fork_id=args.fork_id,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = request["spawn_agent"] if args.spawn_args_only else request
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
