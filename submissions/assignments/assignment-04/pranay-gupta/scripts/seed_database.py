import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecommerce.db")


customers = [
    ("Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-15"),
    ("Priya Sharma", "priya@gmail.com", "Mumbai", "2024-01-20"),
    ("Neha Gupta", "neha@gmail.com", "Delhi", "2024-02-05"),
    ("Amit Verma", "amit@gmail.com", "Bangalore", "2024-02-10"),
    ("Sneha Kapoor", "sneha@gmail.com", "Pune", "2024-02-25"),
    ("Rahul Singh", "rahul@gmail.com", "Hyderabad", "2024-03-02"),
    ("Karan Malhotra", "karan@gmail.com", "Delhi", "2024-03-12"),
    ("Anjali Jain", "anjali@gmail.com", "Chennai", "2024-03-22"),
    ("Vikram Arora", "vikram@gmail.com", "Kolkata", "2024-04-01"),
    ("Pooja Mishra", "pooja@gmail.com", "Mumbai", "2024-04-15")
]


products = [
    ("Wireless Mouse", "Electronics", 899, 4),
    ("Mechanical Keyboard", "Electronics", 2499, 20),
    ("Bluetooth Speaker", "Electronics", 1999, 8),
    ("Yoga Mat", "Fitness", 799, 6),
    ("Dumbbell Set", "Fitness", 2999, 12),
    ("Running Shoes", "Fitness", 3499, 15),
    ("Coffee Mug", "Kitchen", 299, 8),
    ("Mixer Grinder", "Kitchen", 4499, 11),
    ("Cookware Set", "Kitchen", 5999, 9),
    ("Notebook", "Stationery", 99, 100),
    ("Pen Pack", "Stationery", 149, 80),
    ("Office Chair", "Furniture", 7999, 5),
    ("Study Table", "Furniture", 9999, 7),
    ("LED Monitor", "Electronics", 12999, 10),
    ("Smart Watch", "Electronics", 5999, 13)
]


orders = [
    (1, "2025-01-05", "completed", 3898),
    (2, "2025-01-08", "completed", 5999),
    (3, "2025-01-10", "pending", 4499),
    (4, "2025-01-11", "cancelled", 2999),
    (5, "2025-01-15", "completed", 7999),
    (6, "2025-01-18", "completed", 9999),
    (7, "2025-01-20", "pending", 2499),
    (8, "2025-01-22", "completed", 12999),
    (9, "2025-01-24", "completed", 5999),
    (10, "2025-01-25", "cancelled", 899),
    (1, "2025-02-02", "completed", 6998),
    (2, "2025-02-04", "completed", 4499),
    (3, "2025-02-05", "completed", 299),
    (4, "2025-02-06", "pending", 1999),
    (5, "2025-02-08", "completed", 799),
    (6, "2025-02-10", "completed", 149),
    (7, "2025-02-12", "completed", 2499),
    (8, "2025-02-15", "completed", 5999),
    (9, "2025-02-18", "pending", 3499),
    (10, "2025-02-20", "completed", 7999),
    (1, "2025-03-02", "completed", 12999),
    (2, "2025-03-05", "completed", 5999),
    (3, "2025-03-08", "cancelled", 799),
    (4, "2025-03-10", "completed", 4499),
    (5, "2025-03-12", "completed", 2499)
]


order_items = [
    (1,1,2,899),
    (1,2,1,2499),

    (2,15,1,5999),

    (3,8,1,4499),

    (4,5,1,2999),

    (5,12,1,7999),

    (6,13,1,9999),

    (7,2,1,2499),

    (8,14,1,12999),

    (9,15,1,5999),

    (10,1,1,899),

    (11,15,1,5999),
    (11,3,1,999),

    (12,8,1,4499),

    (13,7,1,299),

    (14,3,1,1999),

    (15,4,1,799),

    (16,11,1,149),

    (17,2,1,2499),

    (18,15,1,5999),

    (19,6,1,3499),

    (20,12,1,7999),

    (21,14,1,12999),

    (22,15,1,5999),

    (23,4,1,799),

    (24,8,1,4499),

    (25,2,1,2499),

    (5,7,2,299),
    (6,10,5,99),
    (8,1,3,899),
    (9,11,4,149),
    (12,4,2,799),
    (15,10,3,99),
    (18,7,5,299),
    (19,3,1,1999),
    (20,5,2,2999),
    (21,11,6,149),
    (22,10,10,99),
    (24,7,2,299),
    (25,1,1,899)
]
# total records > 40

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO customers
        (name,email,city,signup_date)
        VALUES (?,?,?,?)
    """, customers)

    cursor.executemany("""
        INSERT INTO products
        (name,category,price,stock_quantity)
        VALUES (?,?,?,?)
    """, products)

    cursor.executemany("""
        INSERT INTO orders
        (customer_id,order_date,status,total_amount)
        VALUES (?,?,?,?)
    """, orders)

    cursor.executemany("""
        INSERT INTO order_items
        (order_id,product_id,quantity,unit_price)
        VALUES (?,?,?,?)
    """, order_items)

    conn.commit()
    conn.close()

    print("Sample data inserted successfully.")


if __name__ == "__main__":
    seed_database()