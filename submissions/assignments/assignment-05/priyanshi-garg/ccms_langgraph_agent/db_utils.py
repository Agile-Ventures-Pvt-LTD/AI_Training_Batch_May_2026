import sqlite3

DB_PATH = "data/ccms.db"

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(query, params)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return rows

import sqlite3

conn = sqlite3.connect("data/ccms.db")
cursor = conn.cursor()

tables = [
    "customer",
    "card",
    "card_type",
    "transaction",
    "transaction_type",
    "transaction_terminal",
    "merchant",
    "merchant_type",
    "netbanking"
]

for table in tables:
    print(f"\n=== {table.upper()} ===")
    cursor.execute(f'PRAGMA table_info("{table}")')
    print(cursor.fetchall())

conn.close()