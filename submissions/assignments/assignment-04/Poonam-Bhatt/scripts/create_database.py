import sqlite3

# below we are connecting with our db...

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

#Creating Table Customer...

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    signup_date TEXT
)
""")

#creating table Product...

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock_quantity INTEGER
)
""")

#creating table orders...

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

#creating table order items...

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items(
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

conn.commit()
conn.close()

print("Database created successfully.")