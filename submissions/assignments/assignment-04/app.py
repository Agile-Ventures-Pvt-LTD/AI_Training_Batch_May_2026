"""
app.py
Entry point for the AI Credit Card Management Agent (Choice 1: LangGraph
Prebuilt ReAct Agent), following the same pattern shown in the
"Function Calling in LangGraph" reference notebook:
    agent = create_react_agent(model=llm, tools=[...], prompt=system_prompt)
    response = agent.invoke({"messages": messages_input})
"""

import os
import pprint

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from tools import ALL_TOOLS

load_dotenv()

llm = ChatGroq(
    model=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    groq_api_key=os.environ["GROQ_API_KEY"],
    temperature=0,
)

system_prompt = """
You are an AI Credit Card Management System Agent.
You answer questions by using tools connected to the ccms.db SQLite database.

Rules:
- Use tools for all database-related questions.
- Do not invent customer, card, transaction, merchant, reward, statement,
  or notification data.
- Do not expose full card numbers, security codes, passwords, or security
  answers. Mask sensitive card and customer data in final answers.
- If the user asks for data that is not available, clearly say no records
  were found.
- For analytical questions, call the appropriate aggregation tool
  (e.g. get_merchant_spend_summary).
- For suspicious transaction questions, use detect_suspicious_transactions
  and never state fraud as certain -- say "potentially suspicious" or
  "requires review".
- Keep final answers clear, concise, and business-friendly. Use a short
  table or bullet list for multiple records.
"""

agent = create_react_agent(
    model=llm,
    tools=ALL_TOOLS,
    prompt=system_prompt,
)


def ask(user_input: str):
    """Runs one query through the agent and prints the final answer."""
    messages_input = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
    response = agent.invoke({"messages": messages_input})
    final_ai_message = response["messages"][-1].content
    print(final_ai_message)
    return response


if __name__ == "__main__":
    # Mandatory test prompts (replace CUST-1001 with a real customer ID
    # from your ccms.db if it does not exist).
    test_prompts = [
        "Show me the database schema.",
        "Show customer profile for customer CUST-1001.",
        "Show card details for customer CUST-1001.",
        "Show the last 5 transactions for customer CUST-1001.",
        "Which customers have the highest amount due?",
        "Show statement summary for customer CUST-1001.",
        "Which merchant type has the highest total spend?",
        "Show reward points for customer CUST-1001.",
        "Identify potentially suspicious transactions.",
        "Which cards are expiring in the next 60 days?",
    ]

    with open("outputs/sample_prebuilt_agent_run.txt", "w") as f:
        for prompt in test_prompts:
            print("=" * 60)
            print("USER:", prompt)
            f.write("=" * 60 + "\n")
            f.write(f"USER: {prompt}\n")
            resp = ask(prompt)
            f.write(f"ANSWER: {resp['messages'][-1].content}\n\n")
