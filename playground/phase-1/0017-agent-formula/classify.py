"""0017 — 读一份系统说明书，判断它是不是本仓库说的 Agent。

公式（书 Ch1 §1.1）：
  Agent = LLM + 上下文 + 工具
  LLM      = 大脑：理解、规划、决定下一步
  上下文   = 眼睛：这一次决策能看到的全部信息
  工具     = 手脚：感知或改变外部世界的接口
  环境     = 公式外面。观察从那儿来，行动打回那儿去。
             仓库里有文件 ≠ 模型看见了——没进上下文就等于不存在。

谁决定下一步：
  model → 自主 Agent（本仓库默认说的「Agent」）
  code  → 工作流（有 LLM、有工具，但路径写死）
  none  → 没有「下一步」这回事（单次补全 / 纯问答）

运行（无第三方包）：
  cd d:\\agent-learning\\playground\\phase-1\\0017-agent-formula
  python classify.py
  # 或用阶段 0 的解释器：
  # d:\\agent-learning\\playground\\python\\.venv\\Scripts\\python.exe classify.py
"""

from __future__ import annotations

from typing import Literal, TypedDict


class Spec(TypedDict):
    name: str
    has_llm: bool
    has_context: bool
    has_tools: bool
    who_picks_next: Literal["none", "code", "model"]
    note: str


def verdict(spec: Spec) -> str:
    """按公式打标签。先列缺的零件，零件齐了再问「下一步谁说了算」。"""
    if not spec["has_llm"]:
        return "不是 Agent：没有大脑（LLM）"
    missing: list[str] = []
    if not spec["has_context"]:
        missing.append("眼睛（上下文）")
    if not spec["has_tools"]:
        missing.append("手脚（工具）")
    if missing:
        return "不是 Agent：缺少" + "、".join(missing)
    if spec["who_picks_next"] == "code":
        return "工作流：有工具，但下一步由代码写死"
    if spec["who_picks_next"] == "model":
        return "自主 Agent：模型根据观察决定下一步"
    return "不是 Agent：有零件，但没有循环（单次调用就结束）"


CASES: list[Spec] = [
    {
        "name": "① 单次补全 API",
        "has_llm": True,
        "has_context": False,
        "has_tools": False,
        "who_picks_next": "none",
        "note": "你发一句，它回一句，没有历史、没有工具。",
    },
    {
        "name": "② 把文档贴进提示词的问答窗",
        "has_llm": True,
        "has_context": True,
        "has_tools": False,
        "who_picks_next": "none",
        "note": "能看资料再答，但仍改不了文件 / 跑不了测试。",
    },
    {
        "name": "③ 订机票四个固定节点",
        "has_llm": True,
        "has_context": True,
        "has_tools": True,
        "who_picks_next": "code",
        "note": "验证 → 搜索 → 付款 → 确认。LLM 只在节点内填字段。",
    },
    {
        "name": "④ Cursor 式 coding agent",
        "has_llm": True,
        "has_context": True,
        "has_tools": True,
        "who_picks_next": "model",
        "note": "读代码、改文件、跑测试；下一步由模型选。",
    },
]


def main() -> None:
    print("公式：Agent = LLM + 上下文 + 工具")
    print("环境在公式外。没进上下文的观察，对模型等于不存在。\n")
    for spec in CASES:
        print(f"=== {spec['name']} ===")
        print("  ", spec["note"])
        print(
            "  零件：",
            f"LLM={spec['has_llm']}",
            f"上下文={spec['has_context']}",
            f"工具={spec['has_tools']}",
            f"下一步={spec['who_picks_next']}",
        )
        print("  判定：", verdict(spec))
        print()


if __name__ == "__main__":
    main()
