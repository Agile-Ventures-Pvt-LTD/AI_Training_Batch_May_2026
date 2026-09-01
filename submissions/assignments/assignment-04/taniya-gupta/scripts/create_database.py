import sqlite3
from pathlib import Path

DB = "data/ecommerce.db"


def create_database():
    Path("data").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        signup_date TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL CHECK (
            status IN ('completed', 'pending', 'cancelled')
        ),
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id)
            REFERENCES orders(order_id)
            ON DELETE CASCADE,
        FOREIGN KEY (product_id)
            REFERENCES products(product_id)
            ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

    print("ecommerce.db created successfully!")
    print("Tables: customers, products, orders, order_items")


if __name__ == "__main__":
    create_database()
