from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from config import MODEL_NAME, GROQ_API_KEY
from prompts import system_prompt

from tools import (issue_classifiction, classify_and_retrieve, generate_grounded_answer, get_user_profile, get_ticket_details,
    get_device_status, get_incident_details, run_diagnostic_check)

system_message=system_prompt()

tools=[issue_classifiction, classify_and_retrieve, get_user_profile,get_ticket_details,
    get_device_status, get_incident_details, run_diagnostic_check, generate_grounded_answer]

llm = ChatGroq(model=MODEL_NAME,groq_api_key=GROQ_API_KEY)

agent=create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_message
)

def prebuilt_agent(user_input):
        try:
            message_input = [HumanMessage(content=user_input)]
            response = agent.invoke({"messages": message_input})
            return response["messages"][-1].content
        except Exception as e:
           return f"Error: {str(e)}"