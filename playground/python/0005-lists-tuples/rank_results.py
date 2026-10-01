"""0005 主脚本 — 假 RAG 检索：候选结果的过滤、排序、截断、组装上下文。

上一课 tools.py 里的 rag_search 只返回 3 条刚好的结果，还已经排好序。
真实检索不会这么省心：候选几十上百条、分数乱序、里面混着低于阈值要丢掉的旧文档。
本脚本走一遍「拿到 hits 之后、喂给模型之前」的处理，把课件讲过的列表操作都串起来。

为什么这样写：检索层负责「找到候选」，RAG 组装层负责「挑出该用的」（过滤低分，
按分排序，截断 top_k），最后才拼成给模型的上下文块。后面读开源 agent，这一小段
反复出现。

运行：
  python 0005-lists-tuples\\rank_results.py
"""

from __future__ import annotations


def fetch_hits() -> list:
    """假装调了一次向量检索：返回乱序的候选，分数各不相同。

    真实 harness 里这是工具函数（0004 的 rag_search 那种）；这里直接造数据，
    让本脚本专注「拿到列表之后怎么处理」。
    """
    return [
        {"id": "d-03", "text": "Tool 是 harness 暴露给模型的一个可调用动作", "score": 0.72},
        {"id": "d-07", "text": "RAG：先检索知识再生成回答", "score": 0.91},
        {"id": "d-01", "text": "（过期的旧版本文档）", "score": 0.31},
        {"id": "d-09", "text": "上下文窗口装不下整本书，只能带相关片段", "score": 0.84},
        {"id": "d-02", "text": "Permission 决定工具能不能执行", "score": 0.45},
    ]


def main() -> None:
    hits = fetch_hits()

    # 1) 过滤：分数低于阈值的候选不要。列表生成式：留「分数够」的。
    threshold = 0.5
    passed = [h for h in hits if h["score"] >= threshold]

    # 2) 排序：按 score 降序。key= 告诉 sorted 用每个元素的哪个字段当排序键；
    #    reverse=True 表示降序。lambda 在 Day16 系统讲，这里先当「取键的一行」用。
    ranked = sorted(passed, key=lambda h: h["score"], reverse=True)

    # 3) 截断：只要前 top_k 条。切片，和 0004 里 hits[:top_k] 是同一条。
    top_k = 3
    top = ranked[:top_k]

    # 4) 组装上下文块：enumerate 给条目编号，解包成 (序号, 命中) 两个变量；
    #    f-string 把分数压成两位小数；join 把列好的 str 拼成一个长文本。
    lines = [f"[{i}] ({h['score']:.2f}) {h['text']}" for i, h in enumerate(top, start=1)]
    context = "\n".join(lines)

    # 每一层都打印出来，方便对照课件里每一步的输出
    print("=== 原始候选（5 条）===")
    print([h["id"] for h in hits])
    print(f"=== 过滤后（score >= {threshold}）===")
    print([h["id"] for h in passed])
    print("=== 排序后（降序）===")
    print([h["id"] for h in ranked])
    print(f"=== top {top_k} ===")
    print([h["id"] for h in top])
    print("=== 拼好的上下文块 ===")
    print(context)


if __name__ == "__main__":
    main()