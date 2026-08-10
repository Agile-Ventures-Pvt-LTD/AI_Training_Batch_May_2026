from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from config import MODEL_NAME, GROQ_API_KEY
from prompts import system_prompt

from tools import (inspect_database_schema, get_customer_profile, get_card_details, search_transactions,
       get_customer_transactions, get_rewards_summary, detect_suspicious_transactions, get_merchant_spend_summary)

system_message=system_prompt()

tools=[inspect_database_schema, get_customer_profile, get_card_details, search_transactions,
       get_customer_transactions, get_rewards_summary, detect_suspicious_transactions, get_merchant_spend_summary]

llm = ChatGroq(model=MODEL_NAME,groq_api_key=GROQ_API_KEY)


agent=create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_message
)

def prebuilt_agent(user_input):
        try:
            message_input = [HumanMessage(content=user_input)]
            response = agent.invoke({"messages": message_input})
            return response["messages"][-1].content
        except Exception as e:
           return f"Error: {str(e)}"

