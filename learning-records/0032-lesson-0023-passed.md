# 0023 过关

用户确认课 0023（North s03 Permission：执行前三道闸门）已按过关标准完成。已在 Windows 上跑通 `s03_permission/code.py`：工作区内 `write_file` 直接通过；`del test.txt` 命中闸门 2 询问后否决；理解否决只挡住**这一次** `tool_use`，换皮命令可以绕过教学版规则。闸门 1 硬拒绝不问人、闸门 2 问人、`safe_path` 改成闸门 2 出界规则、循环出口筛 `tool_calls` 不读 `stop_reason`，可作已知。生产 CC 四态管线过关不要求。

## Implications
- 下一课是 **0024**：North `s04_hooks`（工具前后挂插口；把循环里硬编码的 `check_permission()` 挪到钩子上）
- 阶段 2 讲法不变：当章 README + `code.py`，按块拆到和 0021–0023 同密度；非必要不另写 playground
- 教学版权限不是可靠安全边界：否决后模型仍可能用 `erase` / `cmd /c del` 等未登记命令词删文件
