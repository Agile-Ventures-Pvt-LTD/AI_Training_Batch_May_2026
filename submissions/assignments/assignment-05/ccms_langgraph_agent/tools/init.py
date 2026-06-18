try:
    from .profile_tools import get_customer_profile_tool
    from .analytics_tools import get_merchant_spend_summary_tool
    from .card_tools import get_card_details_tool
    from .security_tools import detect_suspicious_transactions_tool
    from .transaction_tools import search_transactions_tool, get_customer_transactions_tool
    from .inspect_database_schema import inspect_database_schema_tool
except ImportError as e:
    print(f"Error: {e}")


tools = [
    get_customer_profile_tool,
    get_merchant_spend_summary_tool,
    get_card_details_tool,
    detect_suspicious_transactions_tool,
    search_transactions_tool,
    get_customer_transactions_tool,
    inspect_database_schema_tool,
]