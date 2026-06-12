from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)


def test_select_query():

    result = query_ecommerce_database.invoke(
        {
            "sql_query":
            "SELECT COUNT(*) AS total_customers FROM customers"
        }
    )

    assert result is not None


def test_drop_query_blocked():

    result = query_ecommerce_database.invoke(
        {
            "sql_query":
            "DROP TABLE customers"
        }
    )

    assert "Security Validation Error" in result