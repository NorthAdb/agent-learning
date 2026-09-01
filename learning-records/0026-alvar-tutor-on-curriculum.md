# Alvar 教法叠在现有课表上

用户已全局安装 [Alvarmethod](https://github.com/vasanthsreeram/Alvarmethod)（probe → plan → teach）。本仓库不换课表：HTML 仍是主教材，Alvar 只当一对一家教。

全局 skills 落在 `~/.agents/skills` / `~/.claude/skills` 等，Cursor 这场对话不会自动加载它们。本仓库用项目 skill `.cursor/skills/alvar-curriculum/` + 规则 `.cursor/rules/alvar-tutor.mdc` 接上。

## Implications
- 学 / 卡住 / `/teach` → 摸底再讲，一步一测；写课件仍走 Lesson depth
- 状态在 `.alvar/`；过关仍写 `learning-records/`
- 当前试跑目标仍是 **0018**，不是另开主题
