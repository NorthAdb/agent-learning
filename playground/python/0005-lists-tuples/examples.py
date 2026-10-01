"""0005 — 七个例子：列表与元组怎么用。

先读这个文件，再运行。每个例子对应课件「系统讲解」里的同名小节。
注释里写着「为什么这样写」；例子里凡是会崩溃的写法都注释掉了，先看注释再想为什么不能跑。

运行（先激活 venv）：
  cd d:\\agent-learning\\playground\\python
  .\\.venv\\Scripts\\Activate.ps1
  python 0005-lists-tuples\\examples.py
"""

from __future__ import annotations


print("=== 例1：创建与索引 ===")

# 从 range 构造、从字符串构造、用乘法造一排初始值
nums = list(range(1, 6))        # [1, 2, 3, 4, 5]
letters = list("abc")           # ['a', 'b', 'c']
zeros = [0] * 6                 # 6 个 0；0 是不可变对象，这样造没问题
print("nums   =", nums)
print("letters=", letters)
print("zeros  =", zeros)
print("len(nums)=", len(nums))
print("nums[0] =", nums[0])     # 第一个
print("nums[-1] =", nums[-1])   # 倒数第一个（负索引从末尾数）
nums[2] = 99                    # 修改既有元素：列表可变
print("改过 nums =", nums)
# print(nums[9])                # IndexError: list index out of range，越界就崩


print("\n=== 例2：切片（返回新 list；越界不报错）===")

chunks = ["chunk-a", "chunk-b", "chunk-c", "chunk-d", "chunk-e"]
print("chunks[1:3] =", chunks[1:3])       # 1 起，3 止，不含 3
print("chunks[:3]  =", chunks[:3])        # 省 start
print("chunks[::2] =", chunks[::2])       # 隔一个取一个
print("chunks[::-1]=", chunks[::-1])      # 负步长 = 反转，得到新 list
print("chunks[10:] =", chunks[10:])       # 越界不崩，返回 []
print("chunks[:] == 拷贝", chunks[:] == chunks)

# 拷贝和引用是两回事：改 alias 会漏进原列表，改 copy 不会
copy = chunks[:]           # 拷贝：独立的一份
alias = chunks             # 共享同一个 list 对象（不是拷贝！）
alias.append("extra")      # 改 alias 就是改 chunks
print("原列表跟着变了:", chunks[-1] == "extra")    # True
print("拷贝没被波及   :", copy[-1] != "extra")     # True


print("\n=== 例3：遍历与成员 ===")

hits = [
    {"id": "d-07", "score": 0.91},
    {"id": "d-03", "score": 0.72},
    {"id": "d-01", "score": 0.31},
]
# enumerate 每次给一个 (位置, 元素) 二元组；for i, h 就是在解包它
for i, h in enumerate(hits, start=1):
    print(f"  #{i} {h['id']} score={h['score']}")

ids = ["d-07", "d-03", "d-01"]
print("'d-03' in ids =", "d-03" in ids)
print("'d-99' in ids =", "d-99" in ids)

# zip：把两个列表按位置配对（这里是 ids 和分数）
scores2 = [0.91, 0.72, 0.31]
for doc_id, score in zip(ids, scores2):
    print(f"  zip -> {doc_id}: {score}")


print("\n=== 例4：增删与拼接（append 和 extend 的区别在这里）===")

pool = []
pool.append("d-01")               # 加一个元素
pool.append(["d-02", "d-03"])     # append 把整个 list 当一个元素：嵌套了
print("append 之后:", pool)       # ['d-01', ['d-02', 'd-03']]

pool.clear()                      # 清空重来
pool.extend(["d-02", "d-03"])     # extend 把序列元素逐个并入：展平
print("extend 之后:", pool)       # ['d-02', 'd-03']

# remove 按值删（只删第一个命中）；pop 按位置删并把删掉的元素交还给你
pool = ["a", "b", "a"]
pool.remove("a")
print("remove('a') 后:", pool)    # ['b', 'a']，删的是第一个 'a'
last = pool.pop()
print("pop() 返回:", last, "剩下:", pool)
# pool.remove("zz")               # ValueError: 找不到会崩，删人前先 in 判断

# + 拼出新 list；+= 原地并入（等价 extend）
a = [1]
b = [2, 3]
c = a + b
print("a + b =", c, "原 a =", a)
a += b
print("a += b 后 a =", a)


print("\n=== 例5：排序（sort 原地返回 None，sorted 返回新 list）===")

scores = [0.72, 0.91, 0.45, 0.84, 0.31]
print("sorted(scores) =", sorted(scores))        # 新 list，scores 没动
print("scores 还是原样:", scores)
scores.sort()                                     # 原地改 scores
print("scores.sort() 后:", scores)
x = scores.sort()                                 # 注意：sort 返回 None
print("x = scores.sort() 得到:", x)               # None！别把返回值赋回变量
print("min/max/sum =", min(scores), max(scores), sum(scores))

# 对 list[dict] 按字段排：key= 给出「每个元素的排序键」
raw = [
    {"id": "d-07", "score": 0.91},
    {"id": "d-03", "score": 0.72},
    {"id": "d-01", "score": 0.31},
]
ranked = sorted(raw, key=lambda h: h["score"], reverse=True)
print("按 score 降序:", [h["id"] for h in ranked])
print("index/count :", scores.index(0.72), scores.count(0.45))


print("\n=== 例6：列表生成式（过滤 + 投影一条完成）===")

hits = [
    {"id": "d-01", "text": "过期的旧文档", "score": 0.31},
    {"id": "d-03", "text": "Harness 是运行外壳", "score": 0.72},
    {"id": "d-07", "text": "RAG 先检索再生成", "score": 0.91},
]
# 只要 id（投影）
ids = [h["id"] for h in hits]
print("只取 id   :", ids)
# 只留分数够的（过滤），再只取 text（投影）
ok = [h["text"] for h in hits if h["score"] >= 0.5]
print("过滤+投影 :", ok)
# 六行变一行（Day09 的双色球写法同类）：生成式强烈推荐
squares = [n * n for n in range(1, 6)]
print("平方表    :", squares)


print("\n=== 例7：元组与解包 ===")

pair = ("d-07", 0.91)             # 二元组：id + 分数
doc_id, score = pair              # 解包：一个变量接一个元素
print("解包:", doc_id, score)
# pair[0] = "x"                  # TypeError: 元组不可变

a, b = 1, 2
a, b = b, a                       # 交换；Python 不用中间变量
print("交换后 a, b =", a, b)

first, *rest = [1, 2, 3, 4]       # *rest 收走剩下的，得到一个 list
print("first, *rest =", first, rest)

single = ("only", )               # 一元组：逗号不可省
print("类型:", type(single))      # <class 'tuple'>
print("('only') 的类型:", type(("only")))   # <class 'str'>，不带逗号只是括号

ids_list = list(pair)             # tuple -> list
print("tuple 转 list:", ids_list)