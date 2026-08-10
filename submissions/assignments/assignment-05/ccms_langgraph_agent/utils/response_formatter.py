from agents.prebuilt_agent import get_tools_used, extract_response_metadata

def format_agent_response(
    user_question: str,
    response,
    implementation_choice: str = "prebuilt_react_agent"
):
    """
    Convert an agent response into JSON format.
    """

    metadata = extract_response_metadata(response)

    return {
        "user_question": user_question,
        "implementation_choice": implementation_choice,
        "tools_used": get_tools_used(response),
        "records_found": metadata["records_found"],
        "answer": response["messages"][-1].content,
        "sensitive_data_masked": metadata["sensitive_data_masked"],
        "limitations": metadata["limitations"]
    }