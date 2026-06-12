from pathlib import Path

from src.db.connection import get_db_connection


DATABASE_PATH = Path("data/ecommerce.db")


def test_database_file_exists():
    """
    Verify database file exists.
    """

    assert DATABASE_PATH.exists()


def test_database_connection():
    """
    Verify database connection can be established.
    """

    connection = get_db_connection()

    assert connection is not None

    connection.close()


def test_required_tables_exist():
    """
    Verify all required tables exist.
    """

    expected_tables = {
        "customers",
        "products",
        "orders",
        "order_items"
    }

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
        """)

        tables = {
            row["name"]
            for row in cursor.fetchall()
        }

    assert expected_tables.issubset(tables)


def test_customer_count():
    """
    Assignment requires minimum 10 customers.
    """

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM customers
        """)

        count = cursor.fetchone()["total"]

    assert count >= 10


def test_product_count():
    """
    Assignment requires minimum 15 products.
    """

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM products
        """)

        count = cursor.fetchone()["total"]

    assert count >= 15


def test_order_count():
    """
    Assignment requires minimum 25 orders.
    """

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM orders
        """)

        count = cursor.fetchone()["total"]

    assert count >= 25


def test_order_item_count():
    """
    Assignment requires minimum 40 order items.
    """

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM order_items
        """)

        count = cursor.fetchone()["total"]

    assert count >= 40