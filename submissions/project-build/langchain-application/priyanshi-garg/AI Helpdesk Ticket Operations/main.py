import json
from langchain import hub
from langchain.agents import create_react_agent, Tool, AgentExecutor
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_experimental.utilities import PythonREPL
from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    summarize_conversation
)
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq()

tools = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    summarize_conversation
]

from langchain_groq import ChatGroq

import os
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")