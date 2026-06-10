import pandas as pd
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


def validate_query(query: str):

    query_upper = query.upper().strip()

    # Must start with SELECT
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Block dangerous keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False, f"{keyword} queries are not allowed."

    # Block multiple statements
    if ";" in query.strip()[:-1]:
        return False, "Multiple SQL statements are not allowed."

    return True, "Valid"


def execute_query(query: str):

    is_valid, message = validate_query(query)

    if not is_valid:
        return {"error": message}

    try:

        conn = get_connection()

        df = pd.read_sql_query(query, conn)

        conn.close()

        # Limit output rows
        df = df.head(50)

        return df.to_dict(orient="records")

    except Exception as e:

        return {"error": str(e)}