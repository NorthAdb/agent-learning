# 第 9 课过关：类型标注

用户确认 0009 已按过关标准完成：能读 `list[dict[...]]` / `dict[str, Any]` / `str | None`，理解标注默认不强制运行时检查，并知道边界仍要 `isinstance`；`TypedDict` 与 `__future__ annotations` 可对照脚本讲解。

## Implications
- 读开源 agent 函数签名可当已知；下一课 HTTP/`requests` 可直接写带标注的 API 客户端
- 阶段 0 下一关：requests + HTTP JSON；其后包管理与异步扫盲
