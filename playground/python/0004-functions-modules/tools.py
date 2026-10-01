"""工具层：每个工具是普通函数；注册表把名字映射到函数。

为什么单独成文件：二次开发加 RAG 工具时，优先改这里，不动 loop。

运行冒烟测试：
  python tools.py
被别人 import 时，下面的 if __name__ 块不会执行。
"""

from __future__ import annotations


def read_file(path: str) -> str:
    """假读文件。真实 harness 会先做权限检查再读盘。"""
    return f"[file:{path}] once upon a harness..."


def rag_search(query: str, top_k: int = 3) -> list:
    """假检索。top_k 有默认值：模型可以不传这个字段。"""
    hits = [
        {"score": 0.91, "text": "Harness = tools + context + permissions"},
        {"score": 0.80, "text": f"query={query!r} top_k={top_k}"},
        {"score": 0.70, "text": "RAG 先检索再生成"},
    ]
    return hits[:top_k]


def shell(cmd: str) -> str:
    return f"$ {cmd}\n(ok)"


# 函数是对象，可以放进 dict。这就是工具注册表。
TOOLBOX = {
    "read_file": read_file,
    "rag_search": rag_search,
    "shell": shell,
}


def run_tool(name: str, arguments: dict) -> dict:
    """把模型给的 arguments dict，展开成函数的关键字参数。

    若 name="rag_search" 且 arguments={"query": "x", "top_k": 2}
    则 TOOLBOX[name](**arguments) 等价于 rag_search(query="x", top_k=2)
    """
    if name not in TOOLBOX:
        return {"ok": False, "error": f"unknown tool: {name}"}
    try:
        result = TOOLBOX[name](**arguments)
        return {"ok": True, "result": result}
    except TypeError as e:
        # 缺参数 / 多参数 / 类型对不上时，函数会抛 TypeError
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    print(run_tool("rag_search", {"query": "what is harness", "top_k": 1}))
    print(run_tool("nope", {}))
