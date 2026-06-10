from langchain.tools import tool

from src.db.connection import get_connection

BLOCKED_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
]


@tool
def query_ecommerce_database(query: str) -> str:
    """
    Query the ecommerce SQLite database.

    Available tables:
    - customers
    - products
    - orders
    - order_items

    Use ONLY SELECT statements.

    Return database results so they can be converted
    into business-friendly answers.
    """

    print("\n" + "=" * 60)
    print("DATABASE TOOL CALLED")
    print("=" * 60)

    print("\nGenerated SQL:")
    print(query)

    query_upper = query.upper().strip()

    if not query_upper.startswith("SELECT"):
        print("\nBlocked Query")
        return "Only SELECT queries are allowed."

    for keyword in BLOCKED_KEYWORDS:

        if keyword in query_upper:
            print(f"\nBlocked Keyword: {keyword}")
            return f"{keyword} operations are not allowed."

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        print("\nRaw Database Result:")
        print(rows)

        conn.close()

        return str(rows)

    except Exception as e:

        print("\nDatabase Error:")
        print(str(e))

        return f"Database Error: {str(e)}"