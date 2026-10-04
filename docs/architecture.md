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

## Design philosophy

The implementation stays deliberately small because the plugin is not trying to build a second agent framework.

Its deeper design position is:

> **A subagent is a governance relationship, not an information hierarchy.**

The host may call an execution branch a child, but that does not imply the child must have less context than the parent.

Keep these dimensions separate:

    authority relation
    information relation
    task relation

For this plugin, the executable path focuses on one case:

    authority: child
    information: equivalent full parent context
    task: chosen by the current user/agent situation

The broader theory allows information relations such as subset, equal, superset, and fused context. Those belong to the theory documents rather than to extra runtime machinery here.

A practical design slogan is:

> **Do not default to making a subagent forget.**

The code is only a convenient button for a native full-context fork. The conceptual value is reminding the agent that "sub" does not mean "less informed."

## Deconstraint, not a replacement framework

The project should not replace one rigid convention with another.

Minimal-context delegates remain useful. Full-context twins are not mandatory. The architectural change is simply that context size is no longer inferred from the word "child."

In other words:

    old habit: child -> less context
    restored design space: child -> context chosen for the task

This is why the executable implementation should stay thin. If a large custom runtime were required merely to create a full-context child, the project would be inventing new infrastructure. Here, Codex already owns the capability; the plugin exposes an underused configuration and the Skill reminds the agent to consider it.

> **The smallness of the code is part of the thesis: the potential was already there.**

## Optional explorations

[Epistemology](epistemology.md), [possible worlds](possible-worlds.md), and the Skill's [theory note](../skills/open-task-twin/references/theory.md) preserve earlier ideas for discussion. They do not define architecture requirements, prescribe a child's mission, or promise additional runtime capabilities.
