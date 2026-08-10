
import sqlite3
from config import DB_PATH

print("\nUSING DATABASE:")
print(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nTABLES AND VIEWS:")

cursor.execute("""
SELECT name, type
FROM sqlite_master
WHERE type IN ('table','view')
ORDER BY type, name
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()