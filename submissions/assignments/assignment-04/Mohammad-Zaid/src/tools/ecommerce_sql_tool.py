import re

from langchain.tools import tool

from src.db.connection import get_connection


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE"
]


def validate_sql_query(query: str):
    """
    Validates SQL queries before execution.

    Rules:
    - Only SELECT queries allowed
    - No multiple statements
    - Block dangerous keywords
    """

    query = query.strip()

    # Must start with SELECT

    if not re.match(r"^\s*SELECT\b", query, re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    # Prevent multiple statements

    cleaned_query = query.rstrip(";")

    if ";" in cleaned_query:
        return False, "Multiple SQL statements are not allowed."

    upper_query = query.upper()

    # Block dangerous operations

    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(rf"\b{keyword}\b", upper_query):
            return (False, f"{keyword} queries are not allowed.")

    return True, "Valid Query"


@tool
def query_ecommerce_database(
    sql_query: str
) -> str:
    """
    Use this tool to query the SQLite ecommerce database.

    The database contains:
    - customers
    - products
    - orders
    - order_items

    Only use SELECT queries.

    Do not perform:
    INSERT
    UPDATE
    DELETE
    DROP
    ALTER
    TRUNCATE
    CREATE
    REPLACE
    """

    try:

        is_valid, message = validate_sql_query(sql_query)

        if not is_valid:
            return (f"SQL Validation Error: {message}")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No records found."

        return str(rows)

    except FileNotFoundError as e:
        return f"Database Error: {str(e)}"

    except Exception as e:
        return f"Database Error: {str(e)}"