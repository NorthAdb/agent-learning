"""0018 — 给一件工作贴标签：Agency（模型）还是 Harness（载具）？

两套公式叠在一起（书 Ch1）：
  0017:  Agent = LLM + 上下文 + 工具          # 零件清单
  本课:  Agent = Model + Harness             # 谁决策 / 谁提供世界
         Model  = LLM（大脑）
         最小 Harness = 上下文管理 + 工具接口
         生产 Harness = 最小 + 约束 + 验证 + 纠正

North：Agency（感知—推理—行动）来自模型训练，不是编排代码赋予的。
       原文：learn-claude-code-north/README-zh.md 第 9 行（标题在第 5 行）。
       书 Ch1 没有 Agency 这个词。
       模型是驾驶者，harness 是载具。

书第二套公式：AI-Agents-in-Depth-md/第01章…/第01章 AI Agent 入门.md
       §1.2 第 261 行起；公式约第 270 行；约束/验证/纠正约第 273、288–291 行。

三案「我说我在开发 Agent」：
  ① 调权重 / 后训练     → 开发 Agency（本仓库不做）
  ② 拼上下文、暴露工具、设权限 → 开发 Harness（本仓库要做）
  ③ 节点图 / 规则树模拟智能 → 不是（提示词水管工）

运行（无第三方包）：
  cd d:\\agent-learning\\playground\\phase-1\\0018-agency-vs-harness
  python label_jobs.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

Kind = Literal["agency", "harness_min", "harness_prod", "workflow", "train"]


class Job(TypedDict):
    name: str
    kind: Kind
    note: str


LABEL = {
    "agency": "Agency / 模型：决定下一步（感知—推理—行动）",
    "harness_min": "最小 Harness：拼上下文 或 执行工具",
    "harness_prod": "生产 Harness：约束 / 验证 / 纠正",
    "workflow": "工作流：下一步由代码写死（不是在造 Agency）",
    "train": "训练 Agency：改权重（本仓库不做）",
}


JOBS: list[Job] = [
    {
        "name": "① 模型选择：先 read app.py，再跑 pytest",
        "kind": "agency",
        "note": "决策在权重里。代码没有写死「必须先 read」。",
    },
    {
        "name": "② 把 read 到的正文追加进 messages",
        "kind": "harness_min",
        "note": "上下文管理：观察 → 模型下次能看见的文本。",
    },
    {
        "name": "③ 真的执行 bash，拿到 stdout",
        "kind": "harness_min",
        "note": "工具接口：模型只能发 tool_call，跑命令的是 harness。",
    },
    {
        "name": "④ 拦截 rm -rf /，先问用户",
        "kind": "harness_prod",
        "note": "约束。不是把下一步写死，是给驾驶者设护栏。",
    },
    {
        "name": "⑤ 没通过 pytest 就不许宣告完成",
        "kind": "harness_prod",
        "note": "验证。不能只听模型说「做完了」。",
    },
    {
        "name": "⑥ 超时后重试一次，再失败就回退",
        "kind": "harness_prod",
        "note": "纠正。做错了怎么补救。",
    },
    {
        "name": "⑦ 代码写死：验证 → 搜索 → 付款 → 确认",
        "kind": "workflow",
        "note": "0017：有工具，但下一步由代码决定。",
    },
    {
        "name": "⑧ 用轨迹微调，让模型更会选工具",
        "kind": "train",
        "note": "这才是在开发 Agency。使命：地基阶段不做。",
    },
]


def main() -> None:
    print("Agent = Model + Harness")
    print("Model 做决策；Harness 提供世界并执行。\n")
    for job in JOBS:
        print(f"=== {job['name']} ===")
        print("  ", job["note"])
        print("  标签：", LABEL[job["kind"]])
        print()


if __name__ == "__main__":
    main()
