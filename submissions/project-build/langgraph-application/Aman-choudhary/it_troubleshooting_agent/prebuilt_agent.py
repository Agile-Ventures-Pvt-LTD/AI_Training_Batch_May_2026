from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from config import (GROQ_API_KEY,GROQ_MODEL)
from prompts import SYSTEM_PROMPT
from tools import (classify_issue_type,retrieve_troubleshooting_steps,get_user_profile,get_device_status,check_known_incidents,run_diagnostic_check,get_ticket_details,create_resolution_plan)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL
)

agent = create_react_agent(
    model=llm,
    tools=[
        classify_issue_type,
        retrieve_troubleshooting_steps,
        get_user_profile,
        get_device_status,
        check_known_incidents,
        run_diagnostic_check,
        get_ticket_details,
        create_resolution_plan
    ],
    prompt=SYSTEM_PROMPT
)