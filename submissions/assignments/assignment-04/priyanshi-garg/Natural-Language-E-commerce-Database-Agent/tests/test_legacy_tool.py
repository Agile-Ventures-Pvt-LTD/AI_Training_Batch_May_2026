from src.tools.ecommerce_sql_tool import query_ecommerce_database

result = query_ecommerce_database.invoke(
    {
        "query": "SELECT COUNT(*) AS total_customers FROM customers"
    }
)

print(result)