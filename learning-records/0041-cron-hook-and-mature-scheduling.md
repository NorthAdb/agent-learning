# 0032 增补：hook 做不到定时，以及成熟产品的做法

用户先问「s12 讲的内容用 hook 不能实现吗」，追问「成熟的 agent 是怎么实现定时任务的」。核对官方文档后按建议增补课件，不改 s12 的机制讲解，也不改过关标准。

## 结论

- hook 挂在生命周期事件上（`UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop`…）。命令 hook 不能触发 `/` 命令或工具调用，也就不能自己发起一轮。定时最典型的场景是人不在、循环没在跑，没有事件可挂。
- 官方做法印证：Claude Code 用 `CronCreate` / `CronList` / `CronDelete` + 每秒检查的调度器做定时，而不是 hook。它和 s12 的 `cron_scheduler_loop` + `cron_queue` 是同一套结构。
- 成熟产品 = s12 的三件事（保存定义、到点入队、空闲交付）搬到进程外，再补六件：漏跑策略、重叠策略、抖动、过期与上限、审批策略、触发器信任边界。
- 形态分三层：会话内调度（本课、`/loop`）／本机常驻（Desktop 任务）／托管云（Routines、LangGraph cron、ChatGPT tasks）；通用底座是 Temporal Schedules、Quartz、crontab、GitHub Actions `schedule`。

## 落点

- `lessons/phase-2/0032-cron-scheduler.html`：新增延伸小节「s12 之后：真实产品怎么做定时」（含「为什么不是 hook」、三档部署表、六件事对照表、两种取舍、本节新名词出处表、自己要做时的五步）。
- `reference/phase-2/s12-cron-scheduler.html`：新增「生产化补丁（s12 之后）」速查块。
- `GLOSSARY.md` 的 Cron Scheduler 段补 6 条：调度面/投递面/执行面、抖动、补跑/漏跑策略、重叠策略、一次一 run、持久定时器。

## Implications

- 0032 的过关标准不变；新增内容是延伸，不进入过关要求。
- 「hook 不能做定时」已写成课件结论，以后同类问题直接引 0032，不重复展开。
- 增补顺带把「绿点 ≠ 任务成功」接到 s17 判断器上，讲 s17 时可从这里回顾。
