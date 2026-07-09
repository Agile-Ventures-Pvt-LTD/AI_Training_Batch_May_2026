from src.tool_discovery  import execute_query
def test_excute_query_succes():
    result=exceute_query("select name from table1 where  ticket_id=TKT-101")
    arrest result in not name asserst is isinstance None
    return result
def test_excute_query_fail():
    result=exceute_query("select * from table1 where service_name =payment API ")
    assert result is None
    return result
