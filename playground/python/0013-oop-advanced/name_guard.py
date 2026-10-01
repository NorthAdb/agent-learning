"""0013 主脚本：Day19 四块收在一个小工具名校验器里。

运行：
  cd d:\\agent-learning\\playground\\python
  python 0013-oop-advanced\\name_guard.py
"""

from __future__ import annotations


class ToolNameError(ValueError):
    """工具名不合法。"""


class ToolName:
    """工具名的值对象：创建时校验，之后当只读属性用。

    四块对照课件：
    - __slots__：只许 _value，防打错字变成野属性（讲解 2）
    - _value：单下划线内部存储；外面请用 .value（讲解 1）
    - @property value：只读对外接口，无 setter（讲解 3）
    - is_valid / parse：staticmethod 纯规则 + classmethod 工厂（讲解 4）
    """

    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not self.is_valid(raw):
            raise ToolNameError(f"invalid tool name: {raw!r}")
        self._value = raw

    @property
    def value(self) -> str:
        """getter（只读门面）：bash.value 走这里。

        没有 @value.setter → 写通道不存在；bash.value = ... 会 AttributeError。
        真格子是 _value；初值在 __init__ 里直接写 _value，不经过对外名。
        「@」是装饰器，不是注释器。
        """
        return self._value

    @staticmethod
    def is_valid(raw: str) -> bool:
        """纯规则，无 self/cls：造对象之前就能问（见课件 4.3）。"""
        if not raw or " " in raw:
            return False
        return raw.replace("_", "").isalnum()

    @classmethod
    def parse(cls, raw: str) -> ToolName:
        """工厂（课件 4.4「要造实例 + 子类仍得子类」）：

        ① 要造实例：返回 cls(...)，不是只算 True/False（那是 is_valid）。
        ② 照顾子类：写 cls 不写死 ToolName；若有 StrictName(ToolName)，
           StrictName.parse(...) 时 cls 就是 StrictName。
        """
        return cls(raw.strip())

    def __repr__(self) -> str:
        return f"ToolName({self._value!r})"


def main() -> None:
    bash = ToolName.parse("bash")
    print("ok:", bash, "value=", bash.value)
    print("is_valid glob:", ToolName.is_valid("glob"))
    print("is_valid bad:", ToolName.is_valid("bad name"))

    try:
        ToolName.parse("bad name")
    except ToolNameError as error:
        print("parse 失败 ->", type(error).__name__, error)

    try:
        bash.extra = True  # type: ignore[attr-defined]
    except AttributeError as error:
        print("slots 拦住动态属性 ->", type(error).__name__)


if __name__ == "__main__":
    main()
