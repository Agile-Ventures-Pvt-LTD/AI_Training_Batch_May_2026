def format_final_response(state, answer, records_found=0, limitations=None):
    tools_used = state.get("tools_used", [])
    lines = [
        f"Question: {state.get('user_question', '')}",
        f"Tools Used: {', '.join(tools_used) if tools_used else 'None'}",
        f"Records Found: {records_found}", "",
        "Answer:",answer,
    ]
    if limitations:
        lines.append("")
        lines.append("Limitations:")
        for item in limitations:
            lines.append(f"- {item}")
    return "\n".join(lines)