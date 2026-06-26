from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

query = """
SELECT *
FROM customers
LIMIT 5
"""

result = query_ecommerce_database.invoke(
    {"query": query}
)

print(result)