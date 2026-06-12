import re
import pandas as pd

from langchain.tools import tool

from src.db.connection import get_connection


MAX_ROWS = 100

FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "MERGE",
    "EXEC",
]


def validate_sql(sql: str):
    """
    Security validation
    """

    sql = sql.strip()

    if not sql.upper().startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # block multiple statements
    if ";" in sql[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    upper_sql = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            raise ValueError(
                f"Forbidden SQL keyword detected: {keyword}"
            )

    return True


@tool
def query_ecommerce_database(sql_query: str) -> str:
    """
    Query Ecommerce SQLite Database.

    Use this tool to query the ecommerce database.

    Available tables:
    - customers
    - products
    - orders
    - order_items

    Only SELECT statements are allowed.
    """

    try:

        validate_sql(sql_query)

        conn = get_connection()

        df = pd.read_sql_query(
            sql_query,
            conn
        )

        conn.close()

        if df.empty:
            return "No matching records found."

        if len(df) > MAX_ROWS:
            df = df.head(MAX_ROWS)

        return df.to_string(index=False)

    except Exception as e:
        return f"Database Error: {str(e)}"