import sqlite3
import random
from faker import Faker

fake = Faker("en_IN")

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# ------------------------
# Customers
# ------------------------

cities = [
    "Delhi",
    "Mumbai",
    "Jaipur",
    "Bangalore",
    "Pune",
    "Chennai",
    "Hyderabad",
    "Kolkata"
]

for _ in range(10):
    cursor.execute(
        """
        INSERT INTO customers(name,email,city,signup_date)
        VALUES(?,?,?,?)
        """,
        (
            fake.name(),
            fake.email(),
            random.choice(cities),
            fake.date_between(
                start_date="-2y",
                end_date="today"
            ).isoformat()
        )
    )

# ------------------------
# Products
# ------------------------

products = [
    ("Laptop", "Electronics", 65000, 15),
    ("Keyboard", "Electronics", 1500, 7),
    ("Mouse", "Electronics", 800, 5),
    ("Monitor", "Electronics", 12000, 20),
    ("Headphones", "Electronics", 2500, 8),
    ("Coffee Mug", "Kitchen", 350, 4),
    ("Mixer Grinder", "Kitchen", 4500, 12),
    ("Water Bottle", "Kitchen", 500, 9),
    ("Yoga Mat", "Fitness", 1200, 6),
    ("Dumbbells", "Fitness", 3500, 10),
    ("T-Shirt", "Fashion", 799, 30),
    ("Jeans", "Fashion", 1999, 25),
    ("Sneakers", "Fashion", 3999, 18),
    ("Backpack", "Accessories", 1499, 14),
    ("Smart Watch", "Electronics", 7999, 11)
]

cursor.executemany(
    """
    INSERT INTO products
    (name,category,price,stock_quantity)
    VALUES(?,?,?,?)
    """,
    products
)

# ------------------------
# Orders
# ------------------------

statuses = [
    "completed",
    "completed",
    "completed",
    "pending",
    "cancelled"
]

for _ in range(25):

    customer_id = random.randint(1, 10)

    cursor.execute(
        """
        INSERT INTO orders
        (customer_id,order_date,status,total_amount)
        VALUES(?,?,?,?)
        """,
        (
            customer_id,
            fake.date_between(
                start_date="-1y",
                end_date="today"
            ).isoformat(),
            random.choice(statuses),
            round(random.uniform(500, 25000), 2)
        )
    )

# ------------------------
# Order Items
# ------------------------

for _ in range(50):

    order_id = random.randint(1, 25)

    product_id = random.randint(1, 15)

    quantity = random.randint(1, 5)

    cursor.execute(
        """
        SELECT price
        FROM products
        WHERE product_id=?
        """,
        (product_id,)
    )

    unit_price = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO order_items
        (order_id,product_id,quantity,unit_price)
        VALUES(?,?,?,?)
        """,
        (
            order_id,
            product_id,
            quantity,
            unit_price
        )
    )

conn.commit()
conn.close()

print("Database seeded successfully.")