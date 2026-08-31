"""
test_database.py
"""

from src.db.connection import (
    database_exists,
    test_connection,
    get_table_names,
    execute_query
)


def run_database_tests():

    print("\n" + "=" * 60)
    print("DATABASE TESTS")
    print("=" * 60)

    # Database Exists

    assert database_exists() is True

    print("Database exists")

    # Connection Test

    assert test_connection() is True

    print("Database connection successful")

    # Table Validation

    tables = get_table_names()

    expected_tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    for table in expected_tables:

        assert table in tables

    print("Required tables exist")

    # Data Validation

    customers = execute_query(
        "SELECT COUNT(*) as count FROM customers"
    )

    print(customers[0]["count"])

    products = execute_query(
        "SELECT COUNT(*) as count FROM products"
    )

    orders = execute_query(
        "SELECT COUNT(*) as count FROM orders"
    )

    order_items = execute_query(
        "SELECT COUNT(*) as count FROM order_items"
    )

    print(
        f"Customers: {customers[0]['count']}"
    )

    print(
        f"Products: {products[0]['count']}"
    )

    print(
        f"Orders: {orders[0]['count']}"
    )

    print(
        f"Order Items: {order_items[0]['count']}"
    )

    print("\nDatabase tests passed")


if __name__ == "__main__":
    run_database_tests()