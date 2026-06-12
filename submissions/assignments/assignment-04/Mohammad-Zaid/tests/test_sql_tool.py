# tests/test_sql_tool.py

from src.tools.ecommerce_sql_tool import (
    validate_sql_query,
    query_ecommerce_database
)


def test_valid_select():

    is_valid, _ = validate_sql_query(
        "SELECT * FROM customers"
    )

    assert is_valid is True


def test_drop_query_blocked():

    is_valid, _ = validate_sql_query(
        "DROP TABLE customers"
    )

    assert is_valid is False


def test_multiple_statements_blocked():

    is_valid, _ = validate_sql_query(
        "SELECT * FROM customers; DROP TABLE orders;"
    )

    assert is_valid is False


def test_tool_execution():

    result = query_ecommerce_database.invoke(
        {
            "sql_query":
            "SELECT COUNT(*) FROM customers"
        }
    )

    assert "(10,)" in result