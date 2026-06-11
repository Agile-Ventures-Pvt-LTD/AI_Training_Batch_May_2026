from src.tools.ecommerce_sql_tool import query_ecommerce_database
def test_select_query():

    result = query_ecommerce_database.invoke(
        {
            "query": "SELECT * FROM customers LIMIT 1"
        }
    )

    assert "ERROR" not in result


def test_block_update():

    result = query_ecommerce_database.invoke(
        {
            "query": "UPDATE customers SET name='abc'"
        }
    )

    assert "ERROR" in result


def test_block_delete():

    result = query_ecommerce_database.invoke(
        {
            "query": "DELETE FROM customers"
        }
    )

    assert "ERROR" in result


def test_multiple_statements():

    result = query_ecommerce_database.invoke(
        {
            "query": "SELECT * FROM customers; DROP TABLE customers;"
        }
    )

    assert "ERROR" in result
