from tools.sql_tool import query_database
def test_valid_select_query():

    result = query_database.invoke(
        {
            "query": "SELECT COUNT(*) AS total_orders FROM orders"
        }
    )
    assert "rows" in result
