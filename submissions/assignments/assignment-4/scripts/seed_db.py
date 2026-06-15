import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

customers = [
    ("Rahul Sharma", "rahul@gmail.com", "Delhi", "2023-01-15"),
    ("Priya Patel", "priya@gmail.com", "Mumbai", "2023-02-20"),
    ("Anil Kumar", "anil@gmail.com", "Bangalore", "2023-03-10"),
    ("Sneha Reddy", "sneha@gmail.com", "Chennai", "2023-04-05"),
    ("Vikram Singh", "vikram@gmail.com", "Jaipur", "2023-05-18"),
    ("Meera Nair", "meera@gmail.com", "Hyderabad", "2023-06-22"),
    ("Arjun Das", "arjun@gmail.com", "Kolkata", "2023-07-30"),
    ("Kavita Joshi", "kavita@gmail.com", "Pune", "2023-08-14"),
    ("Rohit Verma", "rohit@gmail.com", "Ahmedabad", "2023-09-09"),
    ("Lakshmi Iyer", "lakshmi@gmail.com", "Coimbatore", "2023-10-25"),
]
cursor.executemany(
    "INSERT INTO customers (name, email, city, signup_date) VALUES (?, ?, ?, ?)",
    customers
)
conn.commit()

products = [
    ("Samsung 65-inch 4K TV", "Electronics", 54999.0, 12),
    ("OnePlus Nord CE 3", "Electronics", 24999.0, 25),
    ("boAt Rockerz 450 Headphones", "Electronics", 1499.0, 5),
    ("Realme Watch 3 Pro", "Electronics", 5999.0, 8),
    ("HP Pavilion Laptop 15", "Electronics", 62999.0, 3),
    ("Decathlon Push-up Board", "Fitness", 799.0, 40),
    ("Boldfit Resistance Bands Set", "Fitness", 549.0, 55),
    ("Skullcandy Yoga Mat", "Fitness", 999.0, 30),
    ("Nivia Football", "Fitness", 699.0, 7),
    ("Whey Protein 2kg", "Fitness", 2499.0, 18),
    ("Prestige Induction Cooktop", "Kitchen", 2999.0, 14),
    ("Hawkins Pressure Cooker 3L", "Kitchen", 1299.0, 22),
    ("Pigeon Mixer Grinder", "Kitchen", 3499.0, 9),
    ("Peter England Formal Shirt", "Clothing", 1299.0, 50),
    ("Levi's 511 Slim Jeans", "Clothing", 2999.0, 35),
]
cursor.executemany(
    "INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)",
    products
)
conn.commit()

orders = [
    (1, "2024-01-10", "completed", 56498.0),
    (1, "2024-03-05", "completed", 1499.0),
    (2, "2024-01-20", "completed", 27998.0),
    (2, "2024-04-12", "cancelled", 5999.0),
    (3, "2024-02-01", "completed", 65998.0),
    (3, "2024-05-18", "pending", 2499.0),
    (4, "2024-02-14", "completed", 4298.0),
    (4, "2024-06-01", "completed", 1299.0),
    (5, "2024-03-03", "completed", 3498.0),
    (5, "2024-07-10", "pending", 62999.0),
    (6, "2024-03-22", "completed", 2998.0),
    (6, "2024-08-05", "cancelled", 24999.0),
    (7, "2024-04-07", "completed", 1848.0),
    (7, "2024-09-01", "completed", 3499.0),
    (8, "2024-04-19", "completed", 54999.0),
    (8, "2024-10-03", "pending", 799.0),
    (9, "2024-05-11", "completed", 5998.0),
    (9, "2024-11-12", "cancelled", 1299.0),
    (10, "2024-05-25", "completed", 2999.0),
    (10, "2024-12-01", "completed", 4798.0),
    (1, "2025-01-15", "completed", 2999.0),
    (3, "2025-02-10", "pending", 5999.0),
    (5, "2025-03-20", "completed", 1299.0),
    (7, "2025-04-05", "completed", 549.0),
    (9, "2025-05-18", "cancelled", 3499.0),
]
cursor.executemany(
    "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)",
    orders
)
conn.commit()

order_items = [
    (1, 1, 1, 54999.0), (1, 2, 1, 1499.0),
    (2, 3, 1, 1499.0), (2, 15, 1, 2999.0), (2, 14, 1, 1299.0), (2, 3, 1, 1499.0),
    (3, 2, 1, 24999.0), (3, 1, 1, 1499.0), (3, 4, 1, 5999.0),
    (4, 4, 1, 5999.0),
    (5, 5, 1, 62999.0), (5, 8, 3, 999.0),
    (6, 10, 1, 2499.0),
    (7, 6, 2, 799.0), (7, 7, 2, 549.0), (7, 8, 2, 999.0),
    (8, 14, 1, 1299.0),
    (9, 6, 1, 799.0), (9, 7, 2, 549.0), (9, 9, 1, 699.0),
    (10, 5, 1, 62999.0),
    (11, 11, 1, 2999.0),
    (12, 2, 1, 24999.0),
    (13, 7, 2, 549.0), (13, 9, 1, 699.0), (13, 8, 1, 999.0),
    (14, 13, 1, 3499.0),
    (15, 1, 1, 54999.0),
    (16, 6, 1, 799.0),
    (17, 4, 1, 5999.0), (17, 4, 1, 5999.0),
    (18, 14, 1, 1299.0),
    (19, 11, 1, 2999.0),
    (20, 12, 1, 1299.0), (20, 15, 1, 2999.0), (20, 6, 1, 799.0),
    (21, 15, 1, 2999.0),
    (22, 4, 1, 5999.0),
    (23, 14, 1, 1299.0),
    (24, 7, 1, 549.0),
    (25, 13, 1, 3499.0),
]
cursor.executemany(
    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
    order_items
)
conn.commit()
conn.close()
print("Database seeded successfully.")
