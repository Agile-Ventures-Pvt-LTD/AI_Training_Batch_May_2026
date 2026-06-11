import sqlite3
import os


DB_PATH = "data/ecommerce.db"


def create_database():
    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------------------------
    # Customers Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        signup_date TEXT NOT NULL
    )
    """)

    # -------------------------
    # Products Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
    """)

    # -------------------------
    # Orders Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
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

    # -------------------------
    # Order Items Table
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
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

    conn.commit()
    conn.close()

    print("Database created successfully!")
    print(f"Location: {DB_PATH}")


if __name__ == "__main__":
    create_database()