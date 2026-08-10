import json



def format_agent_response(
        user_request,
        plan_summary,
        tools_used,
        tool_result_summary,
        reflection_summary,
        final_answer,
        memory_used=False,
        write_action_performed=False
):

    response = {
        "user_request": user_request,
        "plan_summary": plan_summary,
        "tools_used": tools_used,
        "tool_result_summary": tool_result_summary,
        "reflection_summary": reflection_summary,
        "final_answer": final_answer,
        "memory_used": memory_used,
        "write_action_performed": write_action_performed
    }

    return response




def to_json(response_dict):

    return json.dumps(
        response_dict,
        indent=4,
        ensure_ascii=False
    )



def pretty_print(response):

    print("\n" + "=" * 80)

    print("\nUSER REQUEST")
    print("-" * 80)
    print(response["user_request"])

    print("\nPLAN SUMMARY")
    print("-" * 80)
    print(response["plan_summary"])

    print("\nTOOLS USED")
    print("-" * 80)

    if response["tools_used"]:
        for tool in response["tools_used"]:
            print(f"• {tool}")
    else:
        print("None")

    print("\nTOOL RESULT SUMMARY")
    print("-" * 80)
    print(response["tool_result_summary"])

    print("\nREFLECTION SUMMARY")
    print("-" * 80)
    print(response["reflection_summary"])

    print("\nFINAL ANSWER")
    print("-" * 80)
    print(response["final_answer"])

    print("\nMEMORY USED")
    print("-" * 80)
    print(response["memory_used"])

    print("\nWRITE ACTION PERFORMED")
    print("-" * 80)
    print(response["write_action_performed"])

    print("\n" + "=" * 80)




def summarize_tool_results(intermediate_steps):

    if not intermediate_steps:
        return "No tool execution."

    summaries = []

    for step in intermediate_steps:

        try:

            tool_name = step[0].tool

            tool_output = str(step[1])

            if len(tool_output) > 300:
                tool_output = tool_output[:300] + "..."

            summaries.append(
                f"{tool_name}: {tool_output}"
            )

        except Exception:

            summaries.append(
                str(step)
            )

    return "\n".join(summaries)




def detect_memory_usage(
        tools_used
):

    memory_tools = {
        "save_user_preference",
        "recall_user_preference",
        "recall_previous_conversation",
        "summarize_and_store_conversation"
    }

    return any(
        tool in memory_tools
        for tool in tools_used
    )


def detect_write_action(
        tools_used
):

    write_tools = {
        "update_ticket_status",
        "add_ticket_comment",
        "save_user_preference",
        "summarize_and_store_conversation"
    }

    return any(
        tool in write_tools
        for tool in tools_used
    )




def build_complete_response(
        user_request,
        plan_summary,
        tools_used,
        intermediate_steps,
        reflection_summary,
        final_answer
):

    tool_summary = summarize_tool_results(
        intermediate_steps
    )

    memory_used = detect_memory_usage(
        tools_used
    )

    write_action = detect_write_action(
        tools_used
    )

    response = format_agent_response(
        user_request=user_request,
        plan_summary=plan_summary,
        tools_used=tools_used,
        tool_result_summary=tool_summary,
        reflection_summary=reflection_summary,
        final_answer=final_answer,
        memory_used=memory_used,
        write_action_performed=write_action
    )

    return response





def save_output(
        response,
        filepath
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            response,
            f,
            indent=4,
            ensure_ascii=False
        )





if __name__ == "__main__":

    sample = format_agent_response(
        user_request="Show overdue tickets",
        plan_summary="Search overdue tickets",
        tools_used=[
            "search_tickets"
        ],
        tool_result_summary="Found 5 tickets",
        reflection_summary="Answer complete",
        final_answer="5 overdue tickets found.",
        memory_used=False,
        write_action_performed=False
    )

    pretty_print(sample)

    print("\nJSON OUTPUT\n")
    print(to_json(sample))