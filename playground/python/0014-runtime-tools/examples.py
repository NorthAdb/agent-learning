"""0014 — getattr / subprocess.run / glob。

为何学：North s01 起就要读 SDK 消息块、跑 bash；s02 起要按模式找文件。
三件分别解决：安全取对象属性、起子进程、通配枚举文件。

运行：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0014-runtime-tools\\examples.py
"""

from __future__ import annotations

import glob
import subprocess
from pathlib import Path


print("=== 例1：getattr —— 对象按字符串取属性，可给默认 ===")
# 解决：SDK content block 是对象（不是 dict），字段可能缺失。
# getattr 面向任意对象（list/tuple/str/dict/自定义实例都能用），
# 取的是「属性/方法名」，不是容器下标、也不是 dict 的键。
# ① obj.type          字段一定在时
# ② data["type"]      确定是 dict 时
# ③ getattr(obj, n, d) 对象 + 可能缺失 → 给默认，不崩
# 错用：dict 用点号 → AttributeError；对象用 [] → TypeError
# 口诀：身上的方法用 getattr；里面的元素用 [] / .get


class Block:
    """模仿 Anthropic 返回的 content block：是对象，不是 dict。"""

    def __init__(self, type: str, text: str | None = None) -> None:
        self.type = type
        self.text = text


obj = Block("text", "hello")
data = {"type": "text", "text": "hello"}

print("① 对象点号:     ", obj.type)
print("② dict 下标:    ", data["type"])
print("③ getattr 默认: ", getattr(obj, "type", None), getattr(obj, "missing", None))
try:
    print(data.type)  # type: ignore[attr-defined]
except AttributeError as error:
    print("dict 用点号 ->", type(error).__name__)
try:
    print(obj["type"])  # type: ignore[index]
except TypeError as error:
    print("对象用下标 ->", type(error).__name__)


print("\n=== 例2：subprocess.run —— 起子进程并等结束 ===")
# 解决：Agent bash 工具必须真的在 OS 上跑命令，再把输出当观察。
# argv 列表更安全；North 因模型吐字符串才用 shell=True（本课不模仿注入面）。
# 三案：① returncode==0  ② 非零退出（未必抛异常） ③ 超时 → TimeoutExpired

completed = subprocess.run(
    ["python", "-c", "print('ok')"],
    capture_output=True,  # 抓住输出
    text=True,            # str 而非 bytes
    timeout=10,           # 防止卡死 agent loop
)
print("① 正常: returncode=", completed.returncode, "stdout=", completed.stdout.strip())

failed = subprocess.run(
    ["python", "-c", "raise SystemExit(2)"],
    capture_output=True,
    text=True,
    timeout=10,
)
print("② 非零退出: returncode=", failed.returncode, "(run 本身通常不抛)")

try:
    subprocess.run(
        ["python", "-c", "import time; time.sleep(30)"],
        capture_output=True,
        text=True,
        timeout=0.2,
    )
except subprocess.TimeoutExpired as error:
    print("③ 超时 ->", type(error).__name__)


print("\n=== 例3：glob —— 通配找文件名；无匹配是空，不是错 ===")
# 解决：按 *.py 等模式枚举文件路径（s02 glob 工具）。
# glob 找「哪些文件」；grep 找「文件里哪些行有某段字」——别混。
# Python 有 import glob；没有叫 grep 的标准库模块（正文搜索 → 0015 re 或调系统 grep）。
# Path.glob / glob.glob 语义同类；找不到 → []，不要当成异常。

here = Path(__file__).resolve().parent
from_path = sorted(p.name for p in here.glob("*.py"))
from_mod = sorted(Path(p).name for p in glob.glob(str(here / "*.py")))
print("Path.glob:", from_path)
print("glob.glob:", from_mod)
print("无匹配:", list(here.glob("*.nope")))
