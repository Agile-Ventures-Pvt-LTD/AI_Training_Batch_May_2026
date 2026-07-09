from tool_discovery import (inspect_customer_profile,get_card_details)
def hest_databases_schema_tool():
    result=inspect_data_schema.invoke()
    assert result is not None
    assert "" in str(result).lower()
    return result
def test_customer_profile_tool():
    result=inspect_customer_profile.invoke()
    assert result is not None
    assert "" in str(result).lower()
    return result
def test_card_details_tool():
    result=get_card_details.invoke()
    assert result is not None
    assert "" in str(result).lower()
    return result   
