# Architecture

Codex Twin Agents wraps an existing native capability in a convenient Skill.

```text
User invokes $codex-twin-agents:open-task-twin or asks for a context-sharing child
    -> Skill supplies native spawn_agent arguments
    -> host creates child with fork_turns="all" by default
    -> parent and child collaborate through native agent channels
```

The Skill is the entry point. `scripts/twin_fork.py` is an optional JSON argument generator. It carries only `task_name`, `message`, and `fork_turns`; the user's requested work is the child's task.

The host remains responsible for copying its available parent context, exposing tools, delivering messages and results, scheduling agents, and ending their execution. The plugin needs no conversation serialization, Fork Handle, inheritance matrix, custom mailbox, secondary dialogue, or orchestration server.

The current fork shares the history available at creation time. Later changes can be communicated with the native messaging tools. Workspace coordination follows normal host behavior and user instructions.

The default is a full-context request. Explicit `none` or bounded history values remain native options and are described accurately. A host without `spawn_agent` cannot create a native child through this Skill.

The success criterion is simple: a user can request a native child once, with their task and current context, without extra handoff work or new plugin restrictions.

## Optional explorations

[Epistemology](epistemology.md), [possible worlds](possible-worlds.md), and the Skill's [theory note](../skills/open-task-twin/references/theory.md) preserve earlier ideas for discussion. They do not define architecture requirements, prescribe a child's mission, or promise additional runtime capabilities.
