"""Agent loop：只负责「问模型 → 调工具 → 再问」的控制流。

工具实现见 tools.py，模型剧本见 model.py。
"""

from __future__ import annotations

from model import fake_model
from tools import run_tool


def agent_loop(max_turns: int = 5) -> None:
    turn = 0
    while turn < max_turns:
        print(f"\n=== turn {turn} ===")
        msg = fake_model(turn)

        if msg["type"] == "final":
            print("FINAL:", msg["content"])
            break

        if msg["type"] == "tool_calls":
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

        print("unknown message type:", msg.get("type"))
        break
    else:
        print("\nstopped: hit max_turns")
