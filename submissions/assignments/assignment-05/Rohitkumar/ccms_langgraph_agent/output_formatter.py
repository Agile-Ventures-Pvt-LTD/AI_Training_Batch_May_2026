def format_and_print(user_question, response, implementation_choice):
    """Print a comprehensive human-readable output showing all tool calls, results, errors, and the final answer."""
    messages = response.get("messages", [])

    print("\n" + "=" * 70)
    print(f"  User Question: {user_question}")
    print(f"  Agent Type: {implementation_choice}")
    print("=" * 70)

    
    tools_called = False
    for i, msg in enumerate(messages):
        msg_type = type(msg).__name__

        
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tools_called = True
            for tc in msg.tool_calls:
                tool_name = tc.get("name", "unknown")
                tool_args = tc.get("args", {})
                print(f"\n  [{i}] Tool Called: {tool_name}")
                print(f"      Arguments: {tool_args}")

       
        if msg_type == "ToolMessage":
            tool_name = getattr(msg, "name", "unknown")
            content = msg.content
            print(f"\n  [{i}] Tool Result ({tool_name}):")
            # Truncate very long results for readability
            if len(str(content)) > 2000:
                print(f"      {str(content)[:2000]}...")
            else:
                print(f"      {content}")

       
        if msg_type == "AIMessage" and hasattr(msg, "content") and msg.content:
           
            is_final = True
            for j in range(i + 1, len(messages)):
                later_msg = messages[j]
                later_type = type(later_msg).__name__
                if later_type == "AIMessage":
                    is_final = False
                    break
                if hasattr(later_msg, "tool_calls") and later_msg.tool_calls:
                    is_final = False
                    break

            if is_final:
                print(f"\n  [FINAL ANSWER]:")
                print(f"      {msg.content}")
            else:
                print(f"\n  [{i}] AI Thought:")
                print(f"      {msg.content[:500]}{'...' if len(msg.content) > 500 else ''}")

    if not tools_called:
    
        answer = ""
        for msg in reversed(messages):
            if hasattr(msg, "content") and isinstance(msg.content, str) and msg.content:
                answer = msg.content
                break
        if answer:
            print(f"\n  [FINAL ANSWER]: {answer}")

    print("=" * 70 + "\n")

   
    answer = ""
    for msg in reversed(messages):
        if hasattr(msg, "content") and isinstance(msg.content, str) and msg.content:
            answer = msg.content
            break
    return answer