try:
    import json
    from utils.gClient import get_client
    from tools.init import tools
    from prompts import SYSTEM_PROMPT
    from langgraph.prebuilt import create_react_agent
except ImportError as e:
    print(f"Error: {e}")

try:
    llm = get_client()
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )
except ValueError as e:
    print(f"Fatal Error: {e}")



# Primary Agent function


def ask_agent(
    user_query: str
):
    '''
    Using this function, the agent interprets the request, selects appropriate database tools, retrieves data, and generates a response.
    
    Args:
        user_query (str): User request.
    '''
    
    response = agent.invoke(
        {
            "messages": [
                ("user", user_query)
            ]
        }
    )
    return response





# Secondary agent functions


def get_tools_used(response):
    """
    Extract names of tools invoked by the agent.
    """

    tools_used = []

    for msg in response["messages"]:
        if hasattr(msg, "tool_calls"):
            if msg.tool_calls:
                for call in msg.tool_calls:
                    tools_used.append(
                        call["name"]
                    )

    return tools_used




def get_tool_outputs(response):
    """
    Extracts tool outputs from a LangGraph agent response.
    """

    outputs = []

    for msg in response["messages"]:

        if msg.__class__.__name__ == "ToolMessage":

            content = msg.content

            try:
                content = json.loads(content)
            except Exception:
                pass

            outputs.append(content)

    return outputs




def extract_response_metadata(response):
    '''Extract records_found, sensitive_data_masked, and limitations from tool outputs contained in response.'''
    tool_outputs = get_tool_outputs(response)
    
    records_found = 0
    sensitive_data_masked = True
    limitations = []

    for output in tool_outputs:

        if not isinstance(output, dict):
            continue

        if "records_found" in output:
            records_found = max(
                records_found,
                output["records_found"]
            )

        elif "transaction_count" in output:
                records_found = max(
                records_found,
                output["transaction_count"]
            )

        elif "found" in output:
            records_found = 1 if output["found"] else 0

        if "sensitive_data_masked" in output:
            sensitive_data_masked = (
                output["sensitive_data_masked"]
            )

        if "error" in output:
            limitations.append(
                output["error"]
            )

    return {
        "records_found": records_found,
        "sensitive_data_masked": sensitive_data_masked,
        "limitations": limitations
    }
