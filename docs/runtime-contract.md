# Runtime contract

The plugin is a shortcut to the host's native `spawn_agent`. The user supplies the purpose; the host supplies agents, context propagation, communication, tools, and lifecycle.

## Invocation

`$codex-twin-agents:open-task-twin` creates one native child with `fork_turns="all"` by default. A natural-language request can invoke the same Skill. The child receives the user's requested task in `message`; the Skill does not replace it with a mandatory review mission.

The optional parameter helper outputs a plain native request:

```json
{
  "task_name": "context_twin",
  "message": "<the requested task>",
  "fork_turns": "all"
}
```

It does not call `spawn_agent`, copy context, or produce an agent handle. The parent passes the generated arguments to its native tool. Directly constructing the same arguments is also valid.

`--task-name`, `--message`, and `--fork-turns all|none|N` override the defaults. `none` requests no inherited turns and a number requests bounded history; neither should be described as full-context inheritance. Any additional options exposed by the host remain ordinary native capabilities, without a plugin-defined protocol.

## Context and communication

The host propagates the context it makes available for the selected `fork_turns` value. This is the context at the fork; subsequent parent turns are not promised to synchronize automatically. New information can be shared through native messages as needed.

The parent uses the host's ordinary agent messaging, completion results, and wait mechanisms. Whether to continue concurrently or wait depends on the current task. There is no custom mailbox schema, result format, or mandatory synchronization checkpoint.

User instructions and native host rules continue to apply normally. This plugin adds no read-only default, permission layer, approval gate, fixed budget, or restrictions on the child's authorized work.

## Availability and lifecycle

Only a successful native call establishes that a child exists. If `spawn_agent` is unavailable or fails, report that outcome using the ordinary host behavior. A newly created main conversation or a short briefing handoff is not a full-context fork.

Agent concurrency and lifetime belong to the host. The plugin does not provide a persistent worker or guarantee that a child continues after the parent turn or session ends.

Theory documents in this repository are optional explorations. They do not add runtime obligations to this contract.
