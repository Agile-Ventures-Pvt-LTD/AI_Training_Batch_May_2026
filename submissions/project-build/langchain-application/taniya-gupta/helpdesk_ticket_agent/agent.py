from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import search_tickets, get_ticket_details, get_ticket_comments, calculate_sla_status, prioritize_tickets, update_ticket_status, add_ticket_comment, save_archival_memory, recall_archival_memory, recall_conversation,summarize_conversation, save_conversation, get_overdue_tickets
from prompts import SYSTEM_PROMPT
from config import Config

def create_helpdesk_agent():
    llm=ChatGroq(
        model=Config.GROQ_MODEL,
        temperature=0,
        groq_api_key=Config.GROQ_API_KEY
    )
    tools=[
        search_tickets, get_ticket_details, get_ticket_comments, calculate_sla_status,
        prioritize_tickets, update_ticket_status, add_ticket_comment,
        save_archival_memory, recall_archival_memory, recall_conversation,
        summarize_conversation, save_conversation, get_overdue_tickets
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent= create_tool_calling_agent(llm, tools, prompt)

    agent_executor= AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True, 
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor