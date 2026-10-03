# Minimal eval cases

Evaluate whether the shortcut preserves native behavior and reduces handoff work. These are maintainer acceptance scenarios, not instructions that every child must execute.

## Case 1 — one invocation, one native child

**Setup:** in a host exposing `spawn_agent`, invoke `$codex-twin-agents:open-task-twin` once.

**Pass:** the Skill makes one successful native call with `fork_turns="all"` and reports the real child result or identifier returned by the host.

**Fail:** it only generates JSON, adds a plugin-specific confirmation, opens another main conversation, or creates a custom orchestration service.

## Case 2 — an inherited constraint is usable

**Setup:** establish a distinctive constraint earlier in the parent conversation, such as “use the label 青竹 for the sample.” Later ask the child to produce the sample without repeating that constraint in its task message.

**Pass:** inspect the native call's `fork_turns="all"` and confirm the child uses 青竹 from inherited context.

**Fail:** the shortcut substitutes a briefing or claims complete context merely because the request arguments exist.

## Case 3 — the user's purpose passes through

**Setup:** ask “分一个继承当前上下文的分身，帮我继续写刚才的例子。”

**Pass:** the child is asked to continue the example using available context and existing user instructions.

**Fail:** the plugin replaces that task with a fixed audit checklist or adds read-only, approval, budget, or other plugin-specific restrictions.

## Case 4 — ordinary native communication

**Setup:** after creating the child, share a useful update with a native message and receive its result through the host's usual mechanism.

**Pass:** ordinary native messaging and completion work; the parent waits or continues according to the task.

**Fail:** the plugin requires its own mailbox schema, separate dialogue, persistent worker, or new coordination protocol.

## Case 5 — explicit partial context

**Setup:** generate a request with `--fork-turns none` or a positive turn count.

**Pass:** the native request retains the chosen value; its message does not falsely claim full inherited history.

**Fail:** partial or absent inheritance is labeled as a full-context child.

## Case 6 — unavailable native tool

**Setup:** invoke the Skill in a host without `spawn_agent`, or simulate a failed native call.

**Pass:** it explains that the requested native child was not created.

**Fail:** it silently launches another main conversation or a briefing-based delegate and presents that fallback as a full-context fork.

The helper's unit tests can validate request shape. Cases involving actual context inheritance, communication, or child creation require a live host; generated arguments alone do not verify those behaviors.
