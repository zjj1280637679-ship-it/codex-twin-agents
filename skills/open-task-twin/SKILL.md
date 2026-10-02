---
name: open-task-twin
description: Use when substantial Codex work would benefit from a same-context asynchronous twin that independently checks unfinished, unverified, inconsistent, or improvable work without interrupting the main thread. Prefer this over briefing-based delegation when the task depends heavily on the parent's accumulated context.
---

# Open Task Twin

Treat the twin as a cognitive fork, not as a specialist receiving a handoff.

## When to fork

Fork a twin at a natural checkpoint when at least one is true:

- a complex implementation or debugging task has reached an apparent completion point;
- the work depends on many implicit constraints accumulated through the conversation;
- a second full-context pass could catch missed cleanup, documentation, repository, or delivery steps;
- a premise, acceptance criterion, or root-cause claim deserves independent verification;
- the project knowledge base or memory should be consolidated without interrupting the main task;
- an alternative cognitive path may reveal an issue that a narrow delegated subtask would miss.

Do not fork for tiny, easily described tasks where a normal bounded subagent is cheaper and equally faithful.

## How to fork

1. Use the host's native multi-agent/subagent mechanism.
2. Propagate the full or maximum available parent context. If the host exposes a context propagation parameter, request all parent turns; in Responses multi-agent this is `fork_turns: "all"`.
3. Give the twin a short open-ended mission rather than a long re-description of the parent context. The twin already inherits the context.
4. Do not wait by default. Continue the main task while the twin works.
5. Avoid spawning multiple twins that would write concurrently to the same mutable files unless the work is explicitly coordinated.

A suitable initial mission is:

> You are an asynchronous same-context twin. You already share the parent's history. Independently inspect the current work for unfinished commitments, missing verification, false premises, documentation or repository drift, knowledge-base cleanup, regressions, and other worthwhile follow-up the parent may have missed. Complete only already-authorized low-risk reversible work. For higher-impact findings, send the parent a concise evidence-backed message instead of silently changing the main decision.

## Twin priorities

The twin should inspect the whole situation, not mechanically run a fixed checklist. Common high-value directions include:

- closure: promised but unfinished work, dirty worktree, unsynced docs or repository state;
- verification: whether tests and evidence actually prove the user's original acceptance goal;
- premise audit: assumptions that were used but never established;
- regression and side effects: nearby behavior that may have been broken;
- knowledge hygiene: stale docs, conflicting project notes, missing rationale, useful evidence pointers;
- retrospective: failed hypotheses, turning points, reusable lessons, and unresolved uncertainty;
- delivery quality: whether the artifact, commit, issue, release note, or handoff is actually complete.

## Action policy

The twin may directly complete work only when all of these hold:

- the action is already within the user's authorization for the parent task;
- it is low-risk and reasonably reversible;
- it does not silently change a major design decision;
- it does not create a new external commitment that the user did not authorize.

Otherwise, report the finding to the parent with evidence and a recommended next action.

## Reporting

Use native inter-agent messaging for urgent findings while the parent is still active. A final report should be short and evidence-first.

Prefer this shape:

```text
severity: info | warning | critical
kind: cleanup | verification | premise | regression | knowledge | follow-up
finding: <what was discovered>
evidence: <files/tests/logs/commits/docs>
action_taken: <what the twin safely completed, if anything>
recommended_next: <what the parent should do next, if anything>
```

If nothing material is found, say so briefly. Do not manufacture work just to justify the twin.
