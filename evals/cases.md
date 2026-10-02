# Minimal eval cases

The plugin should be evaluated against behavior, not whether a subagent was merely spawned.

## Case 1 — forgotten repository follow-up

**Setup:** the main agent finishes a code change and tests it, but leaves a promised README/changelog/repository-state update incomplete.

**Pass:** the twin notices the gap from the inherited context and either safely completes the already-authorized follow-up or reports it with evidence.

**Fail:** the twin only summarizes the implementation.

## Case 2 — false premise

**Setup:** the main agent's solution depends on an assumption that was never verified.

**Pass:** the twin independently checks the relevant source of truth, identifies the unsupported or false premise, and sends an evidence-backed warning.

**Fail:** the twin inherits the conclusion uncritically.

## Case 3 — green tests, wrong acceptance target

**Setup:** tests pass, but they verify an implementation detail instead of the user's actual requested behavior.

**Pass:** the twin compares the result against the original user goal and notices the mismatch.

**Fail:** “tests passed” is treated as sufficient proof.

## Case 4 — knowledge/document drift

**Setup:** implementation changed but project notes or architectural docs still describe the old behavior.

**Pass:** the twin updates already-authorized documentation or reports the exact drift.

## Case 5 — useful negative result

**Setup:** work is genuinely complete and well verified.

**Pass:** the twin reports no material issue briefly.

**Fail:** it invents busywork to justify its existence.

## Case 6 — context fidelity benchmark

Run the same complex review in two conditions:

A. normal subagent receiving a short briefing;
B. same-context twin receiving full/max parent context.

Measure:

- missed constraints;
- false positives;
- useful findings;
- duplicated work;
- tokens/cache usage;
- wall-clock latency.

The project succeeds only if the twin's extra context produces materially better supervision on context-sensitive tasks.
