# 进 North 前一次性补齐 Python（全套 code.py 扫描）

扫过 `learn-claude-code-north` 根目录 20 个 `s*/code.py`：Day19 的 `__slots__` / `@property` / `@staticmethod` **全程未出现**；但 s01 起就有 `getattr`、`subprocess.run`，s02 起有 `glob`，后半有 `re`、`ast.literal_eval`、`threading`、`datetime`。用户要求不要因「早期用不到」跳过、也不要学到一半再倒回来。阶段 0 在进心智模型之前加 0013–0016。

## Implications
- 0012 仍只负责 Day18 + dataclass；Day19 进 0013
- 0014–0016 按 North 真实用法补标准库，不补 async（20 章都没有）
- Django / 爬虫 / ML 仍不排
- 速查 / GLOSSARY / path / 100-Days 对照已扩到 0013–0016；阶段 1 仍等这四课过关后再开

