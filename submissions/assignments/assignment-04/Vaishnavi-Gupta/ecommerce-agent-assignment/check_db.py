
import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(orders)")
print(cur.fetchall())

conn.close()