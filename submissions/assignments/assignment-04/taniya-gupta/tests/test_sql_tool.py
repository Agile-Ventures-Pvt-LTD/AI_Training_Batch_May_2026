from src.tools.ecommerce_sql_tool import (
    validate_query,
    query_ecommerce_database,
)


def test_valid_select_query():
    is_valid, message = validate_query(
        "SELECT * FROM customers"
    )

    assert is_valid is True
    assert message == ""


def test_empty_query():
    is_valid, message = validate_query("")

    assert is_valid is False
    assert "empty" in message.lower()


def test_insert_blocked():
    is_valid, _ = validate_query(
        "INSERT INTO customers VALUES (1)"
    )

    assert is_valid is False


def test_update_blocked():
    is_valid, _ = validate_query(
        "UPDATE customers SET name='test'"
    )

    assert is_valid is False


def test_delete_blocked():
    is_valid, _ = validate_query(
        "DELETE FROM customers"
    )

    assert is_valid is False


def test_multiple_statements_blocked():
    is_valid, _ = validate_query(
        "SELECT * FROM customers; DROP TABLE orders"
    )

    assert is_valid is False

def test_select_query_execution():
    result = query_ecommerce_database.invoke(
        {"query": "SELECT COUNT(*) AS total FROM customers"}
    )

    assert result is not None
    assert "total" in str(result)


def test_low_stock_query_execution():
    result = query_ecommerce_database.invoke(
        {
            "query": """
                SELECT name, stock_quantity
                FROM products
                WHERE stock_quantity < 10
            """
        }
    )

    assert result is not None


def test_unsafe_query_execution():
    result = query_ecommerce_database.invoke(
        {
            "query": "DELETE FROM customers"
        }
    )

    assert "SQL Validation Error" in result