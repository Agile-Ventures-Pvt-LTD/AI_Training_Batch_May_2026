import sqlite3
import os

DB_PATH = "data/ecommerce.db"


def create_database():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        city TEXT,
        signup_date TEXT
    )
    """)

    # Products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        stock_quantity INTEGER
    )
    """)

    # Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        total_amount REAL,
        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
    )
    """)

    # Order Items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY(order_id)
        REFERENCES orders(order_id),
        FOREIGN KEY(product_id)
        REFERENCES products(product_id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully")


if __name__ == "__main__":
    create_database()