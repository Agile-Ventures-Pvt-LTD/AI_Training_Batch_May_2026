import sqlite3

def test_database_connection():
    conn = sqlite3.connect("data/ecommerce.db")
    assert conn is not None
    conn.close()