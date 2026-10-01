"""0008 例程：JSON 类型对照、dumps/loads、常见失败。"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent


def show_type_mapping() -> None:
    """JSON 文本 ↔ Python 对象的基本类型映射。"""
    text = '{"ok": true, "score": 0.91, "tags": ["rag", "tool"], "note": null}'
    data = json.loads(text)
    print("loads 之后的 Python 类型:")
    print("  ok   ->", data["ok"], type(data["ok"]).__name__)
    print("  score->", data["score"], type(data["score"]).__name__)
    print("  tags ->", data["tags"], type(data["tags"]).__name__)
    print("  note ->", data["note"], type(data["note"]).__name__)

    again = json.dumps(data, ensure_ascii=False, indent=2)
    print("dumps 回去（ensure_ascii=False，中文可读）:")
    print(again)


def show_dumps_vs_dump() -> None:
    """字符串通道 vs 文件通道：问的是两个不同问题。"""
    payload = {"name": "final", "arguments": {"answer": "先接工具边界"}}
    d = {"msg": "it's fine"}   # 值里有撇号
    print(d)
    print(json.dumps(d, ensure_ascii=False))  # 输出：{"msg": "it's fine"}

    # 通道 1：内存字符串 —— 适合 LLM 输出、HTTP body
    as_text = json.dumps(payload, ensure_ascii=False)
    print("dumps → str:", as_text)
    print("loads ← str:", json.loads(as_text))

    # 通道 2：直接写文件 —— 适合配置、缓存、会话落盘
    out = BASE_DIR / "roundtrip.json"
    with open(out, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    with open(out, "r", encoding="utf-8") as file:
        loaded = json.load(file)
    print("dump/load 文件往返:", loaded)


def show_number_traps() -> None:
    """数字三案：JSON 数字 / JSON 字符串数字 / 缺键默认。"""
    cases = [
        '{"top_k": 3}',
        '{"top_k": "3"}',
        "{}",
    ]
    for raw in cases:
        data = json.loads(raw)
        raw_value = data.get("top_k", 3)
        top_k = int(raw_value)
        print(f"{raw} -> get={raw_value!r} ({type(raw_value).__name__}) -> int={top_k}")


def show_json_errors() -> None:
    """坏 JSON：用标准范式捕获 JSONDecodeError 并转换语义。"""
    bad = '{"name": "rag_search",}'  # 尾逗号非法
    try:
        json.loads(bad)
    except json.JSONDecodeError as error:
        print("底层消息:", error)
        print("位置: line", error.lineno, "col", error.colno)
        raise ValueError("tool_call JSON 非法，无法解析") from error


def main() -> None:
    show_type_mapping()
    print("---")
    show_dumps_vs_dump()
    print("---")
    show_number_traps()
    print("---")
    try:
        show_json_errors()
    except ValueError as error:
        print("边界转换后:", error)


if __name__ == "__main__":
    main()
