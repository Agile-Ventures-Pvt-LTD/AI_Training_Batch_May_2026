"""
seed_database.py

Purpose:
--------
Populate ecommerce.db with realistic sample data.

Run:
----
python scripts/seed_database.py
"""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta


# Database Configuration

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "ecommerce.db"

# Sample Data

CUSTOMER_NAMES = [
    "Rohan Mehta",
    "Priya Sharma",
    "Neha Gupta",
    "Amit Verma",
    "Sneha Kapoor",
    "Rahul Singh",
    "Anjali Jain",
    "Vikas Agarwal",
    "Pooja Malhotra",
    "Karan Arora",
    "Arjun Patel",
    "Nidhi Bansal",
    "Saurabh Yadav",
    "Meera Nair",
    "Ritika Khanna",
    "Vivek Joshi",
    "Ayesha Khan",
    "Tarun Malhotra",
    "Shweta Gupta",
    "Mohit Sharma"
]

CITIES = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad"
]

PRODUCTS = [
    ("Wireless Mouse", "Electronics", 799),
    ("Mechanical Keyboard", "Electronics", 2499),
    ("Bluetooth Speaker", "Electronics", 1999),
    ("Smart Watch", "Electronics", 4999),
    ("Laptop Stand", "Electronics", 1299),
    ("Yoga Mat", "Fitness", 699),
    ("Dumbbell Set", "Fitness", 2499),
    ("Resistance Bands", "Fitness", 499),
    ("Running Shoes", "Fashion", 2999),
    ("T-Shirt", "Fashion", 799),
    ("Jeans", "Fashion", 1499),
    ("Jacket", "Fashion", 2499),
    ("Coffee Mug", "Kitchen", 299),
    ("Water Bottle", "Kitchen", 499),
    ("Mixer Grinder", "Kitchen", 3499),
    ("Rice Cooker", "Kitchen", 2999),
    ("Study Table", "Furniture", 5999),
    ("Office Chair", "Furniture", 7499),
    ("Bookshelf", "Furniture", 4499),
    ("Bedside Lamp", "Furniture", 999),
    ("Notebook", "Stationery", 99),
    ("Pen Set", "Stationery", 199),
    ("Marker Pack", "Stationery", 299),
    ("Backpack", "Accessories", 1499),
    ("Wallet", "Accessories", 899),
    ("Sunglasses", "Accessories", 1299),
    ("Power Bank", "Electronics", 1599),
    ("USB Cable", "Electronics", 299),
    ("Headphones", "Electronics", 2999),
    ("Gaming Mouse", "Electronics", 3499)
]

ORDER_STATUSES = [
    "completed",
    "completed",
    "completed",
    "completed",
    "pending",
    "cancelled"
]


# Helper Functions

def random_date(start_days=365):
    """
    Generate random date in last N days.
    """

    today = datetime.now()

    random_days = random.randint(0, start_days)

    return (
        today - timedelta(days=random_days)
    ).strftime("%Y-%m-%d")


# Seed Customers

def seed_customers(cursor):

    customers = []

    for idx, name in enumerate(CUSTOMER_NAMES, start=1):

        email = (
            name.lower()
            .replace(" ", ".")
            + "@gmail.com"
        )

        city = random.choice(CITIES)

        signup_date = random_date(700)

        customers.append(
            (
                name,
                email,
                city,
                signup_date
            )
        )

    cursor.executemany(
        """
        INSERT INTO customers
        (
            name,
            email,
            city,
            signup_date
        )
        VALUES (?, ?, ?, ?)
        """,
        customers
    )

    print(f"Inserted {len(customers)} customers")

# Seed Products

def seed_products(cursor):

    rows = []

    for name, category, price in PRODUCTS:

        stock = random.randint(3, 100)

        rows.append(
            (
                name,
                category,
                price,
                stock
            )
        )

    cursor.executemany(
        """
        INSERT INTO products
        (
            name,
            category,
            price,
            stock_quantity
        )
        VALUES (?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted {len(rows)} products")


# Seed Orders

def seed_orders(cursor):

    orders = []

    for _ in range(100):

        customer_id = random.randint(1, 20)

        order_date = random_date(365)

        status = random.choice(ORDER_STATUSES)

        total_amount = round(
            random.uniform(500, 15000),
            2
        )

        orders.append(
            (
                customer_id,
                order_date,
                status,
                total_amount
            )
        )

    cursor.executemany(
        """
        INSERT INTO orders
        (
            customer_id,
            order_date,
            status,
            total_amount
        )
        VALUES (?, ?, ?, ?)
        """,
        orders
    )

    print(f"Inserted {len(orders)} orders")

# Seed Order Items

def seed_order_items(cursor):

    cursor.execute(
        "SELECT order_id FROM orders"
    )

    order_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    rows = []

    for order_id in order_ids:

        item_count = random.randint(1, 4)

        for _ in range(item_count):

            product_id = random.randint(1, 30)

            quantity = random.randint(1, 5)

            cursor.execute(
                """
                SELECT price
                FROM products
                WHERE product_id=?
                """,
                (product_id,)
            )

            price = cursor.fetchone()[0]

            rows.append(
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )
            )

    cursor.executemany(
        """
        INSERT INTO order_items
        (
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted {len(rows)} order items")

# Main Seeder

def seed_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    print("Seeding database...\n")

    seed_customers(cursor)

    seed_products(cursor)

    seed_orders(cursor)

    seed_order_items(cursor)

    conn.commit()

    conn.close()

    print("\nDatabase seeding completed successfully.")


# Run

if __name__ == "__main__":
    seed_database()