SCHEMA_DESCRIPTION = """
Database: ecommerce.db

Table: customers
--------------------------------
customer_id INTEGER PRIMARY KEY
name TEXT
email TEXT
city TEXT
signup_date TEXT

Table: products
--------------------------------
product_id INTEGER PRIMARY KEY
name TEXT
category TEXT
price REAL
stock_quantity INTEGER

Table: orders
--------------------------------
order_id INTEGER PRIMARY KEY
customer_id INTEGER
order_date TEXT
status TEXT
total_amount REAL

Table: order_items
--------------------------------
order_item_id INTEGER PRIMARY KEY
order_id INTEGER
product_id INTEGER
quantity INTEGER
unit_price REAL

Relationships:
--------------------------------
customers.customer_id -> orders.customer_id

orders.order_id -> order_items.order_id

products.product_id -> order_items.product_id
"""