"""
create_database.py

Purpose:
--------
Creates the SQLite database and all required tables
for the LangChain E-commerce Agent Assignment.

Run:
----
python scripts/create_database.py
"""

import sqlite3
from pathlib import Path

# Database Configuration

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "ecommerce.db"

# Create Database Function

def create_database():
    """
    Creates ecommerce.db and all required tables.
    """

    DATA_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # Enable Foreign Key Support
    cursor.execute("PRAGMA foreign_keys = ON")

    print("Creating database tables...")

    # Customers Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        signup_date TEXT NOT NULL
    )
    """)

    # Products Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
    """)

    # Orders Table

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
    )
    """)

    # Order Items Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,

        order_id INTEGER NOT NULL,

        product_id INTEGER NOT NULL,

        quantity INTEGER NOT NULL,

        unit_price REAL NOT NULL,

        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
    )
    """)

    # Indexes

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_customer_city
    ON customers(city)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_product_category
    ON products(category)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_order_customer
    ON orders(customer_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_order_status
    ON orders(status)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_order_items_order
    ON order_items(order_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_order_items_product
    ON order_items(product_id)
    """)

    conn.commit()

    conn.close()

    print(f"Database created successfully.")
    print(f"Location: {DB_PATH}")

if __name__ == "__main__":
    create_database()