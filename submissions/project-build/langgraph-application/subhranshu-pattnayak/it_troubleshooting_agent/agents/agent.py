from prompts import SYSTEM_PROMPT
from tools.init import tools
from langgraph.prebuilt import create_react_agent
from utils.gClient import get_client

llm = get_client()

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

def ask_agent(user_input):
    '''
    Using this function, the agent interprets the request, selects appropriate database tools, retrieves data, and generates a response.
    
    Args:
        user_input (str): User request.
    '''
    return agent.invoke({
        "messages": [
            ("user", user_input)
        ]
    })

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
