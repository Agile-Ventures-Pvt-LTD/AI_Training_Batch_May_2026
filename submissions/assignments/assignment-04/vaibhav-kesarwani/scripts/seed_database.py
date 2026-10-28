import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# ------------------
# Customers
# ------------------

customers = [
    ("Rahul Sharma","rahul@gmail.com","Delhi","2024-01-10"),
    ("Priya Singh","priya@gmail.com","Mumbai","2024-02-15"),
    ("Amit Kumar","amit@gmail.com","Bangalore","2024-03-20"),
    ("Neha Verma","neha@gmail.com","Pune","2024-04-01"),
    ("Rohan Patel","rohan@gmail.com","Ahmedabad","2024-01-25"),
    ("Anjali Gupta","anjali@gmail.com","Jaipur","2024-02-08"),
    ("Karan Mehta","karan@gmail.com","Chandigarh","2024-03-05"),
    ("Sneha Joshi","sneha@gmail.com","Lucknow","2024-01-12"),
    ("Vikram Rao","vikram@gmail.com","Hyderabad","2024-04-12"),
    ("Meera Nair","meera@gmail.com","Kochi","2024-05-01")
]

cursor.executemany("""
INSERT INTO customers (name, email, city, signup_date)
VALUES (?, ?, ?, ?)
""", customers)

# ------------------
# Products
# ------------------

products = [
    ("Laptop","Electronics",65000,10),
    ("Smartphone","Electronics",25000,5),
    ("Headphones","Electronics",3000,25),
    ("Keyboard","Electronics",1500,4),
    ("Mouse","Electronics",800,2),
    ("Office Chair","Furniture",7000,8),
    ("Desk","Furniture",12000,6),
    ("Water Bottle","Home",500,30),
    ("Coffee Maker","Home",3500,7),
    ("Backpack","Accessories",1500,15),
    ("Running Shoes","Fashion",4500,12),
    ("T-Shirt","Fashion",700,50),
    ("Notebook","Stationery",120,100),
    ("Pen Set","Stationery",250,80),
    ("Monitor","Electronics",12000,3)
]

cursor.executemany("""
INSERT INTO products (name, category, price, stock_quantity)
VALUES (?, ?, ?, ?)
""", products)

# ------------------
# Orders (25)
# ------------------

orders = [
    (1,"2024-06-01","completed",71000),
    (1,"2024-06-15","completed",3000),
    (2,"2024-06-02","pending",25000),
    (2,"2024-06-10","completed",26500),
    (3,"2024-06-03","completed",12000),
    (3,"2024-06-11","cancelled",1500),
    (4,"2024-06-04","completed",7000),
    (4,"2024-06-12","pending",3500),
    (5,"2024-06-05","completed",4500),
    (5,"2024-06-13","completed",700),
    (6,"2024-06-06","completed",65000),
    (6,"2024-06-14","pending",500),
    (7,"2024-06-07","completed",12000),
    (7,"2024-06-15","completed",1500),
    (8,"2024-06-08","cancelled",3000),
    (8,"2024-06-16","completed",250),
    (9,"2024-06-09","completed",7000),
    (9,"2024-06-17","pending",4500),
    (10,"2024-06-10","completed",120),
    (10,"2024-06-18","completed",800),
    (1,"2024-06-19","completed",3500),
    (2,"2024-06-20","completed",12000),
    (3,"2024-06-21","pending",7000),
    (4,"2024-06-22","completed",1500),
    (5,"2024-06-23","completed",4500)
]

cursor.executemany("""
INSERT INTO orders (customer_id, order_date, status, total_amount)
VALUES (?, ?, ?, ?)
""", orders)

# ------------------
# Order Items (43)
# ------------------

order_items = [
    (1,1,1,65000),
    (1,3,2,3000),

    (2,3,1,3000),

    (3,2,1,25000),

    (4,2,1,25000),
    (4,4,1,1500),

    (5,15,1,12000),

    (6,4,1,1500),

    (7,6,1,7000),

    (8,9,1,3500),

    (9,11,1,4500),

    (10,12,1,700),

    (11,1,1,65000),

    (12,8,1,500),

    (13,15,1,12000),

    (14,10,1,1500),

    (15,3,1,3000),

    (16,14,1,250),

    (17,6,1,7000),

    (18,11,1,4500),

    (19,13,1,120),

    (20,5,1,800),

    (21,9,1,3500),

    (22,15,1,12000),

    (23,6,1,7000),

    (24,10,1,1500),

    (25,11,1,4500),

    (1,5,1,800),
    (2,8,2,500),
    (3,10,1,1500),
    (4,13,3,120),
    (5,14,2,250),
    (6,3,1,3000),
    (7,7,1,12000),
    (8,12,2,700),
    (9,4,1,1500),
    (10,9,1,3500),
    (11,2,1,25000),
    (12,5,1,800),
    (13,8,2,500),
    (14,3,1,3000),
    (15,10,1,1500)
]

cursor.executemany("""
INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    unit_price
)
VALUES (?, ?, ?, ?)
""", order_items)

conn.commit()
conn.close()

print("Database seeded successfully!")