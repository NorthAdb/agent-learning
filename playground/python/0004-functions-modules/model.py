"""假模型：按 turn 返回剧本。真实世界这里是 LLM API。

拆成模块的原因：换模型适配器时，loop 和 tools 都不用动。
"""

from __future__ import annotations


def fake_model(turn: int) -> dict:
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
