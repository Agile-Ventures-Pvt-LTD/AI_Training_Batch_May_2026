import re

from langchain.tools import tool

from src.db.connection import get_connection
from src.logger import log_query


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "ATTACH",
    "DETACH"
]


def validate_sql(query: str):

    query_upper = query.upper().strip()

    # Only SELECT allowed
    if not query_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # Block dangerous keywords
    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(
            rf"\b{keyword}\b",
            query_upper
        ):
            raise ValueError(
                f"{keyword} is not allowed."
            )

    # Prevent multiple SQL statements
    if ";" in query.strip()[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return True


@tool
def query_ecommerce_database(query: str) -> str:
    """
    Query the ecommerce SQLite database.

    Available Tables:
    - customers
    - products
    - orders
    - order_items

    Rules:
    - Only SELECT queries allowed
    - No INSERT
    - No UPDATE
    - No DELETE
    - No DROP
    - No ALTER
    - No TRUNCATE

    Returns:
    Database query results.
    """

    try:

        validate_sql(query)

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchmany(50)

        column_names = [
            desc[0]
            for desc in cursor.description
        ]

        conn.close()

        if not rows:

            result_string = "No records found."

            log_query(
                sql_query=query,
                result=result_string
            )

            return result_string

        result = []

        result.append(
            " | ".join(column_names)
        )

        result.append("-" * 50)

        for row in rows:

            result.append(
                " | ".join(
                    str(value)
                    for value in row
                )
            )

        result_string = "\n".join(result)

        log_query(
            sql_query=query,
            result=result_string
        )

        return result_string

    except Exception as e:

        error_message = (
            f"ERROR: {str(e)}"
        )

        log_query(
            sql_query=query,
            result=error_message
        )

        return error_message