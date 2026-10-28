from langchain.tools import tool
from src.db.connection import get_connection

FORBIDDEN = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE"
]

@tool
def query_ecommerce_database(query: str) -> str:
    """
    Use this tool to query the SQLite ecommerce database. The database contains customers, 
    products, orders, and order_items tables. Only use SELECT queries. Do not perform 
    INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE operations.
    """

    try:
        query_upper = query.upper().strip()

        if not query_upper.startswith("SELECT"):
            return "Error: Only SELECT queries are allowed."

        if ";" in query.strip()[:-1]:
            return "Error: Multiple SQL statements are not allowed."

        for keyword in FORBIDDEN:
            if keyword in query_upper:
                return f"Error: {keyword} operations are not permitted."

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchmany(50)

        conn.close()

        if not rows:
            return "No matching data found."
        
        print("\nSQL query:")
        print(query_upper)

        return str(rows)

    except Exception as e:
        return f"Database error: {str(e)}"