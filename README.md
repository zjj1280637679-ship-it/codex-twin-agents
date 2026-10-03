# Codex Twin Agents

**一键创建继承当前上下文的原生 Codex 分身。**

Codex 已经能调用 `spawn_agent` 创建分身并传递上下文。这个插件把这组操作包装成一个方便入口：调用 Skill，创建一个原生子代理，用原生消息渠道交流。它的价值是少写交接说明、少重复操作。

## 使用

在已安装插件、提供原生 `spawn_agent` 的 Codex 宿主中调用：

```text
$open-task-twin
```

也可以自然地说：

```text
分一个继承当前上下文的分身，帮我继续看看。
```

需要明确分工时，直接补上任务，例如“分一个继承当前上下文的分身，检查刚才修复的登录问题”。分身沿用用户目标和宿主规则，具体做什么由当前请求决定。

Skill 默认发起一次原生调用，参数为 `task_name`、`message`、`fork_turns`，其中 `fork_turns="all"`。宿主负责传播它实际可提供的上下文；插件脚本本身不读取或复制主对话。

主代理与分身通过宿主原有的消息、结果和等待机制协作，是否等待按当前任务决定。分身的运行期限由宿主决定；本插件不保证主代理结束后仍持续运行。

## 可选参数助手

Skill 可以直接调用原生工具。需要查看或生成参数时，可选运行：

```sh
python skills/open-task-twin/scripts/twin_fork.py
```

脚本只输出原生调用所需的 JSON 参数，默认使用 `context_twin` 和完整上下文。可用 `--task-name`、`--message`、`--fork-turns all|none|N` 覆盖；选择 `none` 或有限轮数时，仅按该值请求上下文，不能称为完整上下文分身。生成参数并不代表已创建代理，仍需宿主实际调用 `spawn_agent`。

v0.3.0 移除了旧原型的模式、Fork Handle 和包装输出；旧版 CLI 命令请改用以上无位置参数的调用。

## 范围

插件只提供入口和参数助手。权限、工具、授权判断、并发协作和生命周期继续由原生宿主与用户指令决定。实现中不增加另一条主对话、旁路编排、持久后台服务，也不附加只读、审批、预算或固定审查任务。

若宿主没有原生 `spawn_agent`，应说明当前无法通过此入口创建分身；不能用摘要交接或另建对话冒充完整上下文分身。

## 仓库

- [Skill](skills/open-task-twin/SKILL.md)：调用入口。
- [参数助手](skills/open-task-twin/scripts/twin_fork.py)：原生请求参数生成器。
- [运行约定](docs/runtime-contract.md)与[架构](docs/architecture.md)：实现边界。
- [验收场景](evals/cases.md)：检查入口是否方便且保持原生行为。
- [认识论](docs/epistemology.md)、[可能世界](docs/possible-worlds.md)、[理论笔记](skills/open-task-twin/references/theory.md)：可选设想，供阅读讨论，不是运行指令或实现要求。

**v0.3.0：原生上下文分身快捷入口。**
