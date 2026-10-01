"""0004 — 四个小例：函数参数怎么传。

先读这个文件，再运行。每个例子都对应课件「系统讲解」里的同名小节。

运行（先激活 venv）：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0004-functions-modules\\examples.py
"""

from __future__ import annotations


print("=== 例1：def + return（没有 return 就得到 None）===")


def wrap_observation(text: str) -> dict:
    """工具跑完后，harness 通常要把结果包成结构化观察。"""
    return {"role": "tool", "content": text}


def log_only(text: str) -> None:
    """故意不 return：调用方拿到的是 None。

    没有 return ≠ 跳过函数体。调用时这行 print 照常执行（副作用）；
    函数结束后才交回 None。所以下一行会先看到 (logged)，再看到 None。
    """
    print("  (logged)", text)


obs = wrap_observation("harness = tools + context")
print("wrap_observation ->", obs)
print("log_only ->", log_only("side effect only"))  # 先执行 log_only，再打印它的返回值 None


print("\n=== 例2：位置参数 / 关键字参数 / 默认值 ===")


def call_model(prompt: str, temperature: float = 0.2, max_tokens: int = 256) -> str:
    """temperature / max_tokens 有默认值，调用时可以省略。"""
    return f"prompt={prompt!r} temp={temperature} max_tokens={max_tokens}"


print(call_model("what is RAG"))
print(call_model("what is RAG", 0.0))
print(call_model("what is RAG", temperature=0.0, max_tokens=64))
# 关键字参数可以换顺序；位置参数必须在关键字前面
print(call_model(max_tokens=32, prompt="short", temperature=0.1))


print("\n=== 例3：** 把 dict 展开成关键字参数（tool call 的核心）===")


def rag_search(query: str, top_k: int = 3) -> list:
    return [{"query": query, "top_k": top_k}]


arguments = {"query": "what is harness", "top_k": 2}
# 下面两行完全等价：
print("explicit:", rag_search(query="what is harness", top_k=2))
print("unpacked:", rag_search(**arguments))


print("\n=== 例4：可变默认值是共享的（和 Java 直觉相反）===")


def bad_collect(item: str, bucket: list | None = []) -> list:
    """错误示范：默认 list 只创建一次，多次调用会互相污染。"""
    bucket.append(item)
    return bucket


def good_collect(item: str, bucket: list | None = None) -> list:
    """正确：可变对象默认用 None，函数里再新建。"""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print("bad 1st:", bad_collect("a"))
print("bad 2nd:", bad_collect("b"))  # 期望 ['b']，实际 ['a', 'b']
print("good 1st:", good_collect("a"))
print("good 2nd:", good_collect("b"))


print("\n=== 例4 对照：history=[] 会在两次 agent 调用之间串会话 ===")


def leaky_turn(user_msg: str, history: list | None = []) -> list:
    """错误：默认 list 只创建一次，独立对话会互相污染。"""
    history.append(user_msg)
    return history


def safe_turn(user_msg: str, history: list | None = None) -> list:
    """正确：没传入时每次新建；传入同一份 list 时才累加。"""
    if history is None:
        history = []
    history.append(user_msg)
    return history


print("leaky A:", leaky_turn("用户A：检索 harness"))
print("leaky B:", leaky_turn("用户B：你好"))  # 带着 A
print("safe A:", safe_turn("用户A：检索 harness"))
print("safe B:", safe_turn("用户B：你好"))    # 只有 B

# 同一场对话：自己拿着 list 传入，才应该累加
session: list = []
print("same session 1:", safe_turn("第一句", history=session))
print("same session 2:", safe_turn("第二句", history=session))
