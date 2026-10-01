"""0009 主脚本 B：带标注的 tool_call 校验（延续 0006/0008）。

读本文件时请对照课件「逐段读 typed_tool_call.py」一节。
流水线：JSON 文件/文本 → dict[str, Any] → 校验 → (name, arguments) → 归一化。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# frozenset：不可变集合。白名单不应被 append/add 改掉，用 frozenset 比 set 更稳。
# 「in 判断」对 set / frozenset 都是平均 O(1)，比每次扫 list 更合适。
KNOWN_TOOLS = frozenset({"rag_search", "read_file", "final"})

# Path(__file__).parent = 本脚本所在目录 0009-type-hints/
# 再 .parent = playground/python/，然后进入 0008-json/ 读样例 JSON
CALL_PATH = Path(__file__).parent.parent / "0008-json" / "sample_tool_call.json"


def parse_tool_call(raw: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """把「松散 tool_call dict」收成可执行的 (工具名, 参数dict)。

    签名怎么读：
      入参 raw: dict[str, Any]
        - 键是 str（JSON 对象键本来就是字符串）
        - 值是 Any：刚从 JSON 来，还没验证每个字段类型
      返回 -> tuple[str, dict[str, Any]]
        - 第 0 元：工具名（str）
        - 第 1 元：arguments 对象（仍可能含未归一化的值，如 top_k="2"）
    """
    name = raw.get("name")
    # 标注说希望是 str，但运行时可能缺键 → None，或类型不对 → 必须 isinstance
    if not isinstance(name, str):
        raise TypeError("name 必须是字符串")
    if name not in KNOWN_TOOLS:
        raise ValueError(f"unknown tool: {name!r}")

    # 缺 arguments 时用 {}，避免后面 .get 再炸；但仍要确认真的是 dict
    arguments = raw.get("arguments", {})
    if not isinstance(arguments, dict):
        raise TypeError("arguments 必须是对象")
    # return a, b 等价于 return (a, b)：一次返回两个结果，用元组打包
    return name, arguments


def normalize_rag_args(arguments: dict[str, Any]) -> dict[str, int | str]:
    """把外部不稳定类型收成内部稳定类型。

    返回标注 dict[str, int | str] 怎么读：
      - 键：str
      - 值：每个值要么是 int，要么是 str（不是「同一个值同时是两种」）
      - 本函数里 query 是 str，top_k 是 int
    """
    query_raw = arguments.get("query", "")
    top_k_raw = arguments.get("top_k", 3)
    # 清洗 query（0006）：去两端空白、压缩中间空白
    query = " ".join(str(query_raw).strip().split())
    # 数字三案（0008）：JSON 数字 / "3" 字符串 / 缺键 → 统一 int
    top_k = int(top_k_raw)
    return {"query": query, "top_k": top_k}


def load_call_from_file(path: Path) -> dict[str, Any]:
    """文件 → JSON → dict；根节点必须是对象。"""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise TypeError("tool_call 根必须是对象")
    return data


def main() -> None:
    # 路径 1：从磁盘 JSON 文件来
    raw = load_call_from_file(CALL_PATH)
    name, arguments = parse_tool_call(raw)  # 元组解包：左=名，右=参数
    normalized = normalize_rag_args(arguments)
    print("=== validated ===")
    # {"name": name, **normalized}
    # ** 把 normalized 里的键值「摊开」并进外层 dict
    # 等价于 {"name": name, "query": normalized["query"], "top_k": normalized["top_k"]}
    print({"name": name, **normalized})

    # 路径 2：模拟模型吐出的 JSON 字符串
    text = json.dumps(
        {"name": "final", "arguments": {"answer": "类型标注帮助读代码"}},
        ensure_ascii=False,
    )
    from_text = json.loads(text)
    if not isinstance(from_text, dict):
        raise TypeError("解析结果必须是 dict")
    name2, args2 = parse_tool_call(from_text)
    print("=== from text ===")
    print({"name": name2, "arguments": args2})


if __name__ == "__main__":
    main()
