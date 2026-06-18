# test_tools.py

from tools import (
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary
)

def test_inspect_database_schema():
    result = inspect_database_schema.invoke("")
    assert isinstance(result, dict)

def test_customer_profile_valid():
    result = get_customer_profile.invoke("CUST-1001")
    assert isinstance(result, dict)

def test_customer_profile_invalid():
    result = get_customer_profile.invoke("INVALID")
    assert isinstance(result, dict)

def test_card_details():
    result = get_card_details.invoke("CUST-1001")
    assert isinstance(result, dict)

def test_search_transactions():
    result = search_transactions.invoke({
        "cust_id": "CUST-1001",
        "limit": 5
    })
    assert isinstance(result, dict)

def test_customer_transactions():
    result = get_customer_transactions.invoke({
        "cust_id": "CUST-1001",
        "limit": 5
    })
    assert isinstance(result, dict)

def test_statement_summary():
    result = get_statement_summary.invoke("CUST-1001")
    assert isinstance(result, dict)

def test_rewards_summary():
    result = get_rewards_summary.invoke("CUST-1001")
    assert isinstance(result, dict)

def test_merchant_spend_summary():
    result = get_merchant_spend_summary.invoke(5)
    assert isinstance(result, dict)