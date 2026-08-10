
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path


DB_PATH = Path("data/ecommerce.db")


CUSTOMERS = [
    ("Rohan Mehta", "rohan@example.com", "Delhi"),
    ("Priya Sharma", "priya@example.com", "Mumbai"),
    ("Neha Gupta", "neha@example.com", "Delhi"),
    ("Amit Verma", "amit@example.com", "Pune"),
    ("Karan Singh", "karan@example.com", "Jaipur"),
    ("Sneha Kapoor", "sneha@example.com", "Chandigarh"),
    ("Rahul Arora", "rahul@example.com", "Delhi"),
    ("Pooja Jain", "pooja@example.com", "Bangalore"),
    ("Ankit Yadav", "ankit@example.com", "Lucknow"),
    ("Meera Joshi", "meera@example.com", "Hyderabad"),
]

PRODUCTS = [
    ("Wireless Mouse", "Electronics", 799, 4),
    ("Keyboard", "Electronics", 1499, 25),
    ("Monitor", "Electronics", 12999, 12),
    ("Laptop Stand", "Electronics", 999, 8),
    ("Yoga Mat", "Fitness", 699, 6),
    ("Dumbbells", "Fitness", 2499, 15),
    ("Resistance Band", "Fitness", 499, 30),
    ("Coffee Mug", "Kitchen", 299, 8),
    ("Water Bottle", "Kitchen", 499, 20),
    ("Mixer Grinder", "Kitchen", 3499, 9),
    ("Novel Book", "Books", 399, 50),
    ("Python Guide", "Books", 899, 18),
    ("Desk Lamp", "Home", 1199, 14),
    ("Office Chair", "Home", 7999, 5),
    ("Wall Clock", "Home", 699, 22),
]


def random_date(days_back=365):
    start = datetime.now() - timedelta(days=days_back)
    random_days = random.randint(0, days_back)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def seed_customers(cursor):
    cursor.executemany(
        """
        INSERT INTO customers(name, email, city, signup_date)
        VALUES (?, ?, ?, ?)
        """,
        [
            (name, email, city, random_date())
            for name, email, city in CUSTOMERS
        ]
    )


def seed_products(cursor):
    cursor.executemany(
        """
        INSERT INTO products(name, category, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """,
        PRODUCTS
    )


def seed_orders(cursor):
    statuses = ["completed", "pending", "cancelled"]

    for _ in range(25):
        customer_id = random.randint(1, 10)

        cursor.execute(
            """
            INSERT INTO orders(
                customer_id,
                order_date,
                status,
                total_amount
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer_id,
                random_date(),
                random.choice(statuses),
                round(random.uniform(500, 25000), 2)
            )
        )


def seed_order_items(cursor):
    cursor.execute("SELECT order_id FROM orders")
    orders = [row[0] for row in cursor.fetchall()]

    for _ in range(40):
        order_id = random.choice(orders)
        product_id = random.randint(1, 15)
        quantity = random.randint(1, 5)

        cursor.execute(
            "SELECT price FROM products WHERE product_id=?",
            (product_id,)
        )

        unit_price = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO order_items(
                order_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                order_id,
                product_id,
                quantity,
                unit_price
            )
        )


def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    seed_customers(cursor)
    seed_products(cursor)
    seed_orders(cursor)
    seed_order_items(cursor)

    conn.commit()
    conn.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()

