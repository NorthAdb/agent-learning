"""0009 例程：标注长什么样、运行时会不会强制、None 与 Any。"""

from __future__ import annotations

from typing import Any, get_type_hints


def greet(name: str) -> str:
    return f"hello, {name}"


def pick_top_k(hits: list[dict[str, float]], top_k: int = 3) -> list[dict[str, float]]:
    return sorted(hits, key=lambda h: h["score"], reverse=True)[:top_k]


def load_optional_label(path: str | None = None) -> str:
    """path 可为 None；返回用于日志的标签字符串。"""
    if path is None:
        return "default-config"
    return path


def show_annotations() -> None:
    print("greet 的标注:", greet.__annotations__)
    print("pick_top_k 的标注:", pick_top_k.__annotations__)
    hints = get_type_hints(pick_top_k)
    print("get_type_hints:", hints)


def show_runtime_not_enforced() -> None:
    result = greet("agent")
    print("正常调用:", result)


def show_any_at_boundary(raw: Any) -> dict[str, Any]:
    """JSON 刚 load 出来时，用 Any 承认「形状未验证」。"""
    if not isinstance(raw, dict):
        raise TypeError("根节点必须是 dict")
    return raw


def main() -> None:
    show_annotations()
    print("---")
    show_runtime_not_enforced()
    print("---")
    print("None 默认:", load_optional_label())
    print("有路径:", load_optional_label("agent_config.json"))
    print("---")
    payload = show_any_at_boundary({"model": "demo"})
    print("边界后:", payload)


if __name__ == "__main__":
    main()
