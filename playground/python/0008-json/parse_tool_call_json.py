"""0008 主脚本 B：从 JSON 解析 tool_call，并在边界做校验。"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
CALL_PATH = BASE_DIR / "sample_tool_call.json"
KNOWN_TOOLS = {"rag_search", "read_file", "final"}


def load_tool_call(path: Path) -> dict:
    """读取 tool_call JSON 文件。"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"tool_call 文件不存在: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"tool_call 不是合法 JSON: {path}") from error

    if not isinstance(data, dict):
        raise TypeError("tool_call 根节点必须是对象")
    return data


def parse_tool_call_text(raw: str) -> dict:
    """解析模型可能吐出的 JSON 字符串。"""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("模型输出不是合法 JSON tool_call") from error
    if not isinstance(data, dict):
        raise TypeError("tool_call 必须是 JSON 对象")
    return data


def validate_call(call: dict) -> tuple[str, dict]:
    """进入执行层前的最小校验（延续 0006）。"""
    name = call.get("name")
    if name not in KNOWN_TOOLS:
        raise ValueError(f"unknown tool: {name!r}")
    arguments = call.get("arguments", {})
    if not isinstance(arguments, dict):
        raise TypeError("arguments must be a dict")
    return str(name), arguments


def normalize_rag_args(arguments: dict) -> dict:
    """把外部 JSON 里不稳定的类型收成内部稳定类型。"""
    query = " ".join(str(arguments.get("query", "")).strip().split())
    top_k = int(arguments.get("top_k", 3))
    return {"query": query, "top_k": top_k}


def main() -> None:
    from_file = load_tool_call(CALL_PATH)
    name, arguments = validate_call(from_file)
    normalized = normalize_rag_args(arguments)
    print("=== from file ===")
    print({"name": name, **normalized})

    # 模拟模型返回的字符串（注意 top_k 仍可能是字符串）
    raw = json.dumps(
        {
            "name": "rag_search",
            "arguments": {"query": "  harness 与 RAG  ", "top_k": "5"},
        },
        ensure_ascii=False,
    )
    from_text = parse_tool_call_text(raw)
    name2, args2 = validate_call(from_text)
    print("=== from model text ===")
    print({"name": name2, **normalize_rag_args(args2)})


if __name__ == "__main__":
    main()
