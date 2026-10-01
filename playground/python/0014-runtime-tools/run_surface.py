"""0014 主脚本：假 content block + 跑一条安全命令 + 列出本课文件。

对照 North：
  s01 getattr(block, "type", None)  —— 读 SDK 对象字段
  s01 subprocess.run(...)           —— bash 工具
  s02 glob                          —— 按模式找文件

运行：
  cd d:\\agent-learning\\playground\\python
  python 0014-runtime-tools\\run_surface.py
"""

from __future__ import annotations

import glob as globmod
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


class FakeBlock:
    """用 setattr 按字符串写属性，模仿 SDK 返回的对象（不是 dict）。"""

    def __init__(self, **fields: object) -> None:
        for key, value in fields.items():
            setattr(self, key, value)  # 等价于 self.key = value


def block_type(block: object) -> str | None:
    """对象用 getattr（可缺省）；dict 用 .get。North s01 面对的是对象。"""
    if isinstance(block, dict):
        return block.get("type")
    return getattr(block, "type", None)


def run_python_snippet(code: str, timeout: float = 5.0) -> str:
    """用 argv 列表调当前解释器，避免 shell=True。

    非零退出 / 超时都收成错误字符串返回——像 s01 把失败变成 tool 观察，
    而不是让异常直接打爆 agent loop。
    """
    try:
        completed = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(HERE),
        )
    except subprocess.TimeoutExpired:
        return "Error: Timeout"
    out = (completed.stdout + completed.stderr).strip()
    if completed.returncode != 0:
        return f"Error: exit {completed.returncode} {out}"
    return out or "(no output)"


def list_lesson_py() -> list[str]:
    """glob：按模式枚举；零命中就是空列表。"""
    pattern = str(HERE / "*.py")
    return sorted(Path(p).name for p in globmod.glob(pattern))


def main() -> None:
    text_block = FakeBlock(type="text", text="hi")
    tool_block = FakeBlock(type="tool_use", name="bash")
    dict_block = {"type": "text"}
    print("types:", block_type(text_block), block_type(tool_block), block_type(dict_block))
    print("missing attr:", getattr(text_block, "name", None))

    print("subprocess ->", run_python_snippet("print(1+1)"))
    print("files ->", list_lesson_py())


if __name__ == "__main__":
    main()
