import sqlite3
import re

from langchain.tools import tool

DB_PATH = "data/olist.sqlite"
FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
]


def validate_sql(query: str):
    query = query.strip()

    if not query.upper().startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    if ";" in query[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    upper_query = query.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_query):
            raise ValueError(
                f"{keyword} operations are not allowed."
            )

@tool
def query_database(query: str):
    """
    Execute a SQLite SELECT query against the Olist ecommerce database.
    Input:
        A valid SQLite SELECT statement.
    Use this tool whenever information needs to be retrieved from:
    customers, orders, order_items, order_payments,
    order_reviews, products, sellers, geolocation,
    leads_closed, or leads_qualified tables.
    Only SELECT queries are allowed.
    """
    try:
        validate_sql(query)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(50)
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return {
            "columns": columns,
            "rows": rows,
        }

    except Exception as e:
        return {
            "error": str(e)
        }