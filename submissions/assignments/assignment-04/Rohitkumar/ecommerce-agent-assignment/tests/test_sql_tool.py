from src.tools.ecommerce_sql_tool import query_ecommerce_database

def test_select():
    result = query_ecommerce_database("SELECT * FROM customers")
    assert isinstance(result, list)