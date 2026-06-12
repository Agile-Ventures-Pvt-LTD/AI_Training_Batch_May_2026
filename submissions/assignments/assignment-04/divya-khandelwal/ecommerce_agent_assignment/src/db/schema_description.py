SCHEMA_DESCRIPTION = """
DATABASE NAME: ecommerce.db

TABLE: customers

customer_id INTEGER PRIMARY KEY
name TEXT
email TEXT
city TEXT
signup_date TEXT


TABLE: products

product_id INTEGER PRIMARY KEY
name TEXT
category TEXT
price REAL
stock_quantity INTEGER


TABLE: orders

order_id INTEGER PRIMARY KEY
customer_id INTEGER
order_date TEXT
status TEXT
total_amount REAL


TABLE: order_items

order_item_id INTEGER PRIMARY KEY
order_id INTEGER
product_id INTEGER
quantity INTEGER
unit_price REAL


RELATIONSHIPS

customers.customer_id = orders.customer_id

orders.order_id = order_items.order_id

products.product_id = order_items.product_id


IMPORTANT RULES

- Only generate SELECT queries.
- Never generate INSERT queries.
- Never generate UPDATE queries.
- Never generate DELETE queries.
- Never generate DROP queries.
- Never generate ALTER queries.
- Never generate CREATE queries.
- Never generate TRUNCATE queries.

Common statuses:
completed
pending
cancelled
"""