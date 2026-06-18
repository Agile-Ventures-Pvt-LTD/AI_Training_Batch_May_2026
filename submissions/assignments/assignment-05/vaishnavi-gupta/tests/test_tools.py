from tools import (
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    get_customer_transactions,
    get_merchant_spend_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon,
    get_statement_summary, 
    get_rewards_summary
)


def test_schema():

    result = inspect_database_schema.invoke({})

    assert "tables" in result


def test_customer_profile():

    result = get_customer_profile.invoke(
        {
            "customer_id": "cust_id: 1"
        }
    )

    assert isinstance(result, dict)


def test_card_details():

    result = get_card_details.invoke(
        {
            "customer_id": "cust_id: 1"
        }
    )

    assert isinstance(result, dict)


def test_transactions():

    result = get_customer_transactions.invoke(
        {
            "customer_id": "cust_id: 1",
            "limit": 5
        }
    )

    assert isinstance(result, dict)



def test_merchant_summary():

    result = get_merchant_spend_summary.invoke({})

    assert isinstance(result, dict)


def test_suspicious_transactions():

    result = detect_suspicious_transactions.invoke({})

    assert isinstance(result, dict)


def test_expiring_cards():

    result = get_cards_expiring_soon.invoke({})

    assert isinstance(result, dict)

def get_summary():

    result = get_statement_summary.invoke({})

    assert isinstance(result, dict)    


def get_rewards():

    result = get_rewards_summary.invoke({})

    assert isinstance(result, dict)    