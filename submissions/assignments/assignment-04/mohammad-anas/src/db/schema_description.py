SCHEMA_INFO = """
The database has the following tables:
1. customers (customer_id, name, email, city, signup_date)
2. products (product_id, name, category, price, stock_quantity)
3. orders (order_id, customer_id, order_date, status, total_amount)
4. order_items (order_item_id, order_id, product_id, quantity, unit_price)
"""