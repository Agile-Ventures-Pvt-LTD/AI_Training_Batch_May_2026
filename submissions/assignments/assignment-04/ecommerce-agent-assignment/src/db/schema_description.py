"""
schema_description.py

Purpose
-------
Provides schema information to the LLM.

The agent uses this information to:
- Understand available tables
- Understand available columns
- Generate correct SQL
- Perform joins correctly
"""


SCHEMA_DESCRIPTION = """
DATABASE NAME:
ecommerce.db

TABLE: customers

Purpose:
Stores customer information.

Columns:

customer_id
    Unique customer identifier
    INTEGER PRIMARY KEY

name
    Customer full name

email
    Customer email address

city
    Customer city

signup_date
    Date customer registered

    
TABLE: products

Purpose:
Stores product catalog information.

Columns:

product_id
    Unique product identifier

name
    Product name

category
    Product category

price
    Product price

stock_quantity
    Current inventory quantity


TABLE: orders

Purpose:
Stores customer orders.

Columns:

order_id
    Unique order identifier

customer_id
    Customer who placed order

order_date
    Date of order

status
    Order status

Possible values:
    completed
    pending
    cancelled

total_amount
    Total order value


TABLE: order_items

Purpose:
Stores products contained in each order.

Columns:

order_item_id
    Unique row identifier

order_id
    Related order

product_id
    Related product

quantity
    Quantity purchased

unit_price
    Product price at purchase time


TABLE RELATIONSHIPS

customers.customer_id
    ->
orders.customer_id

orders.order_id
    ->
order_items.order_id

products.product_id
    ->
order_items.product_id


COMMON BUSINESS QUESTIONS

Revenue:
    Use orders.total_amount

Completed Revenue:
    Filter status='completed'

Top Customers:
    Join customers and orders

Top Products:
    Join products and order_items

Low Stock Products:
    Use products.stock_quantity

Category Revenue:
    Join products and order_items

Average Order Value:
    AVG(orders.total_amount)

Customer Orders:
    COUNT(order_id)

Monthly Revenue:
    GROUP BY month(order_date)

Cancelled Orders:
    status='cancelled'

Pending Orders:
    status='pending'


IMPORTANT RULES

1. Only generate SELECT queries.

2. Never generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   TRUNCATE
   CREATE

3. Use JOINs when data exists across tables.

4. Do not invent columns.

5. Do not invent tables.

6. If information cannot be derived from
   the database, say so.

7. Prefer concise and efficient SQL.
"""