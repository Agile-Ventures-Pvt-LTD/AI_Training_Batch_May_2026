import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from prompts import system_prompt
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

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

tools = [
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
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
)
