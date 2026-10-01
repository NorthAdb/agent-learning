from pathlib import Path


BASE_DIR = Path(__file__).parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge.txt"


def show_path_anchors() -> None:
    """三种路径锚点，并对照 exists（有没有）与 resolve（绝对路径）。"""
    print("当前工作目录(cwd):", Path.cwd())
    print("脚本所在目录:", BASE_DIR)
    print("相对名 'knowledge.txt' 会相对 cwd 查找")
    print("脚本目录拼接:", KNOWLEDGE_FILE)
    print("exists → 磁盘上有没有:", KNOWLEDGE_FILE.exists())
    print("resolve → 规范后的绝对路径:", KNOWLEDGE_FILE.resolve())
    missing = BASE_DIR / "no-such.txt"
    print("缺失文件 exists:", missing.exists())
    print("缺失文件 resolve:", missing.resolve())


def show_file_modes() -> None:
    """演示读取、覆盖写入和追加写入的差别。"""
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        print("读取到的原文:")
        print(file.read())

    log_file = BASE_DIR / "run.log"
    with open(log_file, "w", encoding="utf-8") as file:
        file.write("第一次写入：w 会覆盖旧内容\n")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write("第二次写入：a 会追加到末尾\n")
    print("日志已写入:", log_file.name)


def read_lines_safely(path: Path) -> list[str]:
    """标准范式示例：窄 try + 具体 except + else；失败时转换后上抛。"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError as error:
        # 策略 2：补业务语义，保留原因链，交给调用方决定
        raise FileNotFoundError(f"知识文件不存在: {path}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"知识文件不是有效的 UTF-8 文本: {path}") from error
    else:
        print(f"成功读取 {len(lines)} 行")
        return lines


def show_exception_strategies() -> None:
    """对照标准范式决策表：能恢复 / 改语义上抛 / 不捕获。"""
    missing = BASE_DIR / "missing.txt"

    # 策略 1：局部恢复 —— 缺文件时继续，用空结果顶上
    try:
        text = missing.read_text(encoding="utf-8")
    except FileNotFoundError:
        text = ""
    print("策略1 局部恢复后的 text:", repr(text))

    # 策略 2：转换后上抛 —— 补充业务语义，仍让上层决定
    try:
        read_lines_safely(missing)
    except FileNotFoundError as error:
        print("策略2 转换上抛:", error)

    # 策略 3：不捕获 —— 调用方必须自己处理，否则程序中断
    print("策略3 不捕获：交给调用方；本课在 main 里演示捕获")


def main() -> None:
    show_path_anchors()
    print("---")
    show_file_modes()
    print("---")
    lines = read_lines_safely(KNOWLEDGE_FILE)
    print("清洗后的行:", lines)
    print("---")
    show_exception_strategies()


if __name__ == "__main__":
    main()
