"""0012：对照读 North s01 的 Python 表面（不调用模型、不需要 API Key）。

本脚本只打开本地 learn-claude-code-north/s01_agent_loop/code.py，
标出你已经学过的语法落在哪几行。读不懂 class 的章节请先看 examples.py。

运行：
  cd d:\\agent-learning\\playground\\python
  python 0012-classes\\read_s01_surface.py
"""

from __future__ import annotations

from pathlib import Path

# playground/python/0012-classes → 仓库根
REPO_ROOT = Path(__file__).resolve().parents[3]
S01 = REPO_ROOT / "learn-claude-code-north" / "s01_agent_loop" / "code.py"

# 关键词 → 本仓库已过关课。只认「表面语法」，不讲 Anthropic SDK。
MARKERS: list[tuple[str, str]] = [
    ("import os", "0004 模块 / 0011 标准库"),
    ("from anthropic import", "0011 第三方包（本课不装、不跑）"),
    ("load_dotenv", "0011 第三方包；.env 不进 git"),
    ("TOOLS = [{", "0006 dict + 0008 JSON 形状的工具说明书"),
    ("def run_bash", "0004 函数"),
    ("subprocess.run", "标准库；以后跑 North 再细看"),
    ("except (FileNotFoundError, OSError)", "0007 具体 except"),
    ("def agent_loop", "0004 函数 + 0003 while"),
    ("while True:", "0003 循环（配 break / return）"),
    ("messages.append", "0005 list"),
    ("if response.stop_reason", "0003 分支"),
    ("for block in response.content:", "0003 for"),
    ('block.input["command"]', "0006 嵌套 dict 取值"),
    ('if __name__ == "__main__":', "0004 入口"),
    ("history = []", "0005 会话 list；0004 注意可变默认值"),
    ("isinstance(", "0009 运行时校验"),
]


def main() -> None:
    print("s01 path:", S01)
    if not S01.is_file():
        print("找不到 North s01。确认 learn-claude-code-north/ 已拷在仓库旁。")
        return

    lines = S01.read_text(encoding="utf-8").splitlines()
    print(f"共 {len(lines)} 行。下面是「已学语法」落点（class / dataclass：s01 里没有）。\n")
    found = 0
    for needle, lesson in MARKERS:
        hits = [i for i, line in enumerate(lines, start=1) if needle in line]
        if not hits:
            continue
        found += 1
        loc = ", ".join(str(n) for n in hits[:3])
        print(f"  L{loc:<12} {needle}")
        print(f"               ← {lesson}")

    print(f"\n命中 {found} 类标记。s01 是函数 + dict + while；class 从 North 后半（如 s12 Task）才密集出现。")
    print("本课主技能仍是 class；这张表只证明：你现在的 Python 已经够读 s01 表面。")


if __name__ == "__main__":
    main()
