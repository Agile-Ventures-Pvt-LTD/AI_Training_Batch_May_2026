import sqlite3

def get_connection():
    return sqlite3.connect("data/ecommerce.db")

SCHEMA_DESCRIPTION = """
Tables and columns:

customers(customer_id, name, email, city, signup_date)
products(product_id, name, category, price, stock_quantity)
orders(order_id, customer_id, order_date, status, total_amount)
  - status values: 'completed', 'pending', 'cancelled'
order_items(order_item_id, order_id, product_id, quantity, unit_price)
  - links orders to products; use JOIN with orders and products for full details
"""
