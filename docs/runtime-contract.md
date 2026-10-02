# Runtime contract

The runtime contract keeps the twin useful without turning it into an uncontrolled second main agent.

## Parent responsibilities

The parent should:

- fork only at meaningful checkpoints;
- propagate full or maximum useful context;
- give the twin an open-ended supervisory mission;
- continue its own work instead of waiting by default;
- read twin findings at natural synchronization points;
- make final decisions when findings would materially change the user's requested direction.

## Twin responsibilities

The twin should:

- assume it already knows the shared history;
- independently inspect the current reality rather than paraphrasing the parent;
- avoid duplicating work that the parent is actively performing;
- prefer evidence from files, tests, logs, repository state, and authoritative docs;
- safely complete already-authorized low-risk cleanup;
- report consequential findings instead of silently rewriting the project's direction;
- remain quiet when there is nothing material to add.

## Mailbox message

Recommended schema:

```json
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
```

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

Do not treat “more twins” as inherently better.
