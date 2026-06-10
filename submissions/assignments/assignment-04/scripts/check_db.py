import sqlite3

# below we are connecting with our db...

conn = sqlite3.connect("data/ecommerce.db")

cursor = conn.cursor()

# Getting table names...

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print(cursor.fetchall())

conn.close()