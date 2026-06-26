from db_utils import get_db_connection


conn = get_db_connection()

cursor = conn.cursor()


cursor.execute(
    "SELECT * FROM customer limit 5"
)


rows = cursor.fetchall()


for row in rows:
    print(row)


conn.close()