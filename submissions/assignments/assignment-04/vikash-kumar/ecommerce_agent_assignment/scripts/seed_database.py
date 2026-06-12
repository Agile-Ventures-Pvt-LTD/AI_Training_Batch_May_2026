import sqlite3

DB_PATH = "data/ecommerce.db"


def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------------------------------------------------
    # Customers (10 Records)
    # -------------------------------------------------

    customers = [
        (1, "Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-10"),
        (2, "Priya Sharma", "priya@gmail.com", "Mumbai", "2024-01-15"),
        (3, "Neha Gupta", "neha@gmail.com", "Delhi", "2024-02-01"),
        (4, "Amit Verma", "amit@gmail.com", "Bangalore", "2024-02-12"),
        (5, "Karan Singh", "karan@gmail.com", "Pune", "2024-03-05"),
        (6, "Anjali Kapoor", "anjali@gmail.com", "Chandigarh", "2024-03-15"),
        (7, "Vikas Yadav", "vikas@gmail.com", "Lucknow", "2024-04-01"),
        (8, "Sneha Jain", "sneha@gmail.com", "Jaipur", "2024-04-18"),
        (9, "Rahul Arora", "rahul@gmail.com", "Delhi", "2024-05-01"),
        (10, "Pooja Malhotra", "pooja@gmail.com", "Mumbai", "2024-05-10")
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO customers
        VALUES (?, ?, ?, ?, ?)
        """,
        customers
    )

    # -------------------------------------------------
    # Products (15 Records)
    # -------------------------------------------------

    products = [
        (1, "Wireless Mouse", "Electronics", 799, 4),
        (2, "Keyboard", "Electronics", 1499, 15),
        (3, "Laptop Stand", "Electronics", 999, 12),
        (4, "Coffee Mug", "Kitchen", 299, 8),
        (5, "Water Bottle", "Kitchen", 499, 25),
        (6, "Yoga Mat", "Fitness", 899, 6),
        (7, "Dumbbells", "Fitness", 2499, 18),
        (8, "T-Shirt", "Fashion", 699, 30),
        (9, "Jeans", "Fashion", 1499, 20),
        (10, "Sneakers", "Fashion", 2999, 10),
        (11, "Notebook", "Stationery", 99, 50),
        (12, "Pen Set", "Stationery", 199, 40),
        (13, "Desk Lamp", "Home Decor", 1299, 14),
        (14, "Wall Clock", "Home Decor", 899, 11),
        (15, "Bluetooth Speaker", "Electronics", 3499, 7)
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO products
        VALUES (?, ?, ?, ?, ?)
        """,
        products
    )

    # -------------------------------------------------
    # Orders (25 Records)
    # -------------------------------------------------

    orders = [
        (1, 1, "2025-01-02", "completed", 2500),
        (2, 2, "2025-01-05", "completed", 4500),
        (3, 3, "2025-01-08", "pending", 1200),
        (4, 4, "2025-01-10", "completed", 3500),
        (5, 5, "2025-01-12", "cancelled", 2000),
        (6, 1, "2025-01-15", "completed", 5000),
        (7, 2, "2025-01-18", "completed", 2700),
        (8, 6, "2025-01-20", "pending", 1800),
        (9, 7, "2025-01-25", "completed", 4200),
        (10, 8, "2025-01-28", "completed", 3900),
        (11, 9, "2025-02-01", "completed", 2100),
        (12, 10, "2025-02-05", "completed", 6400),
        (13, 3, "2025-02-08", "completed", 3300),
        (14, 4, "2025-02-12", "cancelled", 2500),
        (15, 5, "2025-02-15", "completed", 4700),
        (16, 6, "2025-02-18", "completed", 1500),
        (17, 7, "2025-02-22", "pending", 2200),
        (18, 8, "2025-02-25", "completed", 5100),
        (19, 9, "2025-03-01", "completed", 1900),
        (20, 10, "2025-03-05", "completed", 7300),
        (21, 1, "2025-03-08", "completed", 2800),
        (22, 2, "2025-03-12", "completed", 5400),
        (23, 3, "2025-03-15", "cancelled", 1700),
        (24, 4, "2025-03-18", "completed", 3600),
        (25, 5, "2025-03-20", "completed", 4100)
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO orders
        VALUES (?, ?, ?, ?, ?)
        """,
        orders
    )

    # -------------------------------------------------
    # Order Items (40+ Records)
    # -------------------------------------------------

    order_items = []

    order_item_id = 1

    for order_id in range(1, 26):

        product1 = ((order_id - 1) % 15) + 1
        product2 = ((order_id + 2) % 15) + 1

        order_items.append(
            (
                order_item_id,
                order_id,
                product1,
                2,
                500
            )
        )
        order_item_id += 1

        order_items.append(
            (
                order_item_id,
                order_id,
                product2,
                1,
                800
            )
        )
        order_item_id += 1

    cursor.executemany(
        """
        INSERT OR REPLACE INTO order_items
        VALUES (?, ?, ?, ?, ?)
        """,
        order_items
    )

    conn.commit()
    conn.close()

    print("Database seeded successfully!")
    print(f"Customers : {len(customers)}")
    print(f"Products  : {len(products)}")
    print(f"Orders    : {len(orders)}")
    print(f"OrderItems: {len(order_items)}")


if __name__ == "__main__":
    seed_database()