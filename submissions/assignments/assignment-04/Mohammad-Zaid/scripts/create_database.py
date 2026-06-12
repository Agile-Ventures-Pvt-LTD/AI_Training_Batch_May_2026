import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecommerce.db")


def create_database():
    """
    Creates the ecommerce SQLite database and tables.
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        city TEXT,
        signup_date TEXT
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        stock_quantity INTEGER
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        total_amount REAL,
        FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY(order_id)
            REFERENCES orders(order_id),
        FOREIGN KEY(product_id)
            REFERENCES products(product_id)
    );
    """)

    conn.commit()
    conn.close()

    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_database()
    
    