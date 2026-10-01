"""0015 主脚本：从模型乱文本里抽出 list，再用 literal_eval 变成对象。

对照 North：s09 re.search 抽 [...]；s05 ast.literal_eval 解析 todos。
流程：DOTALL 找方括号 → literal_eval → isinstance list。
本课不装 PyYAML；s07 yaml.safe_load 课件扫一眼即可。

运行：
  cd d:\\agent-learning\\playground\\python
  python 0015-text-parse\\extract_todos.py
"""

from __future__ import annotations

import ast
import re


class ParseError(ValueError):
    """模型输出不是合法字面量。"""


# 跨行抓住第一对方括号（模型 list 常折行）
# compile：模式备成常量，后面只 TODO_BLOCK.search(text)
TODO_BLOCK = re.compile(r"\[.*\]", re.DOTALL)


def extract_list_literal(text: str) -> list[object]:
    matched = TODO_BLOCK.search(text)
    if matched is None:
        raise ParseError("no list brackets in text")
    chunk = matched.group(0)
    try:
        value = ast.literal_eval(chunk)
    except (ValueError, SyntaxError) as error:
        # 0007：转换后上抛，保留原因链
        raise ParseError(f"not a literal: {chunk!r}") from error
    if not isinstance(value, list):
        raise ParseError("expected a list")
    return value


def main() -> None:
    messy = """
    here is the plan
    [{'id': '1', 'content': 'read files', 'status': 'pending'},
     {'id': '2', 'content': 'write tests', 'status': 'in_progress'}]
    thanks
    """
    todos = extract_list_literal(messy)
    print("count:", len(todos))
    print("first:", todos[0])

    try:
        extract_list_literal("no brackets at all")
    except ParseError as error:
        print("no list ->", error)

    try:
        extract_list_literal("[__import__('os')]")
    except ParseError as error:
        print("code in brackets ->", type(error).__name__)


if __name__ == "__main__":
    main()
