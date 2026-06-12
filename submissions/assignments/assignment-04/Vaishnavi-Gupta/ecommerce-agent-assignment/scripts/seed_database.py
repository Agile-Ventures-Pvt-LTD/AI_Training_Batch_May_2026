import sqlite3
from faker import Faker
import random
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "ecommerce.db"

fake = Faker()

conn = sqlite3.connect(DB_PATH)

cur = conn.cursor()

cities = [
    "Delhi",
    "Mumbai",
    "Pune",
    "Bangalore",
    "Chennai"
]

for i in range(1,11):
    cur.execute("""
    INSERT INTO customers
    VALUES(?,?,?,?,?)
    """,(
        i,
        fake.name(),
        fake.email(),
        random.choice(cities),
        str(fake.date())
    ))

products = [
("Laptop","Electronics",70000,12),
("Mouse","Electronics",800,6),
("Keyboard","Electronics",1200,5),
("Shoes","Fashion",2500,18),
("Tshirt","Fashion",900,25),
("Watch","Fashion",5000,8),
("Bottle","Home",300,15),
("Chair","Home",4500,9),
("Table","Home",6000,4),
("Book","Education",500,20),
("Bag","Education",1500,11),
("Notebook","Education",100,30),
("Yoga Mat","Fitness",1000,7),
("Dumbbell","Fitness",2500,10),
("Cycle","Fitness",15000,3)
]

for idx, p in enumerate(products, 1):
    cur.execute(
        "INSERT INTO products VALUES(?,?,?,?,?)",
        (idx, *p)
    )

statuses = ["completed", "pending", "cancelled"]

# Create Orders
for order_id in range(1, 101):

    customer_id = random.randint(1, 10)
    total_amount = round(random.uniform(500, 50000), 2)

    cur.execute(
        """
        INSERT INTO orders
        VALUES (?,?,?,?,?)
        """,
        (
            order_id,
            customer_id,
            str(fake.date()),
            random.choice(statuses),
            total_amount
        )
    )

# Create Order Items
order_item_id = 1

for order_id in range(1, 101):

    num_items = random.randint(1, 4)

    for _ in range(num_items):

        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 5)

        cur.execute(
            """
            SELECT price
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        )

        price = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO order_items
            VALUES (?,?,?,?,?)
            """,
            (
                order_item_id,
                order_id,
                product_id,
                quantity,
                price
            )
        )

        order_item_id += 1

conn.commit()
conn.close()

print("Data Seeded")

