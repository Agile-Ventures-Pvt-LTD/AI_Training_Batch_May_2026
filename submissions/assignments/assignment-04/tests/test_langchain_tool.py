from src.tools.langchain_sql_tool import query_ecommerce_database

result = query_ecommerce_database.invoke(
    {
        "query": "SELECT * FROM customers"
    }
)

print(result)