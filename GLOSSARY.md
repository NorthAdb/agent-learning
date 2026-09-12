# Agent Learning Glossary

本仓库术语表。课件、速查、learning-records 用词以此为准。压缩定义；别名放在 _Avoid_。

## Harness & Agent

**Model**:
提供感知—推理—行动决策的 LLM 权重与推理服务；Agency 的主要来源。
_Avoid_: 把整个 Agent 产品称作「模型」

**Agency**:
感知、推理、行动的能力。来自模型训练，不是编排代码赋予的。书 Ch1 不用这个词。
出处：`learn-claude-code-north/README-zh.md` L5 标题、L9 加粗定义、L11 节「Agency 从哪来」。
_Avoid_: 以为堆节点图 / 提示词链就能「做出 agency」

**Harness**:
围绕 Model 的运行外壳（载具）。书：最小 = 上下文管理 + 工具接口；生产再加约束、验证、纠正（第01章 §1.2 L261 / L273）。North：Tools + Knowledge + Observation + Action interfaces + Permissions（README-zh.md L54）。两套切法描述同一层，不是两套产品。
_Avoid_: 任意 prompt 工作流、纯 if-else 编排冒充 harness；把整个产品叫「模型」

**约束**（生产 Harness）:
限定能做什么、不能做什么（权限、沙箱、审批）。不是把下一步写死——写死路径是工作流。出处：书第01章 §1.2 L273；伪代码 `constrain` L288。
_Avoid_: 和「验证 / 纠正」混成一件事；当成状态机节点

**验证**（生产 Harness）:
检查做得对不对（测试、lint、完成定义）。不能只听模型说「做完了」。出处：书第01章 §1.2 L273；伪代码 `verify` L290。讲义把「口嗨完成 vs 实际正确」叫验证缺口（L01 关键名词解释）。
_Avoid_: 和约束（拦操作）混用；和纠正（补救）混用

**纠正**（生产 Harness）:
做错了怎么补救（重试、回退、换路）。出处：书第01章 §1.2 L273；伪代码 `correct` L291。
_Avoid_: 当成验证本身；本课只认名字，细节以后按 North 章展开

**Tool**:
Harness 暴露给 Model 的一个可调用动作，通常以 name + arguments 描述。
_Avoid_: 笼统的「插件」（未区分 MCP / Skill / 函数工具时）

**Tool call**:
Model 发出的一次工具调用请求（结构化数据，常为 dict）。
_Avoid_: 整段对话、一次 HTTP 请求（除非恰好一一对应）

**Agent loop**:
重复「Model 输出 → 执行 Tool（可选）→ 观察 → 再请求 Model」直到 final 或触顶的控制结构。书称 ReAct 循环（想 → 做 → 看）。出处：书第01章 §1.1.5 L168 / L172；North 循环图 README-zh.md L140（不用 ReAct 这个词）。
_Avoid_: 单次补全、无工具聊天；把 `fake_model(turn)` 剧本当成已经实现了 ReAct

**ReAct**:
Reasoning + Acting；书强调实际还有「看」。想 = Model 决策，做 = Harness 执行工具，看 = 观察追加进轨迹。North README 不用此词。出处：书 §1.1.5 L168、L172。
_Avoid_: 以为只有两个环节；和订票工作流的固定节点混为一谈

**轨迹**（trajectory）:
用户消息、模型回复、工具结果随交互追加的消息历史。每次调用的上下文 = 静态前缀 + 轨迹。出处：书 §1.1.5 L174。
_Avoid_: 把磁盘上的文件当成已经在轨迹里；和静态前缀混成一份列表

**静态前缀**（stable_prefix）:
每次调模型都拼在轨迹前面的系统提示词 + 工具定义；通常不出现在轨迹列表示例里。出处：书 §1.1.5 L174、L226。
_Avoid_: 以为前缀会随工具结果变长；以为轨迹列表里看不见就等于没发给模型

**stop_reason**:
模型本轮生成结束的原因。官方枚举含 `end_turn` / `max_tokens` / `stop_sequence` / `tool_use` / `pause_turn` / `refusal` / `model_context_window_exceeded`。字段仍在 Message 上。当前 s01–s02 循环改为筛 `content` 里的 `tool_use` 块（`tool_calls`），列表空则 `return`，不再读这个字段。出处：North README-zh.md L146、L219；书 L189；SDK `anthropic.types.StopReason`。
_Avoid_: 当成 HTTP 状态码；以为 README 的 `while True` 骨架已经含最大轮数

**tool schema**:
给 Model 看的工具契约：工具名、用途和参数的结构化约定；其中 JSON Schema 是用 JSON 写的字段与类型约束。它描述可调用动作，但不执行 Python 函数。出处：North [`s01_agent_loop/code.py`](./learn-claude-code-north/s01_agent_loop/code.py) [`L59–67`](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:59)。
_Avoid_: 把 schema 当成 handler；以为声明了工具就已经跑过命令

**`tool_use`**:
Model 内容中的结构化工具调用块，包含工具名、输入参数和本次调用的 `id`。s01 用它判断 Harness 是否继续执行工具。出处：North [`s01_agent_loop/code.py`](./learn-claude-code-north/s01_agent_loop/code.py) [`L98–102`](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:98)。
_Avoid_: 当成命令成功或最终文本

**`tool_result`**:
Harness 执行 `tool_use` 后回传给 Model 的结果块；通常带 `tool_use_id` 和实际输出。出处：North [`s01_agent_loop/code.py`](./learn-claude-code-north/s01_agent_loop/code.py) [`L110–114`](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:110)。
_Avoid_: 只追加 assistant 回复而漏掉观察

**`tool_use_id`**:
工具结果与具体工具调用之间的配对键：`tool_result.tool_use_id == tool_use.id`。同一个工具可被调用多次，不能只靠工具名配对。出处：North [`s01_agent_loop/code.py`](./learn-claude-code-north/s01_agent_loop/code.py) [`L112`](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:112)。
_Avoid_: 当成工具名、模型 ID 或 HTTP 状态码

**Message**（`response`）:
`messages.create` 返回的一条助手消息对象，不是纯文本。顶层：`id` / `type="message"` / `role="assistant"` / `model` / `content` / `stop_reason` / `stop_sequence` / `usage`；可选 `container` / `stop_details`。对象上仍有 `stop_reason`；当前 s01–s02 循环只筛 `content` 里的 `tool_use`。出处：SDK `anthropic.types.Message`；[Messages API](https://docs.anthropic.com/en/api/messages)；课 0022 节 F。
_Avoid_: 当成一段字符串；把 `response.type`（恒为 message）和 `block.type`（text / tool_use）当成同一个字段

**Messages 请求**（`create`）:
发给模型的调用。s01–s02 实际传五个顶层字段：`model` / `system` / `messages` / `tools` / `max_tokens`。`system` 与工具 schema 是静态前缀，不进 `messages` 列表；本机 `TOOL_HANDLERS` 不发送。出处：North [`s02_tool_use/code.py` L155–158](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:155)；课 0022 节 E′。
_Avoid_: 以为有 `role: system` 消息；把 handlers 字典当成请求体；把 `max_turns` 当成 create 参数

**content block**:
Messages API 里一轮回复的一截内容：常见 `type=text` 或 `type=tool_use`，排在 `response.content` 列表里。`tool_use` 块带 `id` / `name` / `input`。出处：North [`s02_tool_use/code.py` L159、L161–173](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:161)；s01 [`L106`](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:106)。[Messages API](https://docs.anthropic.com/en/api/messages)。
_Avoid_: 当成整段 HTTP body；以为 `response` 本身就是字符串；以为一轮只能有一种块

**`load_dotenv`**:
python-dotenv 把 `.env` 读进 `os.environ`。s01 用 `override=True`，文件里的值覆盖进程里已有的同名变量。出处：North [`code.py` L48](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:48)；[python-dotenv](https://github.com/theskumar/python-dotenv)。书未用。
_Avoid_: 以为不 load 也能读到 `.env`；把 `override` 理解成「覆盖磁盘文件」

**`max_tokens`**:
本轮模型最多生成多少 token，限制这一次回复长度，不是上下文窗口，也不是 `max_turns`。出处：North [`code.py` L91](cursor://file/d:/agent-learning/learn-claude-code-north/s01_agent_loop/code.py:91)。
_Avoid_: 和轮数上限、上下文窗口混成一个旋钮

**max_turns**:
Agent loop 的轮数上限，harness 自己在 `while` 上数圈，**不是** Messages API 字段。s01 的 `code.py` 没有它，只有 `while True`。对照 0003 / 0019；书称「最大迭代次数」。
_Avoid_: 当成 `client.messages.create` 的参数；和 `max_tokens` 当成同一个旋钮

**REPL**:
Read-Eval-Print Loop：读一行输入 → 执行 → 打印结果 → 再等下一行。s01 / s02 外层 `s01 >>` / `s02 >>` 是 REPL；内层 `agent_loop` 不是。出处：North [`s02_tool_use/code.py` L178–196](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:178)。书 / North README 不用此缩写。
_Avoid_: 把 REPL 和 agent loop / Messages API 当成一回事

**handler**（工具处理函数）:
真正执行一次工具调用的函数，如 `run_read`。模型不直接调用它；Harness dispatch 之后才跑。出处：North [`s02_tool_use/code.py` L78、L170](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:170)；README [`L6`](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/README.zh.md:6)「只加一个 handler」。
_Avoid_: 和 0012 对象字段名 `handler` 混成语法关键字；当成 API 字段

**dispatch map** / **`TOOL_HANDLERS`**:
「工具名 → handler」的字典。表本身不执行命令。出处：North [`s02_tool_use/code.py`](./learn-claude-code-north/s02_tool_use/code.py) [`L143`](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:143)；README [`L90`](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/README.zh.md:90)。
_Avoid_: 键写成 Python 函数名 `run_read`；为每个工具复制一份 `agent_loop`

**dispatch**（工具分发）:
按 `block.name` 查 dispatch map 并调用对应 handler 的动作。出处：North [`code.py` L170–171](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:170)；README 「工具分发」[`L20`](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/README.zh.md:20)、[`L87`](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/README.zh.md:87)。
_Avoid_: 当成第二套循环；和 map、handler 三个词混成一个

**`safe_path`**:
把工具给的路径接到 `WORKDIR` 并 `resolve`，再用 `is_relative_to` 拒绝逃出工作区。只用于 s02 的文件工具，bash 不走这里。s03 删掉了它，改成闸门 2 询问。出处：North [`s02_tool_use/code.py` L71–75](cursor://file/d:/agent-learning/learn-claude-code-north/s02_tool_use/code.py:71)。
_Avoid_: 当成完整权限系统；以为 s03 的 `run_write` 仍会硬拦出界路径

**permission pipeline**（权限管线）:
工具执行前固定顺序的检查。s03 是三道闸门：`DENY_LIST` 硬拒绝 → `PERMISSION_RULES` 命中则问人 → 否则执行。出处：North [`s03_permission/README.zh.md` L6–8](cursor://file/d:/agent-learning/learn-claude-code-north/s03_permission/README.zh.md:6)；[`code.py` L191–202](cursor://file/d:/agent-learning/learn-claude-code-north/s03_permission/code.py:191)。总览 Permissions：[`README-zh.md` L54–60](cursor://file/d:/agent-learning/learn-claude-code-north/README-zh.md:54)。
_Avoid_: 当成 SYSTEM 提示词；当成 s04 hooks；以为与 CC 生产四态一一对应

**fail-closed**（默认拒绝）:
询问时只有明确允许才放行；空回车、乱按都当拒绝。s03 提示符 `[y/N]`。出处：North [`s03_permission/code.py` L183–187](cursor://file/d:/agent-learning/learn-claude-code-north/s03_permission/code.py:183)。书 / README 未用这个英文词。
_Avoid_: 把回车当成确认；和闸门 1 硬拒绝混成一件事

**`Permission denied.`**:
s03 拒绝执行后回填的 `tool_result.content`。不是 HTTP 401，也不是 Python 异常。必须带 `tool_use_id`。出处：North [`s03_permission/code.py` L226–229](cursor://file/d:/agent-learning/learn-claude-code-north/s03_permission/code.py:226)。
_Avoid_: 拒绝后不 append；把这句话当成闸门 1 打印的红字原因

**Environment**（环境）:
Agent 与之交互的外部世界（文件系统、网络、用户机器、数据库）。书：不在公式「Agent = LLM + 上下文 + 工具」之内；观察从环境来，行动打回环境。
_Avoid_: 把环境算进公式右边；把「跑脚本的那台电脑」和「模型权重」混为一谈

**观察**（observation）:
环境返回给 Agent 的信息。Harness 把它转成上下文；没进上下文的，对模型等于不存在。
_Avoid_: 和「用户盯着屏幕看」混为一谈；以为仓库里有文件模型就自动看见

**工作流**（Workflow）:
执行路径由开发者预先写死；LLM 只在节点内部生成。与自主 Agent 相对：后者由模型根据反馈决定下一步。出处：书第01章 §1.2.4.1 L369 / §1.2.4.2 L407。
_Avoid_: 把节点图 / 提示词链直接叫 Agent（本仓库默认指自主 Agent）

**能力鸿沟**（Capability Gap）:
模型在基准测试上的表现和真实任务上的表现之间的落差。书 / North 不用此词。出处：Harness 讲义 L01「关键名词解释」https://walkinglabs.github.io/learn-harness-engineering/zh/lectures/lecture-01-why-capable-agents-still-fail/#关键名词解释
_Avoid_: 当成「这模型数学不行」；忽略真实任务往往缺规格和验证

**Harness 诱导失败**:
模型能力足够，因执行环境有结构性缺陷而失败。出处：L01「关键名词解释」；对照实验「同一匹马，两种命运」。
_Avoid_: 一失败就换更贵的模型

**验证缺口**:
agent 宣称完成与实际正确性之间的偏差。出处：L01「关键名词解释」。叠生产 Harness 的验证层（书 L273 / L290）。
_Avoid_: 当成模型人格「爱撒谎」

**完成定义**（Definition of Done）:
一组能用命令验证的完成条件。没有它，agent 会自己编一个。出处：L01「关键名词解释」与「遇到失败，先修 harness」。
_Avoid_: 用一段很文学的「做好就行」代替可跑命令

**诊断循环**:
执行 → 观察失败 → 定位到 harness 某一层 → 修补那一层 → 再执行。出处：L01「关键名词解释」。
_Avoid_: 失败后只换模型或把 prompt 加长再碰运气

**五层归因**（L01）:
任务规范、上下文供给、执行环境、验证反馈、状态管理。是失败排查清单。出处：L01「遇到失败，先修 harness」。
_Avoid_: 和 L02 五子系统（指令/工具/环境/状态/反馈）当成同一张表；本阶段不讲 L02

## Python（阶段 0）

**异常标准范式**:
窄 `try` + 具体 `except`（可选 `else` / `finally`）；先问本层能否恢复、能否改写语义再上抛，否则不捕获让其冒泡；文件清理优先 `with`。
_Avoid_: 裸 `except:`、整段 `main` 包进一个 try、把异常当普通 if

**转换后上抛**:
`raise NewError("业务语义") from error`：边界改写消息并保留原因链。
_Avoid_: 吞掉异常后返回模糊空值却不说明失败

**JSON**:
文本数据交换格式；Python 用 `json.dumps/loads`（字符串）与 `dump/load`（文件）在 dict/list 与文本之间转换。
_Avoid_: 把 JSON 文件路径传给 `loads` 当读盘；把 Python `True/None` 手写进 `.json` 文件

**DTO** (Data Transfer Object):
边界上搬数据用的对象，字段形状通常对齐一份 JSON；Java 里常是带字段的类/record，由 Jackson 绑定。Python 的 `json.loads` / `response.json()` 默认只给 `dict`/`list`，没有编译期 DTO；可用 `TypedDict`（标注）或后续校验库逼近。
_Avoid_: 以为 `response.json()` 已经等价于 Java 的 `readValue(..., XxxDTO.class)`

**类型标注**:
函数/变量上的形状说明（如 `list[str]`、`dict[str, Any]`）；默认不在运行时强制，边界仍要 `isinstance`。
_Avoid_: 以为写了标注就不必校验 JSON；在业务深处滥用 `Any`

**requests**:
第三方 HTTP 客户端；Agent 工具常用它调模型 API / RAG / 业务服务。
_Avoid_: 不设 `timeout`；只靠 `json()` 判断成功；用 `data=dict` 当 JSON API 正文

**raise_for_status**:
`Response` 方法：非 2xx 时抛 `HTTPError`；应在 `json()` 之前调用。
_Avoid_: 以为 requests 默认会因 404 自动失败

**Bearer** (Bearer Token):
HTTP 鉴权方案名，写在 `Authorization` 头：`Bearer` + 空格 + token。含义是「持有此令牌者被授权」；模型 API / OAuth 常见。不要漏空格，也不要把 token 写进 URL。
_Avoid_: `BearerTOKEN`（无空格）；把 API Key 塞进 `json=` 当业务字段（除非文档要求）

**Basic** (HTTP Basic Authentication):
另一种 `Authorization` 方案：值为 `Basic` + 空格 + `Base64(用户名:密码)`。requests 可用 `auth=("user", "pass")` 自动生成。Base64 不是加密，须配 HTTPS。Agent/模型 API 主线认 Bearer；Basic 见到能读即可。
_Avoid_: 在明文 HTTP 上传 Basic；把 Basic 和 Bearer 的后半段格式混用

## Knowledge

**RAG**:
Retrieval-Augmented Generation：先检索知识再生成回答；Harness 的 Knowledge 能力的一种接法，不是 Agent 本身。
_Avoid_: 「有向量数据库 = 已完成 Agent」

**hits** (检索):
检索接口返回的「命中结果」列表字段名；每一项通常是一条文档/片段（如 `id` / `score` / `text`）。不是点击数。Agent 工具常取出 `hits` 再拼进 prompt。
_Avoid_: 把整份响应当字符串塞进模型而不取 `hits[].text`

**stdout / stderr**:
进程的两个默认输出流：stdout（标准输出）放正常结果，`print()` 默认写这里；stderr（标准错误）放警告/错误/诊断日志。终端里通常都能看见，但分开是为便于重定向或管道区分。
_Avoid_: 把 stderr 当成「一定红色报错」——日志也常写 stderr，未必是程序崩溃

**PreparedRequest** (requests):
`Request(...).prepare()` 得到的「已组装、尚未发送」的请求包，含 method、url、headers、body。用于调试或自定义发送流程；`requests.post()` 内部也会先 prepare 再联网。
_Avoid_: 以为 prepare() 已经发出请求——只有 session.send(prepared) 或 post/get 才会真发

**venv** (virtual environment):
项目级独立 Python 环境，自带 site-packages；避免多项目依赖版本冲突。练习场路径 `playground/python/.venv`。
_Avoid_: 全局 pip install 装大型第三方栈；复制别人的 .venv 目录

**pip**:
Python 包安装器；推荐 `python -m pip install ...` 绑定当前解释器。clone 后常见 `pip install -r requirements.txt`。
_Avoid_: 不激活 venv 就装包；把 API Key 写进 requirements

**requirements.txt**:
一行一个依赖的文本清单；`pip install -r` 批量安装。进 git 的是**声明**（要什么包），不是 `.venv` **实例**。类似 Maven 依赖列表。
_Avoid_: 与 `pyproject.toml` 混为一谈；把 `.venv` 提交进 git；把 API Key 写进 requirements

**声明式依赖**:
进 git 的小文本（requirements / pyproject）描述需要什么包；每人本地 venv + `pip install` **重建**环境。解释器大版本靠 README，不靠拷贝 .venv。
_Avoid_: 以为 requirements 锁死 Python 小版本；复制同事的 .venv 目录

**site-packages**:
当前 Python 环境下第三方包的安装目录；`pip install` 默认写入激活 venv 的 site-packages。
_Avoid_: 以为 import 的包一定在项目源码目录里

**class / 实例**:
类是模板；实例是按模板造出的对象。`Session("alice")` 构造，没有 `new`。
_Avoid_: 把类本身当成已经有数据的对象；`c = a` 当克隆

**self**:
方法的第一个参数，表示当前实例（Java `this`，但必须写出来）。点号左边的对象会填进 `self`。
_Avoid_: 漏写 `self.` 导致变成局部变量

**属性（实例属性）**:
对象上的命名数据格子。名字大多由作者起（`user`、`handler`）；一次赋值装一份值，再赋覆盖。要多个函数：用 list/dict，或多份对象进注册表——不是「任意属性自动绑多个函数」。
_Avoid_: 以为 `handler` 是 Python 关键字；以为 class 自带固定属性清单

**Python 特殊名 vs 作者起名**:
语言认的如 `__init__`、`__name__`；约定如 `self`。业务字段/方法名（`handler`、`dispatch`、`run_echo`）都是作者起的，可改，但本课脚本请保持原名以便对照。
_Avoid_: 把 `handler` 当成内置；为学概念随意改课件脚本里的名字

**dataclass**:
`@dataclass` 装饰器给 class 自动生成 `__init__` / `repr`。可变默认字段用 `field(default_factory=list)`，不是关键字——`field` 来自 `dataclasses`，`default_factory` 是其参数名，`= list` 传函数本身（无括号），每次造实例时 `list()` 新建。
_Avoid_: 写 `calls: list = []`；写 `default_factory=list()`（定义时就建 list）

**Callable[..., str]**:
类型标注：格子里应存可调用对象，返回 str；`...` 表示参数形状不写死。本课首次出现，衔接 0004 存函数 + 0009 标注。真正存的是 `run_echo` 等，不是 `Callable` 本身；`self.handler(**arguments)` 调的是存着的函数。
_Avoid_: 以为 handler 存的是 Callable；以为标注会在运行时拦截

**field / default_factory**:
`dataclasses.field()` 用来配置 dataclass 字段。`default_factory=list` 表示默认值由「每次调用 `list()`」生成，对应三案 ①。不是 Python 语法关键字。
_Avoid_: 当成内置关键字；在 `default_factory` 里加括号

**注册表（tool registry）**:
「工具名 → 可调用实现」的对照表。模型只给字符串名字和参数 dict；harness 查表再执行。常见形态：`TOOLBOX[name] = fn`（dict）或 `ToolRegistry.register(ToolSpec)`（对象）。
_Avoid_: 把注册表当成「已经跑完的结果表」；用一长串 `if name == ...` 代替查表

**函数对象 / 存函数**:
`run_echo` 是函数本身（可再调用）；`run_echo()` 是立刻执行并得到返回值。注册时必须存前者（无括号）；dispatch 时才 `handler(**arguments)`。
_Avoid_: 注册写成 `handler = run_echo()`；以为存进去的是字符串结果

**装饰器（认 @）**:
`@foo` 写在下一行 `def`/`class` 之上，表示该定义被 `foo` 加工过。标准译名是**装饰器（decorator）**，不是「注释器」；`#` 才是注释。本阶段认 `@dataclass` / `@property` / `@名.setter` / `@staticmethod` / `@classmethod`；不必自己写通用装饰器函数。
_Avoid_: 叫成注释器；以为 `@` 和 `#` 一样；本阶段自己实现装饰器

**工厂（方法/函数语境）**:
职责是「按某种输入造出对象并返回」的入口；常先加工输入再调用构造。本课 `@classmethod` 工厂用 `return cls(...)`（如 `from_dict` / `ToolName.parse`），便于子类调用仍得子类实例。
_Avoid_: 当成工业/制造业务词；和「抽象工厂」设计模式全书划等号（本阶段只需认「造实例的入口」）

**getter / setter**:
getter = `@property` 那支，读 `obj.名` 时调用（不加 `()`）；setter = `@名.setter` 那支，写 `obj.名 = ...` 时调用。只有 getter、无 setter → 写通道不存在 → `AttributeError`（故意只读），不会退化成普通字段。
_Avoid_: 把无 setter 的赋值失败当成莫名 bug；读 property 还加 `()`

**`_name` / `__name`（属性前缀）**:
单下划线 = 约定内部（语法不拦，别当公开 API）；双下划线（且不是 `__x__`）= 名称改写成 `_Class__name`，主要为防子类踩名。North s19 的 `_DISALLOWED_CHARS` 是模块级单下划线约定。
_Avoid_: 以为 `_x` 会报错；把改写当成 Java `private`；把 `__secret` 和 `__name__`/`__init__`（两边双下划线的语言特殊名）当成一类

**公开 API（Python 命名语境）**:
类/模块作者承诺可稳定依赖的名字（无 `_` 前缀的属性、函数、方法）。带单 `_` 的是实现零件，外面能摸到也不该写进调用方逻辑。
_Avoid_: 把「语法能访问」等同于「接口保证」

**`__slots__`**:
类里声明实例允许的属性名名单；名单外赋值 → `AttributeError`。「三案」= 无 slots 可动态加 / slots 内可读写 / slots 外报错。防打错字野属性、略省内存；不是 private。North 20 章未用，0013 已补。
_Avoid_: 和「私有」搞混；把「三案」当成第三个 API；单元素写成 `("name")` 漏逗号

**`@property`**:
把无参方法伪装成属性读取（不加 `()`）。对外名（如 `max_retries`）是门面；真存储用 `_max_retries`。读走 getter，写走 `@xxx.setter`（先校验再写入真格子）；无 setter=只读。创建时可 `self.对外名 = 实参` 故意走一遍 setter。getter 须 `return self._x`，写 `return self.对外名` 会递归。
_Avoid_: 写成 `obj.area()`；getter 里 `return self.area`

**`@staticmethod` / `@classmethod`**:
static 无 `self`/`cls`，纯函数挂在类命名空间；class 的第一个参数是 `cls`（类/图纸），常当工厂，须 `return cls(...)` 以便子类调用仍得子类实例。口诀：self=成品，cls=图纸。
_Avoid_: static 里用 `self`；classmethod 里写死父类名

**`getattr`**:
内置函数：`getattr(对象, "属性名", 默认值)`，按字符串读属性；缺失则返回默认。面向任意对象（含 list/tuple/str/dict/int 与自定义实例），取的是属性/方法名，不是容器下标或 dict 键。SDK block 用它；dict 键仍用 `.get`。
_Avoid_: 对对象用 `[]`、对 dict 用点号；以为只能用于类；用 getattr 取 dict 键

**`setattr`**:
`setattr(obj, "k", v)` 按字符串写属性，等价 `obj.k = v`。0014 组装 FakeBlock 时用；见到能懂即可。
_Avoid_: 和 getattr 读写方向搞反

**`subprocess.run`**:
在当前进程里再起一个 OS 子进程并等结束。解决 Agent bash 工具「必须真执行命令」的问题。常用 argv 列表 + `capture_output` / `text` / `timeout`；看 `returncode`（非零往往不抛异常）；超时抛 `TimeoutExpired`。North 因模型吐命令串才用 `shell=True`。
_Avoid_: `shell=True` 拼模型/用户字符串；不设 timeout；只看 stdout 不看 returncode

**glob**:
按通配符（`*` / `?`）枚举**文件路径/文件名**；`Path.glob` 或 `glob.glob`。解决「按模式找哪些文件」（North s02）。无匹配 → 空列表/空迭代，不是错误。
_Avoid_: 把零命中当成 FileNotFoundError；和 **grep**（搜文件**内容**）混为一谈

**grep**（概念对照）:
按模式搜索文件**正文**里的行（常见为终端命令）。与 glob 常连用（先展开文件名再搜内容），但问题不同：glob=哪些文件，grep=哪些行有字。Python 标准库无同名模块；正文正则见 0015 `re`。
_Avoid_: 以为 `import grep`；把 glob 工具当成内容搜索

**`re.search` / `re.compile`**:
`re.search(模式, 文本)` 找第一处匹配；找不到返回 `None`，须先判断再 `group`。`re.compile(模式)` 先编译成 Pattern，再反复 `.search` / `.match`（适合复用或模块常量，如主脚本 `TODO_BLOCK`）。`re.DOTALL` 让 `.` 匹配换行。对照：glob 找文件名；grep 概念=搜正文；Python 搜字符串用 `re`。
_Avoid_: 对 `None` 调 `group`；和 glob 混用；以为 compile 是另一种正则语言

**`eval`**:
Python 内置函数：`eval(字符串)` 把字符串当**可执行表达式**求值（如 `eval("1+2")`→3）。能力含函数调用/import，对模型或不可信输入**禁止**使用。0006 集合里的 `"eval"` 只是工具名字符串，不是此函数；本课 0015 第一次讲。
_Avoid_: 用 `eval` 解析模型输出；与 `literal_eval` 混为一谈

**`ast.literal_eval`**:
只把 Python 字面量字符串变成对象（list/dict/数字等），拒绝函数调用与 import。与 `eval` 不同：eval 会把字符串当可执行代码（如 `__import__('os').system(...)` 会真跑）；literal_eval 在解析阶段就拒绝，不执行。模型输出不可信 → 用 literal_eval/json.loads，禁止 eval。
_Avoid_: 用 `eval` 解析模型输出；以为 literal_eval 和 eval 一样只是「算个值」

**线程 / `threading.Thread`**:
同一进程里另一条执行线。`Thread(target=fn, args=..., daemon=True).start()` 立刻返回。解决「慢命令别堵死 agent loop」（North s13）。`target` 传函数对象，不要加 `()`；单元素 `args` 别忘逗号 `("x",)`；`join` 才等结束。
_Avoid_: `target=fn()`；`args=("x")` 少逗号；以为 `start` 会等到结束；把线程当成 async

**`threading.Lock`**:
多线程读写同一共享状态时的互斥；用 `with lock:`（退出自动放锁）。读改共享 dict 放锁内；sleep/网络/慢活放锁外。
_Avoid_: 无共享也加锁；锁内长时间阻塞；嵌套同一把普通 Lock 导致死锁

**`datetime`**:
`datetime.now()` 取本地现在；`timedelta` 做差；`strftime` 自定义格式（给人看）；`isoformat(timespec="seconds")` 标准串（给程序存/JSON）。North s14 cron 用 now 判断触发。
_Avoid_: 本阶段纠结时区大全；实现完整 cron 表达式解析；把 strftime 和 isoformat 当成一回事

**`asdict`**:
把 dataclass 实例变成普通 dict，才能 `json.dumps`。North s12 `save_task`；0016 `snapshot` 锁内 asdict。
_Avoid_: 直接 dumps dataclass 实例

**`global`（模块级赋值）**:
函数里要给模块级变量**重新赋值**须写 `global 名`；只读或改对象内部（`dict[k]=` / `list.append`）不必。三案：赋值要 / 只读不必 / 改内部不必。s13 计数器同款。
_Avoid_: 和 `self.x` 实例属性搞混；以为改任何共享状态都要 global

## Hooks

**hook**（钩子）:
挂在某个事件时机上的扩展入口；事件发生时由 Harness 调用，不必把扩展逻辑写进 Agent loop 正文。North s04 格言「挂在循环上，不写进循环里」。
出处：[`s04_hooks/README.zh.md` L6–8](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/README.zh.md:6)、方案 [`L38–52`](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/README.zh.md:38)。
_Avoid_: 以为注册 hook 就会自动运行；必须注册且必须在正确时机调用 `trigger_hooks`

**event**（事件）:
Harness 规定的触发时机名称，如 `PreToolUse`；描述「什么时候触发」，不是具体功能。s04 有 `UserPromptSubmit`、`PreToolUse`、`PostToolUse`、`Stop` 四个事件。
出处：[`s04_hooks/README.zh.md` L46–52](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/README.zh.md:46)。
_Avoid_: 和 callback 混成一个词；event 是时机，callback 才是被调用的函数

**callback**（回调）:
先作为值保存、以后由触发器调用的函数。注册时传 `log_hook`，不要传 `log_hook()`；后者会在注册阶段立即执行并保存返回值。
出处：[`s04_hooks/code.py` L130–131](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:130)、[`L203–208`](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:203)。
_Avoid_: 把 callback 当成已经执行的输出

**`HOOKS`（hook 注册表）**:
字典 `事件名 → callback 列表`，保存每个事件要运行的扩展及其顺序；表本身不执行函数。
出处：[`s04_hooks/code.py` L128](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:128)。
_Avoid_: 和 `TOOL_HANDLERS` 混为一张表；前者按事件挂扩展，后者按工具名找 handler

**`register_hook`**:
把 callback 用 `append` 加到指定事件列表末尾的函数。传函数对象，不加括号。
出处：[`s04_hooks/code.py` L130–131](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:130)。

**`trigger_hooks`**:
按事件名取 callback 列表，按注册顺序调用；第一个非 `None` 返回值会立即返回，后面的同事件 callback 不再运行。
出处：[`s04_hooks/code.py` L133–138](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:133)。
_Avoid_: 以为四个事件一起广播；一次调用只触发指定 event

**短路**（hook short-circuit）:
callback 链遇到第一个非 `None` 返回值就停止。s04 中 `permission_hook` 注册在 `log_hook` 前，拒绝时后者可能不会运行。
出处：[`s04_hooks/code.py` L133–137](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:133)、注册顺序 [`L203–205`](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:203)。

**`*args`（可变位置参数）**:
定义处把任意数量的位置参数打包成元组，调用处把元组解包为位置参数。s04 用它让 `trigger_hooks` 能转交不同事件的参数：`block` 或 `block, output`。同一函数里可同时出现：`def f(event, *args)` 是打包，`callback(*args)` 是解包——方向相反。`callback(*args)` ≠ `callback(args)`（后者把整个元组当成一个参数）。
出处：[`s04_hooks/code.py` L133–134](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:133)；课 0024 节 3′。North 章节未单独定义此词，来自 Python 函数参数语法。
_Avoid_: 当成乘法；当成并行；把解包写成 `callback(args)`

**s04 hook 返回值协议**:
`None` = 本 callback 不阻止；非 `None` = 触发器短路。但主循环是否采用该信号取决于调用点：PreToolUse 用它拒绝工具，Stop 用它继续循环，UserPromptSubmit / PostToolUse 当前忽略。
出处：[`s04_hooks/README.zh.md` L64–80](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/README.zh.md:64)、循环接入 [`code.py` L221–248](cursor://file/d:/agent-learning/learn-claude-code-north/s04_hooks/code.py:221)。
_Avoid_: 以为所有事件的非 `None` 都有同样效果；当前调用方还会用真假判断，拒绝应返回非空字符串

## Planning / TodoWrite

**TodoWrite / `todo_write`**:
给 Agent 更新待办清单的规划工具；`todo_write` 只更新进程内的计划状态，不创建文件、不执行命令、不自动完成任务。README 用 TodoWrite 讲机制，schema 使用小写下划线工具名。
出处：North [`s05_todo_write/README.zh.md` L23–29](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/README.zh.md:23)、工具接线 [`code.py` L196–203](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:196)。
_Avoid_: 把计划工具当成 `write_file`；把 `completed` 当成测试已通过

**`TodoManager`**:
保存内存中的 todo 列表，负责解析、校验、整体替换和渲染。`update` 先在局部 `validated` 中检查，全部通过后才执行 `self.items = validated`；输入不合法时旧列表保持。
出处：North [`s05_todo_write/code.py` L115–171](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:115)。
_Avoid_: 以为它是文件数据库；以为 `update` 会 append 一条项目

**todo item / `content` / `status`**:
一条 todo 是字典，当前实现归一化后只保留非空 `content` 和合法 `status`。`status` 允许 `pending`（等待）、`in_progress`（进行中）、`completed`（已完成），同一列表最多一个 `in_progress`，最多 20 项。
出处：North [`s05_todo_write/code.py` L129–151](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:129)、schema [`L197–198`](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:197)。
_Avoid_: 把三种 status 当成三个工具；以为代码自动推进状态

**内存状态**（in-memory state）:
只存在当前 Python 进程对象中的值。North 的模块级 `TODO = TodoManager()` 让多个 prompt 在同一进程内共享 `TODO.items`，但程序重启后不自动恢复，也不是持久化记忆。
出处：North [`s05_todo_write/code.py` L174](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:174)；README「内存中的任务列表」[`L33–62`](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/README.zh.md:33)。
_Avoid_: 和 `messages`、工作区文件、跨会话记忆混成同一层

**整体替换（full-snapshot update）**:
North `TodoManager.update` 每次接收更新后的完整列表；校验通过后用 `self.items = validated` 替换旧列表，不是按 id 合并或 append 一项。只发送一项会让旧的其他项消失。
出处：[`s05_todo_write/code.py` L134–154](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:134)。
_Avoid_: 把 `update` 误读成局部 patch；把缺失项目当成“保持不变”

**schema 与运行时校验**:
tool schema 是给模型看的输入契约（如 `maxItems`、`minLength`、`enum`）；`TodoManager.update` 的 Python 检查才是实际写入 `TODO.items` 前的运行时保护。两层规则可能有细微差异，本课实现会先 `str(...)` 再检查 content。
出处：schema [`s05_todo_write/code.py` L197–198](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:197)、运行时校验 [`L129–151`](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:129)。
_Avoid_: 以为 schema 声明本身会执行 Python 校验；把 `enum` 当成 Python Enum 类

**`reminder`**:
连续三个没有使用 `todo_write` 的 tool-call round 后，Harness 追加到本轮 `results` 末尾的普通 text block：`<reminder>Update your todos.</reminder>`。它是提示，不是权限拒绝或强制更新。
出处：North [`s05_todo_write/README.zh.md` L96–106](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/README.zh.md:96)、循环 [`code.py` L334–340](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:334)。
_Avoid_: 把 reminder 当成 `tool_result`、API 顶层字段或自动调用

**`rounds_since_todo`**:
一次 `agent_loop` 内距离上次出现 `todo_write` 的工具调用轮次计数器。一轮可含多个 tool call；只要其中一个是 `todo_write` 就清零；无 tool_use 的回复直接走 Stop，不进此计数。当前实现每个新用户 prompt 重新从 0。
出处：North [`s05_todo_write/code.py` L292–340](cursor://file/d:/agent-learning/learn-claude-code-north/s05_todo_write/code.py:292)。
_Avoid_: 和单个 tool call 数量、用户 prompt 数量、跨进程会话轮数混淆

## Subagents

**Subagent**（子 Agent）:
被父 Agent 通过 `task` 委派来完成明确子任务的另一段 Agent loop。s06 子 Agent 从新的 `messages` 开始，内部工具调用留在子轨迹，最后只返回最终文本；不是新进程，也不是自动沙箱。
出处：North [`s06_subagent/README.zh.md` L23–29](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/README.zh.md:23)、[`code.py` L270–307](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:270)。
_Avoid_: 把 fresh messages 误读成共享文件系统也被隔离；把子 Agent 返回的摘要当成验证证据

**父 Agent / 子 Agent**:
父 Agent 发出 `task` 并等待结果；子 Agent 在 `run_subagent` 中使用自己的消息列表执行子任务。当前实现是同步嵌套调用：子循环结束后父循环才得到 task 的 output。
出处：North [`s06_subagent/README.zh.md` L75–87](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/README.zh.md:75)、[`code.py` L328–358](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:328)。
_Avoid_: 当成两个并行线程；以为父子自动共享 messages

**委派**（delegate）:
父 Agent 通过 `task(prompt)` 把边界清楚的工作交给子 Agent loop，并把返回文本作为工具结果接回。委派不会自动补全任务规格，仍需写清目标、范围、证据和完成条件。
出处：North [`s06_subagent/README.zh.md` L13–29](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/README.zh.md:13)、[`code.py` L310–322](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:310)。
_Avoid_: 把“调用了 task”当成任务已验证；把模糊的大任务原样转交

**干净上下文**（fresh context）:
子 Agent 以 `messages = [{"role": "user", "content": prompt}]` 开始，不复制父 Agent 的历史消息。它隔离的是对话轨迹，不是进程、WORKDIR 或文件副作用。
出处：North [`s06_subagent/code.py` L272–279](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:272)、README [`L23–29`](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/README.zh.md:23)。
_Avoid_: 当成新 OS 进程、独立目录或只读权限

**`task` 工具**:
父 Agent 可调用的委派工具；schema 只有字符串 `prompt`，handler 是 `run_subagent`。它先启动子循环，子循环再决定是否调用基础工具。
出处：North [`s06_subagent/code.py` L310–322](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:310)。
_Avoid_: 当成 `bash`；以为 schema 自己会执行子任务

**`SUB_TOOLS` / `SUB_HANDLERS`**:
子 Agent 的工具说明列表与本地 handler map，分别由 `BASE_TOOLS` 和 `BASE_HANDLERS` 派生，故意没有 `task`。父有 `TOOLS` / `TOOL_HANDLERS` 中的 `task`，当前因此只允许一层委派。
出处：North [`s06_subagent/code.py` L256–257](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:256)、[`L320–322`](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:320)。
_Avoid_: 把子工具列表当成安全沙箱；把 `list(...)` / `dict(...)` 当成新进程

**共享工作区**（shared `WORKDIR`）:
父子使用同一个 Python 进程和 `WORKDIR`；子 Agent 的 write/edit/bash 副作用会出现在父 Agent 后续可访问的文件系统中。消息隔离不等于文件隔离。
出处：North [`s06_subagent/README.zh.md` L23–29](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/README.zh.md:23)、基础 handler [`code.py` L51–111](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:51)。
_Avoid_: 以为 child messages 新建就自动建立沙箱

**`execute_tool(block, handlers)`**:
s06 抽出的公共工具执行边界：先触发 PreToolUse，再按传入的 handlers 查表执行，最后触发 PostToolUse。父传 `TOOL_HANDLERS`，子传 `SUB_HANDLERS`。
出处：North [`s06_subagent/code.py` L240–252](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:240)。
_Avoid_: 以为它固定使用父 map；把它当成 Agent loop

**结果边界**（final-text boundary）:
子 Agent 的内部 assistant 消息、tool_use 和 tool_result 留在子循环；`run_subagent` 穿过边界返回的只有最终文本，或 30 轮耗尽的固定停止说明。
出处：North [`s06_subagent/code.py` L287–307](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:287)。
_Avoid_: 把最终文本当成完整审计轨迹或测试通过证明

**子循环轮数上限**:
s06 的 `for _ in range(30)` 只限制一次 `run_subagent` 的模型回复轮次；父循环仍是独立的 `while True`。它不是 `max_tokens`，也不是整个系统的总预算。
出处：North [`s06_subagent/code.py` L274](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:274)、[`L328–329`](cursor://file/d:/agent-learning/learn-claude-code-north/s06_subagent/code.py:328)。
_Avoid_: 和 `max_tokens=8000`、父 Agent 总轮数混为一谈

## Skill Loading

**Skill / 技能**:
一个目录中的 `SKILL.md` 指令文档，提供某类任务的知识、规则和步骤；不是自动执行的 Python 函数。
出处：North [`s07_skill_loading/README.zh.md` L30–40](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/README.zh.md:30)、示例 [`skills/code-review/SKILL.md` L1–8](cursor://file/d:/agent-learning/learn-claude-code-north/skills/code-review/SKILL.md:1)。
_Avoid_: 把 Skill 当成 Tool handler；把加载 Markdown 当成执行其中命令

**技能目录**（catalog）:
只包含技能名称和简短描述的字符串。s07 用 `catalog()` 把它放进 system prompt；完整 `SKILL.md` 不在目录中。
出处：North [`s07_skill_loading/code.py` L110–116](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:110)、[`L125–134`](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:125)。
_Avoid_: 把 catalog 当成完整技能正文；把它当成自动路由器

**YAML frontmatter**:
Markdown 文件最上方由两行 `---` 包围的 YAML metadata 区域。s07 从中读取 `name` / `description`，再把正文和 metadata 一起保存到 `content`。
出处：示例 [`skills/code-review/SKILL.md` L1–4](cursor://file/d:/agent-learning/learn-claude-code-north/skills/code-review/SKILL.md:1)、解析 [`s07_skill_loading/code.py` L59–82](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:59)。
_Avoid_: 和 Markdown 正文混为一段；以为 YAML metadata 本身就是工具

**`SkillLoader`**:
s07 的技能扫描与查询对象。构造时调用 `scan()`，把 `skills/*/SKILL.md` 的名称、简介和完整文本建立为内存 registry。
出处：North [`s07_skill_loading/code.py` L51–56](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:51)、[`L84–108`](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:84)。
_Avoid_: 当成新 Agent loop；以为它负责执行技能正文

**按需加载**（on-demand loading）:
启动时只把技能名称和描述注入 system；模型调用 `load_skill(name)` 后，完整技能作为 tool_result 进入 messages。s07 的全文实际在启动扫描时已缓存，按需的是模型上下文注入。
出处：North [`s07_skill_loading/README.zh.md` L33–40](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/README.zh.md:33)、[`code.py` L115–122](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:115)。
_Avoid_: 误解成每次调用才从磁盘读取；加载后仍会占用 messages 上下文

**技能 registry**:
本地字典 `self.skills`，键是技能名称，值含 `name` / `description` / `content`。模型不直接接触 registry，只通过 `catalog()` 或 `load()` 间接看到结果。
出处：North [`s07_skill_loading/code.py` L97–108](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:97)。
_Avoid_: 把 registry 当成已执行结果表；和发送给模型的 `TOOLS` schema 混为一谈

**`load_skill`**:
父 Agent 可调用的知识加载工具；schema 需要一个字符串 `name`，handler 是 `SKILL_LOADER.load`，按 registry 键返回缓存的完整 `SKILL.md` 或 Unknown 错误字符串。
出处：North [`s07_skill_loading/code.py` L201–223](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:201)。
_Avoid_: 当成 `read_file` 的任意路径版本；以为 schema 自己会查表

**`resolve()` / `is_relative_to()`（技能扫描语境）**:
`resolve()` 把路径规范化为绝对路径；`is_relative_to(root)` 检查它是否位于 root 下。s07 组合二者后用 `continue` 跳过越界的 manifest。
出处：North [`s07_skill_loading/code.py` L89–93](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:89)。
_Avoid_: 以为 `resolve()` 本身就是权限拒绝；和模型调用 `load(name)` 的字典查找混为一谈

**启动缓存**:
s07 `scan()` 读取完整 `SKILL.md` 并保存到 registry 的 `content`；`load()` 直接返回缓存，不自动检测磁盘变化。重启或显式重扫才可能得到新文件。
出处：North [`s07_skill_loading/code.py` L94–108](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:94)、[`L115–118`](cursor://file/d:/agent-learning/learn-claude-code-north/s07_skill_loading/code.py:115)。
_Avoid_: 和热更新混为一谈；以为“按需注入”意味着“按需读盘”

## Context Compact

**上下文窗口**:
一次模型请求能接收的输入范围。s08 用 `json.dumps(messages)` 的字符数作教学近似，不等于服务端精确 token 计数。
出处：North [`s08_context_compact/README.zh.md` L17–31](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/README.zh.md:17)、[`code.py` L248–270](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:248)。
_Avoid_: 和 `max_tokens` 混为一谈；把字符数当成真实 token 数

**压缩**（compaction）:
减少当前 `messages` 的信息量，同时保留继续任务所需的目标、约束和状态。s08 按“转存 → 归档 → 替换旧结果 → 摘要”的成本顺序执行。
出处：North [`s08_context_compact/README.zh.md` L35–49](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/README.zh.md:35)。
_Avoid_: 以为压缩就是删除且不可恢复；以为每轮都会调用模型摘要

**可恢复转存**（persist）:
把完整工具输出保存到 `.task_outputs/tool-results/`，消息中只留下路径和预览；模型需要细节时必须再次调用工具读取。
出处：North [`s08_context_compact/code.py` L330–360](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:330)。
_Avoid_: 把转存理解成把结果移入 system prompt；把预览当成完整输出

**工具结果批次**:
同一轮模型回复产生的多个 `tool_result`，在执行完后一起放入最后一条 `role=user` 消息。s08 的 budget 先处理最新批次。
出处：North [`s08_context_compact/code.py` L549–573](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:549)。
_Avoid_: 把一个 tool call 等同于一个批次；忘记一轮可能有多个调用

**已消费工具结果**:
已经被模型回复覆盖、属于较早历史的工具结果。s08 `micro_compact` 可优先缩短它们；尚未消费的最新结果要保留，除非自身已撑爆上下文。
出处：North [`s08_context_compact/code.py` L287–306](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:287)、[`L410–434`](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:410)。
_Avoid_: 以为所有旧结果都能直接删；以为“已消费”表示内容已写入磁盘

**微压缩**（micro compact）:
不调用模型，把较早且已消费的长工具结果完整落盘，并在 `messages` 中替换为恢复路径；默认保留最近 3 条已消费结果。
出处：North [`s08_context_compact/code.py` L410–434](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:410)。
_Avoid_: 把它和模型生成摘要混为一谈；以为它处理的主要是最新未读结果

**历史摘要**（history summary）:
模型根据旧消息生成的事实状态，包含目标、文件、决定、剩余工作和用户约束；它是有损继续工作表示，不是完整备份。
出处：North [`s08_context_compact/code.py` L464–488](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:464)。
_Avoid_: 把摘要里的历史指令当成待执行命令；以为摘要替代 transcript

**反应式压缩**（reactive compact）:
API 已因输入过长拒绝请求后执行的补救：保存 transcript、摘要旧历史、保留最近消息，并由 `MAX_REACTIVE_RETRIES=1` 限制重试一次。
出处：North [`s08_context_compact/README.zh.md` L201–220](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/README.zh.md:201)、[`code.py` L529–548](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:529)。
_Avoid_: 当成自动无限重试；把服务端拒绝当成 Python 工具异常

**`messages[:]` 原地替换**:
用切片赋值替换原列表内容，保留列表对象身份；s08 用它让外层 `history` 看到 `prepare()` 或压缩后的消息。`messages = new_list` 只会重新绑定当前变量。
出处：North [`s08_context_compact/code.py` L529–531](cursor://file/d:/agent-learning/learn-claude-code-north/s08_context_compact/code.py:529)。
_Avoid_: 以为两种写法对所有共享引用效果相同

## Memory

**Memory / 记忆**:
跨当前会话保存、以后可能复用的结构化知识；不是 `messages` 的无损 transcript 备份。s09 用 `.memory/*.md` 保存记录，用召回选择相关正文。
出处：North [`s09_memory/README.zh.md` L13–30](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/README.zh.md:13)。
_Avoid_: 把保存全部聊天历史叫成已经完成的记忆；把记忆当模型权重。

**单下划线辅助函数**（如 `_memory_slug`）:
名字前的单个 `_` 是模块内部约定，表示不把它当稳定公开 API；它不会像 Java `private` 那样阻止外部访问。s09 的 `_memory_slug` 只是转调 `memory_slug`。
出处：North [`s09_memory/code.py` L102–103](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:102)；课件 0029 的存储节。
_Avoid_: 以为单下划线会自动产生权限拒绝；把约定当语法闸门。

**`_normalized_memory_text`**:
为重复比较准备文本的内部辅助函数：统一小写、折叠空白，再用一个空格拼回；不修改真正写盘的正文，也不是语义去重。
出处：North [`s09_memory/code.py` L105–106](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:105)；调用 [`L126–137`](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:126)。
_Avoid_: 把它当翻译器、正文清洗器或 embedding 相似度计算。

**记忆记录**（memory record）:
`.memory/` 下的一份 Markdown 文件，YAML frontmatter 保存 `name`、`description`、`type`，正文保存可复用内容。
出处：North [`s09_memory/README.zh.md` L35–68](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/README.zh.md:35)。
_Avoid_: 把 `MEMORY.md` 索引当成所有记录正文。

**记忆索引**（memory index）:
`.memory/MEMORY.md` 中由记录文件派生出的短目录；每行提供名称、文件链接和描述，用于选择相关记录。
出处：North [`s09_memory/code.py` L165–186](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:165)。
_Avoid_: 把索引当唯一真相；正文记录文件才是可重建索引的来源。

**召回**（recall）:
根据当前请求先从记忆目录选择少量记录，再读取对应正文并加入本次 system 背景。s09 最多选择 5 条，正文累计最多 20000 字符。
出处：North [`s09_memory/README.zh.md` L70–92](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/README.zh.md:70)；[`code.py` L280–330](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:280)。
_Avoid_: 把召回理解成把所有 `.memory` 文件全文发给模型。

**持久性 scope**（`persistent` / `current_task`）:
提取候选的适用范围。`persistent` 表示允许跨会话保存；`current_task` 表示一次性命令、临时路径或当前任务状态，不应写成长期记忆。
出处：North [`s09_memory/code.py` L360–386](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:360)。
_Avoid_: 看到模型返回候选就忽略 scope；把“本次不要创建文件”保存成永久规则。

**关键词降级**（keyword fallback）:
召回模型调用或 JSON 解析失败时，按当前请求词在记录的 name/description 中命中计分，取排名靠前的记录。它是可解释后备方案，不是向量语义检索。
出处：North [`s09_memory/code.py` L264–278](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:264)、[`L299–318`](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:299)。
_Avoid_: 以为关键词命中能理解所有同义表达；以为模型选择失败就必须让整个 Agent 退出。

**记忆提取**（memory extraction）:
在 Agent 到达没有 `tool_use` 的 Stop 点后，从对话中生成可能耐久的候选；候选仍须经过 scope、类型、非空、临时标记和重复检查。
出处：North [`s09_memory/code.py` L388–445](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:388)；loop 接入 [`L740–751`](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:740)。
_Avoid_: 把候选直接当成已验证事实；在工具尚未执行完时保存中间猜测。

**整理**（consolidation）:
记录达到阈值后，由模型合并重复、应用较新修正、删除无用内容；North 先校验结果并保存快照，再替换旧文件。
出处：North [`s09_memory/code.py` L450–532](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:450)。
_Avoid_: 把整理成功当成事实验证；把快照当成数据库事务。

**记忆快照**（memory snapshot）:
整理前保存的旧文件名到完整文件内容的字典；替换失败时删除半成品、写回快照并重建索引。
出处：North [`s09_memory/code.py` L493–528](cursor://file/d:/agent-learning/learn-claude-code-north/s09_memory/code.py:493)。
_Avoid_: 以为快照能解决并发写入、模型事实错误或所有崩溃时序。

## Frameworks (workspace stance)

当前不学封装层（LangChain / LangGraph 等）。对照用词以本书公式为准：Agent = LLM + 上下文 + 工具；Harness 是环绕模型的运行与治理层。
