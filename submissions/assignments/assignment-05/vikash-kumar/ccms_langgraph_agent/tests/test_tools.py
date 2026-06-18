from pprint import pprint

from tools import (inspect_database_schema,get_customer_profile,get_card_details,search_transactions,get_customer_transactions,get_statement_summary,get_rewards_summary,get_merchant_spend_summary,detect_suspicious_transactions)


def test_inspect_database_schema():
    result = inspect_database_schema()
    pprint(result)


def test_get_customer_profile():
    result = get_customer_profile(2)
    pprint(result)


def test_get_card_details():
    result = get_card_details(2)
    pprint(result)


def test_search_transactions():
    result = search_transactions(min_amount=1000,max_amount=50000,limit=5)
    pprint(result)


def test_get_customer_transactions():
    result = get_customer_transactions(cust_id=6,limit=10)
    pprint(result)


def test_get_statement_summary():
    result = get_statement_summary(6)
    pprint(result)


def test_get_rewards_summary():
    result = get_rewards_summary(6)
    pprint(result)


def test_get_merchant_spend_summary():
    result = get_merchant_spend_summary()
    pprint(result)


def test_detect_suspicious_transactions():
    result = detect_suspicious_transactions()
    pprint(result)


if __name__ == "__main__":
    test_inspect_database_schema()
    test_get_customer_profile()
    test_get_card_details()
    test_search_transactions()
    test_get_customer_transactions()
    test_get_statement_summary()
    test_get_rewards_summary()
    test_get_merchant_spend_summary()
    test_detect_suspicious_transactions()

    print("\nAll the tools are checked successfully.")