"""0011：看清「当前用的是哪个 Python / 包装在哪」+ 本仓库路径对照。

不装新包；只打印解释器、venv、site-packages，并标出本脚本在练习场中的位置。
读 Agent 仓库 README 时，第一步常是确认 venv 是否激活对。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 本脚本文件路径 → 可推算练习场根与 .venv 邻居关系
THIS_FILE = Path(__file__).resolve()
LESSON_DIR = THIS_FILE.parent  # .../0011-packages
PLAYGROUND_ROOT = LESSON_DIR.parent  # .../playground/python
EXPECTED_VENV = PLAYGROUND_ROOT / ".venv"
EXPECTED_SITE_PACKAGES = EXPECTED_VENV / "Lib" / "site-packages"


def main() -> None:
    print("=== 本仓库路径（对照课件 §2.2）===")
    print("本脚本:     ", THIS_FILE)
    print("课目录:     ", LESSON_DIR)
    print("练习场根:   ", PLAYGROUND_ROOT)
    print("期望 .venv: ", EXPECTED_VENV)
    print("期望 site-packages:", EXPECTED_SITE_PACKAGES)

    print("\n=== sys（当前进程用的 Python）===")
    # sys.executable：正在跑本脚本的 python.exe 完整路径
    print("executable:", sys.executable)
    # sys.prefix：该 Python 的「环境根」；venv 激活后应接近 EXPECTED_VENV
    print("prefix:    ", sys.prefix)
    print("version:   ", sys.version.split()[0])

    print("\n=== venv 是否对齐本练习场 ===")
    exe_path = Path(sys.executable)
    prefix_path = Path(sys.prefix)
    using_playground_venv = EXPECTED_VENV in exe_path.parents or exe_path == EXPECTED_VENV / "Scripts" / "python.exe"
    print("executable 在 playground .venv 下:", using_playground_venv)
    if not using_playground_venv:
        print("提示：先 cd playground\\python，再 .\\.venv\\Scripts\\Activate.ps1")
        print("或不激活，直接用: .\\.venv\\Scripts\\python.exe 本脚本.py")

    print("\n=== site-packages（第三方包装在哪）===")
    # site 模块：列出当前环境搜索第三方包的目录
    import site

    for p in site.getsitepackages():
        marker = "  ← requests 等第三方包在这里" if "site-packages" in p else ""
        print(f"  {p}{marker}")


if __name__ == "__main__":
    main()
