"""0002 — 变量与类型：一次「假」tool_call。

读这个文件时对照 Java：
- 不用先声明类型；运行时用 type() / isinstance() 查看
- dict ≈ Map；list ≈ List
- f-string ≈ 更方便的字符串格式化

运行（先激活 venv）：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0002-vars\\tool_call.py
"""

# --- 标量：配置里最常见的几种 ---
model = "gpt-ish-local"  # str
temperature = 0.2  # float
max_tokens = 512  # int
stream = False  # bool

# --- 序列：工具清单 ---
tools = ["read_file", "shell", "rag_search"]  # list[str]

# --- 映射：模型返回的 tool_call 解析后几乎总是 dict ---
tool_call = {
    "name": "rag_search",
    "arguments": {
        "query": "what is a harness",
        "top_k": 3,  # 注意：这里是 int，不是 "3"
    },
}

print(f"model={model} temp={temperature} stream={stream}")
print("types:", type(model), type(max_tokens), type(tools), type(tool_call))
print("tool:", tool_call["name"])
print("query:", tool_call["arguments"]["query"])
print("known tools:", ", ".join(tools))
print("isinstance dict?", isinstance(tool_call, dict))

# top_k 若被弄成字符串，后面做数值比较会埋雷（见 sibling 文件）
print("top_k raw:", tool_call["arguments"]["top_k"], type(tool_call["arguments"]["top_k"]))
