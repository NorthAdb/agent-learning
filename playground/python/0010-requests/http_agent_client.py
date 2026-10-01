"""0010 主脚本：把 RAG 检索与假 LLM 调用封装成带异常边界的客户端。

依赖：另开终端先跑 fake_api_server.py。

和 examples.py 的关系：
  examples 是「裸 requests」零件练习；本文件是「能当 Agent 工具用的封装层」。
  每个 HTTP 调用都能在 examples 里找到对应裸写版。
"""

from __future__ import annotations

from typing import Any

import requests

# 假 API 根地址；path 参数会拼在后面，如 BASE_URL + "/rag/search"
BASE_URL = "http://127.0.0.1:8765"
DEFAULT_TIMEOUT = 5.0  # 秒；Agent 工具几乎总要设 timeout，防止卡死 loop


class AgentHttpError(Exception):
    """工具边界对外暴露的业务错误（转换后上抛）。

    底层 requests 抛 Timeout / HTTPError / RequestException 太「系统」；
    Agent 工具层转成 AgentHttpError，上层 loop 当作 tool error 观察。
    对应 0007「转换后上抛」：raise AgentHttpError(...) from error
    """


def get_json(
    path: str,
    *,
    params: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """GET → raise_for_status → json()；失败时转成 AgentHttpError。

    path：只写路径部分，如 "/rag/search"（不含 host）
    params：查询参数，对应 requests.get(..., params=...)
    """
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, params=params, timeout=timeout)
        # 非 2xx 在这里变 HTTPError；必须在 json() 前调用
        response.raise_for_status()
        return response.json()  # 松散 dict/list，不是 Java DTO
    except requests.Timeout as error:
        raise AgentHttpError(f"请求超时: GET {path}") from error
    except requests.HTTPError as error:
        # error.response 里仍可能带着 404 的 body，供调试
        status = error.response.status_code if error.response is not None else "?"
        raise AgentHttpError(f"HTTP {status}: GET {path}") from error
    except requests.RequestException as error:
        # 连接失败、DNS 等「发不出去」类问题
        raise AgentHttpError(f"网络失败: GET {path}") from error
    except ValueError as error:
        # response.json() 在非法 JSON 时抛 ValueError / JSONDecodeError
        raise AgentHttpError(f"响应不是合法 JSON: GET {path}") from error


def post_json(
    path: str,
    payload: dict[str, Any],
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """POST JSON body → 检查状态 → 解析 JSON。

    业务层传 path + payload；映射到 requests：
      url      = BASE_URL + path
      json=    = payload   ← 关键字名必须是 json，不能写成 post(url, payload)
      timeout= = timeout
    真 API 时再加 headers={"Authorization": "Bearer ..."}。
    """
    url = f"{BASE_URL}{path}"
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as error:
        raise AgentHttpError(f"请求超时: POST {path}") from error
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "?"
        raise AgentHttpError(f"HTTP {status}: POST {path}") from error
    except requests.RequestException as error:
        raise AgentHttpError(f"网络失败: POST {path}") from error
    except ValueError as error:
        raise AgentHttpError(f"响应不是合法 JSON: POST {path}") from error


def rag_search(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """调用假 RAG 检索，返回 hits 列表（每项含 id / score / text）。

    对应 fake_api_server do_GET /rag/search 和 examples show_get_basics。
    """
    data = get_json("/rag/search", params={"q": query, "top_k": top_k})
    if not isinstance(data, dict):
        raise TypeError("rag 响应根必须是对象")
    hits = data.get("hits", [])
    if not isinstance(hits, list):
        raise TypeError("hits 必须是数组")
    # 过滤非 dict 项，避免后面 hit.get 崩掉
    return [h for h in hits if isinstance(h, dict)]


def chat_completion(user_text: str, model: str = "demo-model") -> str:
    """调用假 chat API，返回助手文本字符串。

    对应 fake_api_server do_POST /v1/chat/completions 和 examples show_post_json。
    响应路径：choices[0].message.content（模仿 OpenAI 形状）
    """
    body = post_json(
        "/v1/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": user_text}],
        },
    )
    if not isinstance(body, dict):
        raise TypeError("chat 响应根必须是对象")
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("choices 缺失或为空")
    first = choices[0]
    if not isinstance(first, dict):
        raise TypeError("choice 必须是对象")
    message = first.get("message", {})
    if not isinstance(message, dict):
        raise TypeError("message 必须是对象")
    return str(message.get("content", ""))


def main() -> None:
    """演示最小 RAG 链路：检索 → 拼上下文 → chat → 故意 404。"""
    try:
        hits = rag_search("Java 如何接入 Agent", top_k=2)
        print("=== RAG hits ===")
        for hit in hits:
            print(f"  [{hit.get('id')}] score={hit.get('score')} {hit.get('text')}")

        # 0006 join：把多条 hit 的 text 拼成一段上下文
        context = "\n".join(str(h.get("text", "")) for h in hits)
        answer = chat_completion(f"根据资料回答：{context}\n问题：Java 如何接入？")
        print("=== LLM answer ===")
        print(answer)

        # 演示失败路径：404 应变成 AgentHttpError，而不是裸 HTTPError
        try:
            get_json("/status/404")
        except AgentHttpError as error:
            print("=== expected tool error ===")
            print(error)
    except AgentHttpError as error:
        raise SystemExit(f"工具调用失败: {error}") from error


if __name__ == "__main__":
    main()
