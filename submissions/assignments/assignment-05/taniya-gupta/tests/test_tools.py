import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import (
    mask_card_number, parse_id, parse_num, get_database_schema,
    get_customer_profile, get_card_details, search_transactions,
    get_merchant_spend_summary, get_rewards_summary, get_statement_summary,
    get_notifications, detect_suspicious_transactions
)
from db_utils import run
from output_formatter import format_as_table

def test_mask_card_number():
    assert mask_card_number("1234567812345678") == "**** **** **** 5678"
    assert mask_card_number(1234567812345678) == "**** **** **** 5678"

def test_parse_id():
    assert parse_id("123") == 123
    assert parse_id("ID: 456") == 456
    assert parse_id("all") is None
    assert parse_id("") is None
    assert parse_id("none") is None

def test_parse_num():
    assert parse_num("100") == 100.0
    assert parse_num("$1,234.56") == 1234.56

def test_db_run():
    df = run("SELECT 1 as val", ())
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df["val"][0] == 1

def test_format_as_table():
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    result = format_as_table(df)
    assert "col1" in result
    assert "col2" in result
    assert "1" in result
    assert "a" in result

def test_get_database_schema():
    schema = get_database_schema.invoke({})
    assert isinstance(schema, str)
    assert "customer:" in schema
    assert "card:" in schema
    assert "transaction:" in schema

def test_get_customer_profile():
    result = get_customer_profile.invoke({"search_query": "1"})
    assert isinstance(result, str)
    assert "cust_id" in result

def test_get_card_details():
    result = get_card_details.invoke({})
    assert isinstance(result, str)
    assert "**** **** ****" in result

def test_search_transactions():
    result = search_transactions.invoke({"min_amt": "100"})
    assert isinstance(result, str)
    assert "TX_AMOUNT" in result

def test_get_merchant_spend_summary():
    result = get_merchant_spend_summary.invoke({"by_type": True})
    assert isinstance(result, str)
    assert "merchant_type" in result
    assert "total" in result

def test_get_statement_summary():
    result = get_statement_summary.invoke({"cust_id": "1"})
    assert isinstance(result, str)
    assert "total_amount_due" in result

def test_get_rewards_summary():
    result = get_rewards_summary.invoke({})
    assert isinstance(result, str)
    assert "total_points" in result

def test_get_notifications():
    result = get_notifications.invoke({})
    assert isinstance(result, str)
    # The result could be a table string
    assert "High Value Alert" in result or "|" in result

def test_detect_suspicious_transactions():
    result = detect_suspicious_transactions.invoke({})
    assert isinstance(result, str)
    assert "TX_AMOUNT" in result or "|" in result
