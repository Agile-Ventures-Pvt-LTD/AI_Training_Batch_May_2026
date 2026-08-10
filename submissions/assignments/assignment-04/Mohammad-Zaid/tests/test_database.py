# tests/test_database.py

import sqlite3

from src.db.connection import get_connection


def test_database_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    conn.close()

    expected_tables = {
        "customers",
        "products",
        "orders",
        "order_items"
    }

    assert expected_tables.issubset(tables)


def test_customer_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count == 10


def test_product_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    count = cursor.fetchone()[0]

    conn.close()

    assert count == 15