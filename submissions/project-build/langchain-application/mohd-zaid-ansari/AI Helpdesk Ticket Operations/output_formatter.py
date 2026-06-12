import json

def format_output(
    user_request: str,
    plan_summary: str,
    tools_used: list,
    tool_result_summary: str,
    reflection_summary: dict,
    final_answer: str,
    memory_used: bool,
    write_action_performed: bool
):

    output = {
        "user_request": user_request,
        "plan_summary": plan_summary,
        "tools_used": tools_used,
        "tool_result_summary": tool_result_summary,
        "reflection_summary": reflection_summary,
        "final_answer": final_answer,
        "memory_used": memory_used,
        "write_action_performed": write_action_performed
    }
    return json.dumps(output, indent=4)