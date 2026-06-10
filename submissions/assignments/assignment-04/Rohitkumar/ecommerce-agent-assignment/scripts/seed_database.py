import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

#  CUSTOMERS
customers = [
    (1, "Rohit Sharma", "rohit@gmail.com", "Delhi", "2022-01-10"),
    (2, "Amit Kumar", "amit@gmail.com", "Mumbai", "2022-03-15"),
    (3, "Priya Singh", "priya@gmail.com", "Bangalore", "2022-05-20"),
    (4, "Neha Verma", "neha@gmail.com", "Chennai", "2022-07-25"),
    (5, "Rahul Das", "rahul@gmail.com", "Kolkata", "2022-09-12"),
    (6, "Anjali Mehta", "anjali@gmail.com", "Pune", "2022-11-05"),
    (7, "Vikas Gupta", "vikas@gmail.com", "Hyderabad", "2023-01-18"),
    (8, "Sneha Kapoor", "sneha@gmail.com", "Jaipur", "2023-02-22"),
    (9, "Arjun Nair", "arjun@gmail.com", "Kochi", "2023-03-10"),
    (10, "Karan Malhotra", "karan@gmail.com", "Delhi", "2023-04-01")
]

cursor.executemany("""
INSERT INTO customers VALUES (?, ?, ?, ?, ?)
""", customers)

# Products
products = [
    (1, "Laptop", "Electronics", 60000, 10),
    (2, "Phone", "Electronics", 20000, 5),   # low stock
    (3, "Headphones", "Electronics", 2000, 50),
    (4, "Shoes", "Fashion", 3000, 20),
    (5, "T-Shirt", "Fashion", 800, 100),
    (6, "Watch", "Accessories", 5000, 8),   # low stock
    (7, "Backpack", "Accessories", 1500, 25),
    (8, "Tablet", "Electronics", 25000, 7), # low stock
    (9, "Chair", "Furniture", 4000, 15),
    (10, "Desk", "Furniture", 7000, 12),
    (11, "Bottle", "Daily Use", 300, 60),
    (12, "Pen", "Stationery", 50, 200),
    (13, "Notebook", "Stationery", 120, 150),
    (14, "Camera", "Electronics", 45000, 3), # low stock
    (15, "Speaker", "Electronics", 3500, 9)  # low stock
]

cursor.executemany("""
INSERT INTO products VALUES (?, ?, ?, ?, ?)
""", products)

# ORDERS
orders = [
    (1, 1, "2023-05-01", "completed", 62000),
    (2, 2, "2023-05-02", "pending", 20000),
    (3, 3, "2023-05-03", "completed", 3000),
    (4, 4, "2023-05-04", "cancelled", 800),
    (5, 5, "2023-05-05", "completed", 5000),
    (6, 6, "2023-05-06", "completed", 25000),
    (7, 7, "2023-05-07", "pending", 4000),
    (8, 8, "2023-05-08", "completed", 7000),
    (9, 9, "2023-05-09", "completed", 1500),
    (10, 10, "2023-05-10", "cancelled", 300),
    (11, 1, "2023-05-11", "completed", 45000),
    (12, 2, "2023-05-12", "completed", 3500),
    (13, 3, "2023-05-13", "pending", 2000),
    (14, 4, "2023-05-14", "completed", 120),
    (15, 5, "2023-05-15", "completed", 1500),
    (16, 6, "2023-05-16", "pending", 800),
    (17, 7, "2023-05-17", "completed", 5000),
    (18, 8, "2023-05-18", "completed", 25000),
    (19, 9, "2023-05-19", "cancelled", 7000),
    (20, 10, "2023-05-20", "completed", 60000),
    (21, 1, "2023-05-21", "completed", 2000),
    (22, 2, "2023-05-22", "pending", 4000),
    (23, 3, "2023-05-23", "completed", 800),
    (24, 4, "2023-05-24", "completed", 1500),
    (25, 5, "2023-05-25", "completed", 3000)
]

cursor.executemany("""
INSERT INTO orders VALUES (?, ?, ?, ?, ?)
""", orders)

# ORDER ITEMS
order_items = [
    (1, 1, 1, 1, 60000),
    (2, 1, 3, 1, 2000),
    (3, 2, 2, 1, 20000),
    (4, 3, 4, 1, 3000),
    (5, 4, 5, 1, 800),
    (6, 5, 6, 1, 5000),
    (7, 6, 8, 1, 25000),
    (8, 7, 9, 1, 4000),
    (9, 8, 10, 1, 7000),
    (10, 9, 7, 1, 1500),
    (11, 10, 11, 1, 300),
    (12, 11, 14, 1, 45000),
    (13, 12, 15, 1, 3500),
    (14, 13, 3, 1, 2000),
    (15, 14, 13, 1, 120),
    (16, 15, 7, 1, 1500),
    (17, 16, 5, 1, 800),
    (18, 17, 6, 1, 5000),
    (19, 18, 8, 1, 25000),
    (20, 19, 10, 1, 7000),
    (21, 20, 1, 1, 60000),
    (22, 21, 3, 1, 2000),
    (23, 22, 9, 1, 4000),
    (24, 23, 5, 1, 800),
    (25, 24, 7, 1, 1500),
    (26, 25, 4, 1, 3000),
    (27, 5, 2, 1, 20000),
    (28, 6, 3, 1, 2000),
    (29, 7, 4, 1, 3000),
    (30, 8, 5, 1, 800),
    (31, 9, 6, 1, 5000),
    (32, 10, 7, 1, 1500),
    (33, 11, 8, 1, 25000),
    (34, 12, 9, 1, 4000),
    (35, 13, 10, 1, 7000),
    (36, 14, 11, 1, 300),
    (37, 15, 12, 1, 50),
    (38, 16, 13, 1, 120),
    (39, 17, 14, 1, 45000),
    (40, 18, 15, 1, 3500)
]

cursor.executemany("""
INSERT INTO order_items VALUES (?, ?, ?, ?, ?)
""", order_items)

conn.commit()
conn.close()
