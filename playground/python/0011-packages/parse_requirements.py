"""0011：读 requirements 文件——不调用 pip，只解析文本。

学会认 requirements.txt 每一行长什么样；
真安装用 pip install -r，本脚本只「读清单」。
"""

from __future__ import annotations

from pathlib import Path


def parse_requirements_line(line: str) -> str | None:
    """把一行解析成包名；注释/空行返回 None。

    本课只处理简单行：name 或 name>=version（不展开 extras、环境标记）。
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    # 取运算符前的名字：requests>=2.31 → requests
    for sep in ("==", ">=", "<=", "~=", "!=", ">", "<"):
        if sep in stripped:
            return stripped.split(sep, 1)[0].strip()
    return stripped


def load_requirements(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    names: list[str] = []
    for line in text.splitlines():
        name = parse_requirements_line(line)
        if name:
            names.append(name)
    return names


def main() -> None:
    req_path = Path(__file__).parent / "requirements-agent-demo.txt"
    print(f"读取: {req_path.resolve()}")
    packages = load_requirements(req_path)
    print("解析出的包名:", packages)
    print("\n对应安装命令（本课练习场已装过 requests，此处演示命令形状）:")
    print(f"  python -m pip install -r {req_path.name}")


if __name__ == "__main__":
    main()
