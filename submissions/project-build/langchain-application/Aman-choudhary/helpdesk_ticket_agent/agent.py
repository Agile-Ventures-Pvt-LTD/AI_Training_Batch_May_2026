from langchain_groq import ChatGroq
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from config import (GROQ_API_KEY,MODEL_NAME)
import tools
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=0)
tools_list = [
    tools.search_tickets,
    tools.get_ticket_details,
    tools.get_ticket_comments,
    tools.get_overdue_tickets,
    tools.get_work_queue,
    tools.update_ticket_status,
    tools.save_archival_memory,
    tools.recall_archival_memory,
]
agent = initialize_agent(tools=tools_list,llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)