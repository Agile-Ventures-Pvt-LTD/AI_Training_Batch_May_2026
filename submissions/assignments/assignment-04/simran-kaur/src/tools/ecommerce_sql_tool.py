from langchain.tools import tool

from src.db.connection import get_connection



@tool
def execute_sql(query: str):

    """
    Execute SQL query against
    ecommerce database.
    """

    query = query.strip()

    if not query.lower().startswith("select"):

        return (
            "Only SELECT queries "
            "are allowed."
        )

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(query)

        results = cursor.fetchall()

        conn.close()

        return str(results)

    except Exception as e:

        return f"Database Error: {e}"


# run ```python -m src.tools.ecommerce_sql_tool``` to execute