from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq
from config import GROQ_API_KEY,GROQ_MODEL
from tools import retrieve_hr_policy,retrieve_travel_policy,retrieve_reimbursement_policy,retrieve_it_security_policy,retrieve_ai_usage_policy

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL)

tools = [retrieve_hr_policy,retrieve_travel_policy,retrieve_reimbursement_policy,retrieve_it_security_policy,retrieve_ai_usage_policy]

agent = create_react_agent(llm,tools)