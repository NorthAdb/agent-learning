# 课 0031–0037 过关

用户确认 0031–0037（North s11–s17）均已按各课过关标准完成。阶段 2 主线到 s17 收口。

已掌握（按课压缩）：

- **0031 / s11**：只有 bash 且 `run_in_background is True` 才进后台；占位 `tool_result` 配完这次 `tool_use`；完成结果是稍后的 `task_notification`，不会自己叫醒模型。
- **0032 / s12**：五段 cron（分时日月周）；到点入队、抢到 `agent_lock` 才交付 `[Scheduled]`；`durable` 只留定义，关机不补跑；确认的是模型收下 prompt，不是工作做完。
- **0033 / s13**：队友各写各的 messages；收件箱读完即删；`result` 和 `idle_notification` 分开；扫描不是认领；没认领就没有 cwd；计划闸门挡住 bash/写/改。
- **0034 / s14**：`connect_mcp` 成功后，带前缀的工具要到下一轮才进工具池；授权看宿主策略，不看 `readOnlyHint`。
- **0035 / s15**：不新增机制。一轮顺序是注入 cron/后台通知 → 压缩 → 组池 → 调用成功才确认 cron。`task` 是一次性子代理，不是 `create_task`。异步回合所有 bash 直接拒绝。CLI 的 `async_event_loop` 才能在不打字时叫醒。
- **0036 / s16**：`Workflow` 是工具，不替换主循环。模型只选注册名。`parallel` 等齐，`pipeline` 按条目往下。journal 键来自调用内容哈希。脚本结束不等于目标完成。
- **0037 / s17**：没有 tool_use 只表示想停。判断器没有工具，只读对话。`block` 写回同一份 messages；`limit` / `error` / `max_turns` 把人叫回来，不把目标标成完成。

本批不要求：把 Goal 接进 s15 全套工具、真实 MCP 传输、操作系统 crontab 代替进程内闹钟。

## Implications

- 阶段 2 已过关到 **0037 / s17**。North 根目录 `s01–s17` 课件与过关记录对齐。
- 下一课不在这条主线上；卡住时按 NOTES 的卫星材料回看，不另开 LangChain 或旧 s18–s20 章号。
- 已钉边界：后台编号不是任务图；闹钟不是关机定时器；队友对话不共享；MCP 新工具隔一轮；集成只规定事件入口；编排结束不是验收完成。
