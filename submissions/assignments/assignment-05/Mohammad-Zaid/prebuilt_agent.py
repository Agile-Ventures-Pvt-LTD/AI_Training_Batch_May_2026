# prebuilt_agent.py

from db_tools import (
    get_card_details,
    get_customer_profile,
    get_customer_transactions,
    get_merchant_spend_summary,
    get_rewards_summary,
    get_statement_summary,
    inspect_database_schema,
    search_transactions
    )

from config import MODEL_NAME, GROQ_API_KEY
from prompts import SYSTEM_PROMPT
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage



tools = [
    get_card_details,
    get_customer_profile,
    get_customer_transactions,
    get_merchant_spend_summary,
    get_rewards_summary,
    get_statement_summary,
    inspect_database_schema,
    search_transactions
    ]

llm = ChatGroq(model=MODEL_NAME,
               groq_api_key=GROQ_API_KEY,
               temperature=0
               )

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

def prebuilt_langgraph_agent(user_input):
    
    try: 
        message_input = [HumanMessage(content=user_input)]
        
        response = agent.invoke({"messages": message_input})
        
        return response["messages"][-1].content
    
    except Exception as e:
        return f"Error: {str(e)}"