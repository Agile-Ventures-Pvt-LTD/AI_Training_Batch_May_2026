
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import *


def test_inspect_database_schema():
    result = inspect_database_schema.invoke({})
    assert "tables" in result
    assert "schema" in result
    assert len(result["tables"]) > 0
    assert "customer" in result["tables"]
    assert "card" in result["tables"]
    assert "transaction" in result["tables"]
    print("PASS: inspect_database_schema")


def test_get_customer_profile_found():
    result = get_customer_profile.invoke({"cust_id": "1"})
    assert result["found"] is True
    assert result["customer"]["cust_id"] == 1
    assert "name" in result["customer"]
    assert "email" in result["customer"]
    assert "phone" in result["customer"]
    print("PASS: get_customer_profile (found)")


def test_get_customer_profile_not_found():
    result = get_customer_profile.invoke({"cust_id": "99999"})
    assert result["found"] is False
    assert result["customer"] is None
    print("PASS: get_customer_profile (not found)")


def test_get_customer_profile_by_name():
    result = get_customer_profile.invoke({"name": "Denise"})
    assert result["found"] is True
    print("PASS: get_customer_profile (by name)")


def test_get_card_details():
    result = get_card_details.invoke({"cust_id": "1"})
    assert result["found"] is True
    assert "cards" in result
    for card in result["cards"]:
        assert "****" in card["card_number"]
        assert card["card_number"].startswith("****")
    print("PASS: get_card_details (masked numbers)")


def test_search_transactions():
    result = search_transactions.invoke({"cust_id": "1", "limit": 5})
    assert "count" in result
    assert "transactions" in result
    assert len(result["transactions"]) <= 5
    if result["count"] > 0:
        assert "card" in result["transactions"][0]
        assert "****" in result["transactions"][0]["card"]
    print("PASS: search_transactions")


def test_get_customer_transactions():
    result = get_customer_transactions.invoke({"cust_id": "1", "limit": 5})
    assert "transactions" in result
    if result["count"] > 0:
        assert "card_id" in result["transactions"][0]
    print("PASS: get_customer_transactions")


def test_get_statement_summary():
    result = get_statement_summary.invoke({"cust_id": "1"})
    assert "total_amount_due" in result
    assert "min_amount_due" in result
    assert "risk_level" in result
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    print("PASS: get_statement_summary")


def test_get_rewards_summary():
    result = get_rewards_summary.invoke({"cust_id": "1"})
    assert "reward_points" in result
    assert "customer_id" in result
    print("PASS: get_rewards_summary")


def test_get_merchant_spend_summary():
    result = get_merchant_spend_summary.invoke({})
    assert "results" in result
    if len(result["results"]) > 0:
        assert "merchant_type" in result["results"][0]
        assert "total_spend" in result["results"][0]
    print("PASS: get_merchant_spend_summary")


def test_detect_suspicious_transactions():
    result = detect_suspicious_transactions.invoke({"cust_id": "1"})
    assert "suspicious_count" in result
    assert "transactions" in result
    print("PASS: detect_suspicious_transactions")


def test_get_notification_summary():
    result = get_notification_summary.invoke({})
    assert "count" in result
    assert "notifications" in result
    print("PASS: get_notification_summary")


def test_get_cards_expiring_soon():
    result = get_cards_expiring_soon.invoke({"days": 36500})
    assert "days" in result
    assert "count" in result
    assert "cards_expiring" in result
    print("PASS: get_cards_expiring_soon")


def test_get_top_customers_by_due():
    result = get_top_customers_by_due.invoke({"limit": 10})
    assert "count" in result
    assert "top_customers" in result
    print("PASS: get_top_customers_by_due")


def test_get_transaction_type_summary():
    result = get_transaction_type_summary.invoke({})
    assert "results" in result
    print("PASS: get_transaction_type_summary")


def test_masking():
    """Verify sensitive data is masked in customer profile."""
    result = get_customer_profile.invoke({"cust_id": "1"})
    email = result["customer"]["email"]
    assert "***" in email or email is None, f"Email should be masked but got: {email}"
    phone = result["customer"]["phone"]
    assert "****" in phone or phone is None, f"Phone should be masked but got: {phone}"
    print("PASS: Sensitive data masking")


def test_card_number_masked():
    """Verify card numbers are masked in card details."""
    result = get_card_details.invoke({"cust_id": "1"})
    for card in result["cards"]:
        parts = card["card_number"].split()
        assert parts[0] == "****"
        assert parts[1] == "****"
        assert parts[2] == "****"
        assert len(parts[3]) == 4
    print("PASS: Card numbers properly masked")


if __name__ == "__main__":
    test_inspect_database_schema()
    test_get_customer_profile_found()
    test_get_customer_profile_not_found()
    test_get_customer_profile_by_name()
    test_get_card_details()
    test_search_transactions()
    test_get_customer_transactions()
    test_get_statement_summary()
    test_get_rewards_summary()
    test_get_merchant_spend_summary()
    test_detect_suspicious_transactions()
    test_get_notification_summary()
    test_get_cards_expiring_soon()
    test_get_top_customers_by_due()
    test_get_transaction_type_summary()
    test_masking()
    test_card_number_masked()
    print("\n=== ALL TESTS PASSED ===")