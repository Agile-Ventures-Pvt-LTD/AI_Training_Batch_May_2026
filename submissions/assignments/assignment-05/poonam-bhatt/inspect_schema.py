import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

for table in tables:
    table_name = table[0]

    print("\n" + "=" * 50)
    print("TABLE:", table_name)
    print("=" * 50)

    cursor.execute(
        f"PRAGMA table_info('{table_name}')"
    )

    for col in cursor.fetchall():
        print(col)

conn.close()