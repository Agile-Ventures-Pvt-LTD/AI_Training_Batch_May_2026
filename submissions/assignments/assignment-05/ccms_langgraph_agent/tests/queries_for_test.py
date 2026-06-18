TEST_QUERIES = [
    "Show me the database schema.",
    "Show customer profile for customer 132.",
    "Show card details for customer 131.",
    "Show the last 5 transactions for customer 113.",
    "Show transactions made on 5th June 2022.",
    "Which merchant type has the highest total spend?",
    "Identify potentially suspicious transactions."
]

TEST_CASES = {
    "inspect_database_schema": {},
    "get_customer_profile": {
        "customer_id": "132"
    },
    "get_merchant_spend_summary": {
        "group_by": "merchant"
    },
    "get_card_details": {
        "customer_id": "131"
    },
    "get_customer_transactions": {
        "customer_id": "113",
        "limit": 5
    },
    "search_transactions": {
        "min_amount": 100
    },
    "detect_suspicious_transactions": {},
    "get_merchant_spend_summary": {}
}