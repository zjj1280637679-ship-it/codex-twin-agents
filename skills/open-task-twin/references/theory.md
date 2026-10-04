# Theory for the Open Task Twin skill

This skill rests on a simple separation:

```text
G = root goal
C = world conditions / evidence
S = local strategy
M = success metric
```

A normal continuation tends to preserve all four:

```text
(G, C, S, M) -> continue
```

An open same-context twin intentionally preserves the shared past while
releasing the local action frame:

```text
(G, C, S, M) -> (G, C, S', M')
```

The twin therefore remembers why the project is here and what evidence exists,
but does not owe loyalty to the main branch's current plan, KPI, or
"we are almost done" pressure.

This is **teleological reboot**, not amnesia.

## Why full context matters

A briefing can carry explicit facts but often drops:

- why a route was rejected;
- which constraints came from real failures;
- uncertainty that never became a written requirement;
- the difference between a provisional hypothesis and an established fact;
- the user's root intent behind a local request.

For context-sensitive tasks, the accumulated cognition is an asset. Use native
`fork_turns="all"` instead of compressing that asset into a small handoff.

## Why full context is not enough

Same-context twins can inherit the same cognitive blind spots. They are good at
escaping **action inertia** but not guaranteed to escape **world-model inertia**.

If the important question is "are our conditions C themselves wrong?", use a
fresh or independently reconstructed reality-calibration path instead of asking
the open twin to magically forget its own past.

The project therefore separates:

- **same-context twin**: same G/C, freedom to recompute S/M;
- **fresh observer / reality calibrator**: freedom to challenge C;
- **re-foundation**: preserve G and raw evidence while rebuilding C/S/M when
  both forms of inertia appear material.

## Why the parent should keep moving

The main branch's pressure is not merely a defect. Stable execution requires
continuity. The architecture does not force the main branch to become
permanently reflective; it gives reflection another body.

A useful mental model is:

> The main branch is allowed to stay committed because another branch is
> allowed to become uncommitted.

See `docs/epistemology.md` for the full model.

## Design thesis: "sub" is governance, not cognition

This project does not try to invent a new kind of intelligence. It removes a default assumption that narrows how existing intelligence is used:

> **A subagent is a governance position, not a cognitive form.**

The word "sub" describes who created, coordinates, redirects, or stops an agent. It does not imply that the child must know less, receive a shorter briefing, inherit weaker context, or be cognitively subordinate.

Keep three topologies separate:

    Authority topology  -> who can govern whom
    Information topology -> who has which context, memory, evidence, or project history
    Task topology       -> who works on which branch of work

Therefore all of these are valid:

    authority(child) < authority(parent)
    information(child) = information(parent)

or even:

    authority(child) < authority(parent)
    information(child) > information(parent)

Parent/child is a runtime relationship. It is not an epistemic hierarchy.

## Context is a design space

Traditional multi-agent systems often assume:

    C_child < C_parent

because the child receives a compressed briefing. But context relations can be richer:

    MINIMAL     child receives only task-essential context
    PARTIAL     child receives selected or recent parent history
    EQUIVALENT  child receives the same full context as the parent
    SUPERSET    child receives parent context plus extra knowledge
    FUSED       child combines multiple project/context sources

Codex Twin Agents currently focuses on the EQUIVALENT case because Codex already exposes native full-history forking. The wider theory is that context should be composed according to the cognitive job, not minimized merely because an execution branch is called a child.

A practical Skill principle is:

> **When using subagents, also consider creating one with the same complete context as you for difficult division of labor or open-ended assistance.**

Even shorter:

> **A subagent does not have to know less than you.**

## From multi-agent to context topology

The deeper object is not parent_agent / child_agent. It is:

    context_state + execution_branch

Digital context can be copied, cropped, expanded, fused, forked, replayed, compared, and merged. Many apparently new agent abilities emerge when these operations stop being artificially coupled to one human organizational metaphor.

The wider thesis is therefore:

> **Authority is not information. "Sub" describes governance, not cognition. Do not enhance intelligence first; remove the unnecessary constraints that stop it from using the context it can already have.**
