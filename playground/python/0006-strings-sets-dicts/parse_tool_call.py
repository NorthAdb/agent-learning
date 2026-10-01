"""0006 主脚本：清洗 prompt、解析 tool call、校验字段。"""

from __future__ import annotations


KNOWN_TOOLS = {"rag_search", "read_file", "final"}


def clean_query(raw: str) -> str:
    """把用户输入变成适合检索的单行 query。"""
    return " ".join(raw.strip().split())


def build_prompt(question: str, snippets: list[str]) -> str:
    """用 join 组装稳定、可观察的上下文块。"""
    blocks = [f"[{i}] {snippet.strip()}" for i, snippet in enumerate(snippets, start=1)]
    context = "\n".join(blocks) if blocks else "（没有检索到相关资料）"
    return f"请仅依据以下资料回答：\n{context}\n\n问题：{question}"


def validate_call(call: dict) -> tuple[str, dict]:
    """读取嵌套 dict，并在进入执行层前做最小校验。"""
    name = call.get("name")
    if name not in KNOWN_TOOLS:
        raise ValueError(f"unknown tool: {name!r}")
    arguments = call.get("arguments", {})
    if not isinstance(arguments, dict):
        raise TypeError("arguments must be a dict")
    return name, arguments


def main() -> None:
    raw_question = "  如何把 Java 服务接入 Agent harness？\n"
    question = clean_query(raw_question)
    snippets = [
        "Harness 负责围绕模型组织工具、权限和观察结果。",
        "Java 服务可以作为受权限控制的业务 API 被工具封装。",
    ]
    print("=== prompt ===")
    print(build_prompt(question, snippets))

    call = {
        "name": "rag_search",
        "arguments": {"query": question, "top_k": "2"},
    }
    name, arguments = validate_call(call)
    query = clean_query(arguments.get("query", ""))
    top_k = int(arguments.get("top_k", 3))
    print("=== validated tool call ===")
    print({"name": name, "query": query, "top_k": top_k})


if __name__ == "__main__":
    main()
