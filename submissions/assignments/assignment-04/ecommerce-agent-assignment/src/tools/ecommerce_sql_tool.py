"""
ecommerce_sql_tool.py

Purpose
-------
Custom LangChain tool for querying the SQLite
ecommerce database safely.

Responsibilities
----------------
1. Validate SQL
2. Allow only SELECT queries
3. Block unsafe SQL
4. Execute query
5. Return results
6. Handle errors gracefully
"""

import re
from typing import Any

from langchain.tools import tool
import json

from src.db.connection import execute_query

# Security Configuration

FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "PRAGMA",
    "ATTACH",
    "DETACH",
    "VACUUM",
]


MAX_ROWS = 100


# Remove SQL Comments

def remove_sql_comments(query: str) -> str:
    """
    Remove SQL comments.

    Example:

    -- comment
    SELECT * FROM customers

    Returns cleaned query.
    """

    query = re.sub(
        r"--.*",
        "",
        query
    )

    query = re.sub(
        r"/\*.*?\*/",
        "",
        query,
        flags=re.DOTALL
    )

    return query.strip()


# Validate SELECT

def starts_with_select(query: str) -> bool:
    """
    Ensure query begins with SELECT.
    """

    return query.strip().upper().startswith("SELECT")


# Detect Forbidden Keywords

def contains_forbidden_keywords(
    query: str
):
    """
    Return list of forbidden keywords.
    """

    query_upper = query.upper()

    violations = []

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in query_upper:

            violations.append(keyword)

    return violations


# Detect Multiple Statements

def has_multiple_statements(
    query: str
) -> bool:
    """
    Prevent:

    SELECT * FROM customers;
    DROP TABLE orders;
    """

    query = query.strip()

    if query.endswith(";"):

        query = query[:-1]

    return ";" in query


# Enforce LIMIT

def enforce_limit(
    query: str,
    limit: int = MAX_ROWS
):
    """
    Add LIMIT if missing.
    """

    if "LIMIT" not in query.upper():

        query += f" LIMIT {limit}"

    return query


# SQL Validation

def validate_sql(query: str):
    """
    Validate SQL query.

    Returns
    -------
    (bool, message)
    """

    if not query:

        return (
            False,
            "Query cannot be empty."
        )

    query = remove_sql_comments(query)

    if not starts_with_select(query):

        return (
            False,
            "Only SELECT queries are allowed."
        )

    violations = contains_forbidden_keywords(
        query
    )

    if violations:

        return (
            False,
            f"Forbidden SQL detected: "
            f"{', '.join(violations)}"
        )

    if has_multiple_statements(query):

        return (
            False,
            "Multiple SQL statements are not allowed."
        )

    return (
        True,
        "Validation passed."
    )


# Prepare Query

def prepare_query(query: str):
    """
    Validate and prepare query.
    """

    valid, message = validate_sql(query)

    if not valid:

        return (
            False,
            message
        )

    query = enforce_limit(query)

    return (
        True,
        query
    )

# Format Results



def format_results(results):
    """
    Convert results into JSON string.
    """

    if not results:
        return "No matching records found."

    return json.dumps(
        results,
        indent=2,
        default=str
    )

# LangChain Tool

@tool
def query_ecommerce_database(
    query: str
) -> str:
    """
    Query the ecommerce SQLite database.

    IMPORTANT:
    - Only use SELECT statements.
    - Never use INSERT.
    - Never use UPDATE.
    - Never use DELETE.
    - Never use DROP.
    - Never use ALTER.

    Input:
        SQL SELECT query

    Output:
        Query results
    """

    try:

        # Validate Query

        success, result = prepare_query(
            query
        )

        if not success:

            return (
                "SQL Validation Error:\n"
                f"{result}"
            )

        safe_query = result

        # Execute Query

        results = execute_query(
            safe_query
        )

        # Format Results

        return format_results(results)

    except Exception as error:

        return (
            "Database Execution Error:\n"
            f"{str(error)}"
        )