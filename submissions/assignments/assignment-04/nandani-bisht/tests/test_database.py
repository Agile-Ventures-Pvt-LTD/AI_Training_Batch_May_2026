from src.db.connection import get_connection


def test_database_connection():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)

    tables = cursor.fetchall()

    assert len(tables) > 0

    conn.close()