import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecommerce.db")


def seed_database():
    """
    Inserts deterministic sample data into ecommerce.db
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --------------------------
    # Customers
    # --------------------------

    customers = [
        (1, "Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-15"),
        (2, "Priya Sharma", "priya@gmail.com", "Mumbai", "2024-02-10"),
        (3, "Amit Verma", "amit@gmail.com", "Delhi", "2024-03-05"),
        (4, "Neha Gupta", "neha@gmail.com", "Pune", "2024-01-20"),
        (5, "Arjun Singh", "arjun@gmail.com", "Bangalore", "2024-04-12"),
        (6, "Sneha Kapoor", "sneha@gmail.com", "Chennai", "2024-02-15"),
        (7, "Karan Malhotra", "karan@gmail.com", "Hyderabad", "2024-05-01"),
        (8, "Anjali Jain", "anjali@gmail.com", "Mumbai", "2024-03-11"),
        (9, "Vikas Kumar", "vikas@gmail.com", "Delhi", "2024-01-30"),
        (10, "Pooja Mishra", "pooja@gmail.com", "Pune", "2024-04-22"),
    ]

    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers
    )

    # --------------------------
    # Products
    # --------------------------

    products = [
        (1, "Wireless Mouse", "Electronics", 799, 5),
        (2, "Mechanical Keyboard", "Electronics", 2499, 20),
        (3, "Bluetooth Speaker", "Electronics", 1999, 8),
        (4, "Yoga Mat", "Fitness", 599, 6),
        (5, "Dumbbells Set", "Fitness", 2999, 15),
        (6, "Coffee Mug", "Kitchen", 299, 8),
        (7, "Mixer Grinder", "Kitchen", 3499, 12),
        (8, "Cookware Set", "Kitchen", 4599, 9),
        (9, "Python Programming", "Books", 799, 25),
        (10, "Data Science Handbook", "Books", 999, 18),
        (11, "Men T-Shirt", "Fashion", 499, 30),
        (12, "Women Kurti", "Fashion", 899, 14),
        (13, "Laptop Stand", "Electronics", 1299, 7),
        (14, "Water Bottle", "Fitness", 399, 22),
        (15, "Notebook Pack", "Books", 249, 35),
    ]

    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

    # --------------------------
    # Orders
    # --------------------------

    orders = [
        (1,1,'2024-05-01','completed',3500),
        (2,2,'2024-05-02','completed',4200),
        (3,3,'2024-05-03','pending',1800),
        (4,4,'2024-05-04','completed',2700),
        (5,5,'2024-05-05','cancelled',900),
        (6,2,'2024-05-06','completed',5600),
        (7,6,'2024-05-07','pending',1200),
        (8,7,'2024-05-08','completed',6200),
        (9,8,'2024-05-09','completed',2100),
        (10,9,'2024-05-10','cancelled',1500),
        (11,10,'2024-05-11','completed',4100),
        (12,1,'2024-05-12','completed',3200),
        (13,2,'2024-05-13','completed',3800),
        (14,3,'2024-05-14','completed',2900),
        (15,4,'2024-05-15','pending',1700),
        (16,5,'2024-05-16','completed',4800),
        (17,6,'2024-05-17','completed',2500),
        (18,7,'2024-05-18','completed',7100),
        (19,8,'2024-05-19','completed',1900),
        (20,9,'2024-05-20','completed',2700),
        (21,10,'2024-05-21','pending',2200),
        (22,2,'2024-05-22','completed',4900),
        (23,4,'2024-05-23','completed',3600),
        (24,6,'2024-05-24','cancelled',1100),
        (25,1,'2024-05-25','completed',5300),
    ]

    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)

    # --------------------------
    # Order Items
    # --------------------------

    order_items = []

    item_id = 1

    for order_id in range(1, 26):

        order_items.append((item_id, order_id, (order_id % 15) + 1, 2, 500))
        
        item_id += 1

        order_items.append((item_id, order_id, ((order_id + 3) % 15) + 1, 1, 1000))

        item_id += 1

    cursor.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", order_items)

    conn.commit()
    conn.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()