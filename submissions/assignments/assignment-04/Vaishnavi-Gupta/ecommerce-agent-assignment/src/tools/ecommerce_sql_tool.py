import sqlite3
from langchain.tools import tool
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "ecommerce.db"

BLOCKED = [
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
    Query ecommerce database.
    Only SELECT statements allowed.
    """

    query_upper = query.upper().strip()

    if not query_upper.startswith("SELECT"):
        return "Only SELECT queries are allowed."

    if ";" in query[:-1]:
        return "Multiple statements are not allowed."

    for word in BLOCKED:
        if word in query_upper:
            return f"{word} operations are blocked."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchmany(50)

        conn.close()

        return str(rows)

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print("query_ecommerce_database")
