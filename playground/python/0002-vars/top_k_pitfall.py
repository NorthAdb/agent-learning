"""0002 对照：把 top_k 弄成 str 会发生什么。

先跑 tool_call.py，再跑本文件，对比打印。
Agent/RAG 代码里「看起来像数字的字符串」是高频坑。
"""

tool_call = {
    "name": "rag_search",
    "arguments": {
        "query": "what is a harness",
        "top_k": "3",  # 错：JSON 里有时是字符串
    },
}

top_k = tool_call["arguments"]["top_k"]

print("top_k =", repr(top_k), "type =", type(top_k))

# 和数字比：Python 3 直接 TypeError；有的库会默默转错
try:
    print("top_k > 5 ?", top_k > 5)
except TypeError as e:
    print("比较失败:", e)

# 和字符串比：语法能跑，语义经常错
print("top_k > '5' ?", top_k > "5")  # 字典序，不是数值大小

# 正确做法：显式转换 + 校验
fixed = int(top_k)
print("fixed =", fixed, "fixed > 5 ?", fixed > 5)
