import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.db.connection import get_connection


def test_database_connection():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    print("\nTables Found:\n")

    for table in tables:
        print(table["name"])

    conn.close()


if __name__ == "__main__":
    test_database_connection()