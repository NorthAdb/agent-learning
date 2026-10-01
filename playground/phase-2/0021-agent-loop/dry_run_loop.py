"""用假模型演示 North s01 的消息往返，不访问网络、不执行 shell。"""


def fake_model(messages: list[dict]) -> dict:
    """只根据消息历史决定：第一次要工具，看到结果后结束。"""
    has_tool_result = any(
        message["role"] == "user" and isinstance(message["content"], list)
        for message in messages
    )
    if not has_tool_result:
        return {
            "stop_reason": "tool_use",
            "content": [
                {"type": "text", "text": "先查看当前目录。"},
                {
                    "type": "tool_use",
                    "id": "call_1",
                    "name": "bash",
                    "input": {"command": "python -c \"print('demo.py')\""},
                },
            ],
        }
    return {
        "stop_reason": "end_turn",
        "content": [
            {"type": "text", "text": "我看到了工具结果：当前目录有 demo.py。"}
        ],
    }


def run_fake_bash(command: str) -> str:
    """假装执行命令，故意不把字符串交给操作系统。"""
    print(f"$ {command}")
    return "demo.py"


def agent_loop(messages: list[dict]) -> str:
    """复刻 s01 的控制结构，但把真实 API 和 shell 换成了假实现。"""
    while True:
        response = fake_model(messages)
        messages.append({"role": "assistant", "content": response["content"]})

        tool_calls = [
            block for block in response["content"] if block["type"] == "tool_use"
        ]
        if not tool_calls:
            return "".join(
                block["text"]
                for block in response["content"]
                if block["type"] == "text"
            )

        results = []
        for block in tool_calls:
            output = run_fake_bash(block["input"]["command"])
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block["id"],
                    "content": output,
                }
            )
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    history = [{"role": "user", "content": "当前目录有什么文件？"}]
    answer = agent_loop(history)
    print(answer)
    print(f"消息条数：{len(history)}")
