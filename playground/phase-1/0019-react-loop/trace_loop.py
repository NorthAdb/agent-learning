"""0019 — 三种「下一步谁决定」对照。

① ReAct：模型看轨迹再决定（想 → 做 → 看）
② 0003 剧本：fake_model(turn)，下一步按回合号写死
③ 工作流：代码写死 read → 数 TODO → 回答；模型不选路

不调真实 LLM，不跑 North s01/code.py。

原文：
  书 §1.1.5 标题 L168；三环节 L172；无 tool call 就返回 L189
  North README-zh.md 循环图 L140；「代码只是执行模型的要求」L156–157
  书用 ReAct 这个词；North README 不用，只画最小循环。

运行：
  cd d:\\agent-learning\\playground\\phase-1\\0019-react-loop
  python trace_loop.py
"""

from __future__ import annotations

from typing import Any

# Environment：磁盘上的假文件。没被工具读到，对模型等于不存在（0017）。
FILES = {
    "app.py": "# TODO: auth\n# TODO: cache\nprint('hi')\n",
}

USER = "app.py 里有几个 TODO？"


def env_read(path: str) -> str:
    """做：Harness 调工具；看：Environment 返回观察。"""
    if path not in FILES:
        return f"error: no such file {path!r}"
    return FILES[path]


def has_tool_call(decision: dict[str, Any]) -> bool:
    return bool(decision.get("tool_calls"))


# --- ① ReAct：下一步由「当前轨迹」决定 ---------------------------------


def react_model(trajectory: list[dict[str, Any]]) -> dict[str, Any]:
    """想：只根据已经进轨迹的东西做决定。不是按回合号取剧本。"""
    last = trajectory[-1]
    if last.get("role") == "user":
        return {
            "role": "assistant",
            "think": "文件内容不在轨迹里，先 read。",
            "tool_calls": [{"name": "read_file", "path": "app.py"}],
        }
    if last.get("role") == "tool":
        text = last.get("content", "")
        n = text.count("TODO")
        return {
            "role": "assistant",
            "think": "已经看见文件，可以数 TODO 并回答。",
            "content": f"有 {n} 个 TODO。",
        }
    return {"role": "assistant", "content": "不知道下一步。"}


def run_react(max_turns: int = 4) -> None:
    print("=== ① ReAct：模型看轨迹 ===")
    print("规则：代码只执行模型点名的工具，不替它选下一步。\n")
    trajectory: list[dict[str, Any]] = [{"role": "user", "content": USER}]
    for turn in range(max_turns):
        print(f"-- turn {turn} 想 --")
        decision = react_model(trajectory)
        print("  Model:", decision.get("think") or decision.get("content"))
        trajectory.append(decision)
        if not has_tool_call(decision):
            print("  无 tool call → 停。答案：", decision.get("content"))
            print()
            return
        print("-- 做 / 看 --")
        for call in decision["tool_calls"]:
            # 本课最小循环不写校验；constrain 是 0018 的生产层，阶段 2 再接。
            obs = env_read(call["path"])
            print(f"  Harness 执行 {call['name']}({call['path']!r})")
            print("  Environment 观察：", repr(obs)[:60])
            trajectory.append({"role": "tool", "name": call["name"], "content": obs})
    print("  触顶 max_turns，安全带停。\n")


# --- ② 0003 形状：下一步按回合号，不看轨迹 --------------------------------


def scripted_model(turn: int) -> dict[str, Any]:
    """0003 的 fake_model(turn)：作者写死第 0 轮调工具、第 1 轮给答案。"""
    script = [
        {
            "role": "assistant",
            "think": "（剧本第 0 轮）去 read。",
            "tool_calls": [{"name": "read_file", "path": "app.py"}],
        },
        {
            "role": "assistant",
            "think": "（剧本第 1 轮）给最终句。",
            "content": "有 2 个 TODO。",
        },
    ]
    if turn >= len(script):
        return {"role": "assistant", "content": "(剧本用完)"}
    return script[turn]


def run_scripted() -> None:
    print("=== ② 0003 剧本：下一步按回合号 ===")
    print("形状也是 while；但模型函数不读轨迹，只看 turn。\n")
    turn = 0
    while turn < 4:
        print(f"-- turn {turn} --")
        decision = scripted_model(turn)
        print("  剧本：", decision.get("think") or decision.get("content"))
        if not has_tool_call(decision):
            print("  停。答案：", decision.get("content"))
            print()
            return
        for call in decision["tool_calls"]:
            obs = env_read(call["path"])
            print(f"  仍会执行工具（观察={obs.count('TODO')} 个 TODO），但下一轮不靠这份观察来选。")
        turn += 1
    print()


# --- ③ 工作流：路径写死 -------------------------------------------------


def run_workflow() -> None:
    print("=== ③ 工作流：代码写死 read → 数 → 答 ===")
    print("LLM 若出现，也只在节点里填字，不选节点。本课连填字都省略。\n")
    print("  节点 1 写死：read app.py")
    text = env_read("app.py")
    print("  节点 2 写死：用 Python 数 TODO（不是模型决定要数）")
    n = text.count("TODO")
    print(f"  节点 3 写死：输出「有 {n} 个 TODO。」")
    print()


def main() -> None:
    print("用户问：", USER)
    print("对照：谁决定「下一步调不调工具、调哪个」。\n")
    run_react()
    run_scripted()
    run_workflow()
    print("记住：① 才是 ReAct。② 是控制流预习。③ 是 0017 的工作流。")


if __name__ == "__main__":
    main()
