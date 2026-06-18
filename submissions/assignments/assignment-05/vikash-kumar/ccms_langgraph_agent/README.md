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

# Testing 

One can run the app.py for the agent execution and the user can ask the questions. For testing, I have added the test_tools.py under tests folder.