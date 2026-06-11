import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from src.tools.ecommerce_sql_tool import query_ecommerce_database

def run_modern_agent(user_question: str):
    load_dotenv()
    
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    
    tools = [query_ecommerce_database]
    
    system_message = """
    You are an AI assistant for an e-commerce business.
    You can answer business questions using the ecommerce SQLite database.
    The database has the following tables:
    - customers
    - products
    - orders
    - order_items

    Use the database tool only when the user asks a question that requires data.

    Important rules:
    - Only generate SELECT queries.
    - Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE queries.
    - Always explain results in simple business language.
    - If the data is unavailable, clearly say that the answer cannot be determined from the database.
    - Do not make up numbers.
    - If a query returns no records, explain that no matching data was found.
    """
    
    agent_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_message
    )
    
    print(f"User Question: {user_question}\n")
    
    inputs = {"messages": [{"role": "user", "content": user_question}]}
    response = agent_graph.invoke(inputs)
    
    print(response["messages"][-1].content)

if __name__ == "__main__":
    run_modern_agent("Which customer has spent the most money?")