from langchain.tools import tool

from src.db.connection import get_connection


@tool
def query_ecommerce_database(query: str) -> str:
    """Use this tool to query the SQLite ecommerce database. The database contains customers, products, orders, and order_items tables. Only use SELECT queries. Do not perform INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE operations."""

    query = query.strip()
    lower_query = query.lower()

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace"
    ]

    if not lower_query.startswith("select"):
        return "ERROR: Only SELECT queries are allowed."

    for keyword in forbidden_keywords:
        if keyword in lower_query:
            return f"ERROR: Unsafe SQL detected ({keyword})."

    query_without_last = query.rstrip(";").strip()

    if ";" in query_without_last:
        return "ERROR: Multiple SQL statements are not allowed."

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(50)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return str(results)

    except Exception as e:
        return f"ERROR: {str(e)}"

    finally:
        if conn:
            conn.close()
