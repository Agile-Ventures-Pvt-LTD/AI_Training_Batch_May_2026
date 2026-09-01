import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM sqlite_sequence")

    customers = [
        ("Priya Sharma", "priya@gmail.com", "Delhi", "2024-01-15"),
        ("Rohan Mehta", "rohan@gmail.com", "Mumbai", "2024-02-10"),
        ("Neha Gupta", "neha@gmail.com", "Delhi", "2024-03-05"),
        ("Arjun Singh", "arjun@gmail.com", "Pune", "2024-01-22"),
        ("Aman Verma", "aman@gmail.com", "Bangalore", "2024-04-12"),
        ("Simran Kaur", "simran@gmail.com", "Chandigarh", "2024-02-08"),
        ("Rahul Jain", "rahul@gmail.com", "Jaipur", "2024-05-11"),
        ("Anjali Das", "anjali@gmail.com", "Kolkata", "2024-03-18"),
        ("Karan Shah", "karan@gmail.com", "Ahmedabad", "2024-06-01"),
        ("Sneha Roy", "sneha@gmail.com", "Delhi", "2024-07-09"),
    ]

    cursor.executemany(
        "INSERT INTO customers(name,email,city,signup_date) VALUES(?,?,?,?)",
        customers,
    )

    products = [
        ("Wireless Mouse", "Electronics", 899, 5),
        ("Mechanical Keyboard", "Electronics", 3499, 12),
        ("Bluetooth Speaker", "Electronics", 2499, 8),
        ("Laptop Stand", "Electronics", 1499, 15),
        ("Smart Watch", "Electronics", 5999, 6),

        ("Yoga Mat", "Fitness", 799, 7),
        ("Dumbbell Set", "Fitness", 2499, 18),
        ("Resistance Bands", "Fitness", 499, 20),

        ("Coffee Mug", "Kitchen", 299, 9),
        ("Mixer Grinder", "Kitchen", 3999, 14),
        ("Water Bottle", "Kitchen", 499, 22),

        ("Novel Book", "Books", 399, 25),
        ("Data Science Book", "Books", 899, 10),

        ("Office Chair", "Furniture", 6999, 4),
        ("Study Table", "Furniture", 8999, 11),
    ]

    cursor.executemany(
        "INSERT INTO products(name,category,price,stock_quantity) VALUES(?,?,?,?)",
        products,
    )

    random.seed(4)
    statuses = ["completed", "pending", "cancelled"]
    orders = []

    for _ in range(25):
        customer_id = random.randint(1, 10)
        order_date = (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 180))
        ).strftime("%Y-%m-%d")
        status = random.choices(statuses, weights=[70, 20, 10])[0]
        total_amount = round(random.uniform(500, 15000), 2)

        orders.append((customer_id, order_date, status, total_amount))

    cursor.executemany(
        "INSERT INTO orders(customer_id,order_date,status,total_amount) VALUES(?,?,?,?)",
        orders,
    )

    order_items = []

    for order_id in range(1, 26):
        num_products = random.randint(1, 3)
        selected_products = random.sample(range(1, 16), num_products)

        for product_id in selected_products:
            cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            unit_price = cursor.fetchone()[0]
            quantity = random.randint(1, 5)
            order_items.append((order_id, product_id, quantity, unit_price))

    cursor.executemany(
        "INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(?,?,?,?)",
        order_items,
    )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_items")
    order_item_count = cursor.fetchone()[0]

    conn.close()

    print("\nDatabase Seeded Successfully!")
    print(f"Customers   : {customer_count}")
    print(f"Products    : {product_count}")
    print(f"Orders      : {order_count}")
    print(f"Order Items : {order_item_count}")


if __name__ == "__main__":
    seed_database()
