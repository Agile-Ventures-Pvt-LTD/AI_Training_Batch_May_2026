def format_agent_output(user_question: str, state: dict) -> dict:
    """
    Parses the LangGraph agent state and formats it according to 
    the required hackathon submission format.
    """
    messages = state.get("messages", [])
    tools_used = []
    final_answer = ""
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tools_used.append(tc["name"])
        if msg.type == "ai" and not getattr(msg, "tool_calls", []):
            final_answer = msg.content
    records_found = 1 if final_answer else 0
    return {
        "user_question": user_question,
        "implementation_choice": "prebuilt_react_agent",
        "tools_used": list(set(tools_used)),
        "records_found": records_found,
        "answer": final_answer,
        "sensitive_data_masked": True,
        "limitations": []
    }