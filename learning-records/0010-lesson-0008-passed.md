# 第 8 课过关：JSON 配置与 tool_call

用户确认 0008 已按过关标准完成：`dumps/loads` 与 `dump/load`、类型对照、`ensure_ascii`、数字三案、非法 JSON 与异常边界转换上抛，以及配置落盘与 tool_call 解析链均可讲解并跑通。

## Implications
- 对象 ↔ JSON 文本 ↔ 文件这条边界可作已知；下一课类型标注可直接引用 `list[dict[str, str]]` 等写法
- 阶段 0 下一关：类型标注（读开源 agent 代码）；之后 requests / 包管理
