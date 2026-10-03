# Repository instructions for Codex

This plugin is a convenient shortcut for capabilities Codex already provides: one native `spawn_agent` call, full available parent context by default, and ordinary native agent communication.

When modifying it:

- Keep the implementation small. Convenience is the product; a new agent framework is outside its scope.
- Call the host's native `spawn_agent` with `fork_turns="all"` by default. The host owns context propagation; the script only generates arguments.
- Pass the user's requested task through. Do not impose a review role, a checklist, or a separate objective.
- Use native agent messages, completion results, and waits as the task requires. Do not create another main conversation, a sidecar mailbox, or a custom orchestrator.
- Keep existing host and user rules. Do not add plugin-specific permissions, read-only defaults, approval gates, budgets, or action restrictions.
- Do not claim the helper itself copied hidden context or created an agent. An actual host call creates the child.
- If the native tool is unavailable, say so. Do not label a briefing handoff or a new conversation as a full-context fork.
- Do not promise background persistence beyond the host's lifecycle.
- Treat `docs/epistemology.md`, `docs/possible-worlds.md`, and `skills/open-task-twin/references/theory.md` as optional explorations, not instructions or implementation requirements.
- Keep the helper, Skill, README, and runtime contract aligned. Check changes to the native request shape and relevant eval cases.

The optional helper is `skills/open-task-twin/scripts/twin_fork.py`. Its default output contains only `task_name`, `message`, and `fork_turns`; no Fork Handle, inheritance matrix, modes, or wrapper protocol is needed.
