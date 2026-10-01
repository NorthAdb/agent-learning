"""0003 — 最小 Agent tool loop（if + while）。

读代码时抓住三件事：
1. while：不知道要转几圈，直到「模型说结束」或触顶
2. if / elif：根据 tool 名字走不同分支（Java 里像 switch）
3. for：遍历本轮返回的多个 tool_calls

这不是真 LLM，用假模型按剧本吐 tool_call，专门练控制流。

运行：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0003-control-flow\\mini_agent_loop.py
"""

from __future__ import annotations

# 假工具：名字 -> 可调用对象
TOOLBOX = {
    "read_file": lambda path: f"[file:{path}] once upon a harness...",
    "rag_search": lambda query, top_k=3: [
        {"score": 0.91, "text": "Harness = tools + context + permissions"},
        {"score": 0.80, "text": f"query={query!r} top_k={top_k}"},
    ][:top_k],
    "shell": lambda cmd: f"$ {cmd}\n(ok)",
}


def run_tool(name: str, arguments: dict):
    """分支：未知工具要显式失败，不能默默吞掉。"""
    if name not in TOOLBOX:
        return {"ok": False, "error": f"unknown tool: {name}"}
    try:
        result = TOOLBOX[name](**arguments)
        return {"ok": True, "result": result}
    except TypeError as e:
        # 参数对不上（缺字段 / 类型错）时常见
        return {"ok": False, "error": str(e)}


def fake_model(turn: int) -> dict:
    """假模型剧本：第 0 轮调工具，第 1 轮再调，第 2 轮给最终回答。"""
    script = [
        {
            "type": "tool_calls",
            "tool_calls": [
                {"name": "rag_search", "arguments": {"query": "what is harness", "top_k": 2}},
                {"name": "read_file", "arguments": {"path": "MISSION.md"}},
            ],
        },
        {
            "type": "tool_calls",
            "tool_calls": [
                {"name": "shell", "arguments": {"cmd": "git status -sb"}},
            ],
        },
        {
            "type": "final",
            "content": "Harness 给模型手和眼；loop 负责反复 tool -> observe。",
        },
    ]
    if turn >= len(script):
        return {"type": "final", "content": "(stopped: no more script)"}
    return script[turn]


def agent_loop(max_turns: int = 5) -> None:
    turn = 0
    # while：停止条件在循环内用 break；max_turns 防无限转
    while turn < max_turns:
        print(f"\n=== turn {turn} ===")
        msg = fake_model(turn)

        if msg["type"] == "final":
            print("FINAL:", msg["content"])
            break

        if msg["type"] == "tool_calls":
            # for：一轮里可能并行/串行多个工具
            for call in msg["tool_calls"]:
                name = call["name"]
                args = call["arguments"]
                print(f"CALL {name}({args})")
                out = run_tool(name, args)
                if out["ok"]:
                    print("  OK ->", out["result"])
                else:
                    print("  ERR ->", out["error"])
            turn += 1
            continue

        # 防御分支：协议变了也不能静默
        print("unknown message type:", msg.get("type"))
        break
    else:
        # while-else：循环「没有被 break」才走这里（触顶）
        print("\nstopped: hit max_turns")


if __name__ == "__main__":
    agent_loop()
