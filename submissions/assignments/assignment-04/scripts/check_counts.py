import sqlite3

# below we are connecting with our db...

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# all the tables involved in db...

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

#loop on all table at once dynamically...

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count}")

conn.close()