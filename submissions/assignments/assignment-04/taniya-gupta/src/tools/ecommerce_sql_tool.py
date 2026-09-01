import re
from langchain.tools import tool

from src.db.connection import get_connection


FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "TRUNCATE", "CREATE", "REPLACE", "ATTACH", "DETACH", "PRAGMA"
]

MAX_ROWS = 50


def validate_query(query: str):
    query = query.strip()

    if not query:
        return False, "Query cannot be empty."

    query_upper = query.upper()

    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", query_upper):
            return False, f"{keyword} statements are not allowed."

    if ";" in query.rstrip(";"):
        return False, "Multiple SQL statements are not allowed."

    return True, ""


@tool
def query_ecommerce_database(query: str) -> str:
    """
    Run a SELECT query on the ecommerce database.
    """
    is_valid, error_message = validate_query(query)
    if not is_valid:
        return f"SQL Validation Error: {error_message}"

    conn = None
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchmany(MAX_ROWS)

    if not rows:
            return "No matching records found."

    result = [dict(row) for row in rows]

    if len(result) == 1 and len(result[0]) == 1:
            key = list(result[0].keys())[0]
            value = result[0][key]
            return f"{key} = {value}"

    return str(result)

    conn.close()
