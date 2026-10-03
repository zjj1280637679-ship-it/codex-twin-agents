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
