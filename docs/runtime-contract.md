# Runtime contract

The runtime contract keeps the twin useful without turning it into an uncontrolled second main agent.

## What the plugin program can and cannot do

The plugin includes:

    skills/open-task-twin/scripts/twin_fork.py

This program builds and validates a Fork Handle plus a native spawn_agent request.

It intentionally does not attempt to serialize or copy the live Codex conversation itself.

Why:

- the live parent context belongs to the Codex host;
- a plugin script does not have a privileged hidden-context handle;
- re-sending chat history from a script would turn a native fork into a lossy handoff;
- current Codex already provides the correct primitive: spawn_agent(..., fork_turns="all").

Therefore the architecture is:

    plugin helper
      -> define fork semantics
      -> emit spawn request
      -> Codex native spawn_agent
      -> host copies parent history

The program is the fork-policy adapter; Codex is the context-copy engine.

## Fork Handle

A Fork Handle distinguishes identity and continuity without rewriting the whole task.

Example:

    fork_id=twin-...
    self_role=TWIN
    parent_role=MAIN
    mode=OPEN
    execution=ASYNC
    return_channel=PARENT_MAILBOX
    divergence_intent=first_principles_complement

The handle also carries an inheritance matrix.

For OPEN mode:

    inherit:
      root_goal
      world_conditions
      evidence_history
      user_constraints

    release:
      local_strategy
      local_metrics
      completion_pressure

This means:

> remember the same past; do not owe loyalty to the same local future.

## Parent responsibilities

The parent should:

- fork only at meaningful checkpoints;
- use fork_turns="all" when full cognitive continuity is the point;
- continue its own work instead of waiting by default;
- avoid duplicating the twin's assigned cognitive role;
- read twin findings at natural synchronization points;
- make final decisions when findings would materially change the user's requested direction.

## Twin responsibilities

The twin should:

- treat inherited history as its own past, not as a briefing;
- avoid wasting the first turn summarizing what both branches already know;
- independently inspect the current reality;
- distinguish root goal, conditions, strategy, and metrics;
- preserve evidence even when releasing the parent's local plan;
- safely complete already-authorized low-risk cleanup;
- report consequential findings rather than silently rewriting the project's direction;
- remain quiet when there is nothing material to add.

## Mailbox message

Recommended schema:

    {
      "severity": "info | warning | critical",
      "kind": "cleanup | verification | premise | regression | knowledge | follow-up",
      "finding": "Concise description",
      "evidence": [
        "file/test/log/commit/doc reference"
      ],
      "action_taken": "Safe action already completed, or null",
      "recommended_next": "Parent action, or null"
    }

This is a communication shape, not a requirement to serialize all twin cognition into JSON.

## Action boundary

### Twin may act directly

When the action is already authorized, low-risk, and reversible, examples include:

- update local documentation to match an implementation already completed;
- run additional tests;
- clean an obviously generated temporary artifact;
- update a project knowledge note;
- prepare a missing changelog entry;
- inspect repository state and repair a harmless local omission.

### Twin should report first

Examples include:

- changing core architecture;
- reverting substantial parent work;
- publishing or deploying where authorization is unclear;
- destructive file or data operations;
- contacting external parties;
- changing security or permission boundaries;
- any action based on a newly discovered premise conflict that changes the task's intended outcome.

## Concurrency rule

Twins that only read can run freely within host limits.

Twins that write to the same mutable workspace must coordinate. Prefer:

1. one writing twin at a time, or
2. isolated branches/worktrees followed by explicit merge.

Do not treat "more twins" as inherently better.

## Failure behavior

If native spawn_agent is unavailable:

- do not claim a twin exists;
- do not silently replace full-context inheritance with a short briefing;
- the parent may fall back to a normal delegate, but it should label that fallback honestly.

If only bounded history propagation is available:

- request the maximum useful history;
- mark the branch as a partial-context fork;
- do not treat it as equivalent to a full-history twin in evaluation.
