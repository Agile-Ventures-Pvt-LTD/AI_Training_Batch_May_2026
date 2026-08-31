import re

from langchain.tools import tool

from src.db.connection import get_db_connection

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
    "DETACH",
    "PRAGMA"
]


def validate_sql_query(sql_query: str):

    cleaned_query = sql_query.strip()

    if not cleaned_query.upper().startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    if ";" in cleaned_query[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    upper_query = cleaned_query.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(
            rf"\b{keyword}\b",
            upper_query
        ):
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    return True

@tool
def query_ecommerce_database(sql_query: str) -> str:
    """
    Execute safe SELECT queries
    against ecommerce.db.
    """

    try:

        validate_sql_query(sql_query)

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(sql_query)

            rows = cursor.fetchmany(50)

            if not rows:
                return "No matching records found."

            columns = [
                description[0]
                for description in cursor.description
            ]

            results = []

            for row in rows:

                results.append(
                    {
                        column: row[index]
                        for index, column
                        in enumerate(columns)
                    }
                )

            return str(results)

    except ValueError as error:

        return f"Security Validation Error: {error}"

    except FileNotFoundError as error:

        return f"Database Error: {error}"

    except Exception as error:

        return f"Query Execution Error: {error}"