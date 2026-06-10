from src.tools.ecommerce_sql_tool import execute_query

query = """
DROP TABLE customers
"""

print(execute_query(query))