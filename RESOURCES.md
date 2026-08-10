# Agent / Harness Resources

## Knowledge

### 地基
- [Python-100-Days — jackfrued](https://github.com/jackfrued/Python-100-Days)（本地 fork：[`python-100Days/`](./python-100Days)，origin [`NorthAdb/Python-100-Days`](https://github.com/NorthAdb/Python-100-Days)）
  系统重学 Python。Use for: 阶段 0；优先 Day01–20 + 文件/网络/异步/包管理，够跑教程即可，勿沉迷全集。

### 心智模型与 Harness 实战
- [learn-harness-engineering L01](https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-01-why-capable-agents-still-fail/)
  强模型为何仍失败。Use for: 阶段 1 开场。
- [learn-claude-code-north](https://github.com/NorthAdb/learn-claude-code-north)（本地：[`learn-claude-code-north/`](./learn-claude-code-north)）
  从零搭 coding agent harness（s01–s20）。Use for: 阶段 2–5 主实战脊柱；对照闭源 Claude Code。
- [深入理解 AI Agent — bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book)
  Agent = LLM + 上下文 + 工具；含评测、持续改进、多 Agent。Use for: 原理脊柱与面试叙事。

### 广谱地图与框架课
- [Hello-Agents — Datawhale](https://hello-agents.datawhale.cc/#/./README)（仓库 [Hello-Agents](https://github.com/datawhalechina/hello-agents)）
  范式、框架（含 LangGraph）、协议、案例。Use for: 当地图与 Ch6 框架课；勿与 North 并行通读。
- [All-in-RAG — Datawhale](https://datawhalechina.github.io/all-in-rag/#/)（仓库 [all-in-rag](https://github.com/datawhalechina/all-in-rag)）
  RAG 全栈。Use for: 阶段 3；二次开发的知识层必用。

### 二次开发候选（阶段 2 末三选一深挖）
- [Pi — earendil-works/pi](https://github.com/earendil-works/pi)（原 pi-mono / pi coding agent）
  TypeScript；极简 coding agent toolkit。Use for: 对照 Claude Code；扩展点清晰时优先。
- [Hermes Agent — NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
  Python；「会成长」的 agent。Use for: 与 Python 教程栈同语言，二次开发摩擦更小。
- [OpenCode — anomalyco/opencode](https://github.com/anomalyco/opencode)
  TypeScript；用户已在用的开源 coding agent。Use for: 已有使用直觉；插件/扩展路径。

### 封装层（对照 harness）
- LangChain / LangGraph 官方文档（学习时再钉具体入口 URL）
  Use for: 阶段 4；会用 + 能说清与自建 harness 的职责边界。

## Wisdom (Communities)

- Datawhale 开源学习社区（Hello-Agents / all-in-rag Issue 与讨论）
  Use for: 卡关、作业对照、中文场景。
- 各候选框架的 Discussions / Discord（选定后再写入具体链接）
  Use for: 二次开发设计是否 idiomatic。

## Gaps

- Java 侧桥接材料（Spring AI、MCP/HTTP 暴露 Java 服务）→ 春节后阶段 6 补
- LangChain/LangGraph 精读入口与版本钉死 → 阶段 4
- 选定框架后的官方扩展/插件文档 → 阶段 5a 写入
