"""对比 data= 与 json= 两种 POST 身体（不联网）。

本脚本用 Request.prepare()「准备但不发送」请求，只打印会发出去的
Content-Type 和 Body，帮助理解为何 chat API 要用 json= 而不是 data=。

阅读顺序：在 examples.py 的 show_post_json 之前或之后均可；
不依赖 fake_api_server。
"""

from __future__ import annotations

import json

import requests


def main() -> None:
    # 和 tool_call 形状类似的 dict，便于联想 Agent 场景
    payload = {"name": "rag_search", "arguments": {"top_k": 3}}

    # requests.Request：描述「打算发什么请求」（method、url、json/data、headers…）
    # .prepare() → PreparedRequest（已准备好的请求包，但还没发出去）
    #
    # PreparedRequest 是什么：
    #   - requests 库里「组装完毕、随时可以发送」的请求对象
    #   - 字段包括 method、url、headers、body 等——和真正发出去前一模一样
    #   - 本脚本只 prepare 不 send，用来观察 json= vs data= 差在哪
    #   - 日常写法 requests.post(...) 内部也会先 prepare 再发到网络
    #
    # 和 Response 对照：PreparedRequest = 出门前的信封；Response = 对方寄回来的回信
    # --- 写法 A：Request + prepare（本脚本专用，第一次见正常）---
    # 和 examples.py 的 requests.post(url, json=..., timeout=...) 不是同一层 API：
    #
    #   requests.post(...)     → 描述 + 准备 + 立刻联网发送（一步到位）
    #   requests.Request(...).prepare() → 只「描述 + 准备」，不发送
    #
    # 第 1 个参数 "POST" 是 HTTP 方法名（还有 GET/PUT/DELETE…），不是函数名 post。
    # timeout 只在「真要发出去、要等响应」时需要；prepare() 不联网，故这里没有 timeout。
    req_json = requests.Request(
        "POST",  # HTTP 方法
        "http://example.invalid/v1",  # URL；故意无效域名——我们根本不 send
        json=payload,  # 关键字 json=：自动 dumps + Content-Type: application/json
    ).prepare()  # 得到 PreparedRequest；若真要发：session.send(req_json, timeout=5)

    req_data = requests.Request(
        "POST",  # 同样是 HTTP 方法，不是 requests.post 函数
        "http://example.invalid/v1",
        data=payload,  # 关键字 data= 且传 dict：走表单编码，不是 JSON API
    ).prepare()

    print("=== json= 参数 ===")
    # PreparedRequest.headers / .body：即将发出的头与正文（已编码好的形态）
    print("Content-Type:", req_json.headers.get("Content-Type"))
    print("Body:", req_json.body)

    print("=== data= 传 dict ===")
    print("Content-Type:", req_data.headers.get("Content-Type"))
    print("Body:", req_data.body)

    print("=== 手动 dumps + data= 字符串（接近 json=）===")
    # 第三案：自己 dumps，再当普通字符串 body 发，并手写 Content-Type
    # 效果接近 json=，但步骤多、易忘设头——所以 API 客户端优先 json=
    manual = requests.Request(
        "POST",
        "http://example.invalid/v1",
        data=json.dumps(payload),  # data= 这里收的是 str，不是 dict
        headers={"Content-Type": "application/json"},
    ).prepare()
    print("Content-Type:", manual.headers.get("Content-Type"))
    print("Body:", manual.body)


if __name__ == "__main__":
    main()
