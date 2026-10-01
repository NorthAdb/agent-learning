"""0016 主脚本：最小后台任务表（s13 的缩影，不调模型）。

对照：
  Thread(daemon) 派发慢活；Lock 保护 jobs；
  datetime 记 started_at；asdict 做快照；
  global _counter：函数里给模块级变量重新赋值必须写 global。

global 三案提醒：
  ① _counter += 1     → 要 global
  ② 只读 _counter     → 不必
  ③ jobs[id] = ...    → 不必（改对象内部）

运行：
  cd d:\\agent-learning\\playground\\python
  python 0016-threads-time\\background_jobs.py
# 期望：immediate 多为 running；later 为 completed
"""

from __future__ import annotations

import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Job:
    id: str
    status: str
    started_at: str
    output: str | None = None


jobs: dict[str, Job] = {}
lock = threading.Lock()
_counter = 0


def _next_id() -> str:
    global _counter  # 案①：要给模块级 _counter 重新赋值
    _counter += 1
    return f"bg_{_counter:04d}"


def start_job(label: str, delay: float) -> str:
    job_id = _next_id()
    # isoformat：适合进 JSON / 落盘的标准时间字符串
    started = datetime.now().isoformat(timespec="seconds")
    with lock:  # 锁内：登记共享表
        jobs[job_id] = Job(job_id, "running", started)

    def worker() -> None:
        time.sleep(delay)  # 锁外等待，别堵住别人
        with lock:  # 锁内：改状态
            job = jobs[job_id]
            job.status = "completed"
            job.output = f"{label} finished"

    # target=worker 无括号；daemon=True 主进程退出即丢
    # start() 立刻返回 → 主 loop 可继续派发下一个
    threading.Thread(target=worker, daemon=True).start()
    return job_id


def snapshot() -> list[dict[str, object]]:
    # 锁内 asdict：遍历时不被 worker 改表；得到可 json 的 list[dict]
    with lock:
        return [asdict(job) for job in jobs.values()]


def main() -> None:
    a = start_job("compile", 0.2)
    b = start_job("test", 0.35)
    print("dispatched:", a, b)
    print("immediate:", snapshot())  # 多半还是 running
    time.sleep(0.5)
    print("later:", snapshot())  # 应为 completed


if __name__ == "__main__":
    main()
