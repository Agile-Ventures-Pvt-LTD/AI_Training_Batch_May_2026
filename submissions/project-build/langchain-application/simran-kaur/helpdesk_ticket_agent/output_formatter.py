import json


OUTPUT_FILE = "outputs/evaluation_outputs.json"


def get_tools_used(agent_response):
    tools = []

    if agent_response is None:
        return tools

    messages = agent_response.get("messages", [])

    for message in messages:
        tool_calls = getattr(message, "tool_calls", [])

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")

            if tool_name and tool_name not in tools:
                tools.append(tool_name)

        message_name = getattr(message, "name", None)

        if message_name and message_name not in tools:
            tools.append(message_name)

    return tools


def get_json_from_answer(final_answer):
    try:
        return json.loads(final_answer)
    except:
        return {}


def read_json_file():
    try:
        file = open(OUTPUT_FILE, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
        return data
    except:
        return []


def write_json_file(data):
    file = open(OUTPUT_FILE, "w", encoding="utf-8")
    json.dump(data, file, indent=2)
    file.close()


def save_runtime_output(user_query, final_answer, agent_response=None, error=None):
    old_outputs = read_json_file()
    model_json = get_json_from_answer(final_answer)
    tools_used = get_tools_used(agent_response)

    if error:
        final_answer = str(error)
        result_summary = "The agent returned an error."
    else:
        result_summary = model_json.get("tool_result_summary", "The agent answered the user query.")

    if not tools_used:
        tools_used = model_json.get("tools_used", [])

    new_output = {
        "user_request": user_query,
        "plan_summary": model_json.get("plan_summary", "Answer the user query using the helpdesk agent."),
        "tools_used": tools_used,
        "tool_result_summary": result_summary,
        "reflection_summary": model_json.get("reflection_summary", "Saved the agent output in JSON format."),
        "final_answer": model_json.get("final_answer", final_answer),
        "memory_used": model_json.get("memory_used", False),
        "write_action_performed": model_json.get("write_action_performed", "update" in user_query.lower()),
    }

    old_outputs.append(new_output)
    write_json_file(old_outputs)
    return new_output
