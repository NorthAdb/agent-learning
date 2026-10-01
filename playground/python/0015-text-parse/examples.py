"""0015 — re 三案 + DOTALL + eval / literal_eval。

为何学：从模型乱文本里定位结构并安全变成对象。
eval 本课第一次讲（0006 的 "eval" 只是集合里的工具名字符串）。

运行：
  cd d:\\agent-learning\\playground\\python
  python 0015-text-parse\\examples.py
"""

from __future__ import annotations

import ast
import re


print("=== 例1：re.search / group / 找不到 ===")
# text = "ids: [req_1, req_2] trailing"
# matched = re.search(r"\[(.*?)\]", text)
#
# r"..."     原始字符串，\ 交给正则
# search     从左找第一处；找到 Match，找不到 None
# \[  \]     字面量方括号（裸 [ 是字符类，必须转义）
# ( ... )    捕获组 → group(1)
# .*?        任意内容，非贪婪：在第一个 ] 就停
#
# group(0) → "[req_1, req_2]"   整段（含括号）
# group(1) → "req_1, req_2"     括号里面
# 顺序：search → 判不是 None → 再 group

text = "ids: [req_1, req_2] trailing"
matched = re.search(r"\[(.*?)\]", text)
print("① 找到:", matched.group(0), "| 捕获组:", matched.group(1) if matched else None)

missing = re.search(r"\d{8}", "no digits here")
print("② 找不到返回:", missing)  # None，不要对它 .group

# re.compile：先把模式编译成 Pattern，以后反复 .match / .search
# 适合「同一规则用很多次」或挂成模块常量（主脚本 TODO_BLOCK 同款）
# ^...$ = 整串从头到尾都要符合
compiled = re.compile(r"^[A-Za-z0-9._-]{1,16}$")
print("③ compile 复用:", bool(compiled.match("task_01")), bool(compiled.match("bad name")))


print("\n=== 例2：DOTALL 让 . 能匹配换行 ===")
# 默认 . 不跨行；模型吐的 list 常折行 → 加 re.DOTALL

blob = "start[\n  a,\n  b\n]end"
print("无 DOTALL:", re.search(r"\[.*\]", blob))
print("有 DOTALL:", bool(re.search(r"\[.*\]", blob, re.DOTALL)))


print("\n=== 例3：eval（先认） vs literal_eval（模型用） ===")
# eval(s)           内置函数：把字符串当 Python 表达式执行
#                   eval("1+2") → 3；eval("[1,2]") → list
#                   模型/不可信字符串 → 禁止 eval（可执行 os.system 等）
#
# ast.literal_eval  只吃字面量；拒绝函数调用；North s05 解析 todos 用这个
# json.loads        标准 JSON（0008）；双引号

print("eval 演示（自己写死的无害串）:", eval("1 + 2"), eval("[1, 2, 3]"))

literal = ast.literal_eval("[{'id': 1, 'done': False}]")
print("literal_eval 正常数据 ->", literal, type(literal[0]))

bad = "__import__('os').system('echo hack')"
# eval(bad)  # 禁止！会真的执行；本脚本不运行
try:
    ast.literal_eval(bad)
except (ValueError, SyntaxError) as error:
    print("literal_eval 拒绝恶意串 ->", type(error).__name__)
