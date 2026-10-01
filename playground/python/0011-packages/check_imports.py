"""0011：按 requirements 清单尝试 import——验证「装上了没有」。

import 成功 ≠ pip 里一定有（标准库也能 import）；
本脚本配合 requirements-agent-demo.txt，检查第三方包是否在当前 venv 可用。
"""

from __future__ import annotations

import importlib
from pathlib import Path

from parse_requirements import load_requirements


def try_import(module_name: str) -> tuple[bool, str]:
    """尝试 import 模块；返回 (成功与否, 说明)。

    pip 包名与 import 名有时不同（如 pillow → PIL），本课清单用常见一致名。
    """
    try:
        importlib.import_module(module_name)
        return True, "ok"
    except ImportError as error:
        return False, str(error)


def main() -> None:
    req_path = Path(__file__).parent / "requirements-agent-demo.txt"
    packages = load_requirements(req_path)
    print("=== import 检查 ===")
    for name in packages:
        ok, detail = try_import(name)
        mark = "OK" if ok else "MISSING"
        print(f"  [{mark}] {name} — {detail}")
    print("\n若 MISSING：先激活 .venv，再 python -m pip install -r requirements-agent-demo.txt")


if __name__ == "__main__":
    main()
