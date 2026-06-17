from langchain_core.tools import tool
import json

from src.tools.ecommerce_sql_tool import execute_query


@tool
def query_ecommerce_database(query: str) -> str:
    """
    Query the ecommerce SQLite database.
    Only SELECT queries are allowed.
    """

    result = execute_query(query)

    return json.dumps(result, indent=2)