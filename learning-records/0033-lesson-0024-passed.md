# 0024 过关

用户确认课 0024（North s04 Hooks：事件注册表、`register_hook` / `trigger_hooks`、四个时机）已按过关标准完成。已在 Windows 上跑通 `s04_hooks/code.py`：观察到 UserPromptSubmit、PreToolUse（含 `write_file` / `bash` 的 `[HOOK]` 日志）、Stop 统计；删除临时文件时 `permission_hook` 对 `rm` / `del` 各问一次后放行；理解 `rm` 在 Windows 上无效、`del` 才删掉是 OS 命令差异，不是 hook 第一次没放行。能区分 HOOKS / event / callback / trigger；能说明 Pre 按每个 `tool_use` 触发、权限短路后 log 可能不跑、Post 大输出阈值日常难触发。生产异步 hook / 插件发现过关不要求。

## Implications
- 下一课是 **0025**：North `s05_todo_write`（给 Agent 计划工具；先列清单再做）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0024 同密度；非必要不另写 playground
- s03 权限在 s04 已搬到 PreToolUse；后续章继续在同一根循环上挂机制，不要为新能力复制 `agent_loop`
