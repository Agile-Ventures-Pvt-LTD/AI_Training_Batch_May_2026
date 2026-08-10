from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from tools import *

llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0
)

tools = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_rewards_summary,
    get_merchant_spend_summary,
    detect_suspicious_transactions,
    get_statement_summary,
    get_notification_summary,
    get_cards_expiring_soon,
    get_top_customers_by_due,
    get_transaction_type_summary
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)