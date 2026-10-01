"""0012 主脚本：用 class 做工具注册表（对照 North 的 TOOL_HANDLERS dict）。

North s01/s02 用「函数 + dict」就够；s12 起会出现 @dataclass class Task。
本文件把同一套 dispatch 收成对象，方便你对照两种写法。

运行：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0012-classes\\tool_registry.py

────────────────────────────────────────────────────────
整体流程（从上到下读这个文件）
────────────────────────────────────────────────────────

  ① 工具实现（普通函数，写在 class 外）
     run_echo / run_read —— 真正干活的代码；只有「要给模型调用的」才进表。

  ② ToolSpec（dataclass）—— 一条工具的「说明书 + 实现」
     字段：name / description / handler / calls
     构造：ToolSpec("echo", "说明", run_echo)  传 3 个，calls 自动 []
     handler 格子里存 run_echo（函数对象，无括号），不是 Callable 标注本身。
     run(**arguments) → append 调用记录 → self.handler(**arguments)

  ③ ToolRegistry —— 注册表对象
     __init__：self._tools = {}  空 dict，键=工具名，值=ToolSpec
     register(spec)：self._tools[spec.name] = spec  写入（键一定有，来自 spec.name）
     dispatch(name, arguments)：
         spec = _tools.get(name)   读（name 可能没有 → None）
         没有 → UnknownToolError
         有   → spec.run(**arguments) → 返回 str 观察
     list_schemas()：列出已注册工具的 name/description

  ④ build_demo_registry() —— 装配演示用注册表
     registry = ToolRegistry()
     register(ToolSpec("echo", ..., run_echo))
     register(ToolSpec("read", ..., run_read))
     此时 _tools ≈ {"echo": ToolSpec(...), "read": ToolSpec(...)}

  ⑤ main() —— 跑一遍完整链路
     list_schemas()           看注册了哪些工具
     dispatch("echo", {...})  成功 → echo.calls 多一条
     dispatch("read", {...})  成功 → read.calls 多一条；与 echo.calls 互不影响
     dispatch("glob", {...})  失败 → UnknownToolError（glob 没 register）

────────────────────────────────────────────────────────
和 Agent loop 的对应（本脚本没有真调模型，但结构一样）
────────────────────────────────────────────────────────

  模型输出（概念上）:  name="echo", arguments={"text": "pwd"}
           ↓
  harness:             registry.dispatch("echo", {"text": "pwd"})
           ↓
  查表:                _tools["echo"]  → 那份 ToolSpec
           ↓
  执行:                run_echo(text="pwd")  →  "(echo) pwd"
           ↓
  观察:                把 str 塞回 messages，进入下一轮 loop

  对照 North s02：TOOL_HANDLERS[name](**input) —— 同一句话，值从「函数」换成「ToolSpec」。
"""

from __future__ import annotations

# Callable：类型标注用，表示「能 () 调用的对象」。
# collections.abc = 标准库「抽象基类」模块（abc = Abstract Base Classes，不是字母表）。
from collections.abc import Callable
from dataclasses import dataclass, field


class UnknownToolError(Exception):
    """注册表里没有这个工具名。loop 应把它当成一次 tool error 观察。"""


@dataclass
class ToolSpec:
    """一条工具的说明书 + 实现。

    @dataclass：装饰器。写在 class 上一行，等价于
    ToolSpec = dataclass(ToolSpec)，自动生成 __init__ / repr。
    本课不要求自己写装饰器函数；见到 @xxx 就读成「下一行被 xxx 加工过」。

    handler：函数对象（0004）。注意没有 () —— 存的是函数本身。
    calls：每个 ToolSpec 实例自己的调用记录（三案①）。
    """

    name: str
    description: str
    # Callable[..., str] —— 本课（0012）首次出现的标注写法；0009 的标注 + 0004 的存函数。
    #
    # 【存的是什么】格子里的真值是 run_echo 等函数，不是 Callable 这个类型名。
    #   类比：age: int = 18  存的是 18，不是 int。
    #
    # 【Callable[..., str] 拆开】
    #   Callable[..., str]
    #              ↑    ↑
    #              │    └── 标注：应返回 str（本课工具观察文本）
    #              └── ...：参数形状不写死（echo 要 text，read 要 path）
    #
    # 【运行时】self.handler(**arguments) 调的是存着的函数，不是调 Callable。
    #   键对不上形参 → TypeError。标注默认不拦（0009）。
    handler: Callable[..., str]
    # field / default_factory 都不是 Python 关键字，来自 dataclasses 模块：
    #   field()           — 配置字段的函数
    #   default_factory   — 传给 field 的参数名
    #   = list            — 传 list 函数本身（无括号）；每次 ToolSpec(...) 时 list() 新建空列表
    # 对应讲解 4 三案①；不要写 calls: list[str] = []（会串，同 0004 默认 list 坑）
    calls: list[str] = field(default_factory=list)

    # 上面 name/description/handler/calls = 作者选的属性清单，不是语言强制。

    def schema(self) -> dict[str, str]:
        """给模型看的短描述（s01 里 TOOLS 列表的简化版）。"""
        return {"name": self.name, "description": self.description}

    def run(self, **arguments: str) -> str:
        self.calls.append(self.name)
        # **arguments 把 dict 拆成关键字参数；handler 的 ... 就是指「这些键因工具而异」
        return self.handler(**arguments)


class ToolRegistry:
    """名字 → ToolSpec 的注册表（讲解 3）。

    和 0004 的 TOOLBOX dict 同一件事：按名字找到可调用实现再传参。
    register 时存函数对象（run_echo 无括号）；dispatch 时才调用。
    """

    def __init__(self) -> None:
        # 本实例的「工具抽屉」：工具名(str) → 一份 ToolSpec。
        # dict[str, ToolSpec] 是 0009 类型标注；运行时就是普通 {}。
        # 每个 ToolRegistry() 各有一张空表；register 往里塞，dispatch 按名取。
        # 对照 North s02：TOOL_HANDLERS = {"echo": run_echo, ...}（值是函数）；
        # 这里值升级成 ToolSpec（含 name/description/handler/calls）。
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        # 按 spec.name 当键，整份 ToolSpec 当值（含 handler 函数对象，不是执行结果）
        self._tools[spec.name] = spec

    def dispatch(self, name: str, arguments: dict[str, str]) -> str:
        # 模型点名 name + 参数 dict → 查表 → 调 spec.run(**arguments)
        spec = self._tools.get(name)
        if spec is None:
            raise UnknownToolError(f"unknown tool: {name}")
        # spec.run 内部：self.calls.append + self.handler(**arguments)
        return spec.run(**arguments)

    def list_schemas(self) -> list[dict[str, str]]:
        # 列出已注册工具的 name/description，给模型看（s01 的 TOOLS 列表简化版）
        return [spec.schema() for spec in self._tools.values()]


def run_echo(text: str) -> str:
    """假 bash：不真执行命令，只回显。"""
    return f"(echo) {text}"


def run_read(path: str) -> str:
    """假 read：返回固定内容，演示第二个工具。"""
    return f"(read) {path} → hello from knowledge.txt"


def build_demo_registry() -> ToolRegistry:
    registry = ToolRegistry()
    # ToolSpec 类有 4 个字段；下面括号里只写了 3 个实参：
    #   1 name  2 description  3 handler（函数对象，无括号）
    # 第 4 个 calls 有 default_factory，本行省略 → 自动 []。
    # 若手填第 4 个：ToolSpec("echo", "说明", run_echo, ["already"])
    registry.register(
        ToolSpec("echo", "Echo a string; fake bash.", run_echo)
    )
    registry.register(
        ToolSpec("read", "Read a fake file.", run_read)
    )
    return registry


def main() -> None:
    # ── main 逐步对应上面 docstring ⑤ ──
    registry = build_demo_registry()          # ④ 装配：空表 → 注册 echo/read
    print("schemas:", registry.list_schemas())  # ③ list_schemas：给模型看的清单

    print("dispatch echo ->", registry.dispatch("echo", {"text": "pwd"}))
    # ③ dispatch("echo", ...) → get("echo") 有 → run(**{"text":"pwd"}) → run_echo

    print("dispatch read ->", registry.dispatch("read", {"path": "kb.md"}))
    # 同上；read 与 echo 是不同 ToolSpec，calls 各记各的

    echo = registry._tools["echo"]          # 演示：注册后键一定存在，可直接 []
    print("echo.calls（本实例）->", echo.calls)
    print("read.calls（另一实例）->", registry._tools["read"].calls)

    try:
        registry.dispatch("glob", {"pattern": "*.py"})
        # ③ get("glob") → None → UnknownToolError（没 register 的名字）
    except UnknownToolError as error:
        print("unknown tool ->", type(error).__name__, error)

    print("repr:", echo)                    # dataclass 自动 __repr__


if __name__ == "__main__":
    main()
