from langchain.tools import tool

import pandas as pd

from src.db.connection import get_connection


@tool
def query_ecommerce_database(
    sql_query: str
) -> str:
    """
    Execute SELECT query
    on ecommerce database.
    """

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            sql_query,
            conn
        )

        conn.close()

        if df.empty:

            return "No records found."

        return df.to_string(
            index=False
        )

    except Exception as e:

        return f"Database Error: {e}"