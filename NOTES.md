# NOTES

## Local sources (own git remotes)
- 教学根目录 `d:\agent-learning`：独立 git → origin https://github.com/NorthAdb/agent-learning（跟踪 MISSION/lessons 等；子项目在 `.gitignore`）
- `python-100Days/` → origin `https://github.com/NorthAdb/Python-100-Days`
- `learn-claude-code-north/` → origin `https://github.com/NorthAdb/learn-claude-code-north`
- Clone 策略：其余资源仍按阶段按需拉，勿一次塞满

## File layout (where code goes)
- **练习脚本**（如 `hello_agent.py`）→ `playground/python/`（已在 `.gitignore`，本地统一管理）
  - 按课号分子目录更清晰：`playground/python/0001-hello/hello_agent.py`
  - 该目录共用一个 `.venv`（建在 `playground/python/.venv`）
- **课件** → `lessons/*.html`（进教学仓 git）
  - 目录首页：`lessons/index.html`（自动渲染）
  - 课序单一来源：`assets/curriculum.js`（新增课时必须先登记这里）
  - 每课放 `<div data-lesson-id="00NN"></div>` + 文末 `data-lesson-id-footer`；引入 `curriculum.js` + `lesson-nav.js` 自动生成 首页/上一课/下一课
- **速查** → `reference/*.html` + 根目录 `GLOSSARY.md`（进教学仓 git）
  - 索引：`reference/index.html`
  - 过关后把可压缩知识点追加进对应速查；术语冲突以 GLOSSARY 为准
  - 后续每课 HTML 末尾链到相关速查页
- **上游教材/实战仓** → `python-100Days/`、`learn-claude-code-north/`（各自独立 git，不要往里塞你的练习文件）
- 以后按需 clone 的新上游 → `sources/<name>/`

## Preferences / profile
- **学习方式**：练习代码由老师直接创建；用户以读代码 + 运行为主，不要求从空白手写（卡点仍可改着玩）
- **课件深度**：后续课要**稍详细**——不是百日教材逐段翻译，但比 0001–0002 的「极简导读」厚一档（见下节 Lesson depth）
- 目标：2027 暑期实习；主叙事 Java 后端 + Agent 补强
- 硬产出：年前交出可演示二次开发项目（带 RAG）
- 节奏：每天约 2 小时 ≈ 14h/周；单课目标约 60–90 分钟可读完+跑通
- 工具习惯：Cursor / Claude Code / OpenCode 用得多 → 有「当用户」的直觉，缺「造 harness」的肌肉
- Python：需系统重学，服务 Agent/RAG，不追求 100 天全刷
- 二次开发靶子未定：Pi / Hermes / OpenCode；阶段 2 末按「扩展点 × 语言摩擦 × RAG 可演示」选定
- LangChain/LangGraph：要会 + 必须能对照 harness，不当脊柱

## Lesson depth（后续课标准，0003 起对齐）

仍坚持：**一课一个技能核**；主技能=当前阶段该学的（阶段 0 是 Python），Agent/RAG 作载体。

每课 HTML 应包含：
1. **使命挂钩**（为什么这周要学这个）
2. **Java 对照**（降低迁移成本，3–6 条即可）
3. **概念展开**（不止四条子弹；含小代码块讲语法）
4. **主代码逐段导读**（按函数/控制流讲「读到这里应理解什么」）
5. **常见坑**（动态类型、缩进、无限 loop 等）
6. **主阅读地图**（DayXX 要读哪些小节、哪些可跳）
7. **检索练习**（至少 1 题，选项等长）
8. **过关标准**（可自检）
9. **速查链接**（指向 `reference/` 对应页；新稳定知识点写入速查 / GLOSSARY）

练习代码：注释偏多、文件头说明怎么跑；必要时拆 sibling 对照文件。

不做：把整章 DayXX 贴进 HTML；一课塞两个无关大主题；为细而细拖到 3 小时。

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
