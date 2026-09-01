# 第 10 课过关：requests / HTTP JSON

用户确认 0010 已按过关标准完成：能填 `requests.get/post` 的 `url / params / json / headers / timeout`；理解 Response 与 `raise_for_status` 顺序；区分 `json=` vs `data=`；Bearer/Basic/DTO/hits 等概念；能读 `fake_api_server` 三块结构与四脚本阅读顺序；`http_agent_client` 封装链（`get_json`/`post_json` → `rag_search`/`chat_completion` → `AgentHttpError`）可串讲；假服务启动后客户端脚本可跑通。

## Implications
- HTTP 客户端 + 异常边界转换可作已知；下一关阶段 0 收尾：包管理/venv 巩固、异步扫盲（可选压缩）
- 之后进入阶段 1：Agent 心智模型（Harness + North README + Agent Book Ch1）
