from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from prompts import AGENT_SYSTEM_PROMPT
import tools
import memory
import config

if not config.GROQ_API_KEY:
    print("no api key found")

def get_agent():
    llm = ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=0
    )

    all_tools = [
        tools.search_tickets, 
        tools.get_ticket_details, 
        tools.get_ticket_comments,
        tools.get_overdue_tickets, 
        tools.prioritize_tickets, 
        tools.update_ticket_status, 
        tools.add_ticket_comment,
        memory.s_archival_memory, 
        memory.recall_archival_memory, 
        memory.recall_convo,
        memory.sumarize_convo
    ]

    agent_executor = create_react_agent(
        model=llm,
        tools=all_tools,
        state_modifier=AGENT_SYSTEM_PROMPT
    )
    
    return agent_executor