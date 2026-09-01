# 可变默认值：三种情况已分清

用户已能把 `history=[]` 和 `bad_collect(bucket=[])` 认成同一对象被反复 append；也理解默认改成 `None` 后独立对话不再串，同一场对话要显式传入同一份 list 才会累加。

## Implications
- 后续讲消息历史 / 工具缓存时，把「默认 None + 调用方持有 session」当已知，不必从零讲可变默认值
