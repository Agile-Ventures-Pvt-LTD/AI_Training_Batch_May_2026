import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

cities = ["Delhi", "Mumbai", "Pune", "Bangalore", "Chennai"]

for i in range(1, 11):
    cursor.execute("""
    INSERT INTO customers
    VALUES (?,?,?,?,?)
    """, (
        i,
        fake.name(),
        fake.email(),
        random.choice(cities),
        str(fake.date())
    ))

categories = [
    "Electronics",
    "Fashion",
    "Books",
    "Sports"
]

for i in range(1, 16):
    cursor.execute("""
    INSERT INTO products
    VALUES (?,?,?,?,?)
    """, (
        i,
        fake.word().title(),
        random.choice(categories),
        round(random.uniform(100, 10000), 2),
        random.randint(1, 100)
    ))

statuses = [
    "completed",
    "pending",
    "cancelled"
]

for i in range(1, 26):
    cursor.execute("""
    INSERT INTO orders
    VALUES (?,?,?,?,?)
    """, (
        i,
        random.randint(1, 10),
        str(fake.date()),
        random.choice(statuses),
        round(random.uniform(500, 25000), 2)
    ))

for i in range(1, 41):
    cursor.execute("""
    INSERT INTO order_items
    VALUES (?,?,?,?,?)
    """, (
        i,
        random.randint(1, 25),
        random.randint(1, 15),
        random.randint(1, 5),
        round(random.uniform(100, 5000), 2)
    ))

conn.commit()
conn.close()

print("Data Inserted Successfully")