import sqlite3
from pathlib import Path


DB_PATH = Path("data/ecommerce.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def test_database_exists():
    assert DB_PATH.exists(), "Database file does not exist."


def test_required_tables_exist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = {row[0] for row in cursor.fetchall()}

    conn.close()

    required_tables = {
        "customers",
        "products",
        "orders",
        "order_items"
    }

    assert required_tables.issubset(tables)


def test_customers_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count >= 10


def test_products_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count >= 15


def test_orders_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count >= 25


def test_order_items_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM order_items"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count >= 40