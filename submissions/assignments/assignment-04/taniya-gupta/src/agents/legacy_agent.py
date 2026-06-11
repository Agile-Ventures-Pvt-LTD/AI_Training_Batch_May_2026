from dotenv import load_dotenv

from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_groq import ChatGroq

from src.db.connection import get_connection
from src.tools.ecommerce_sql_tool import query_ecommerce_database
from src.prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()


def get_schema_text(_: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    lines = []
    for table in tables:
        table_name = table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        lines.append(f"{table_name}: {', '.join(columns)}")

    conn.close()

    return "\n".join(lines)


get_schema = Tool.from_function(
    func=get_schema_text,
    name="get_schema",
    description="Shows the database tables and columns."
)


def create_legacy_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    agent = initialize_agent(
        tools=[get_schema, query_ecommerce_database],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        early_stopping_method="generate",
        agent_kwargs={"prefix": SYSTEM_PROMPT}
    )

    return agent


agent = create_legacy_agent()
