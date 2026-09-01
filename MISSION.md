# Mission: 打好地基——读懂并跑通 coding agent harness

## Why
日常已经在用 Cursor / Claude Code / OpenCode，缺的是「造 harness」的肌肉，而不是再堆框架课。Java 后端实习仍是长期方向，但当前只做一件事：用 Python 读得动、跑得动真正的 agent 代码，并用一本系统书把概念钉死。地基没打好之前，不谈二次开发、封装框架和面试叙事。

## Success looks like
- 能独立读改 `playground/`，并读懂 North 全套 `s01–s20/code.py` 用到的 Python 语法（venv、文件、JSON、HTTP、类型、class、getattr/subprocess、re、线程）
- 能用一句话解释 **Agent = LLM + 上下文 + 工具**，并指出 Harness 落在哪一层
- 能跑通 North 根目录 `s01` 起的真实循环，对照书/讲义说出每一层机制在干什么
- 遇到失败时先查 harness（规则、工具、验证、上下文），而不是先怪模型

## Constraints
- Python 系统重学；课件 HTML 是主教材，100-Days 仅作选读
- 练习代码由老师创建，用户以读代码 + 运行为主
- 三份材料不并行通读：**书 = 原理**，**North = 可跑代码**，**Harness 讲义 = 工程约束理论（卫星）**
- 不按日历工期排课；进度以 learning-records 和过关为准

## Out of scope
- LangChain / LangGraph 及同类封装层
- 对 Pi / Hermes / OpenCode 做二次开发
- 面试打磨、Java/MCP 桥接冲刺
- 从头训练或深挖后训练
- 同时通读多本框架教程
