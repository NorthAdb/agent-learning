from pathlib import Path


def load_documents(directory: Path) -> list[dict[str, str]]:
    """加载目录下的 Markdown 和文本文件，跳过无法读取的单个文件。"""
    documents: list[dict[str, str]] = []
    for path in sorted(directory.iterdir()):
        if path.suffix not in {".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8").strip()
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            print(f"跳过 {path.name}: {type(error).__name__}")
            continue
        if not text:
            continue
        documents.append({"source": path.name, "text": text})
    return documents


def main() -> None:
    directory = Path(__file__).parent
    documents = load_documents(directory)
    for document in documents:
        print(f"[{document['source']}] {document['text']}")


if __name__ == "__main__":
    main()
