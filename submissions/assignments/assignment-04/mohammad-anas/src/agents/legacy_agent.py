import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from src.tools.ecommerce_sql_tool import query_ecommerce_database

def run_legacy_agent(user_question: str):
    load_dotenv()
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    tools = [query_ecommerce_database]

    react_template = """You are an AI assistant for an e-commerce business.
You can answer business questions using the ecommerce SQLite database (tables: customers, products, orders, order_items).
Important rules:
- Only generate SELECT queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- Always explain results in simple business language.

Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    base_prompt = PromptTemplate.from_template(react_template)

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=base_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # Set to True to see the Thought/Action loop
        handle_parsing_errors=True
    )

    print(f"User Question: {user_question}\n")
    response = agent_executor.invoke({"input": user_question})
    
    print(response["output"])

if __name__ == "__main__":
    run_legacy_agent("What is the total revenue from completed orders?")