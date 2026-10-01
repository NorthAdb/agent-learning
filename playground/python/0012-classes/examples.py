"""0012 — 四个小例：class / 实例 / self / 可变状态三案。

先读这个文件，再运行。每个例子对应课件「系统讲解」里的同名小节。

运行（先激活 venv）：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0012-classes\\examples.py
"""

from __future__ import annotations


print("=== 例1：class 是图纸，实例是按图纸造出来的对象 ===")


class Session:
    """一次对话会话。类 = 模板；每次 Session() 造出一个独立对象。"""

    def __init__(self, user: str) -> None:
        # self：当前正在初始化的那一个实例（不是类本身）
        self.user = user
        self.turns = 0

    def note(self, text: str) -> str:
        self.turns += 1
        return f"{self.user}#{self.turns}: {text}"


a = Session("alice")
b = Session("bob")
print("a.note ->", a.note("search docs"))
print("b.note ->", b.note("run tests"))
print("a.turns / b.turns ->", a.turns, b.turns)
print("a is b ->", a is b, "  # 两个实例，两份内存")
print("type(a) ->", type(a))  # <class '__main__.Session'>


print("\n=== 例2：方法就是「绑在实例上的函数」；self 由点号左边填入 ===")

# 这两种写法是同一件事：点号左边的对象，会进第一个参数 self
print("对象.方法:", a.note("via instance"))
print("类.方法:  ", Session.note(a, "via class"))


print("\n=== 例3：可变状态三案（必背）===")


class Isolated:
    def __init__(self) -> None:
        self.calls: list[str] = []  # 每个实例 __init__ 里新建

    def ping(self) -> None:
        self.calls.append("ping")


class SharedOnClass:
    calls: list[str] = []  # 类属性：所有实例共享同一份 list

    def ping(self) -> None:
        self.calls.append("ping")


class SharedDefault:
    def __init__(self, calls: list[str] = []) -> None:  # noqa: B006 故意演示
        self.calls = calls

    def ping(self) -> None:
        self.calls.append("ping")


x1, x2 = Isolated(), Isolated()
x1.ping()
print("① __init__ 里 self.calls=[]  → x1", x1.calls, "x2", x2.calls, "隔离")

y1, y2 = SharedOnClass(), SharedOnClass()
y1.ping()
print("② 写在 class 体上的 calls=[] → y1", y1.calls, "y2", y2.calls, "串了")

z1, z2 = SharedDefault(), SharedDefault()
z1.ping()
print("③ 默认参数 calls=[]         → z1", z1.calls, "z2", z2.calls, "串了")
print("   ③ 和 0004 函数默认 list 是同一条规则：默认值在定义时求值一次")


print("\n=== 例4：继承 —— 自定义异常是 Exception 的子类 ===")


class UnknownToolError(Exception):
    """工具名不在注册表里。0010 的 AgentHttpError 也是这种写法。"""


try:
    raise UnknownToolError("no tool named glob")
except UnknownToolError as error:
    print("caught:", type(error).__name__, "-", error)
    print("isinstance(error, Exception) ->", isinstance(error, Exception))


print("\n=== 例5：dataclass 的 field(default_factory=list) ===")

from dataclasses import dataclass, field


@dataclass
class MiniSpec:
    """教学用缩小版 ToolSpec：只保留 name + calls，方便单测 default_factory。

    name 会存进实例（见下方 print），本例不测 dispatch；
    完整版见 tool_registry.py 的 ToolSpec：name 用于注册表查表、schema、calls 记录。
    """

    name: str
    # 安全：每次 MiniSpec(...) 调用 list()，对应三案 ①
    calls: list[str] = field(default_factory=list)


m1 = MiniSpec("echo", ["used"]) # name 必填；字符串会存到 m1.name，本例重点在 calls 是否隔离
m2 = MiniSpec("read", ["ud"])
print("  各实例的 name（有存，只是本例逻辑不用它）->", m1.name, m2.name)
m1.calls.append("abc")
print("① field(default_factory=list) → m1", m1.calls, "m2", m2.calls, "隔离")

# 下面这段不要取消注释——故意演示 dataclass 写 = [] 会串（同讲解 6.1）
# @dataclass
# class BadSpec:
#     name: str
#     calls: list[str] = []
# b1, b2 = BadSpec("a"), BadSpec("b")
# b1.calls.append("x")
# print("③ dataclass calls=[] → b1", b1.calls, "b2", b2.calls, "串了")
