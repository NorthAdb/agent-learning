"""0013 — Day19 四块：可见性 / slots / property / 三种方法。

运行：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0013-oop-advanced\\examples.py
"""

from __future__ import annotations


print("=== 例1：三种名字 —— 公开 / 约定内部 / 名称改写 ===")
# Bag / bag 不是关键字：类名 + 实例变量名，换成 Box / box 一样。


class Bag:
    def __init__(self, token: str) -> None:
        self.token = token           # 公开：外面 bag.token 是正式用法
        self._cache = {}             # 单 _：约定内部；外面能读，但不该当 API
        self.__secret = "s3cret"     # 双 __：存成 _Bag__secret（防子类踩名，非沙箱）


bag = Bag("sk-demo")
print("公开 token:", bag.token)                 # 正式接口
print("约定 _cache（能读但不该依赖）:", bag._cache)
print("改写后真名 _Bag__secret:", bag._Bag__secret)
try:
    print(bag.__secret)                         # 按字面找不到
except AttributeError as error:
    print("直接 .__secret ->", type(error).__name__)


print("\n=== 例1b：为什么要改写 —— 子类别踩掉父类 ===")
# 场景：父类有内部状态；子类作者不知情，也写了同名属性。


class Parent:
    def __init__(self) -> None:
        self._cache = "父:_cache"
        self.__secret = "父:__secret"   # 实际存成 _Parent__secret


class Child(Parent):
    def __init__(self) -> None:
        super().__init__()
        self._cache = "子:_cache"       # 同一格子 → 直接盖住父的
        self.__secret = "子:__secret"   # 存成 _Child__secret → 父的那份还在


child = Child()
print("单 _ ：只剩子的 =", child._cache)
print("双 __ 父仍在 =", child._Parent__secret)
print("双 __ 子自己的 =", child._Child__secret)


print("\n=== 例2：__slots__ 三案（无锁 / 名单内 / 名单外）===")
# 「三案」= 三种对照情况。slots 锁的是「允许哪些属性名」，不是 private。


class OpenBox:
    def __init__(self, name: str) -> None:
        self.name = name


class ClosedBox:
    __slots__ = ("name",)  # 单元素元组：逗号不能省

    def __init__(self, name: str) -> None:
        self.name = name


open_box = OpenBox("a")
open_box.extra = 1
print("① 无 slots：可动态加 extra =", open_box.extra)

closed = ClosedBox("b")
closed.name = "b2"
print("② slots 内的 name 可改 =", closed.name)
try:
    closed.extra = 1  # 名单里没有 extra
except AttributeError as error:
    print("③ slots 外动态加属性 ->", type(error).__name__)


print("\n=== 例3：@property —— 当属性读 / setter 校验 / 只读 ===")
# 两个名字：
#   _max_retries = 真格子（普通 int）
#   max_retries  = 对外门面（读走 @property，写走 @xxx.setter）
# setter = 给「赋值」装的钩子：先校验，再写入真格子。
#
# 创建 RetryPolicy(3):
#   __init__ → self._max_retries = 0（不走 setter）
#            → self.max_retries = 3（走 setter → 校验 → _max_retries = 3）
# 读 policy.max_retries     → getter → return _max_retries（不要加 ()）
# 写 policy.max_retries = 5 → setter(value=5) → 校验 → _max_retries = 5
# 写 = -1                   → setter 里 raise；真格子不变
#
# 对照：
#   外面 max_retries ──读──▶ @property ──▶ _max_retries
#                    ──写──▶ @setter   ──▶ 校验后写入 _max_retries


class RetryPolicy:
    def __init__(self, max_retries: int) -> None:
        # ① 建内部格子：写带 _ 的真名，不触发 setter
        self._max_retries = 0
        # ② 赋对外名：触发 setter，创建时就校验（RetryPolicy(-1) 会直接失败）
        self.max_retries = max_retries

    @property
    def max_retries(self) -> int:
        # 读 policy.max_retries 时调用；必须读 _max_retries
        # 写成 return self.max_retries 会再次进 getter → 递归
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        # 写 policy.max_retries = ... 时调用
        if value < 0:  # 门卫：非法则抛错，不改数据
            raise ValueError("max_retries must be >= 0")
        self._max_retries = value  # 合法才写入真格子


class ReadonlyLabel:
    def __init__(self, text: str) -> None:
        self._text = text

    @property
    def text(self) -> str:
        # 只有 getter、没有 .setter → 只读；赋值会 AttributeError
        return self._text


policy = RetryPolicy(3)
print("① 当属性读（无括号）:", policy.max_retries)
policy.max_retries = 5
print("② setter 写入后:", policy.max_retries)
try:
    policy.max_retries = -1
except ValueError as error:
    print("② 非法赋值 ->", error)

label = ReadonlyLabel("bash")
print("③ 只读 property:", label.text)
try:
    label.text = "other"  # type: ignore[misc]
except AttributeError as error:
    print("③ 只读再赋值 ->", type(error).__name__)


print("\n=== 例4：实例方法 / staticmethod / classmethod ===")
# self=某一个成品；cls=图纸。工厂用 return cls(...)，子类调用仍得到子类。


class ToolSpec:
    def __init__(self, name: str) -> None:
        self.name = name

    def schema(self) -> dict[str, str]:
        return {"name": self.name}

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name) and " " not in name

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ToolSpec":
        return cls(data["name"])


class SpecialTool(ToolSpec):
    pass


print("实例方法:", ToolSpec("bash").schema())
print(
    "静态方法（无实例）:",
    ToolSpec.is_valid_name("rag_search"),
    ToolSpec.is_valid_name("bad name"),
)
print("类方法工厂:", ToolSpec.from_dict({"name": "read"}).name)
print("子类调同一工厂:", type(SpecialTool.from_dict({"name": "x"})).__name__)
