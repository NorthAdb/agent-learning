# Agent / Harness Resources

当前只保留地基三件套：原理书、可跑代码、Harness 工程讲义。封装层与二次开发候选已移出主动学习线。

## Knowledge

### Python 地基

- [Python-100-Days — jackfrued](https://github.com/jackfrued/Python-100-Days)（本地 fork：[`python-100Days/`](./python-100Days)，origin [`NorthAdb/Python-100-Days`](https://github.com/NorthAdb/Python-100-Days)）
  系统重学 Python。Use for: 阶段 0；Day01–20 主干已内化进课件 0001–0016，原书仅选读。
- [Python Tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
  官方语言规则：默认值只求值一次、关键字参数、`*args`/`**kwargs`。Use for: 函数课；与 Day14 对照时以官方为准。
- [Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html)
  模块 = `.py` 文件；`__name__ == "__main__"`。Use for: 拆文件、入口脚本、import 规则。
- [Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
  官方文件读写、文本编码、`with open`。Use for: 文件课与加载文档。
- [Python Tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
  官方 `try` / `except` / `else` / `finally` / `raise`。Use for: 异常课与工具边界。
- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
  官方 `dumps`/`loads`/`dump`/`load`。Use for: 配置与 tool_call 文本边界。
- [RFC 8259 — JSON](https://datatracker.ietf.org/doc/html/rfc8259)
  JSON 文本格式规范。Use for: 判断「看起来像 dict 却不是合法 JSON」。
- [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
  官方 `list[str]`、`Any`、`TypedDict`。Use for: 读开源 agent 签名。
- [Requests: HTTP for Humans — Quickstart](https://docs.python-requests.org/en/stable/user/quickstart/)
  官方 `get`/`post`、`json=`、`timeout`、`raise_for_status`。Use for: Agent 调模型/工具 API。
- [Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html)
  官方 class / 实例 / 方法。Use for: 阶段 0 收尾；North 后几章会出现 dataclass / 规则对象。
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html)
  官方 `@dataclass`、`field(default_factory=...)`、`asdict`。Use for: 0012 / 0016；对照 North s12 `Task`。
- [getattr](https://docs.python.org/3/library/functions.html#getattr) · [subprocess](https://docs.python.org/3/library/subprocess.html) · [glob / Path.glob](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob)
  Use for: 0014；North s01–s02 起。
- [re](https://docs.python.org/3/library/re.html) · [ast.literal_eval](https://docs.python.org/3/library/ast.html#ast.literal_eval)
  Use for: 0015；North s05 / s09。YAML 见 PyYAML，跑 s07 再装。
- [threading](https://docs.python.org/3/library/threading.html) · [datetime](https://docs.python.org/3/library/datetime.html)
  Use for: 0016；North s13 / s14。不是 async。

### 原理书（知识脊柱）

- 本地 Markdown 全书：[`AI-Agents-in-Depth-md/`](./AI-Agents-in-Depth-md)（《AI Agents in Depth》中文整理；MinerU 转换）
  Agent = LLM + 上下文 + 工具。Use for: 阶段 1 起每段机制的概念来源；先读对应章，再去 North 跑代码。
  章次地图：Ch1 入门（阶段 1 **切片**进课件，不整章通读）→ Ch2 上下文 → Ch3 记忆/知识库 → Ch4 工具 → Ch5 Coding Agent → 其后按 North 进度按需。
  0017 用：§1.1 公式与 Environment 边界。0018 用：§1.2 开头两个公式怎么叠（最小 Harness = 上下文管理 + 工具接口）。§1.1.5 留给 0019。
- 上游仓库（需要对照目录或追更新时）：[bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book)
  Use for: 与本地整理版核对，不另开一条通读线。

### 实践（技能脊柱）

- [learn-claude-code-north](https://github.com/NorthAdb/learn-claude-code-north)（本地：[`learn-claude-code-north/`](./learn-claude-code-north)）
  从零搭 coding agent harness。Use for: **唯一动手主线**。只跑根目录 `s01_*`–`s20_*` 的 `code.py` + 章内 README；不要混用 `docs/` / `agents/` 旧 12 章编号。阶段 2 起：课件把当章 `code.py` 拆进 HTML，非必要不另写练习脚本。

### Harness 工程（卫星理论）

- [Learn Harness Engineering（中文讲义）](https://walkinglabs.github.io/learn-harness-engineering/zh/)
  模型强 ≠ 执行可靠；规则、验证、跨会话交接。Use for: 与书/North 同步时的「为什么要这层约束」；不单独开第三条主线，也不做它的实战项目 P01 当主作业。
- [L01. 模型能力强，不等于执行可靠](https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-01-why-capable-agents-still-fail/)
  Use for: 阶段 1 的 0020（失败先查 harness）。0017–0019 过关后再读 L01；不要跳到 L02 / 不要做 P01 当主作业。
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
  Codex 实验：环境、意图规格、反馈环。Use for: Harness 一词的业界出处。
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  跨会话：initializer + 进度工件。Use for: 对照 North 记忆/任务持久化。
- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  planner / generator / evaluator。Use for: 「验证缺口」与防止提前宣告完成。

## Wisdom (Communities)

- [learn-claude-code 上游 Discussions](https://github.com/shareAI-lab/learn-claude-code)
  Use for: North 某章跑不通、和旧 12 章对不上号时。
- 用户未要求加入新社区；不主动安推 Discord / 训练营。

## Gaps

- 自己写通用装饰器、`async`/`await`：North 20 章未用，不排
- YAML / PyYAML：0015 只扫一眼；跑 North s07 再装
- 书 Ch1 后半（选型、框架表、护栏三层、全书模式）与 Harness L02 五子系统：阶段 1 故意后置
- North 后半（团队、MCP、合体）对应的书章节尚未排进主动课表
- Django / 爬虫 / 机器学习、封装层、二次开发、面试材料：**故意不补**
