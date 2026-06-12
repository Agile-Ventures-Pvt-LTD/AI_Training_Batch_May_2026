import sqlite3

DB_PATH = "data/ecommerce.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --------------------------------------------------
# CUSTOMERS (10)
# --------------------------------------------------

customers = [
    (1, "Rohan Mehta", "rohan@gmail.com", "Delhi", "2024-01-15"),
    (2, "Priya Sharma", "priya@gmail.com", "Mumbai", "2024-02-20"),
    (3, "Neha Gupta", "neha@gmail.com", "Delhi", "2024-03-10"),
    (4, "Arjun Singh", "arjun@gmail.com", "Bangalore", "2024-01-05"),
    (5, "Karan Verma", "karan@gmail.com", "Pune", "2024-04-02"),
    (6, "Sneha Kapoor", "sneha@gmail.com", "Jaipur", "2024-02-18"),
    (7, "Ananya Roy", "ananya@gmail.com", "Kolkata", "2024-03-25"),
    (8, "Rahul Khanna", "rahul@gmail.com", "Delhi", "2024-04-10"),
    (9, "Meera Joshi", "meera@gmail.com", "Mumbai", "2024-05-05"),
    (10, "Vikas Jain", "vikas@gmail.com", "Chandigarh", "2024-01-28")
]

cursor.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
    customers
)

# --------------------------------------------------
# PRODUCTS (15)
# --------------------------------------------------

products = [
    (1, "Laptop", "Electronics", 65000, 12),
    (2, "Wireless Mouse", "Electronics", 1200, 4),
    (3, "Keyboard", "Electronics", 1800, 15),
    (4, "Smartphone", "Electronics", 45000, 8),
    (5, "Coffee Mug", "Kitchen", 350, 8),
    (6, "Mixer Grinder", "Kitchen", 3200, 20),
    (7, "Yoga Mat", "Fitness", 900, 6),
    (8, "Dumbbells", "Fitness", 2500, 14),
    (9, "Running Shoes", "Fashion", 4000, 25),
    (10, "Backpack", "Fashion", 1500, 30),
    (11, "Office Chair", "Furniture", 7000, 9),
    (12, "Study Table", "Furniture", 9000, 11),
    (13, "Water Bottle", "Lifestyle", 500, 35),
    (14, "Bluetooth Speaker", "Electronics", 2800, 16),
    (15, "Headphones", "Electronics", 3500, 18)
]

cursor.executemany(
    "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
    products
)

# --------------------------------------------------
# ORDERS (25)
# --------------------------------------------------

orders = [
    (1,1,"2025-01-01","completed",66200),
    (2,2,"2025-01-03","completed",45000),
    (3,3,"2025-01-05","completed",7200),
    (4,4,"2025-01-06","pending",1500),
    (5,5,"2025-01-08","completed",3500),
    (6,1,"2025-01-10","completed",2800),
    (7,2,"2025-01-12","cancelled",4000),
    (8,3,"2025-01-15","completed",2500),
    (9,6,"2025-01-18","completed",3200),
    (10,7,"2025-01-20","pending",900),
    (11,8,"2025-01-21","completed",7000),
    (12,9,"2025-01-22","completed",1200),
    (13,10,"2025-01-24","completed",500),
    (14,1,"2025-01-26","completed",45000),
    (15,2,"2025-01-28","completed",9000),
    (16,3,"2025-02-01","completed",350),
    (17,4,"2025-02-03","cancelled",1800),
    (18,5,"2025-02-04","completed",2500),
    (19,6,"2025-02-06","completed",7000),
    (20,7,"2025-02-08","completed",4000),
    (21,8,"2025-02-10","completed",3200),
    (22,9,"2025-02-12","pending",2800),
    (23,10,"2025-02-15","completed",3500),
    (24,1,"2025-02-18","completed",1500),
    (25,2,"2025-02-20","completed",2500)
]

cursor.executemany(
    "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
    orders
)

# --------------------------------------------------
# ORDER ITEMS (40+)
# --------------------------------------------------

order_items = [
(1,1,1,1,65000),
(2,1,2,1,1200),
(3,2,4,1,45000),
(4,3,11,1,7000),
(5,3,5,1,200),
(6,4,10,1,1500),
(7,5,15,1,3500),
(8,6,14,1,2800),
(9,7,9,1,4000),
(10,8,8,1,2500),

(11,9,6,1,3200),
(12,10,7,1,900),
(13,11,11,1,7000),
(14,12,2,1,1200),
(15,13,13,1,500),
(16,14,4,1,45000),
(17,15,12,1,9000),
(18,16,5,1,350),
(19,17,3,1,1800),
(20,18,8,1,2500),

(21,19,11,1,7000),
(22,20,9,1,4000),
(23,21,6,1,3200),
(24,22,14,1,2800),
(25,23,15,1,3500),
(26,24,10,1,1500),
(27,25,8,1,2500),
(28,2,2,2,1200),
(29,5,13,2,500),
(30,8,7,2,900),

(31,11,15,2,3500),
(32,12,14,1,2800),
(33,13,5,2,350),
(34,18,13,3,500),
(35,20,10,2,1500),
(36,21,6,1,3200),
(37,22,2,2,1200),
(38,23,15,1,3500),
(39,24,13,3,500),
(40,25,8,1,2500)
]

cursor.executemany(
    "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
    order_items
)

conn.commit()
conn.close()

print("Database Seeded Successfully")