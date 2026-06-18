# AI Credit Card Management Agent Using LangGraph, Groq, Tools, and SQLit
An AI agent that can answer operational and analytical questions from a credit card
management database named ccms.db.

Two aproaches :
1. Pre-built ReAct Agent
2. Custom LangGraph ReAct Agent


## 2. Setup Instructions
Folder structure :
ccms_langgraph_agent/
│
├── app.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── prebuilt_agent.py
├── custom_react_agent.py
├── output_formatter.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│   └── ccms.db
│
├── outputs/
│   ├── sample_prebuilt_agent_run.txt
│   └── sample_custom_agent_run.txt
│
└── tests/
└── test_tools.py

Create the virtual environment:
install the dependencies:

```bash
python -m venv venv
venv\Scripts\activate          
pip install -r requirements.txt
```


Place `ccms.db` inside the data/` directory:



## 4. Environment Variable Setup

Create .env 


GROQ_API_KEY=......api_key..........
GROQ_MODEL="llama-3.1-8b-instant"
DB_PATH=data/ccms.db


## 5. How to Run Pre-built Agent

```bash
python app.py
```
Select option 1.


## 6. How to Run Custom Graph Agent

```bash
python app.py
```
Select option 2 

Choose any one of the option and then query


## 7. Tool List and Purpose

inspect_database_schema – List all database tables and columns.
get_customer_profile – Find customer details using customer ID, email, phone number, or name.
get_card_details – Retrieve masked credit card information for a customer.
search_transactions – Search and filter transactions based on various criteria.
get_customer_transactions – View transaction history for a specific customer.
get_statement_summary – Get statement details, outstanding dues, and risk level.
get_rewards_summary – View reward points earned (1 point per ₹100 spent).
get_merchant_spend_summary – Analyze spending grouped by merchant category.
detect_suspicious_transactions – Identify potentially anomalous or suspicious transactions.
get_notification_summary – View alerts for high-value transactions (above ₹50,000).
get_cards_expiring_soon – Find cards that will expire within a specified period.
get_top_customers_by_due – List customers with the highest outstanding dues.
get_transaction_type_summary – Get a breakdown of transactions by debit/credit and local/international categories.


## 8. Sample Questions
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

## 9. Sensitive Data Masking Rules

Email Addresses – Only the first two characters are visible ,the rest are masked.
  - Example: jo***@example.com
Phone Numbers – Only the last four digits are visible.
  - Example: ****7890
Card Numbers – Only the last four digits are displayed.
  - Example: **** **** **** 1234



## 10. Known Limitations
  - rate limit exceed issue ( so that i had worked on the given model and then converted to another with new api key)

## 11. Future Improvements

- Streaming responses
- Conversation memory (MemorySaver, Redis, PostgreSQL)
- ML-based fraud detection
- Web UI (Streamlit, Gradio, FastAPI + React)
- Multi-language support 