from src.db.connection import get_connection


def test_database_connection():

    conn = get_connection()

    assert conn is not None

    conn.close()


def test_tables_exist():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    conn.close()

    expected_tables = {
        "customers",
        "orders",
        "products"
    }

    assert expected_tables.issubset(
        tables
    )

# run ```pytest tests/test_database.py``` to execute