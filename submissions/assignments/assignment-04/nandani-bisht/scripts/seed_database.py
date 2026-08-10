import sqlite3
import random

random.seed(42)

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()


customers = [
    ("Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-15"),
    ("Priya Sharma", "priya@gmail.com", "Mumbai", "2024-02-20"),
    ("Neha Gupta", "neha@gmail.com", "Delhi", "2024-03-10"),
    ("Arjun Singh", "arjun@gmail.com", "Bangalore", "2024-03-25"),
    ("Ananya Verma", "ananya@gmail.com", "Pune", "2024-04-12"),
    ("Karan Kapoor", "karan@gmail.com", "Delhi", "2024-05-01"),
    ("Sneha Joshi", "sneha@gmail.com", "Mumbai", "2024-05-15"),
    ("Rahul Jain", "rahul@gmail.com", "Jaipur", "2024-06-05"),
    ("Isha Sharma", "isha@gmail.com", "Gurgaon", "2024-06-20"),
    ("Vikram Malhotra", "vikram@gmail.com", "Noida", "2024-07-01")
]

cursor.executemany(
    "INSERT INTO customers(name,email,city,signup_date) VALUES(?,?,?,?)",
    customers
)


products = [
    ("Wireless Mouse", "Electronics", 899, 5),
    ("Keyboard", "Electronics", 1499, 12),
    ("Laptop Stand", "Electronics", 1999, 8),
    ("Yoga Mat", "Fitness", 799, 6),
    ("Dumbbells", "Fitness", 2499, 20),
    ("Protein Shaker", "Fitness", 399, 15),
    ("Coffee Mug", "Kitchen", 299, 8),
    ("Water Bottle", "Kitchen", 499, 30),
    ("Mixer Grinder", "Kitchen", 3499, 7),
    ("Python Book", "Books", 699, 25),
    ("AI Handbook", "Books", 999, 14),
    ("Data Science Guide", "Books", 1199, 9),
    ("Smart Watch", "Electronics", 5999, 11),
    ("Bluetooth Speaker", "Electronics", 2499, 13),
    ("Desk Lamp", "Home", 799, 18)
]

cursor.executemany(
    "INSERT INTO products(name,category,price,stock_quantity) VALUES(?,?,?,?)",
    products
)


orders = [
    (1, "2025-01-05", "completed", 2500),
    (2, "2025-01-07", "completed", 4200),
    (3, "2025-01-10", "pending", 1500),
    (4, "2025-01-12", "completed", 3200),
    (5, "2025-01-15", "cancelled", 1800),
    (1, "2025-01-18", "completed", 5400),
    (2, "2025-01-20", "completed", 2900),
    (6, "2025-01-21", "pending", 2200),
    (7, "2025-01-23", "completed", 3800),
    (8, "2025-01-25", "completed", 4100),
    (9, "2025-01-27", "completed", 2700),
    (10, "2025-01-30", "cancelled", 1900),
    (3, "2025-02-01", "completed", 6000),
    (4, "2025-02-03", "pending", 2500),
    (5, "2025-02-05", "completed", 3400),
    (6, "2025-02-07", "completed", 2800),
    (7, "2025-02-10", "completed", 4700),
    (8, "2025-02-12", "completed", 3600),
    (9, "2025-02-14", "pending", 1700),
    (10, "2025-02-16", "completed", 5200),
    (1, "2025-02-18", "completed", 3100),
    (2, "2025-02-20", "completed", 4400),
    (3, "2025-02-22", "completed", 2900),
    (4, "2025-02-25", "cancelled", 2100),
    (5, "2025-02-27", "completed", 3900)
]

cursor.executemany(
    "INSERT INTO orders(customer_id,order_date,status,total_amount) VALUES(?,?,?,?)",
    orders
)


order_items = []

for order_id in range(1, 26):
    for _ in range(2):
        product_id = random.randint(1, 15)
        quantity = random.randint(1, 3)
        product_price = products[product_id - 1][2]
        order_items.append((order_id, product_id, quantity, product_price))

cursor.executemany(
    "INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(?,?,?,?)",
    order_items
)

conn.commit()
conn.close()

print("Database seeded successfully!")
