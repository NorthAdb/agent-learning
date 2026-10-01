"""0011：用 subprocess 跑 pip 子命令（list / show），观察当前环境已装什么。

为什么用 python -m pip 而不是直接 pip：
  -m 保证「当前这个 python.exe」对应的 pip，避免激活错 venv 时装到别处。
"""

from __future__ import annotations

import subprocess
import sys


def run_pip(args: list[str]) -> None:
    """用当前解释器调用 pip；打印 stdout。"""
    cmd = [sys.executable, "-m", "pip", *args]
    print(f"$ {' '.join(cmd)}")
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip())
    if completed.returncode != 0:
        print(f"(exit code {completed.returncode})")


def main() -> None:
    print("=== pip list（当前环境已安装的包，节选 requests）===")
    run_pip(["list"])
    print("\n=== pip show requests（单个包的元数据）===")
    run_pip(["show", "requests"])
    print("\n提示：生成清单用 pip freeze > requirements.txt（勿把 .venv 路径写进仓库）")


if __name__ == "__main__":
    main()
