"""本地假 HTTP API（仅标准库），供 0010 离线练习。

本课主线是学客户端（requests）；本文件扮演「对方」。
逐段导读见课件 0010「fake_api_server.py 导读」。

阅读提示（不熟悉 http.server 时）：
  - 先读 main()：进程如何监听端口
  - 再读 _send_json：响应如何组包（和 response.json() 对称）
  - 再读 do_GET / do_POST：各路径如何接客户端请求

启动后监听 127.0.0.1:8765：
  GET  /health
  GET  /rag/search?q=...&top_k=3
  POST /v1/chat/completions   JSON body: {"model","messages"}
  GET  /status/404            故意返回 404
"""

from __future__ import annotations

import json
# http.server：标准库里的简易 HTTP 服务端（本课只认接口，不必深学服务器开发）
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
# urllib.parse：拆 URL、解析查询串（? 后面那一截）
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"  # 本机回环地址：只有本机进程能连，不暴露到局域网
PORT = 8765         # 端口：同一台机器上区分不同服务的编号


# BaseHTTPRequestHandler：标准库「处理一次 HTTP 请求」的基类。
# 子类重写 do_GET / do_POST；框架收到请求后会 new 一个 Handler 实例并调用对应方法。
# 每个请求里 self 就代表「这一次连接」的上下文（path、headers、rfile、wfile 等）。
class FakeAgentAPI(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        """把默认写进 stderr 的访问日志，改到 stdout 并加 [fake-api] 前缀，方便练习时观察。

        参数 format / *args / format % args：
          - 基类调用 log_message 时会传入「格式串 + 若干值」，例如：
              format = '"%s" %s %s'
              args   = ('GET /health HTTP/1.1', '200', '-')
          - *args 把多余位置参数收成元组 args。
          - format % args 是旧式字符串格式化（% 占位符），等价于把 args 填进 format：
              '"%s" %s %s' % ('GET /health HTTP/1.1', '200', '-')
            → '"GET /health HTTP/1.1" 200 -'
          - 现代写法可用 format.format(*args) 或 f-string，这里保留 % 是为兼容基类传入的格式。

        stdout / stderr（标准输出 / 标准错误）：
          - 进程的两个「默认打印出口」，终端里通常都能看到，但用途不同。
          - stdout：正常结果、普通 print() 默认写到这里。
          - stderr：警告、错误、诊断日志；和 stdout 分开，方便重定向或管道时区分。
          - 基类默认把访问日志打到 stderr；这里改用 print() → stdout，和脚本其它输出混在一起更直观。

        address_string()：基类方法，返回「谁连过来了」的可打印字符串，
        通常是客户端 IP，例如 127.0.0.1（本机 client 打本机 server 时）。
        """
        print(f"[fake-api] {self.address_string()} {format % args}")

    def _send_json(self, status: int, payload: object) -> None:
        """把 Python 对象作为 JSON 响应发回客户端（本脚本所有路由的出口）。

        self（实例方法第一个参数，调用时不用手写）：
          - 代表「正在处理这一次 HTTP 请求」的 FakeAgentAPI 实例。
          - 调用 self._send_json(200, {...}) 时，Python 自动把当前实例当作 self 传入。
          - 所以定义写 (self, status, payload) 共 3 个形参，调用只写 2 个实参。
          - self 上能访问 send_response、wfile 等基类属性，用来把响应写回**这一位**客户端。

        作用：do_GET / do_POST 里只关心「返回什么业务 dict」和「状态码多少」；
        具体怎么组 HTTP 响应（头 + 字节正文）都集中在这里，避免每个路由重复写。

        客户端（requests）那边对应关系：
          status  → response.status_code（如 200、404）
          头字段  → response.headers（Content-Type 等）
          body    → response.text / response.json() 读到的内容

        参数：
          status  HTTP 状态码整数（200 成功，400 客户端参数错，404 路径不存在）
          payload 要序列化成 JSON 的 Python 对象（通常是 dict）
        """
        # ensure_ascii=False：中文等非 ASCII 字符原样输出，不转成 \uXXXX
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        # encode("utf-8")：str → bytes；HTTP 正文在网络上走字节，不是 Python str

        # 下面三步是「手写 HTTP 响应」的标准顺序，顺序不能乱：
        self.send_response(status)  # 状态行，如 HTTP/1.0 200 OK
        # Content-Type：告诉客户端正文格式；客户端据此决定怎么解析
        self.send_header("Content-Type", "application/json; charset=utf-8")
        # Content-Length：正文有多少字节；没有它，对方可能不知道何时读完
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()  # 头发完；此后才能写 body

        # wfile（write file）：向客户端写响应体的流，类似「往 socket 里写字节」
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        """处理 GET 请求：按路径分支，最后都通过 _send_json 回 JSON。

        GET 特点：参数通常在 URL 查询串（? 后面），没有单独的大段 body。
        客户端对应：requests.get(url, params={"q": ..., "top_k": ...})
        """
        # self.path 是本次请求的「路径 + 查询串」原始字符串，例如：
        #   /rag/search?q=harness&top_k=2
        # 注意：不含 http://127.0.0.1:8765，只有 path 和 query
        parsed = urlparse(self.path)
        # parsed.path  → 纯路径，如 /rag/search
        # parsed.query → 查询串，如 q=harness&top_k=2（不含开头的 ?）

        if parsed.path == "/health":
            # 健康检查：client 启动前常先 ping 一下能否连通
            self._send_json(200, {"ok": True, "service": "fake-agent-api"})
            return  # return 结束本请求处理，不再往下匹配

        if parsed.path == "/status/404":
            # 教学用：固定路径但状态码是 404，供 examples 练 raise_for_status
            # 注意：body 仍是 JSON，所以「有 JSON」≠「成功」
            self._send_json(404, {"error": "not found", "path": parsed.path})
            return

        if parsed.path == "/rag/search":
            # parse_qs：把 q=harness&top_k=2 变成 dict[str, list]
            # 值是 list 是因为 URL 里可能出现同名参数多次（如 tag=a&tag=b）
            qs = parse_qs(parsed.query)

            # (qs.get("q") or [""])[0] 拆解：
            #   qs.get("q")     → 没有 q 时 None
            #   or [""]         → 换成单元素列表，避免后面 [0] 报错
            #   [0]             → 取第一个值（parse_qs 规定值在列表里）
            query = (qs.get("q") or [""])[0]
            top_k_raw = (qs.get("top_k") or ["3"])[0]  # 缺省 top_k=3

            try:
                # max(1, min(..., 10))：把 top_k 钳在 1～10，防止客户端传 0 或 99999
                top_k = max(1, min(int(top_k_raw), 10))
            except ValueError:
                # int("abc") 会 ValueError → 回 400（客户端参数错误，不是 500 服务端崩了）
                self._send_json(400, {"error": "top_k must be int"})
                return

            # 假文档库；真 RAG 这里会查向量库/搜索引擎，本课只模拟 hits 字段形状
            docs = [
                {"id": "d1", "score": 0.91, "text": f"Harness 把工具接在模型外：与「{query}」相关"},
                {"id": "d2", "score": 0.77, "text": "RAG 先检索再生成，减少胡编。"},
                {"id": "d3", "score": 0.61, "text": "Java 服务可通过工具/HTTP 暴露给 agent。"},
            ]
            # docs[:top_k]：列表切片，取前 top_k 条 → 对应客户端 params top_k=2 只回 2 条 hit
            self._send_json(200, {"query": query, "hits": docs[:top_k]})
            return

        # 走到这里说明 path 没匹配任何已知路由 → 404
        self._send_json(404, {"error": "unknown route", "path": parsed.path})

    def do_POST(self) -> None:  # noqa: N802
        """处理 POST 请求：从 rfile 读 JSON 身体，按路径回 JSON。

        POST 特点：业务数据常在 body 里（如 chat 的 messages），不在 URL。
        客户端对应：requests.post(url, json=payload, timeout=...)
        """
        parsed = urlparse(self.path)

        # --- 读请求体（和 GET 不同，POST 要先读 body）---
        # self.headers：客户端发来的 HTTP 头，类似 dict（键名大小写不敏感）
        # Content-Length：body 有多少字节；必须先知道长度才能正确 read
        length = int(self.headers.get("Content-Length", "0"))

        # rfile（read file）：从客户端读请求体的流
        # b"{}"：bytes 字面量；没有 body 时当空 JSON 对象
        raw = self.rfile.read(length) if length else b"{}"

        try:
            # 解码链：bytes → str（decode utf-8）→ Python 对象（json.loads）
            # or "{}"：decode 结果为空串时，loads 会报错，用 "{}" 兜底
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            # 客户端发的不是合法 JSON 文本 → 400
            self._send_json(400, {"error": "body must be JSON"})
            return

        if parsed.path == "/v1/chat/completions":
            # 边界校验：JSON 根必须是对象 {}，不能是 [] 或纯字符串
            if not isinstance(data, dict):
                self._send_json(400, {"error": "root must be object"})
                return

            # .get(key, default)：键不存在时用默认值，不抛 KeyError
            model = str(data.get("model", "demo-model"))
            messages = data.get("messages", [])

            # 从 messages 里找「最后一条 user 消息」——多轮对话时模型通常看最近 user 话
            last_user = ""
            if isinstance(messages, list):
                # reversed：从后往前遍历；break 找到第一条（即从后数第一条 user）就停
                for msg in reversed(messages):
                    if isinstance(msg, dict) and msg.get("role") == "user":
                        last_user = str(msg.get("content", ""))
                        break

            # 假回复：只截取前 80 字，避免终端刷屏
            answer = f"[fake:{model}] 收到：{last_user[:80]}"

            # 响应 JSON 形状故意模仿 OpenAI chat completion，
            # 这样 http_agent_client.chat_completion 能用同一路径解析：
            #   body["choices"][0]["message"]["content"]
            #
            # 调用 _send_json 传参方式（两个位置参数）：
            #   第 1 个  status=200           → 函数形参 status
            #   第 2 个  {...} 这一整个 dict  → 函数形参 payload
            # self._send_json：实例方法调用；self 由 Python 自动传入，不用手写
            # 大 dict 写在括号里直接当第 2 参数，不必先赋给变量
            self._send_json(
                200,
                {
                    "id": "chatcmpl-fake",
                    "object": "chat.completion",
                    "model": model,  # 上面从客户端 JSON 读出的变量，嵌进 dict
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": answer},
                            "finish_reason": "stop",
                        }
                    ],
                },
            )
            return  # 响应已发出，结束 do_POST

        self._send_json(404, {"error": "unknown route", "path": parsed.path})


def main() -> None:
    """启动假 API 并阻塞等待请求。"""
    # ThreadingHTTPServer：每个请求开一个线程处理（本课练习量很小，够用）
    # 参数 ( (host, port), Handler类 )：
    #   地址元组告诉 OS「在哪个网卡/端口监听」
    #   FakeAgentAPI 告诉框架「每个请求用哪个类来处理」
    server = ThreadingHTTPServer((HOST, PORT), FakeAgentAPI)

    print(f"Fake Agent API listening on http://{HOST}:{PORT}")
    print("Ctrl+C to stop")

    try:
        # serve_forever()：死循环接请求；本函数不会正常 return，除非被打断
        server.serve_forever()
    except KeyboardInterrupt:
        # Ctrl+C 会抛 KeyboardInterrupt，不是 Exception 子类里的「业务错误」，是用户中断
        print("\nshutting down")
        server.server_close()  # 关闭监听 socket，释放 8765 端口


if __name__ == "__main__":
    # 仅「python fake_api_server.py」时执行 main()；
    # 若别的文件 import 本模块，不会误启动服务器（常见 Python 脚本惯例）
    main()
