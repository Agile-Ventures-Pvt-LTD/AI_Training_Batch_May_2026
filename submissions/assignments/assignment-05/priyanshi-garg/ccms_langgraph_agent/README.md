# AI Credit Card Management System Agent Using LangGraph, Groq, Tools, and SQLite

## Business Context
A financial services company has a credit card management system that stores data about customers,
cards, card types, transactions, merchants, merchant categories, transaction terminals, rewards,
notifications, statements, and net banking users.
Currently, business users and support teams depend on manual SQL queries to answer questions such as:
    1. Which customer made a specific transaction?
    2. What are the recent transactions on a card?
    3. Which merchants are associated with high spending?
    4. What rewards were earned by a customer?
    5. Which cards are expiring soon?
    6. Which customers have large dues?
    7. Which transaction categories are debit or credit?
    8. Which notifications were triggered for transactions?
    9. Are there suspicious transaction patterns?
    10.What is the summary of a customer’s credit card activity?
The company wants an AI agent that can interpret natural language questions, decide which database tools
to call, execute those tools safely, and return answers in a clear format.

## Technology Stack Used
Python
SQLite
LangGraph
LangChain Core
langchain-groq
python-dotenv

## Folder Structure
ccms_langgraph_agent/
│
├── app.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── custom_react_agent.py
├── output_formatter.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ └── ccms.db
│
├── outputs/
│ └── sample_custom_agent_run.txt
│
└── tests/
 └── test_tools.py

## Tool list and purpose
1. inspect_database_schema
- This tool is showing the database schema

2. get_customer_profile
- This tools helps to get the customer profile via customer ID, phone, email, first name and last name

3. get_card_details
- Get card information for a customer or card identifier.

4. search_transactions
- Search transactions by filters.
supported filters:-

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

5. get_customer_transactions
- Return recent transactions for a customer.

6. get_statement_summary
- Return statement and due information.

7. get_rewards_summary
- Return reward points by customer or card.

8. get_merchant_spend_summary
- Aggregate transaction amount by merchant or merchant type.


## Sample Questions
1. Show me the database schema.
2. Show customer profile for customer CUST-1001.
3. Show card details for customer CUST-1001.
4. Show the last 5 transactions for customer CUST-1001.
5. Which customers have the highest amount due?
6. Show statement summary for customer CUST-1001.
7. Which merchant type has the highest total spend?
8. Show reward points for customer CUST-1001.
9. Identify potentially suspicious transactions.
10. Which cards are expiring in the next 60 days?

## How to run custom graph agent
- run python app.py in terminal 

## Sensitive data masking rules
    masked_card = (
        "**** **** **** "
        + card_num[-4:]
    )

## Future Improvements
Can implement more tools for resloving user queries more naturally
