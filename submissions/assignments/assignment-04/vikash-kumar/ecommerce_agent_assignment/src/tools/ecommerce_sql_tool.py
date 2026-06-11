import json

from langchain.tools import tool

from src.db.connection import get_connection


@tool
def query_ecommerce_database(sql_query: str) -> str:
    """
    Query the ecommerce SQLite database.

    SCHEMA

    customers
    ---------
    customer_id
    name
    email
    city
    signup_date

    products
    --------
    product_id
    name
    category
    price
    stock_quantity

    orders
    ------
    order_id
    customer_id
    order_date
    status
    total_amount

    order_items
    -----------
    order_item_id
    order_id
    product_id
    quantity
    unit_price

    RELATIONSHIPS

    orders.customer_id -> customers.customer_id

    order_items.order_id -> orders.order_id

    order_items.product_id -> products.product_id

    IMPORTANT RULES

    - Only SELECT queries are allowed.
    - Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
      REPLACE, TRUNCATE or PRAGMA.
    - Use order_items.unit_price when calculating sales.
    - products.price is the current catalog price.
    - order_items.unit_price is the purchase-time price.
    - Always use proper JOINs when combining tables.
    """

    sql_query = sql_query.strip()

    if not sql_query.lower().startswith("select"):
        return (
            "Only SELECT queries are allowed. "
            "INSERT, UPDATE, DELETE, DROP, ALTER, CREATE and PRAGMA are forbidden."
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql_query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        results = []

        for row in rows:
            results.append(dict(zip(columns, row)))

        conn.close()

        return json.dumps(results, indent=4)

    except Exception as e:
        return f"Database Error: {str(e)}"