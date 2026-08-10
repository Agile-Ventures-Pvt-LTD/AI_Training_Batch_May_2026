import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools import (
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary,
    get_notification_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon,
    get_top_customers_by_due,
    get_transaction_type_summary,
)


def test_inspect_database_schema():
    result = inspect_database_schema.invoke({})
    assert "tables" in result
    assert "schema" in result
    assert "customer" in result["tables"]
    assert "transaction" in result["tables"]
    assert "card" in result["tables"]


def test_get_customer_profile_by_id():
    result = get_customer_profile.invoke({"search_value": "1"})
    assert result["found"] is True
    assert "Denise" in result["customer"]["name"]
    assert "Walker" in result["customer"]["name"]
    assert "****@" in result["customer"]["email"]


def test_get_customer_profile_cust_format():
    result = get_customer_profile.invoke({"search_value": "CUST-1"})
    assert result["found"] is True
    assert "Denise" in result["customer"]["name"]


def test_get_customer_profile_by_name():
    result = get_customer_profile.invoke({"search_value": "Howard"})
    assert result["found"] is True
    assert "Howard" in result["customer"]["name"]


def test_get_customer_profile_not_found():
    result = get_customer_profile.invoke({"search_value": "99999999"})
    assert result["found"] is False


def test_get_customer_profile_email_masked():
    result = get_customer_profile.invoke({"search_value": "1"})
    email = result["customer"]["email"]
    assert "****@" in email
    assert "denisewalker717@gmail.com" not in email


def test_get_card_details_found():
    result = get_card_details.invoke({"customer_id": "1"})
    assert result["found"] is True
    assert len(result["cards"]) >= 1
    card = result["cards"][0]
    assert card["card_number"].startswith("**** **** ****")
    assert "card_type" in card
    assert "card_network" in card


def test_get_card_details_not_found():
    result = get_card_details.invoke({"customer_id": "99999999"})
    assert result["found"] is False


def test_get_card_details_cust_format():
    result = get_card_details.invoke({"customer_id": "CUST-2"})
    assert result["found"] is True


def test_search_transactions_basic():
    result = search_transactions.invoke({"customer_id": "1", "limit": 5})
    assert result["count"] <= 5
    assert len(result["transactions"]) <= 5


def test_search_transactions_by_merchant():
    result = search_transactions.invoke({"merchant_name": "Kroger", "limit": 5})
    for txn in result["transactions"]:
        assert "Kroger" in (txn["merchant"] or "")


def test_search_transactions_by_type():
    result = search_transactions.invoke({"transaction_type": "Debit", "limit": 5})
    for txn in result["transactions"]:
        assert txn["transaction_type"] == "Debit"


def test_search_transactions_amount_range():
    result = search_transactions.invoke({"min_amount": 10.0, "max_amount": 50.0, "limit": 10})
    for txn in result["transactions"]:
        assert 10.0 <= txn["amount"] <= 50.0


def test_search_transactions_by_merchant_type():
    result = search_transactions.invoke({"merchant_type": "supermarket", "limit": 5})
    assert result["count"] >= 0


def test_get_customer_transactions():
    result = get_customer_transactions.invoke({"customer_id": "1", "limit": 5})
    assert result["transaction_count"] <= 5
    assert result["customer_id"] == "1"


def test_get_statement_summary():
    result = get_statement_summary.invoke({"customer_id": "1"})
    assert "total_amount_due" in result
    assert "min_amount_due" in result
    assert "risk_level" in result
    assert result["risk_level"] in ("LOW", "MEDIUM", "HIGH")
    assert result["total_amount_due"] > 0
    assert result["min_amount_due"] <= result["total_amount_due"]


def test_get_statement_summary_invalid():
    result = get_statement_summary.invoke({"customer_id": "99999999"})
    assert result["total_amount_due"] == 0


def test_get_rewards_summary():
    result = get_rewards_summary.invoke({"customer_id": "1"})
    assert "reward_points" in result
    assert "related_transactions" in result
    assert result["reward_points"] >= 0


def test_get_rewards_summary_points_calculation():
    result = get_rewards_summary.invoke({"customer_id": "1"})
    for txn in result["related_transactions"]:
        expected = int(txn["amount"] // 100)
        assert txn["earned_points"] == expected


def test_get_merchant_spend_summary_by_type():
    result = get_merchant_spend_summary.invoke({"group_by": "merchant_type"})
    assert "results" in result
    assert len(result["results"]) > 0
    assert "merchant_type" in result["results"][0]
    assert "total_spend" in result["results"][0]


def test_get_merchant_spend_summary_by_merchant():
    result = get_merchant_spend_summary.invoke({"group_by": "merchant"})
    assert "results" in result
    assert len(result["results"]) > 0
    assert "merchant" in result["results"][0]


def test_get_notification_summary():
    result = get_notification_summary.invoke({})
    assert result["status"] == "unavailable"


def test_detect_suspicious_transactions():
    result = detect_suspicious_transactions.invoke({"limit": 10})
    assert "rules_applied" in result
    assert "flagged_transactions" in result
    assert len(result["rules_applied"]) == 3


def test_get_cards_expiring_soon():
    result = get_cards_expiring_soon.invoke({"days": 365, "limit": 10})
    assert "expiring_cards" in result
    assert "count" in result
    for card in result["expiring_cards"]:
        assert card["card_number"].startswith("**** **** ****")


def test_get_top_customers_by_due():
    result = get_top_customers_by_due.invoke({"limit": 5})
    assert "top_customers" in result
    assert len(result["top_customers"]) <= 5
    amounts = [c["total_due"] for c in result["top_customers"]]
    assert amounts == sorted(amounts, reverse=True)


def test_get_transaction_type_summary():
    result = get_transaction_type_summary.invoke({})
    assert "summary" in result
    types = {r["transaction_type"] for r in result["summary"]}
    assert "Debit" in types
    assert "Credit" in types


if __name__ == "__main__":
    tests = [
        test_inspect_database_schema,
        test_get_customer_profile_by_id,
        test_get_customer_profile_cust_format,
        test_get_customer_profile_by_name,
        test_get_customer_profile_not_found,
        test_get_customer_profile_email_masked,
        test_get_card_details_found,
        test_get_card_details_not_found,
        test_get_card_details_cust_format,
        test_search_transactions_basic,
        test_search_transactions_by_merchant,
        test_search_transactions_by_type,
        test_search_transactions_amount_range,
        test_search_transactions_by_merchant_type,
        test_get_customer_transactions,
        test_get_statement_summary,
        test_get_statement_summary_invalid,
        test_get_rewards_summary,
        test_get_rewards_summary_points_calculation,
        test_get_merchant_spend_summary_by_type,
        test_get_merchant_spend_summary_by_merchant,
        test_get_notification_summary,
        test_detect_suspicious_transactions,
        test_get_cards_expiring_soon,
        test_get_top_customers_by_due,
        test_get_transaction_type_summary,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {test.__name__}  ->  {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
