import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, ROOT_DIR)

from tools import (
    inspect_database_schema,
    get_customer_profile,
    find_customer_by_name,
    get_card_details,
    find_customer_by_card,
    get_customer_transactions,
    search_transactions,
    get_merchant_spend_summary,
    detect_suspicious_transactions,
)


def test_schema():
    result = inspect_database_schema()
    assert result


def test_customer_profile():
    result = get_customer_profile(1)
    assert result


def test_customer_name():
    result = find_customer_by_name("Denise")
    assert result


def test_card_details():
    result = get_card_details(1)
    assert result


def test_find_customer_by_card():
    result = find_customer_by_card(
        4279862398471697
    )
    assert result


def test_customer_transactions():
    result = get_customer_transactions(
        1,
        5
    )
    assert result


def test_search_transactions():
    result = search_transactions(
        1000,
        5
    )
    assert result


def test_merchant_summary():
    result = get_merchant_spend_summary()
    assert result


def test_suspicious_transactions():
    result = detect_suspicious_transactions()
    assert result