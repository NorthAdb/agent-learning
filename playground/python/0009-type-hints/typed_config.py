"""0009 主脚本 A：给 0008 配置加载补上类型标注。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR.parent / "0008-json" / "agent_config.json"


class RagConfig(TypedDict, total=False):
  top_k: int
  knowledge_dir: str
  enabled: bool


class AgentConfig(TypedDict, total=False):
  model: str
  max_turns: int
  rag: RagConfig
  allowed_tools: list[str]


class ConfigSummary(TypedDict):
  model: str
  max_turns: int
  rag_enabled: bool
  top_k: int
  knowledge_dir: str
  allowed_tools: list[str]


def load_config(path: Path) -> dict[str, Any]:
  """磁盘 → dict；根类型在边界用 Any，结构校验交给后续函数。"""
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


def summarize_config(config: dict[str, Any]) -> ConfigSummary:
  """把松散 dict 收成稳定字段；TypedDict 描述「我们期望的输出形状」。"""
  rag_raw = config.get("rag", {})
  if not isinstance(rag_raw, dict):
    raise TypeError("rag 必须是对象")

  tools_raw = config.get("allowed_tools", [])
  if not isinstance(tools_raw, list):
    raise TypeError("allowed_tools 必须是数组")

  return {
    "model": str(config.get("model", "unknown")),
    "max_turns": int(config.get("max_turns", 4)),
    "rag_enabled": bool(rag_raw.get("enabled", False)),
    "top_k": int(rag_raw.get("top_k", 3)),
    "knowledge_dir": str(rag_raw.get("knowledge_dir", "docs")),
    "allowed_tools": [str(name) for name in tools_raw],
  }


def main() -> None:
  config = load_config(CONFIG_PATH)
  summary = summarize_config(config)
  print("=== typed summary ===")
  for key, value in summary.items():
    print(f"  {key}: {value!r} ({type(value).__name__})")


if __name__ == "__main__":
  main()
