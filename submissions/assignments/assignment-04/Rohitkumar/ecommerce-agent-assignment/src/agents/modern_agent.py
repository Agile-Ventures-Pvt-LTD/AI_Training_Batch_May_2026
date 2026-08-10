from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools.ecommerce_sql_tool import query_ecommerce_database
from src.prompts.system_prompt import SYSTEM_PROMPT

def create_agent():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    tools = [query_ecommerce_database]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor