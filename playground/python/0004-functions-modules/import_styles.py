"""四种 import：差别不是「加载几次」，而是「当前文件多了哪些名字」。

每个函数是一块干净的局部命名空间，所以 dir() 不会被其它写法污染。

运行：
  python 0004-functions-modules\\import_styles.py
"""

from __future__ import annotations


def demo_import_module() -> None:
    import tools
    print("写法1  import tools")
    print("  有名字 tools?   ", "tools" in dir())
    print("  有名字 run_tool?", "run_tool" in dir())
    print("  调用:", tools.run_tool("nope", {}))


def demo_from_import() -> None:
    from tools import run_tool
    print("写法2  from tools import run_tool")
    print("  有名字 tools?   ", "tools" in dir())
    print("  有名字 run_tool?", "run_tool" in dir())
    print("  调用:", run_tool("nope", {}))


def demo_from_as() -> None:
    from tools import run_tool as exec_tool
    print("写法3  from tools import run_tool as exec_tool")
    print("  有名字 run_tool? ", "run_tool" in dir())
    print("  有名字 exec_tool?", "exec_tool" in dir())
    print("  调用:", exec_tool("nope", {}))


def demo_import_as() -> None:
    import tools as t
    print("写法4  import tools as t")
    print("  有名字 tools?", "tools" in dir())
    print("  有名字 t?    ", "t" in dir())
    print("  调用:", t.run_tool("nope", {}))


if __name__ == "__main__":
    demo_import_module()
    print()
    demo_from_import()
    print()
    demo_from_as()
    print()
    demo_import_as()
    print()
    print("四次都加载同一份 tools.py；loop.py 用的是写法2。")
