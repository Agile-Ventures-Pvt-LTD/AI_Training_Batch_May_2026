from src.tools.ecommerce_sql_tool import query_ecommerce_database

def test_select_query():

    result = query_ecommerce_database.invoke(
        {"query": "SELECT * FROM customers LIMIT 1"}
    )

    assert result is not None