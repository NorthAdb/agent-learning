# NOTES

## Local sources (own git remotes)
- 教学根目录 `d:\agent-learning`：独立 git → origin https://github.com/NorthAdb/agent-learning（跟踪 MISSION/lessons 等；子项目在 `.gitignore`）
- GitHub Pages：https://northadb.github.io/agent-learning/（`master` 根目录静态站；本地 `python -m http.server`）
- `python-100Days/` → origin `https://github.com/NorthAdb/Python-100-Days`
- `learn-claude-code-north/` → origin `https://github.com/NorthAdb/learn-claude-code-north`
- `AI-Agents-in-Depth-md/`：本地全书 Markdown（MinerU 整理），无独立 remote；不要往里面塞练习
- Clone 策略：地基三件套已在仓库旁；其余资源按需拉，勿一次塞满

## File layout (where code goes)
- **练习脚本**（如 `hello_agent.py`）→ `playground/python/`（阶段 0；已在 `.gitignore`，本地统一管理）
  - 按课号分子目录更清晰：`playground/python/0001-hello/hello_agent.py`
  - 该目录共用一个 `.venv`（建在 `playground/python/.venv`）
- **课件** → 按阶段分子目录（进教学仓 git）：`lessons/phase-0/`、`lessons/phase-1/`、`lessons/phase-2/`
  - 目录首页仍是：`lessons/index.html`（自动渲染全阶段）
  - 分册首页：`lessons/phase-0/index.html`、`lessons/phase-1/index.html`、`lessons/phase-2/index.html`
  - 课序单一来源：`assets/curriculum.js`（`file` 相对 `lessons/`，可含子目录）
  - 每课放 `<div data-lesson-id="00NN"></div>` + 文末 `data-lesson-id-footer`；引入 `curriculum.js` + `lesson-nav.js` 自动生成 首页/上一课/下一课
- **速查** → `reference/*.html` + 根目录 `GLOSSARY.md`（进教学仓 git）
  - 索引：`reference/index.html`
  - 阶段 1 速查：`reference/phase-1/`
  - 过关后把可压缩知识点追加进对应速查；术语冲突以 GLOSSARY 为准
  - 路径对照：`reference/path.html`（书 / North / Harness 讲义怎么配）
- **阶段 1 练习** → `playground/phase-1/`（`.gitignore` 已覆盖 `playground/`；无第三方包时可用阶段 0 的 venv 解释器）
- **上游教材/实战仓** → `python-100Days/`、`learn-claude-code-north/`、`AI-Agents-in-Depth-md/`（不要往里塞你的练习文件）
- 以后按需 clone 的新上游 → `sources/<name>/`

## Preferences / profile
- **学习方式**：练习代码由老师直接创建；用户以读代码 + 运行为主，不要求从空白手写（卡点仍可改着玩）
- **课件节奏**：先说明整支脚本的目标、模块地图、一次完整运行和状态流，再按模块逐段讲解；局部规则（如 `update` 的替换语义）必须先交代调用者、输入和状态背景，不能突然抛出结论
- **阶段 2 起（0021 过关后）**：课上代码 = North 当章 `README` + `code.py`。HTML 按块拆到和 0021 同密度。非必要不另写 playground / 假模型脚本；要跑就跑那章 `code.py`
- **课件 = 主教材**：阶段 0 起读 HTML 应能学完当课要点（Python 不必再翻 DayXX；阶段 1 不必整章翻书）。原书/讲义仅作选读/出处链接
- **覆盖目标**：以 Python-100-Days 为范围地图，**适度简化**：冷门、纯趣味、与读 Agent 脚本无关的可跳过或不单独成课；**禁止**整章摘录进 HTML
- 长期背景：Java 后端 + Agent 补强；当前排课只打地基，不按实习窗口倒排
- 工具习惯：Cursor / Claude Code / OpenCode 用得多 → 有「当用户」的直觉，缺「造 harness」的肌肉
- Python：系统重学。100-Days 是范围地图/课本。进 North **之前**把全套 `s01–s17/code.py` 用到的语法补齐（0013–0016），避免读到后半再倒回来。`async`、Django、爬虫、ML 仍不排（North 未用 / 与使命无关）。
- **三份材料分工（硬约束）**：
  - 原理：`AI-Agents-in-Depth-md/`
  - 实践：`learn-claude-code-north/`（只跑根目录新 17 章 `code.py`）
  - 工程约束：[Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/zh/)（卫星阅读，不当第三条主线）
- 单课仍要写满（见 Lesson depth）；不在计划里估工期

## Lesson depth（0004 起强制；取代此前「稍详细」）

**主技能** = 本课对应的知识点。阶段 0 是 Python（Agent 只作载体，不能挤掉语法）。阶段 1 是心智模型。进入 North 主线后是那一章的 harness 机制，Python 只补缺口。

每课 HTML 必须做到：
1. **覆盖声明**：本课对应 DayXX / 书哪一章 / North 哪一节；明确「已内化进课件 / 故意跳过（原因）」
2. **使命挂钩**（1 小段）
3. **Java 对照表**（Agent 课可改成「和你已经会的 Java 概念对照」）
4. **系统讲解**（主体，占全文大半）：概念 → 规则 → 2～4 个由浅入深的完整小例 → 再接到本课主脚本
5. **主脚本导读**（按块，不假设你已从教材学会）
6. **常见坑 + 边界**（含和 Java 易混点）
7. **检索练习** ≥2 题（考规则，不只考 Agent 口号）
8. **过关标准**
9. **选读**：链到原书/讲义「若还想看原文」；默认路径是不打开也能过关
10. **速查**：本课新稳定点写入 `reference/` / GLOSSARY

练习代码：可多文件；注释讲「为什么这样写」、首次见的 API/专有名词要写到和课件同密度；关键语法在 HTML 里先讲清再出现在长脚本里。

**新概念必须先讲**（硬准则）：课件、对照表、示例或脚本里**第一次出现**的专有名词 / 缩写 / 鉴权方案 / API / 运算符 / 特殊变量，都要当场解释，不能假设读者已知，也不能只靠行尾注释带过。
- **范围**：不限于语法——如 DTO、Bearer、Basic、`raise_for_status`、`params` 等都算「新概念」。
- **最低要写清**：是什么（一句话）→ 做什么 / 填在哪 → 和易混兄弟的差别（若有）。
- **必须能跳回教材**（用户 2026-08-31 起要求）：第一次出现时标明出处——哪份材料、哪一节/标题、行号，并给可点开的链接（仓库内相对路径 + `cursor://file/…:行号`）。路径含空格或中文时必须 URL 编码。本机同时装了 VS Code 时 `vscode://` 会被 VS Code 抢走，不要用。教材里没有这个词，要写明「本书未用，出自某某」。禁止只写「见 Ch1 / 见 README / 同上」却点不进去。
- **落点**：优先写进当课 HTML；稳定后补 `GLOSSARY.md` / `reference/`（glossary 条目同样带一句出处）。
- **自检**：若读者问「X 是什么」而课件里只有 X 的名字没有定义 → 该节未过关，需增补后再继续。
- 例：`exists()` vs `resolve()` 问的是两个不同问题；提到 Basic 就不能只写「了解」而不说它是用户名密码方案。

## Tutor loop (Alvar)

一对一家教，**不换课表**。教材仍是 `lessons/**/*.html`。

| 你说 | 老师做什么 |
|------|------------|
| `/alvar-teach`、卡住、讲一遍、测我 | Probe（选择题工具）→ mermaid 计划 → 一次只讲/锁一个节点 |
| 写课件、改练习、过关了 | 原工作流：Lesson depth + `learning-records/` |

状态在 `.alvar/`（`LEARNER.md` / `maps/` / `sessions/`）。过关记录仍写 `learning-records/`。项目 skill：`.cursor/skills/alvar-curriculum/`。

**密度自检**：若把「主阅读：去看 DayXX / 去看书第 N 章」当成讲解主体 → 不合格，需把该节写进 HTML。  
**不做**：全书粘贴；一课塞无关联的两章；为凑时长灌水。
**易混点要写满三种情况**：例如可变默认值，不能只留一句「会漏状态」——要写清「默认 `[]` 串会话 / 默认 `None` 隔离 / 显式传入才累加」，并给可跑对照。

**0005/0006 拆分决定**：0004 预告的「列表 / 字符串 / 字典深挖」拆两课——0005 列表与元组（Day08–10，载体：RAG 候选排序）、0006 字符串·字典·集合（Day11–13，载体：切文本 / 拼 prompt / 解析 tool_call）。原因是六章挤一课会做浅。

## Teaching plan (working)

不写周数。下一课永远是「最近邻且未过关的一项」。

### 材料怎么配
同一主题：**先看书里对应章（概念）→ 再跑 North 那一节 `code.py`（技能）→ 卡住「为什么要这层约束」时再打开 Harness 讲义**。禁止三线并行通读。

### 阶段 0 · Python 地基
- **已过关**：0001–0016（阶段 0 收完）；课件在 `lessons/phase-0/`
- **不补**：`async`/`await`（North 20 章未用）；自己写通用装饰器（除 `@dataclass` / `@property` / `@staticmethod` / `@classmethod`）

### 阶段 1 · 心智模型
Ch1 是概念地图，**禁止整章塞进一课**。课件/练习/速查放 `lessons/phase-1/`、`playground/phase-1/`、`reference/phase-1/`。

- **已过关**：0017–0020（公式 → Agency/Harness → ReAct 循环 → 失败先查 harness）
- 下一课不在本阶段：进入阶段 2

**本阶段故意不讲**（留给后面或卡住再看）：Manus/OpenClaw 案例细读、工具五类、上下文五组件消融、Model as Agent / 苦涩的教训、模型选型、框架对照表（含 LangChain）、护栏三层、全书设计模式、[L02 五子系统](https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-02-what-a-harness-actually-is/)（动手前或阶段 2 再开）。

### 阶段 2 · 能动手（当前）
- **已过关**：0021（s01 循环 + bash）、0022（s02 多工具 + dispatch map）、0023（s03 三道闸门）、0024（s04 hooks）、0025（s05 TodoWrite）、0026（s06 Subagent）、0027（s07 Skill Loading）、0028（s08 Context Compact）
- **下一课**：North **s09**（Memory：筛选、提取、整理持久记忆），讲清 `code.py`，必须真跑
- 卫星：书 Ch4 工具、Ch5 Coding Agent；Harness 里「划清任务边界 / 防止提前宣告完成 / 跑通才算验证」

### 阶段 3 · 上下文、记忆、知识
- North **s07–s09**（skill / compact / memory；s08、s09 为重心）。系统提示不再单开一章。
- 卫星：书 Ch2 上下文工程、Ch3 用户记忆和知识库；Harness 里「仓库即事实来源 / 指令拆文件 / 跨会话连续 / 初始化 / 交接」

### 之后
沿 North 主线继续（复杂任务 s05–s06 → 任务/后台/cron s10–s12 → 协作 s13 → MCP s14 → 集成与收口 s15–s17），每段只带书里对应章。不另开 LangChain、二次开发、面试线。
课表以同步后的根目录 `s01–s17` 为准；不要再用旧的 s18–s20 章号。

## Open questions
- （已关闭）每周小时数、实习窗口、年前项目、封装层与二次开发排期
