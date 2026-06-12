from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from src.db.connection import get_connection
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.tools.ecommerce_sql_tool import query_ecommerce_database

load_dotenv()


def get_schema_text() -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema = []

    for table in tables:
        table_name = table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema.append(f"\nTable: {table_name}")

        for col in columns:
            schema.append(f"- {col[1]} ({col[2]})")

    conn.close()

    return "\n".join(schema)


@tool
def get_schema() -> str:
    """
    Returns database schema.
    """
    return get_schema_text()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def create_modern_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    agent = create_agent(
        model=llm,
        tools=[
            get_schema,
            query_ecommerce_database
        ],
        system_prompt=SYSTEM_PROMPT
    )

    return agent


agent = create_modern_agent()