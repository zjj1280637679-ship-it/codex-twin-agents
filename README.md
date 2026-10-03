# Codex Twin Agents

> **同文异步开放性任务孪生**（Same-Context Asynchronous Open-Ended Task Twin）的 Codex 插件原型。

它不是“把一份 briefing 交给另一个子代理”的普通分工，而是让 Codex 在复杂工作的自然检查点，把**当前完整认知上下文分叉给一个异步孪生体**：主线程继续工作；孪生体在同一现实模型上做开放式收尾、复盘、验证、前提审查、知识库整理和遗漏修复。

## 核心原则

- **同文**：优先继承完整上下文，而不是先摘要再交接。
- **异步**：主线程不因后台复盘而停住。
- **开放性**：孪生体主动发现“还有什么没做完、没验证、可能错了或值得整理”，而不是只执行一条封闭 checklist。
- **分身而非分工**：普通子代理复制任务；孪生代理复制认知现场。
- **低风险自修，高影响上报**：已经授权、可逆、低风险的收尾可以自行完成；会改变主决策、产生新的外部副作用或需要额外授权的事项，应附证据写信给主线程。
- **不为省一点上下文牺牲现实理解**：复杂任务优先保真，成本优化交给缓存和运行时。

## 为什么现在可以做

OpenAI 当前的原生 multi-agent 已经提供了关键底座：根代理可以创建子代理，并决定传播多少父上下文；Responses multi-agent 文档明确暴露 `fork_turns`。Codex/Agent Plugins 也已经有正式的 Plugin + Skill 打包规范。

这意味着第一版不需要发明一个新的代理框架，只需要把“**什么时候值得 fork、孪生体该以什么目标运行、结果如何回到主线程**”固化成可复用 Skill。

## 当前实现路线：Skill-first

v0.1 **故意不伪造一个自动 hook fork**。

Codex hooks 当前支持后台 command hook，但后台 hook 完成后不会主动开启新 turn；而 hook 的 `agent` handler 目前仍是“可解析但跳过执行”。因此，第一阶段采用最小而规范的实现：

1. 主代理在自然检查点识别出“这个任务值得保留完整现实理解再做一次开放审查”。
2. 调用原生 multi-agent 创建孪生体。
3. 在宿主支持时传播完整/最大可用上下文（Responses multi-agent 中对应 `fork_turns: "all"`）。
4. 主线程继续，不默认等待。
5. 孪生体独立执行收尾、验证、复盘、知识整理和前提审查。
6. 低风险已授权事项可直接补完；高影响发现通过 agent message / final report 回到父代理。

等 Codex runtime 提供“hook 原生启动同文 subagent”的稳定能力后，再把触发从 Skill 驱动升级为真正后台自动化。

## 目录

```text
codex-twin-agents/
├── plugin.json                         # 推荐的 Agent Plugins 可移植清单
├── .codex-plugin/
│   └── plugin.json                     # Codex 兼容清单
├── skills/
│   └── open-task-twin/
│       ├── SKILL.md                    # 核心孪生工作流与理论立意
│       ├── scripts/twin_fork.py        # Fork Handle + spawn_agent 请求生成器
│       └── references/theory.md        # Skill 内部理论摘要
├── docs/
│   ├── architecture.md                 # 架构与边界
│   ├── epistemology.md                  # 目标-条件-策略-指标与认知自由度
│   ├── platform-notes.md               # 当前官方能力与实现取舍
│   └── runtime-contract.md             # 孪生体与主线程通信约定
├── evals/
│   └── cases.md                        # 最小验收场景
├── tests/
│   └── test_twin_fork.py               # Fork 请求生成器单元测试
├── AGENTS.md                           # 维护本仓库时给 Codex 的约束
├── LICENSE
└── .gitignore
```

## v0.2：插件现在真正包含什么

插件现在明确分成两个核心部件：

1. **程序层**：skills/open-task-twin/scripts/twin_fork.py 负责构造认知分身句柄、继承矩阵和原生 spawn_agent 参数。真正的上下文复制仍由 Codex 自己执行，关键参数是 fork_turns: "all"。
2. **技能层**：skills/open-task-twin/SKILL.md 负责告诉 Codex 什么时候应该分身、怎样区分普通委派与同文孪生、怎样异步继续、怎样汇报，以及“保留 G/C、重推 S/M”的理论立意。

这个边界是刻意的：**插件不重新序列化主对话；插件只定义如何 fork，Codex runtime 负责复制它真正拥有的上下文。**

## 最小工作流

```text
主线程当前认知状态 C(t)
        │
        ├────────────────→ 主线程继续工作
        │
        └─ fork same context
                ↓
          异步开放孪生
                ↓
   收尾 / 复盘 / 验证 / 查前提 / 整理知识库
                ↓
       ┌────────┴────────┐
       ↓                 ↓
低风险已授权事项       高影响发现
直接完成               写信给主线程
```

## 认识论：什么应该继承，什么应该重推

同文孪生并不是“把一切原样继承”。更精确的模型是四元组：

```text
G = 目标
C = 条件
S = 策略
M = 指标
```

开放孪生的核心变换是：

```text
(G, C, S, M) → (G, C, S', M')
```

即 **保留根目标与现实条件，但解除局部策略、指标和完成压力，从第一性目标重新推导。** 同时，项目也区分“摆脱行动惯性”和“摆脱认知惯性”：同文开放孪生主要负责前者，独立现实校准器负责后者。

完整理论见 [docs/epistemology.md](docs/epistemology.md)。

## 可能世界：这个框架最终能带来什么

工程结构只是手段。这个项目真正想验证的是：**当“完整认知现场”本身变成可复制资源以后，长期 Agent 会出现哪些今天难以获得的能力。**

完整叙事见 [docs/possible-worlds.md](docs/possible-worlds.md)，包括：任务闭环、异步自我纠错、夜间记忆巩固、项目守夜人、多未来认知分叉、知识库自动维护，以及最终的原生认知 fork/merge 运行时。

最短版本：

> 不要让一个已经理解现实的 Agent，为了做第二件复杂事情先失忆再交接。复制它，让另一个自己继续活下去。

## 典型场景

- 主线程功能已经做完，但忘了同步 GitHub、README、issue、版本说明或项目状态。
- 测试全绿，但孪生体发现测试并没有真正覆盖用户原始验收目标。
- 主线程一直依赖某个未验证前提；孪生体异步回查代码、日志或文档后发现前提不成立。
- 工作结束后，孪生体整理知识库、建立复盘记录、补证据链接，但不把“记忆杂务”塞回主线程。
- 一个复杂 Debug 结束后，保留“错误假设 → 证据 → 假设降权 → 真根因”的认知轨迹，而不仅是最终摘要。
- 主线程已经转入下一件事，孪生体继续检查是否存在漏提交流程、脏工作树、文档漂移或未闭环承诺。

## 普通子代理 vs 同文孪生

| | 普通子代理 | 同文孪生 |
|---|---|---|
| 初始输入 | briefing / 有限上下文 | 父代理完整或最大可用上下文 |
| 目标 | 明确分工 | 开放观察与第二条认知分支 |
| 交接损耗 | 较高 | 尽量低 |
| 适合 | 搜索、跑测试、独立模块 | 复杂复盘、验收、根因审查、收尾 |
| 默认是否等待 | 视任务而定 | 不等待，异步运行 |

## 官方规范依据

- Agent Plugins packaging: https://developers.openai.com/plugins/build/plugins
- Skills: https://developers.openai.com/plugins/build/skills
- Plugin architecture: https://developers.openai.com/plugins/concepts/plugins
- Responses multi-agent: https://developers.openai.com/api/docs/guides/responses-multi-agent
- Agents API multi-agent: https://developers.openai.com/api/docs/guides/agents-api/multi-agent
- Codex hooks: https://learn.chatgpt.com/docs/hooks

## 状态

**v0.2.0 — first executable fork helper + skill runtime**

第一阶段只验证一个核心命题：

> 在复杂 Codex 工作中，“完整上下文分身 + 异步开放复盘”是否比 briefing 式普通子代理更少遗漏、更能发现前提错误，并在共享前缀/缓存命中的条件下保持可接受成本。

