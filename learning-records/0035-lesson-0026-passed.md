# 0026 过关

用户确认课 0026（North s06 Subagent：`task` 委派、fresh messages、父子共享 WORKDIR / hooks、一层委派、最终文本回传）已按过关标准完成。已真跑 `s06_subagent/code.py`：观察到 `[Subagent started]`、多条 `[sub]` 工具日志、`[Subagent done]`，以及父侧只经 `task` 得到调研结论（如项目使用 pytest）。能区分 `*BASE_TOOLS` 与 `**BASE_HANDLERS`；能说明 `extract_text` 只取结束轮 text、中间工具结果不进父 messages；能说明终端末尾打印的是父最终 text，不是单独 dump 的 `task` tool_result；能对照 s05：上节在循环内联执行 block，本节抽成 `execute_tool(block, handlers)` 供父子复用。并发子 Agent / 跨进程沙箱 / 多层递归委派过关不要求。

## Implications
- 下一课是 **0027**：North `s07_skill_loading`（按需加载技能，不把知识全堆进 system prompt）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0026 同密度；非必要不另写 playground
- 已钉边界：消息隔离 ≠ 文件隔离；最终 text ≠ 验证证据
