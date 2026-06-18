from config import GROQ_API_KEY,GROQ_MODEL
from langchain_groq import ChatGroq
from tools import get_customer_profile,get_inspect_schema,get_card_details,search_transactions,get_customer_transactions,get_merchant_spend_summary,detect_suspicious_transactions
from langgraph.prebuilt import create_react_agent
from prompts import SYSTEM_PROMPT

llm = ChatGroq(
    model = GROQ_MODEL,
    groq_api_key = GROQ_API_KEY
)

all_tools = [
    get_customer_profile,
    get_inspect_schema,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_merchant_spend_summary,
    detect_suspicious_transactions
]
agent = create_react_agent(
    model = llm,
    tools = all_tools,
    prompt = SYSTEM_PROMPT
)