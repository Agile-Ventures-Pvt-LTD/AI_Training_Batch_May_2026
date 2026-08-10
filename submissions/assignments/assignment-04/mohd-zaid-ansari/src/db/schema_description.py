# Schema of the Database.

SCHEMA_DESCRIPTION = """
Tables available in the database:

customers
- customer_id (PK)
- customer_unique_id
- customer_city
- customer_state

orders
- order_id (PK)
- customer_id (FK -> customers.customer_id)
- order_status
- order_purchase_timestamp
- order_delivered_customer_date

order_items
- order_id (FK -> orders.order_id)
- product_id (FK -> products.product_id)
- seller_id (FK -> sellers.seller_id)
- price
- freight_value

products
- product_id (PK)
- product_category_name
- product_weight_g

order_payments
- order_id (FK -> orders.order_id)
- payment_type
- payment_installments
- payment_value

order_reviews
- review_id
- order_id (FK -> orders.order_id)
- review_score

sellers
- seller_id (PK)
- seller_city
- seller_state

product_category_name_translation
- product_category_name
- product_category_name_english

Important Relationships:

customers.customer_id = orders.customer_id

orders.order_id = order_items.order_id

orders.order_id = order_payments.order_id

orders.order_id = order_reviews.order_id

products.product_id = order_items.product_id

sellers.seller_id = order_items.seller_id

products.product_category_name =
product_category_name_translation.product_category_name
"""