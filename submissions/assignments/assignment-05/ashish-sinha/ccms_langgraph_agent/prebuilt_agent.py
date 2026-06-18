from typing import TypedDict, List
from langgraph.prebuilt import create_react_agent
from config import llm
from tools import tools
from prompts import system_prompt

class AgentState(TypedDict):
    """
    State used by the prebuilt ReAct agent.
    Attributes:
        user_question: User query.
        implementation_choice: Agent implementation used.
        tools_used: Tools invoked during execution.
        final_response: Final formatted response.
    """
    user_question: str
    implementation_choice: str
    tools_used: List[str]
    final_response: dict

compiled_flow = create_react_agent(model=llm,tools=tools,prompt=system_prompt)