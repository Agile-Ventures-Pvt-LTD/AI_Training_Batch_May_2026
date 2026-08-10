SCHEMA = """
You are working with an SQLite ecommerce database.

IMPORTANT RULES:
- Use ONLY the tables and columns listed below
- Do NOT assume any other tables
- Do NOT invent column names

Tables:

customers(
    customer_id,
    name,
    email,
    city,
    signup_date
)

products(
    product_id,
    name,
    category,
    price,
    stock_quantity
)

orders(
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
)

order_items(
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price
)
"""