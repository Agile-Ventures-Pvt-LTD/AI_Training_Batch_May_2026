from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from src.tools.ecommerce_sql_tool import ecommerce_sql_tool_legacy
from src.db.schema_description import SCHEMA

def create_legacy_agent():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    tools = [ecommerce_sql_tool_legacy]

    # 🔥 STRICT SQL CONTEXT (VERY IMPORTANT FOR LEGACY)
    PREFIX = f"""
You are an expert SQL assistant for an ecommerce SQLite database.

Your task:
Convert natural language questions into correct SQL queries.

STRICT RULES:
- Use ONLY the provided schema
- NEVER assume tables like inventory or stock tables
- ONLY use SELECT queries
- ALWAYS use correct column names
- If unsure, check schema carefully before writing SQL
- Do NOT hallucinate columns or tables

DATABASE SCHEMA:
{SCHEMA}
"""

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,

        # keeps agent stable even if model output is messy
        handle_parsing_errors=True,

        # 🔥 IMPORTANT FIX
        agent_kwargs={
            "prefix": PREFIX
        }
    )

    return agent