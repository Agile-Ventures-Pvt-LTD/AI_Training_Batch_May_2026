def formating_agent_response(user_input: str, final_msg: str, tools_used: list) -> str:
    """Formats the agent's response for both the console and the log file."""
    output = f"\nUser Request: {user_input}\n"
    
    if tools_used:
        output += f"Tools Triggered: {', '.join(tools_used)}\n"
    else:
        output += "Tools Triggered: None (Answered from memory/context)\n"
        
    output += f"Agent Response:\n{final_msg}\n"
    output += "-" * 60 + "\n"
    
    return output