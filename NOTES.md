# NOTES

## Local sources (own git remotes)
- 教学根目录 `d:\agent-learning`：独立 git（跟踪 MISSION/lessons 等；子项目在 `.gitignore`）
- `python-100Days/` → origin `https://github.com/NorthAdb/Python-100-Days`
- `learn-claude-code-north/` → origin `https://github.com/NorthAdb/learn-claude-code-north`
- Clone 策略：其余资源仍按阶段按需拉，勿一次塞满

## Preferences / profile
- 目标：2027 暑期实习；主叙事 Java 后端 + Agent 补强
- 硬产出：年前交出可演示二次开发项目（带 RAG）
- 节奏：每天约 2 小时 ≈ 14h/周
- 工具习惯：Cursor / Claude Code / OpenCode 用得多 → 有「当用户」的直觉，缺「造 harness」的肌肉
- Python：需系统重学，服务 Agent/RAG，不追求 100 天全刷
- 二次开发靶子未定：Pi / Hermes / OpenCode；阶段 2 末按「扩展点 × 语言摩擦 × RAG 可演示」选定
- LangChain/LangGraph：要会 + 必须能对照 harness，不当脊柱

## Calendar (2026-08 → 2027-02 年前 → 2027 暑期)

粗算：到春节前约 25–26 周 ≈ 350+ 小时；每天 2h 够用，但**不能三书并行**，必须切片交付。

| 窗口 | 周数（约） | 阶段 | 交付物 |
|------|-----------|------|--------|
| 2026-08 下旬 – 09 中 | 3–4 周 | 0 Python 重装 | 能独立跑脚本、venv/uv、调 LLM API |
| 09 中 – 09 末 | 1–2 周 | 1 心智模型 | 一张 Agent 栈图（面试可用草稿） |
| 10 月 | 4 周 | 2 最小 harness（North s01–s04） | 自跑 tool-use agent loop |
| 11 月 | 4 周 | 3 上下文 + RAG | 最小 RAG 管线接到 agent 工具 |
| 12 上 | 2 周 | 4 LangGraph 对照 | 对照笔记：同一行为在 harness vs 图编排 |
| 12 中 – 12 末 | 2 周 | 5a 三候选拆解 → **选定 1 个** | 选型一页纸 |
| **2027-01 – 春节前** | 4–5 周 | **5b 二次开发冲刺** | **可演示项目：选定框架 + RAG 扩展** |
| 春节后 – 暑期前 | ~4 月 | 6 面试与加深 | 栈口述、Java/MCP 桥接、评测、North 进阶选读 |

### 年前项目的最小定义（防止做大）
- 在 **一个** 框架上：增加「查知识库 / RAG」能力（工具或插件）
- 有 README：问题、架构图、怎么跑、和原版差异
- 能 5 分钟演示 + 10 分钟讲清设计

## Teaching plan (working)
0. Python 重装（文件、venv/uv、requests、类型基础、异步扫盲）
1. 心智模型：Harness L01 + North README + Agent Book Ch1
2. 最小 harness：North s01–s04；卫星 Book Ch2/4、Hello Ch4
3. 上下文 + RAG：North s08–s09 + All-in-RAG 最小管线 + Book Ch3
4. 框架对照：Hello Ch6 + LangGraph 复现 s01–s04 行为
5. 候选框架拆解 → 选定 → 二次开发切片（RAG 接入）← **年前截止**
6. 面试叙事打磨：栈图 + 项目故事 + Java 桥接 ← 春节后到暑期

## Open questions
- （已关闭）每周小时数、实习窗口、年前项目
