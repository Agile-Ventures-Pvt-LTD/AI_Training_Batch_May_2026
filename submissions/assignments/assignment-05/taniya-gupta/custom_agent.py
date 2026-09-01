from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from config import GROQ_API_KEY, MODEL_NAME
from tools import TOOLS
from prompts import SYSTEM_PROMPT

# defining state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    reflection: str
    tools_used: list

llm = ChatGroq(model=MODEL_NAME, temperature=0, api_key=GROQ_API_KEY, max_retries=2)
llm_with_tools = llm.bind_tools(TOOLS)

def agent_node(state: AgentState):
    """Calls the LLM """
    messages = state['messages']
    plan = state.get('plan', '')
    if not plan:
        plan = "Analyze user request and determine best tools to use."
    prompt_messages = [("system", SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(prompt_messages)
    tools_used = list(state.get('tools_used', []))
    if response.tool_calls:
        for tc in response.tool_calls:
            tools_used.append(tc['name'])
    return {
        "messages": [response], 
        "plan": plan, 
        "tools_used": tools_used}

def reflection_node(state: AgentState):
    """reflects on the final answer"""
    last_message = state['messages'][-1].content
    reflection = f"Final response length: {len(last_message)}."
    return {"reflection": reflection}

graph = StateGraph(AgentState)

# add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(TOOLS))
graph.add_node("reflection", reflection_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent", 
    tools_condition, 
    {"tools": "tools", END: "reflection"}
)
graph.add_edge("tools", "agent")
graph.add_edge("reflection", END)

custom_agent = graph.compile()
def run_custom_agent(question):
    """executes the custom agent"""
    initial_state = {
        "messages": [("human", question)],
        "plan": "",
        "reflection": "",
        "tools_used": []
    }
    result = custom_agent.invoke(initial_state, config={"recursion_limit": 10})
    return result
