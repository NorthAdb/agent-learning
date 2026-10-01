"""0008 主脚本 A：读写 Agent / RAG 配置 JSON。"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "agent_config.json"
RUNTIME_PATH = BASE_DIR / "runtime_state.json"


def load_config(path: Path) -> dict:
    """从磁盘加载配置；失败时转换语义上抛。"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"配置文件不存在: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"配置不是合法 JSON: {path}") from error

    if not isinstance(data, dict):
        raise TypeError("配置根节点必须是对象(dict)")
    return data


def save_config(path: Path, data: dict) -> None:
    """把配置漂亮地写回磁盘（中文可读）。"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def summarize_config(config: dict) -> dict:
    """抽出 Agent loop / RAG 关心的字段，并做类型归一化。"""
    rag = config.get("rag", {})
    if not isinstance(rag, dict):
        raise TypeError("rag 必须是对象")

    top_k = int(rag.get("top_k", 3))
    enabled = bool(rag.get("enabled", False))
    tools = config.get("allowed_tools", [])
    if not isinstance(tools, list):
        raise TypeError("allowed_tools 必须是数组")

    return {
        "model": config.get("model", "unknown"),
        "max_turns": int(config.get("max_turns", 4)),
        "rag_enabled": enabled,
        "top_k": top_k,
        "knowledge_dir": str(rag.get("knowledge_dir", "docs")),
        "allowed_tools": [str(name) for name in tools],
    }


def main() -> None:
    config = load_config(CONFIG_PATH)
    summary = summarize_config(config)
    print("=== loaded summary ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 模拟一次运行后写回状态（不是覆盖主配置）
    runtime = {
        "last_model": summary["model"],
        "turns_used": 2,
        "last_tool": "rag_search",
        "ok": True,
    }
    save_config(RUNTIME_PATH, runtime)
    print("已写入运行状态:", RUNTIME_PATH.name)

    # 再读回来确认往返
    again = load_config(RUNTIME_PATH)
    print("=== runtime reload ===")
    print(again)


if __name__ == "__main__":
    main()
