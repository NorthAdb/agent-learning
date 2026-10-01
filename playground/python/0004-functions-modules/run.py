"""入口脚本：只有直接运行本文件时才启动 loop。

python run.py          → __name__ == "__main__" → 跑 agent_loop
import run             → __name__ == "run"      → 不自动开转
"""

from loop import agent_loop

if __name__ == "__main__":
    agent_loop()
