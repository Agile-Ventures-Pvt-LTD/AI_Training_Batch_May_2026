from src.tools.ecommerce_sql_tool import execute_query

query = """
SELECT *
FROM customers
"""

result = execute_query(query)

print(result)