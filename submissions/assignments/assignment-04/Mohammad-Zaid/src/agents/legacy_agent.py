# src/agents/legacy_agent.py

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain.agents import (create_tool_calling_agent, AgentExecutor)

from langchain_core.prompts import (ChatPromptTemplate, MessagesPlaceholder)

from src.tools.ecommerce_sql_tool import (query_ecommerce_database)

from src.prompts.system_prompt import (SYSTEM_PROMPT)

load_dotenv()

# LLM Initialization
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Tools
tools = [query_ecommerce_database]

# Prompt Creation
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

# Agent Creation
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)