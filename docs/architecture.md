# Architecture

## Definition

A **same-context asynchronous open-ended task twin** is a subagent forked from the parent's current cognitive context, allowed to continue asynchronously with an open-ended supervisory mission.

It is not primarily a division-of-labor pattern.

```text
Delegate:
task -> briefing -> new agent -> result

Twin:
current cognition C(t)
        ├─ main future
        └─ twin future
```

The point is to preserve the parent's accumulated model of reality: constraints, discarded hypotheses, evidence, user intent, tool history, and unresolved uncertainty.

## Three layers

### 1. Main thread

Optimized for forward progress:

- understand the current user goal;
- act on files, tools, code, and external systems;
- keep conversational latency reasonable;
- avoid memory and housekeeping work that would derail the task.

### 2. Twin layer

Optimized for second-order cognition:

- open-ended review;
- closure checking;
- premise verification;
- regression search;
- retrospective analysis;
- documentation and knowledge hygiene;
- already-authorized low-risk cleanup.

The twin is useful precisely because it starts from the same context instead of reconstructing the project from a briefing.

### 3. External state

Long-lived state belongs outside the main conversation:

- repository and files;
- project knowledge base;
- vector/semantic memory;
- evidence pointers;
- mailbox / findings log;
- test artifacts and recordings.

The twin may improve these stores without injecting all housekeeping back into the main context.

## Read path vs write path

Keep retrieval and consolidation conceptually separate.

```text
READ PATH
knowledge/memory -> retrieve -> main cognition

WRITE PATH
main snapshot -> twin -> consolidate/index/verify -> external store
```

Retrieval can be part of active reasoning. Consolidation should usually be asynchronous.

## Context fidelity

For complex tasks, context fidelity is treated as a first-class resource.

A normal subagent is preferred when the task is cheap to describe and independent. A twin is preferred when compressing the context into a briefing would remove implicit constraints or the reasoning history required to judge the work correctly.

The design goal is not “maximum number of agents.” It is “minimum loss of reality understanding per useful parallel branch.”

## Fork and merge

The natural lifecycle is:

```text
fork -> explore -> verify -> report/merge -> consolidate
```

A merge is not majority voting. Conflicting twins should return evidence and uncertainty so the parent can update its state rather than blindly choose the most common answer.

## Future extension: memory-native backend

A vector knowledge-base tool is a natural companion:

- twins can index episodes, state changes, failed hypotheses, and evidence pointers;
- the main agent can retrieve only the relevant historical slice;
- raw evidence remains the source of truth;
- future Text-Vector Omni models can replace language serialization with native retrieval/memory representations without changing the high-level twin architecture.
