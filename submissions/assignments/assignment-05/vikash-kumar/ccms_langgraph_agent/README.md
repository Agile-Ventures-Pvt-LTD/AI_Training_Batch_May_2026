# Credit Card Management System Agent

In this project build, we have used the LangGraph, Groq, Tools, and SQLite for building the agent.

## Business Context

A financial services company has a credit card management system that stores data about customers,cards, card types, transactions, merchants, merchant categories, transaction terminals, rewards,notifications, statements, and net banking users.

The company wants an AI agent that can interpret natural language questions, decide which database tools
to call, execute those tools safely, and return answers in a clear format.

## Technology Stack

- Python
- SQLite
- LangGraph
- LangChain Core
- langchain-groq
- python-dotenv
- pydantic
- pandas

## LangGraph Pre-built ReAct Agent

I have used a pre-built ReAct-style agent that can call tools in a loop. LangGraph’s pre-built ReAct helper is designed to create an agent graph that calls tools until a final response is reached. 

##  Agent Responsibilities

- Customer Profile Lookup
- Card Details Lookup
- Transaction Search
- Merchant Spend Summary
- Statement / Dues Summary
- Rewards Summary
- Notification Summary
- Suspicious Transaction Analysis

## Required Tools

- inspect_database_schema
- get_customer_profile
- get_card_details
- search_transactions
- get_customer_transactions
- get_statement_summary
- get_rewards_summary
- get_merchant_spend_summary
- get_notification_summary
- detect_suspicious_transactions
- get_transaction_type_summary
- get_cards_expiring_soon
- get_top_customers_by_due
- get_terminal_transaction_summary

## Tool: inspect_database_schema
Purpose:
Help the participant and agent understand table names and available columns.

Expected output:
{
"tables": ["customer", "card", "transaction", "merchant"],
"schema": {
"customer": ["cust_id", "first_name", "last_name", "email", "phone"]
}}

##  Tool: get_customer_profile
Purpose:
Find customer information by customer ID, email, phone, or name

Input:
{
"cust_id": "CUST-1001"
Output:
{
"found": true,
"customer": {
"cust_id": "CUST-1001",
"name": "Anika Sharma",
"email": "masked@example.com",
"city": "Pune",
"state": "Maharashtra"
}}}

## Tool: get_card_details
Purpose:
Get card information for a customer or card identifier.
Output should not expose:
full card number
security_code
password
security answers

Expected masking:
**** **** **** 1234

## Tool: search_transactions
Purpose:
Search transactions by filters.
Supported filters:
customer_id
card_last4
merchant_name
merchant_type
min_amount
max_amount
from_date
to_date
transaction_type
limit

Output:
{
"count": 5,
"transactions": [
{
"txn_id": "TXN-1001",
"txn_datetime": "2026-01-15 11:30:00",
"amount": 4500,
"merchant": "Amazon",
"transaction_type": "Debit",
"remarks": "Online purchase"
}
]}

##  Tool: get_customer_transactions
Purpose:
Return recent transactions for a customer.
Required output:
{
"customer_id": "",
"transaction_count": 0,
"transactions": []}

## Tool: get_statement_summary
Purpose:
Return statement and due information.
Expected output:
{
"customer_id": "",
"total_amount_due": 0,
"min_amount_due": 0,
"statement_date": "",
"due_date": "",
"risk_level": "LOW | MEDIUM | HIGH"
}

## Tool: get_rewards_summary
Purpose:
Return reward points by customer or card.
Expected output:
{
"customer_id": "",
"reward_points": 0,
"related_transactions": []}

## Tool: get_merchant_spend_summary
Purpose:
Aggregate transaction amount by merchant or merchant type.

Expected output:
{
"group_by": "merchant_type",
"results": [
{
"merchant_type": "Electronics",
"total_spend": 120000,
"transaction_count": 18
}
]}

##  Tool: detect_suspicious_transactions
Purpose:
Find potentially risky transactions using rule-based logic.

Expected output:
{
"rule_applied": "amount > 75000 or suspicious remarks",
"count": 3,
"flagged_transactions": [
{
"txn_id": "TXN-5001",
"amount": 95000,
"reason": "High-value transaction"
}
]}

# Agent Prompt Requirements
Recommended system prompt:

You are an AI Credit Card Management System Agent.
You answer questions by using tools connected to the ccms.db SQLite database.
Rules:
- Use tools for all database-related questions.
- Do not invent customer, card, transaction, merchant, reward, statement, or 
notification data.
- Do not expose full card numbers, security codes, passwords, or security 
answers.
- Mask sensitive card and customer data in final answers.
- If the user asks for data that is not available, clearly say no records were 
found.
- For analytical questions, call the appropriate aggregation tool.
- For suspicious transaction questions, use rule-based suspicious transaction 
detection tools.
- Do not provide financial, legal, or fraud conclusions as final certainty; say 
“potentially suspicious” or “requires review.”
- Keep final answers clear, concise, and business-friendly.

# Testing 

One can run the app.py for the agent execution and the user can ask the questions. For testing, I have added the test_tools.py under tests folder.