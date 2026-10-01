"""0010 例程：GET/POST、Response 零件、timeout、raise_for_status。

本课「裸 requests」练习：每个函数对应课件一个知识点。
封装版见 http_agent_client.py；对方服务见 fake_api_server.py。

先另开终端启动假 API：
  python 0010-requests\\fake_api_server.py
"""

from __future__ import annotations

import requests

# 假服务根地址；与 fake_api_server 的 HOST:PORT 一致
BASE = "http://127.0.0.1:8765"


def show_get_basics() -> None:
    """GET + params：查询参数会拼到 URL 上（对应 fake_api do_GET /rag/search）。

    Response 四件（本函数都会摸到）：
      status_code → 数字状态（200、404…）
      url         → 实际发出的完整 URL（params 已编码拼好）
      headers     → 响应头 dict-like
      text        → 正文原始字符串
      json()      → 正文解析成 dict/list（须先确认状态或 raise_for_status）
    """
    response = requests.get(
        f"{BASE}/rag/search",  # 第 1 参数：完整 URL（到 path，不含查询串）
        params={"q": "harness", "top_k": 2},  # 查询串 → ?q=harness&top_k=2
        timeout=5,  # 最多等 5 秒；不设可能永久卡住
    )
    print("status_code:", response.status_code)
    print("url 实际请求:", response.url)  # 可核对 params 是否拼对
    print("headers Content-Type:", response.headers.get("Content-Type"))
    print("text 前 80 字:", response.text[:80])  # 原始 JSON 字符串片段
    data = response.json()  # 松散 dict；键写错要到运行时才 KeyError
    print("json() 类型:", type(data).__name__, "hits=", len(data["hits"]))


def show_post_json() -> None:
    """POST json=：自动序列化并设 Content-Type: application/json。

    参数对照（必看）：
      第 1 个位置参数 = 完整 URL 字符串
      json=...         = 请求体（Python dict → JSON），关键字名必须是 json
      timeout=5        = 最多等 5 秒
    不要写成 requests.post(url, payload)——第二个位置参数不是 JSON 身体。

    对应 fake_api_server do_POST /v1/chat/completions。
    """
    payload = {
        "model": "demo-model",
        "messages": [{"role": "user", "content": "什么是 RAG？"}],
    }
    response = requests.post(
        f"{BASE}/v1/chat/completions",  # url
        json=payload,  # body：关键字 json=，不是第二个位置参数
        # headers={"Authorization": "Bearer ..."},  # 真 API 时加；假服务不校验
        timeout=5,
    )
    response.raise_for_status()  # 非 2xx → HTTPError；应在 json() 之前
    body = response.json()
    # 假 API 故意模仿 OpenAI：choices[0].message.content
    content = body["choices"][0]["message"]["content"]
    print("assistant:", content)


def show_status_three_ways() -> None:
    """状态码三案：看数字 / raise_for_status / 捕获 HTTPError（对齐 0007 边界）。"""
    # 案 1：只读数字，不抛异常——requests 默认「宽松」
    ok = requests.get(f"{BASE}/health", timeout=5)
    print("健康检查 status:", ok.status_code)

    # 案 2：显式让失败变异常（推荐在工具边界使用）
    bad = requests.get(f"{BASE}/status/404", timeout=5)
    print("404 的 status:", bad.status_code)  # 仍是 404，还没抛
    try:
        bad.raise_for_status()  # 这里才抛 requests.HTTPError
    except requests.HTTPError as error:
        print("raise_for_status 捕获:", type(error).__name__, error)

    # 案 3：有 JSON body ≠ 成功；错误页也可能是合法 JSON
    err_body = bad.json()
    print("404 的 JSON body:", err_body)


def show_timeout_trap() -> None:
    """timeout 三案之一：单浮点 = 连接+读取总超时上限。

    0.001 秒极短，几乎必然 Timeout；演示为何 Agent 工具必须设 timeout。
    """
    try:
        requests.get(f"{BASE}/health", timeout=0.001)
    except requests.Timeout as error:
        print("Timeout 类异常:", type(error).__name__, "—", error)


def main() -> None:
    # 启动自检：连不上假 API 时给出明确提示，而不是后面莫名失败
    try:
        requests.get(f"{BASE}/health", timeout=2).raise_for_status()
    except requests.RequestException as error:
        raise SystemExit(
            "连不上假 API。请先另开终端运行：\n"
            "  python 0010-requests\\fake_api_server.py\n"
            f"底层原因: {error}"
        ) from error

    show_get_basics()
    print("---")
    show_post_json()
    print("---")
    show_status_three_ways()
    print("---")
    show_timeout_trap()


if __name__ == "__main__":
    main()
