---
name: open-task-twin
description: 一次调用 Codex 原生分身工具，默认共享当前完整可用上下文。用于用户想分一个同文分身继续工作、开放探索或执行指定任务时。
---

# Open Task Twin

## Principle

> **When using subagents, also consider creating one with the same complete context as you for difficult division of labor or open-ended assistance.**

A subagent is a governance relationship, not an information hierarchy. Do not assume a child must know less than the parent.

这是原生分身能力的便捷入口。上下文复制、代理运行和通信由宿主完成。

调用当前宿主的原生 `spawn_agent`，例如 `collaboration.spawn_agent`：

- `task_name`：选一个可用的原生任务名，例如 `context_twin`。
- `fork_turns`：默认 `"all"`，继承分叉时宿主能提供的完整上下文。
- `message`：用户指定的分身任务；没有指定时，让分身围绕当前用户目标自行寻找有价值的补充工作。

直接执行原生调用即可，不需要先整理 briefing 或读取理论文档。主代理继续工作，分身通过原生消息或最终报告反馈；是否等待取决于当前任务。

可选的参数生成脚本位于此 Skill 的 `scripts/twin_fork.py`。用宿主可用的 Python 从实际 Skill 路径运行它：

```text
python <skill目录>/scripts/twin_fork.py
python <skill目录>/scripts/twin_fork.py --task-name verification_twin --message "检查刚才的修改是否满足用户原始要求。"
```

脚本输出可直接传给原生 `spawn_agent` 的三个参数；脚本本身不会创建代理。也可以跳过脚本直接调用原生工具。

任务、权限、工具和工作方式沿用用户要求与宿主规则。插件不增加审批、只读模式或额外流程。

若宿主没有原生分身工具，说明当前无法执行；若只支持部分上下文，准确说明实际继承范围。不要用另一条模型对话冒充原生同文分身。
