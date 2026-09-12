# 0021 过关

用户确认课 0021（North s01 Agent Loop：真实 Messages 循环、`tool_use` / `tool_result`、REPL）已按过关标准完成。DeepSeek 兼容端点已跑通；心算题走无工具出口、工具题走 bash 执行器，可作已知。`max_turns` 不是 API 字段、`subprocess.run` 是标准库，可作已知。

## Implications
- 下一课是 **0022**：North `s02_tool_use`（多工具 + `TOOL_HANDLERS` 查表）
- **阶段 2 讲法（用户 2026-09-01）**：以当章 README + `code.py` 为主教材，按块拆到和 0021 同密度；非必要不另写 playground 脚本
- 仍不排 L02、不做 P01
