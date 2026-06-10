from langchain.tools import tool
# import sqlite3
# from pathlib import Path
from src.db.connection import get_db
import sqlite3
import re
from langchain_core.tools import tool


def validate_query(query: str):

    query = query.strip()

    if not query.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    upper_query = query.upper()

    for keyword in forbidden_keywords:
        if re.search(rf"\b{keyword}\b", upper_query):
            raise ValueError(f"{keyword} queries are not allowed.")

    if ";" in query[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")


@tool
def query_ecommerce_database(sql_query: str) -> str:
    """
    Use this tool to query the SQLite ecommerce database. The database contains customers, 
    products, orders, and order_items tables. Only use SELECT queries. Do not perform 
    INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE operations.

    When using query_ecommerce_database:

    - Generate a valid SQLite SELECT query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """

    try:
        # print(sql_query)
        validate_query(sql_query)

        # conn = get_db()
        # conn.row_factory = sqlite3.Row

        # cursor = conn.cursor()

        # cursor.execute(sql_query)
        db=get_db()
        # rows = cursor.fetchall()
        result = db.run(sql_query)

        # print("SQL Query:", sql_query)
        # print("Tool Result:", result)
        result = db.run(sql_query)

        # print(type(result))
        # print(result)

        # return str(result)
        return str(result)

    except Exception as e:

        return f"Database Error: {str(e)}"