import sqlite3
import os



# connect database
conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# ---------------- CUSTOMERS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    signup_date TEXT
)
""")

# ---------------- PRODUCTS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock_quantity INTEGER
)
""")

# ---------------- ORDERS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_amount REAL
)
""")

# ---------------- ORDER ITEMS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")