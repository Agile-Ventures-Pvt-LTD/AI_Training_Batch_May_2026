import sqlite3
import random
from datetime import datetime, timedelta

# below we are connecting with our db...

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# Customers...

customers = [
    ("Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-10"),
    ("Priya Sharma", "priya@gmail.com", "Mumbai", "2024-01-15"),
    ("Neha Gupta", "neha@gmail.com", "Delhi", "2024-02-05"),
    ("Amit Verma", "amit@gmail.com", "Pune", "2024-02-20"),
    ("Anjali Singh", "anjali@gmail.com", "Bangalore", "2024-03-01"),
    ("Karan Kapoor", "karan@gmail.com", "Delhi", "2024-03-10"),
    ("Sneha Jain", "sneha@gmail.com", "Hyderabad", "2024-03-15"),
    ("Vikas Yadav", "vikas@gmail.com", "Lucknow", "2024-04-01"),
    ("Pooja Arora", "pooja@gmail.com", "Chandigarh", "2024-04-12"),
    ("Rahul Malhotra", "rahul@gmail.com", "Jaipur", "2024-05-01")
]

cursor.executemany("""
INSERT INTO customers(name,email,city,signup_date)
VALUES(?,?,?,?)
""", customers)

# Products...


products = [
    ("Laptop", "Electronics", 65000, 15),
    ("Wireless Mouse", "Electronics", 1200, 5),
    ("Keyboard", "Electronics", 2500, 20),
    ("Monitor", "Electronics", 12000, 12),
    ("Coffee Mug", "Kitchen", 400, 8),
    ("Mixer Grinder", "Kitchen", 3500, 18),
    ("Yoga Mat", "Fitness", 1000, 6),
    ("Dumbbells", "Fitness", 2500, 25),
    ("T-Shirt", "Fashion", 799, 40),
    ("Jeans", "Fashion", 1499, 30),
    ("Sneakers", "Fashion", 2999, 22),
    ("Water Bottle", "Fitness", 499, 9),
    ("Headphones", "Electronics", 2999, 14),
    ("Backpack", "Fashion", 1999, 17),
    ("Smart Watch", "Electronics", 7999, 11)
]

cursor.executemany("""
INSERT INTO products(name,category,price,stock_quantity)
VALUES(?,?,?,?)
""", products)


# Orders


statuses = ["completed", "pending", "cancelled"]

orders = []

for i in range(25):
    customer_id = random.randint(1, 10)

    order_date = (
        datetime(2025, 1, 1)
        + timedelta(days=random.randint(0, 180))
    ).strftime("%Y-%m-%d")

    status = random.choices(
        statuses,
        weights=[70,20,10]
    )[0]

    total_amount = round(
        random.uniform(500, 50000), 2
    )

    orders.append(
        (
            customer_id,
            order_date,
            status,
            total_amount
        )
    )

cursor.executemany("""
INSERT INTO orders(
customer_id,
order_date,
status,
total_amount
)
VALUES(?,?,?,?)
""", orders)


# Order Items


order_items = []

for order_id in range(1, 26):

    item_count = random.randint(1, 3)

    for _ in range(item_count):

        product_id = random.randint(1, 15)

        quantity = random.randint(1, 5)

        cursor.execute("""
        SELECT price
        FROM products
        WHERE product_id=?
        """, (product_id,))

        price = cursor.fetchone()[0]

        order_items.append(
            (
                order_id,
                product_id,
                quantity,
                price
            )
        )

cursor.executemany("""
INSERT INTO order_items(
order_id,
product_id,
quantity,
unit_price
)
VALUES(?,?,?,?)
""", order_items)

conn.commit()
conn.close()

print("Database Seeded Successfully!")