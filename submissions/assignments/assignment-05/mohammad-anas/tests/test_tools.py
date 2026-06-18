import json
import pytest
from tools import get_inspect_schema,get_customer_profile,get_card_details,get_customer_transactions,get_merchant_spend_summary,detect_suspicious_transactions



def test_schema_returns_tables():

    result = json.loads(get_inspect_schema())

    assert "tables" in result
    assert "schema" in result
    assert len(result["tables"]) > 0


def test_schema_contains_customer_table():

    result = json.loads(get_inspect_schema())

    assert "customer" in result["tables"]



def test_customer_profile_found():

    result = json.loads(
        get_customer_profile(customer_id=1)
    )

    assert result["cust_id"] == 1


def test_customer_email_masked():

    result = json.loads(
        get_customer_profile(customer_id=1)
    )

    assert "***@" in result["email"]


def test_customer_phone_masked():

    result = json.loads(
        get_customer_profile(customer_id=1)
    )

    assert result["phone"].startswith("******")


def test_customer_not_found():

    result = get_customer_profile(
        customer_id=999999
    )

    assert result == "Customer not found"




def test_card_details_found():

    result = json.loads(
        get_card_details(customer_id=1)
    )

    assert "card_number" in result


def test_card_number_masked():

    result = json.loads(
        get_card_details(customer_id=1)
    )

    assert result["card_number"].startswith(
        "**** **** ****"
    )



def test_customer_transactions_return_data():

    result = json.loads(
        get_customer_transactions(1)
    )

    assert result["customer_id"] == 1
    assert result["transaction_count"] >= 0


def test_customer_transactions_has_list():

    result = json.loads(
        get_customer_transactions(1)
    )

    assert isinstance(
        result["transactions"],
        list
    )




def test_merchant_summary_structure():

    result = json.loads(
        get_merchant_spend_summary()
    )

    assert "results" in result


def test_merchant_summary_not_empty():

    result = json.loads(
        get_merchant_spend_summary()
    )

    assert len(result["results"]) > 0




def test_suspicious_transaction_structure():

    result = json.loads(
        detect_suspicious_transactions()
    )

    assert "rule_applied" in result
    assert "flagged_transactions" in result


def test_suspicious_rule_correct():

    result = json.loads(
        detect_suspicious_transactions()
    )

    assert result["rule_applied"] == "amount > 75000"



def test_all_tools_execute():

    assert get_inspect_schema() is not None
    assert get_customer_profile(customer_id=1) is not None
    assert get_card_details(customer_id=1) is not None
    assert get_customer_transactions(1) is not None
    assert get_merchant_spend_summary() is not None
    assert detect_suspicious_transactions() is not None

