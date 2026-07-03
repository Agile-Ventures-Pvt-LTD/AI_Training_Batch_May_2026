from connection import get_connection

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


def query_travel_database(query: str) -> str:
    try:
        query_upper = query.upper().strip()

        if not query_upper.startswith("SELECT"):
            return "Error: Only SELECT queries are allowed."

        for keyword in FORBIDDEN:
            if keyword in query_upper:
                return "This operation is not permitted"

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
    