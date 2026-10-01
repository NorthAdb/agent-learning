"""0020 — 失败先查哪一层？不要先换模型。

使命：遇到失败时先查 harness（规则、工具、验证、上下文），而不是先怪模型。
原文：MISSION.md 第 10 行。

讲义 L01（网页，无行号，用标题锚点）：
  https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-01-why-capable-agents-still-fail/
  关键名词 → #关键名词解释
  五层归因 → #遇到失败-先修-harness
  书 / North 没有「能力鸿沟」「验证缺口」这两个词。

五层（失败归因清单，不是 L02 的五子系统）：
  spec    任务规范     需求有没有说清楚、完成定义能不能跑命令验证
  context 上下文供给   约定有没有写进模型能看见的地方
  env     执行环境     依赖、工具版本、能不能跑起来
  verify  验证反馈     宣称完成 vs 测试/lint 真过了没有
  state   状态管理     跨会话有没有把进度留下

运行：
  cd d:\\agent-learning\\playground\\phase-1\\0020-fail-check-harness
  python blame_fail.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

Layer = Literal["spec", "context", "env", "verify", "state"]

LAYER = {
    "spec": "任务规范：需求 / 完成定义",
    "context": "上下文供给：约定有没有写进模型能看见的地方",
    "env": "执行环境：依赖、版本、能不能跑",
    "verify": "验证反馈：宣称完成 vs 命令真过了没有",
    "state": "状态管理：跨会话有没有把进度留下",
}


class Case(TypedDict):
    name: str
    layer: Layer
    note: str


CASES: list[Case] = [
    {
        "name": "① 「加个搜索」跑完不像你要的",
        "layer": "spec",
        "note": "对象、分页、高亮都没说。Agent 在猜。先写完成定义，再怪模型。",
    },
    {
        "name": "② 组里都用 SQLAlchemy 2.0，它写了 1.x",
        "layer": "context",
        "note": "规矩在 Slack 和脑子里。没进上下文 = 不存在（0017）。",
    },
    {
        "name": "③ 半小时都在修 pip / Node 版本",
        "layer": "env",
        "note": "环境缺口。上下文窗口花在装依赖上，正事没做。",
    },
    {
        "name": "④ 它说「做完了」，pytest 一跑就红",
        "layer": "verify",
        "note": "验证缺口。听口嗨不算完成；0018 的验证层缺席。",
    },
    {
        "name": "⑤ 新开对话又从 ls 仓库开始",
        "layer": "state",
        "note": "跨会话状态丢了。超过约 30 分钟的任务特别容易死在这层。",
    },
    {
        "name": "⑥ 昨天同一模型、需求写清楚就做成了",
        "layer": "spec",
        "note": "同类任务结构良好时能成 → 优先假设是 harness，不要先换更贵的模型。",
    },
]


def main() -> None:
    print("失败先查 harness，不要先换模型。")
    print("同一条失败，先问落在五层的哪一层。\n")
    for case in CASES:
        print(f"=== {case['name']} ===")
        print("  ", case["note"])
        print("  归因：", LAYER[case["layer"]])
        print()
    print("对照：能力鸿沟 = 基准好看、真实任务差（常常因为真实任务缺 harness）。")
    print("      不是「这模型数学不行」的同义词。")


if __name__ == "__main__":
    main()
