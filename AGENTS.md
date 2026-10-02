# Repository instructions for Codex

This repository implements **same-context asynchronous open-ended task twins**.

When modifying it:

- Preserve the distinction between a cognitive twin and ordinary delegated subagent.
- Do not replace full-context forking with briefing-based summarization and still call it “same-context.”
- Prefer current official OpenAI Plugin/Codex formats over guessed manifests or old third-party conventions.
- Keep the first implementation small. Use native multi-agent primitives before adding a custom orchestration server.
- Do not add hooks merely for appearance. A hook must have a real supported runtime behavior.
- Treat the twin as open-ended supervision, not a giant hard-coded checklist.
- Keep low-risk autonomous cleanup separate from high-impact decisions that require reporting/approval.
- Do not make “number of twins” the primary quality metric; context fidelity and useful findings matter more.
- When platform behavior is uncertain, document the uncertainty and link to the current official specification.
- Add or update an eval case when changing the behavior contract.

The preferred architecture is:

```text
parent cognition
├─ main branch: continue work
└─ twin branch: asynchronous review / cleanup / verification / consolidation
                       ↓
                 evidence-backed message
                       ↓
                    parent
```
