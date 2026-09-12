# 0025 过关

用户确认课 0025（North s05 TodoWrite：计划工具、`TodoManager` 校验与整体替换、`render`、schema/handler 双接线、三轮 reminder）已按过关标准完成。能区分内部状态 `TODO.items` 与 `render` 显示文本；能说明 `update` 是全量替换、校验失败不覆盖旧状态；能说明 schema 给模型看、handler 给 Harness 执行；能说明 reminder 是轻量 nudge 不是强制更新。过关以真跑本章 `code.py` 与课件检索为准。生产持久化 TODO / 优先级依赖 / 多 Agent 共享任务过关不要求。

## Implications
- 下一课是 **0026**：North `s06_subagent`（干净上下文与任务拆分）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0025 同密度；非必要不另写 playground
- 课件节奏偏好已记入 NOTES：先全景与状态流，再局部规则
