# Platform notes — 2026-10

This file records what the current OpenAI platform actually supports so the project does not build around outdated or invented Codex plugin formats.

## Plugin package format

OpenAI's current recommended portable format uses a root `plugin.json` following the Agent Plugins schema.

A Codex compatibility package may also contain:

```text
.codex-plugin/plugin.json
```

Skills live under:

```text
skills/<skill-name>/SKILL.md
```

For portable packages, skills are discovered from the root `skills/` directory. A Codex compatibility manifest may declare `"skills": "./skills/"`.

This repository intentionally ships both the portable root manifest and the Codex compatibility manifest.

Official references:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/concepts/plugins

## Multi-agent context propagation

OpenAI Responses multi-agent exposes a native `spawn_agent` collaboration action. The root agent can choose how much context to propagate through the `fork_turns` parameter.

That is the closest current official primitive to this project's “same-context twin.”

Official reference:

- https://developers.openai.com/api/docs/guides/responses-multi-agent

Agents API multi-agent also provides managed subagents that share the configured environment and tools.

- https://developers.openai.com/api/docs/guides/agents-api/multi-agent

## Why v0.1 is not hook-driven

Codex lifecycle hooks are real and can be bundled with plugins. Command hooks can run with `"async": true`.

However, current documented behavior matters:

1. background hooks do not start a new model turn when they finish;
2. background output is delivered only at the next safe point / next user turn;
3. hook handlers of type `agent` are currently parsed but skipped;
4. public plugin ZIPs containing lifecycle hooks are currently not accepted for submission.

Therefore a hook cannot honestly be presented today as “automatically fork the current Codex cognition into a native asynchronous subagent.”

For v0.1, the correct implementation is Skill-first: let the active Codex agent invoke the native multi-agent primitive and request maximal context propagation.

Hooks can be reconsidered when the runtime exposes a stable native subagent-start action from hooks, or when a local-only plugin deliberately uses an external orchestration service.

Official references:

- https://learn.chatgpt.com/docs/hooks
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission

## Cost model

The repository does not assume that “N twins = N complete context bills.” Shared-prefix caching and platform implementation details can change the effective cost.

The invariant this project cares about is architectural:

> When the task is context-sensitive, preserve context first; optimize shared-prefix execution second.

Any benchmark should measure actual input/cache/output usage rather than assume a fixed multiplier.

## Known current limitation

The exact availability and behavior of `fork_turns` depends on the host/runtime. Skills must degrade gracefully:

- if full context forking is supported, use it;
- if only bounded propagation is supported, request the maximum useful parent context;
- if native subagents are unavailable, do not fake a “same-context twin” by silently replacing it with a small briefing. Report the limitation.
