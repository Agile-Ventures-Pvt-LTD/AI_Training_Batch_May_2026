"""
test_sql_tool.py
"""

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)


def run_sql_tool_tests():

    print("SQL TOOL TESTS")

    # Valid Query

    result = query_ecommerce_database.invoke(
        {
            "query":
            """
            SELECT *
            FROM customers
            LIMIT 5
            """
        }
    )

    print("\nValid Query Result:")

    print(result)

    # Invalid Query

    result = query_ecommerce_database.invoke(
        {
            "query":
            """
            DELETE FROM customers
            """
        }
    )

    print("\nDELETE Query Test:")

    print(result)

    assert (
        "Only SELECT queries are allowed"
        in result
    )

    print("DELETE blocked")

    # SQL Injection Test

    result = query_ecommerce_database.invoke(
        {
            "query":
            """
            SELECT * FROM customers;
            DROP TABLE customers;
            """
        }
    )

    print("\nInjection Test:")

    print(result)

    assert (
    "Multiple SQL statements" in result
    or
    "Forbidden SQL detected" in result
    )

    print("SQL Injection blocked")

    print("\n SQL Tool tests passed")


if __name__ == "__main__":
    run_sql_tool_tests()