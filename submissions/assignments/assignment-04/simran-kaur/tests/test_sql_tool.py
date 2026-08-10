from src.tools.ecommerce_sql_tool import (
    execute_sql
)


def test_select_query():

    result = execute_sql.invoke(
        {
            "query":
            "SELECT COUNT(*) FROM customers"
        }
    )

    assert result is not None


def test_unsafe_query():

    result = execute_sql.invoke(
        {
            "query":
            "DROP TABLE customers"
        }
    )

    assert (
        "Only SELECT queries"
        in result
        or
        "Unsafe SQL"
        in result
    )
    print(result)

# run ```pytest tests/test_agent_queries.py``` to execute
# run ```pytest tests/test_agent_queries.py -v -s``` to execute with verbose output