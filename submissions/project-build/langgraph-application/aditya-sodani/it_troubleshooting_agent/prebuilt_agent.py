from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from prompts import SYSTEM_PROMPT

from config import GROQ_API_KEY, GROQ_MODEL
import tools

def build_agent():

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0
    )

    tool_list = [
        tools.classify_issue_type,
        tools.retrieve_troubleshooting_steps,
        tools.get_user_profile,
        tools.get_device_status,
        tools.check_known_incidents,
        tools.run_diagnostic_check,
        tools.get_ticket_details,
    ]

    agent = create_react_agent(
        model=llm,
        tools=tool_list,
        prompt=SYSTEM_PROMPT
    )

    return agent