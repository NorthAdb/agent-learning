# Agent Learning Glossary

本仓库术语表。课件、速查、learning-records 用词以此为准。压缩定义；别名放在 _Avoid_。

## Harness & Agent

**Model**:
提供感知—推理—行动决策的 LLM 权重与推理服务；Agency 的主要来源。
_Avoid_: 把整个 Agent 产品称作「模型」

**Harness**:
围绕 Model 的运行外壳：Tools + Knowledge + Observation + Action interfaces + Permissions。
_Avoid_: 任意 prompt 工作流、纯 if-else 编排冒充 harness

**Tool**:
Harness 暴露给 Model 的一个可调用动作，通常以 name + arguments 描述。
_Avoid_: 笼统的「插件」（未区分 MCP / Skill / 函数工具时）

**Tool call**:
Model 发出的一次工具调用请求（结构化数据，常为 dict）。
_Avoid_: 整段对话、一次 HTTP 请求（除非恰好一一对应）

**Agent loop**:
重复「Model 输出 → 执行 Tool（可选）→ 观察 → 再请求 Model」直到 final 或触顶的控制结构。
_Avoid_: 单次补全、无工具聊天

**max_turns**:
Agent loop 的轮数上限，用作防死循环的安全带。
_Avoid_: temperature、max_tokens

## Knowledge

**RAG**:
Retrieval-Augmented Generation：先检索知识再生成回答；本使命中常作为二次开发切入的 Knowledge 能力。
_Avoid_: 「有向量数据库 = 已完成 Agent」

## Frameworks (workspace stance)

**封装层**:
如 LangChain / LangGraph 等编排与工程库；需要会用，并对照 Harness 职责边界。
_Avoid_: 将封装层等同于 Agency 或 Harness 的全部
