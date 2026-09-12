# 0028 过关

用户确认课 0028（North s08 Context Compact：`ContextCompactor`、`prepare` 总调度、工具结果转存、消息归档、微压缩、历史摘要、reactive compact）已按过关标准完成。

已掌握：

- 能用一句话说明 s08：上下文超限时，按可恢复性和成本从工具结果整理逐步走到历史摘要；`prepare` 是每次模型调用前的总调度。
- 能按真实顺序讲出 `prepare`：`tool_result_budget` → `snip_compact` →（总窗口 > 50000 时）`micro_compact` → `fit_tool_results` → `compact_history`。
- 能区分三把输入尺子：`CONTEXT_CHAR_LIMIT=50000` 是整段 `messages` 的字符估算；`TOOL_RESULT_BATCH_CHAR_LIMIT=200000` 是最新一批工具结果合计；`LARGE_RESULT_CHAR_LIMIT=30000` 是 budget 里单条是否值得转存。`max_tokens` 是输出上限，不是输入窗口。
- 能区分 `tool_result_budget` 与 `fit_tool_results`：前者每轮只看最新批次、门槛 20 万；后者在微压缩之后仍超 5 万时才跑，扫描全部结果（含最新未消费结果），预览从 2000 字改为 1000 字。
- 能解释 `micro_compact` 只缩短已消费的旧结果并保留最近 3 条，不是按语义判断「没用」；`snip_compact` 量的是消息条数 > 50，不是字符长度。
- 能说明完整工具输出写入 `.task_outputs/tool-results/<tool_use_id>.txt`，消息只留路径和预览；transcript 才是整段 `messages` 备份。摘要是有损表示，不是备份。
- 已真跑 `s08_context_compact/code.py`：读 README 与 `docs.json` 后观察到 `.task_outputs/tool-results/` 落盘。单条约 9.9 万字符未触发 budget（< 20 万），但撑过 5 万总窗口后由 `micro_compact` 搬走旧 README、`fit_tool_results` 把该大结果写成预览。本次未出现 `.transcripts/` 与 `[auto compact]`。

本课不要求：

- 真实 tokenizer、厂商精确 token 计费、多轮摘要质量评测、跨会话记忆、向量检索、无限滚动历史、压缩后的自动事实校验。这些留给 s09 Memory 或生产实现。

## Implications

- 下一课是 **0029**：North `s09_memory`（筛选、提取、整理持久记忆；压缩管的是当前窗口，记忆管的是跨会话该留下什么）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0028 同密度；非必要不另写 playground
- 已钉边界：5 万是教学字符阈值，不是 API 真实窗口；budget 的 20 万与总窗口的 5 万不是同一把尺子；落盘可恢复 ≠ 摘要可靠
