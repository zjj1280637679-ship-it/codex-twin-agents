---
name: open-task-twin
description: Fork a same-context Codex twin when a complex task benefits from a second branch that preserves the parent's full accumulated context while independently continuing, verifying, consolidating, or re-deriving strategy and success metrics. Prefer this over briefing-based delegation when implicit history matters.
---

# Open Task Twin

Use this skill to create a cognitive fork, not merely another worker.

The host-native Codex primitive performs the real context copy. This skill supplies the policy, Fork Handle, and workflow around it.

## Core idea

For an open twin, preserve G = root goal and C = shared conditions/evidence, while deliberately releasing S = local strategy and M = local success metric:

    (G, C, S, M) -> (G, C, S', M')

The twin remembers the same past but is not obliged to continue the same local plan.

Read references/theory.md for the compact theory and ../../docs/epistemology.md for the full project treatment.

## Native runtime contract

Current Codex MultiAgentV2 exposes spawn_agent with task_name, message, and fork_turns. Use:

    fork_turns = "all"

for a true same-context twin unless there is an explicit reason to propagate only bounded recent history.

Do not emulate a same-context twin by writing a compressed briefing when native full-history forking is available.

If the host does not expose native subagents or full-history propagation, say so. Do not silently call a clean-context child a twin.

## Fast path

### 1. Decide whether a twin is justified

Use a twin when the task depends strongly on accumulated context, for example:

- a long implementation or debugging thread;
- a task with many implicit user constraints;
- a conclusion that deserves a second full-context pass;
- apparent completion that may hide unfinished commitments;
- retrospective or knowledge consolidation that should not block the main thread.

Use a normal bounded delegate for small, easily described work.

Use a fresh-context observer when the main question is whether the shared world model itself is wrong.

### 2. Build a fork request

Optional deterministic helper:

    python skills/open-task-twin/scripts/twin_fork.py open \
      --task-name open-twin \
      --spawn-args-only

The helper emits the exact argument shape to pass to native spawn_agent.

Available modes:

    open         preserve G/C, release local S/M, find worthwhile complementary work
    directed     preserve full context, perform one explicitly targeted task
    verify       independently test a claim or completion criterion
    consolidate  organize memory/knowledge without derailing the main task

For directed mode:

    python skills/open-task-twin/scripts/twin_fork.py directed \
      --task-name migration-check \
      --objective "Validate the real migration path in production"

The helper does not copy context by itself. Only Codex can access and fork the live parent conversation. It prepares the Fork Handle and native request.

### 3. Spawn with full history

Execute the emitted arguments with native spawn_agent. The critical field is fork_turns="all".

The child's inherited history should be treated as its own past, not as a briefing supplied by somebody else.

### 4. Keep the parent moving

Do not wait by default.

After spawning:

- the main branch continues the current work;
- the twin runs asynchronously;
- do not duplicate the twin's job just because it is still running;
- synchronize only when the twin reports something material or a natural checkpoint is reached.

This separation is intentional: the main branch retains execution pressure; the twin is released from part of that pressure.

### 5. Communicate consequential findings

Use native inter-agent messaging when a finding materially changes what the main branch should do.

A useful message shape is:

    severity: info | warning | critical
    kind: cleanup | verification | premise | regression | knowledge | follow-up
    finding: <what changed our understanding>
    evidence: <files/tests/logs/commits/docs>
    action_taken: <safe action already completed, if any>
    recommended_next: <what the main branch should reconsider>

The twin should not send progress chatter merely to prove it is alive.

## Open-twin semantics

An open twin should act as follows:

> The inherited parent history is your own past. Preserve the user's root intent, evidence, constraints, and the shared working model of reality as the starting point. Do not treat the parent's current local strategy, current KPI, or "almost finished" pressure as obligations. Re-derive what is worth doing from the root goal and the evidence. Look especially for useful work the main branch may not say aloud or may leave unfinished.

This means the twin can:

- finish already-authorized low-risk cleanup;
- detect missing GitHub/repository/documentation closure;
- challenge whether tests prove the original goal;
- surface an unsupported premise;
- find regressions and side effects;
- consolidate knowledge or memory;
- propose a better metric when the current one has become a proxy rather than the goal.

Do not manufacture disagreement. Full context is valuable because it preserves reality; the point is to release action inertia, not to erase evidence.

## Context blindness and reality calibration

Same-context inheritance has a known limitation: the twin can inherit the same conditions model C and therefore the same blind spot.

An open twin mainly provides:

    C stays mostly continuous
    S/M may reboot

If the important question is instead "Are our conditions, categories, causal story, or evidence selection wrong?", use a fresh-context or independently reconstructed reality calibrator. That is a different cognitive freedom axis.

Do not confuse changing strategy with changing the model of reality.

## Action boundary

A twin may act directly when the action is:

- already authorized by the user's parent task;
- low-risk;
- reversible;
- not a silent change to a major design decision;
- not a new external commitment.

Report first when the action would:

- change core architecture;
- revert substantial work;
- deploy/publish/contact externally without clear authorization;
- perform destructive operations;
- change security or permission boundaries;
- materially reinterpret the user's goal.

## Concurrency and workspace writes

Read-only twins can usually run in parallel within host limits.

For mutable repository work, prefer one writer, or isolated branches/worktrees followed by an explicit merge.

A same-context twin is a cognitive branch, not permission to create uncontrolled write races.

## Success condition

The skill succeeds when the fork produces materially better cognitive coverage than a short briefing would have produced.

Do not judge success merely by whether a subagent was spawned.

High-value evidence includes:

- a missed commitment completed;
- a false premise found;
- an acceptance metric corrected;
- a regression discovered;
- reusable project knowledge consolidated;
- a clean result that credibly confirms no material issue remains.
