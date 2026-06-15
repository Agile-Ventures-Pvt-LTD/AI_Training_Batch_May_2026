from langchain_core.tools import tool
from db import get_connection

@tool
def query_ecommerce_database(sql_query: str) -> str:
    """Use this tool to query the SQLite ecommerce database. Contains customers, products, orders, and order_items tables. Only SELECT queries allowed."""
    sql = sql_query.strip()
    if not sql.upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed."
    if ";" in sql.rstrip(";"):
        return "Error: Multiple statements are not allowed."
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchmany(50)
        conn.close()
        if not rows:
            return "No results found."
        col_names = [desc[0] for desc in cursor.description]
        lines = [", ".join(col_names)]
        for row in rows:
            lines.append(", ".join(str(v) for v in row))
        return "\n".join(lines)
    except Exception as e:
        return f"Query error: {e}"
