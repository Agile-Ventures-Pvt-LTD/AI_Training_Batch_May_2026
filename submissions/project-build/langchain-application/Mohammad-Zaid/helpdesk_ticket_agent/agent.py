# agent.py

from langchain_groq import ChatGroq

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from config import GROQ_API_KEY

from prompts import SYSTEM_PROMPT

from defined_tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
)

from memory import (
    save_memory,
    recall_memory,
    save_conversation,
    recall_conversation,
    summarize_conversation
)

# LLM Client 
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0
)

# Tools:
tools = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    prioritize_tickets,

    update_ticket_status,
    add_ticket_comment,

    save_memory,
    recall_memory,

    save_conversation,
    recall_conversation,
    summarize_conversation
]

# Prompts:
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        )
    ]
)

# Agent:
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)