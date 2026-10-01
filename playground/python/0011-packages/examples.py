"""0011 例程入口：按顺序演示 venv 上下文 → 读 requirements → import 检查 → pip 命令。

无需联网（pip list/show 只读本地元数据）。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    here = Path(__file__).parent
    scripts = [
        "show_venv_context.py",
        "parse_requirements.py",
        "check_imports.py",
        "pip_commands_demo.py",
    ]
    for name in scripts:
        path = here / name
        print("=" * 60)
        print(f"运行 {name}")
        print("=" * 60)
        subprocess.run([sys.executable, str(path)], check=True)
        print()


if __name__ == "__main__":
    main()
