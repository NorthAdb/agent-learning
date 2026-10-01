"""0006 小例：字符串、集合、字典。

运行：python 0006-strings-sets-dicts\\examples.py
"""

from __future__ import annotations


print("=== 例1：字符串不可变 + 清洗 ===")
raw = "  RAG: 先检索，再生成。  "
clean = raw.strip().replace("：", ":")
print("raw  =", repr(raw))
print("clean=", repr(clean))
print("parts=", clean.split(":", 1))  # 表示最多切割1次，maxsplit=1


print("\n=== 例2：split / join 做文本块 ===")
text = "Python 让 harness 读取工具结果。\nRAG 把相关知识放进上下文。"
lines = [line.strip() for line in text.splitlines() if line.strip()]
context = "\n".join(f"[{i}] {line}" for i, line in enumerate(lines, start=1))
print(context)


print("\n=== 例3：集合去重与集合运算 ===")
seen = {"rag", "tool", "rag", "memory"}
requested = {"rag", "eval", "tool"}
print("seen       =", seen)
print("交集       =", seen & requested)
print("缺少的能力 =", requested - seen)
print("是否包含 rag=", "rag" in seen)


print("\n=== 例4：字典安全读取与嵌套 tool call ===")
call = {
    "name": "rag_search",
    "arguments": {"query": "harness permission", "top_k": "3"},
}
name = call.get("name", "unknown")
args = call.get("arguments", {})
query = args.get("query", "")
top_k = int(args.get("top_k", 3))
print(name, query, top_k)


print("\n=== 例5：字典计数 + 生成式 ===")
events = ["tool", "model", "tool", "error", "tool"]
counts: dict[str, int] = {}
for event in events:
    counts[event] = counts.get(event, 0) + 1
print("counts=", counts)
print("hot=", {k: v for k, v in counts.items() if v >= 2})
