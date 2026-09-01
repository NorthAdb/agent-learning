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
模型本轮生成结束的原因。本课只对比：`tool_use` = 还要调工具；其它 = 说完了，返回文本。书写成「没有 tool call 就返回」。出处：North README-zh.md L146、L219；书 L189。
_Avoid_: 当成 HTTP 状态码；以为 README 的 `while True` 骨架已经含最大轮数

**max_turns**:
Agent loop 的轮数上限，用作防死循环的安全带。
_Avoid_: temperature、max_tokens

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

## Frameworks (workspace stance)

当前不学封装层（LangChain / LangGraph 等）。对照用词以本书公式为准：Agent = LLM + 上下文 + 工具；Harness 是环绕模型的运行与治理层。
