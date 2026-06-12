import sqlite3

def test_connection():
    conn = sqlite3.connect("data/ecommerce.db")
    assert conn is not None