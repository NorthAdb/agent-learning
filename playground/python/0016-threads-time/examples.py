"""0016 — Thread + Lock + datetime + asdict + global。对照 North s13 / s14 / s12。

为何学：
  Thread   → 慢命令丢后台，主 loop 不堵死
  Lock     → 多线程改同一 dict 不损坏
  datetime → 记时间 / 调度判断「现在几点」
  asdict   → dataclass → dict，才能 json.dumps
  global   → 函数里给模块级计数器重新赋值（见主脚本）

运行：
  cd d:\\agent-learning\\playground\\python
  python 0016-threads-time\\examples.py
"""

from __future__ import annotations

import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta


print("=== 例1：Thread + daemon；Lock 保护共享 dict ===")
# Thread(target=worker, args=(...), daemon=True)
#   target=worker  → 函数对象，不要写成 worker()
#   args=(...)     → 元组；单元素必须 ("x",)
#   daemon=True    → 主进程退出时丢掉该线程
#   start()        → 立刻返回，不等 worker 结束
#   join(timeout=) → 可选：主线程在这里等结果
#
# Lock：多线程读写同一 dict 时，with lock: 包住读和写
# sleep / 慢活放锁外，别堵住别人

results: dict[str, str] = {}
lock = threading.Lock()


def worker(task_id: str, delay: float) -> None:
    time.sleep(delay)  # 锁外
    with lock:
        results[task_id] = f"done after {delay}s"


t = threading.Thread(target=worker, args=("bg_1", 0.15), daemon=True)
t.start()
print("主线程没等（往往还是空）:", results)
t.join(timeout=2)
print("join 之后:", results)


print("\n=== 例2：datetime.now / timedelta / strftime / isoformat ===")
# datetime.now()              → 本地现在（datetime 对象）
# timedelta(minutes=1)        → 一段时间，可与 now 加减
# strftime("%Y-...")          → 自定义格式字符串（给人看）
# isoformat(timespec="seconds") → ISO 标准字符串（给程序存 / JSON）

now = datetime.now()
print("strftime:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("一分钟后:", (now + timedelta(minutes=1)).strftime("%H:%M:%S"))
print("isoformat:", now.isoformat(timespec="seconds"))


print("\n=== 例3：asdict 把 dataclass 变成可 json 的 dict ===")
# json.dumps 只认 dict/list/数字/字符串/bool/None
# dataclass 实例要先 asdict → 普通 dict，再 dumps（0008）


@dataclass
class Task:
    id: str
    status: str
    owner: str | None = None


task = Task("task_1", "pending")
print("asdict:", asdict(task))
# json.dumps(task)  → TypeError；json.dumps(asdict(task)) → OK
