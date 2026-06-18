# AI Credit Card Management System Agent

## Project Overview

This project is an AI-powered Credit Card Management System Agent built using LangGraph, Groq, SQLite, and custom tools.

The goal of the project is to allow users to ask natural language questions about credit card customers, cards, merchants, and transactions without writing SQL queries manually.

The agent uses the provided SQLite database (`ccms.db`) as the source of truth and answers questions by calling predefined database tools. The agent does not generate database information on its own and only responds using data retrieved from the database.

Two implementations are included:

1. Prebuilt LangGraph ReAct Agent
2. Custom LangGraph ReAct Agent

---

# Project Structure

```text
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
```

---

# Database Used

The project uses the provided SQLite database:

```text
ccms.db
```

The database contains the following tables:

* customer
* netbanking
* card_type
* card
* transaction_type
* transaction_terminal
* merchant_type
* merchant
* transaction

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone <repository_url>
cd ccms_langgraph_agent
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

Windows

```bash
venv\Scripts\activate
```


## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# How to Place ccms.db

Create a folder named:

```text
data
```

Place the database file inside:

```text
data/ccms.db
```

Example:

```text
data/
└── ccms.db
```

---

# Environment Variable Setup

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=data/ccms.db
```

---

# How to Run the Project

Run:

```bash
python app.py
```

The application will ask which implementation to use:

```text
1. Prebuilt ReAct Agent
2. Custom ReAct Agent
```

Choose the desired option and start asking questions.

---

# How to Run Prebuilt Agent

Select:

```text
1
```

when prompted.

The application will load the LangGraph prebuilt ReAct agent and use the registered tools to answer questions.

---

# How to Run Custom Graph Agent

Select:

```text
2
```

when prompted.

The application will load the custom LangGraph graph implementation consisting of:

* Agent Node
* Tool Node
* Reflection Node

---

# Tools Implemented

## 1. get_inspect_schema()

Purpose:

Returns all database tables and columns.

Example:

```text
Show me the database schema
```

---

## 2. get_customer_profile()

Purpose:

Retrieve customer information using:

* Customer ID
* Email
* Phone Number
* First Name
* Last Name

Example:

```text
Show customer details for customer 1
```

---

## 3. get_card_details()

Purpose:

Retrieve card information for a customer.

Sensitive card information is masked before returning results.

Example:

```text
Show card details for customer 1
```

---

## 4. search_transactions()

Purpose:

Search transactions using filters such as:

* Customer ID
* Merchant
* Transaction Type
* Amount Range

Example:

```text
Show transactions above 50000
```

---

## 5. get_customer_transactions()

Purpose:

Returns recent transactions for a customer.

Example:

```text
Show recent transactions for customer 1
```

---

## 6. get_merchant_spend_summary()

Purpose:

Returns total spend grouped by merchant type.

Example:

```text
Which merchant category has the highest spend?
```

---

## 7. detect_suspicious_transactions()

Purpose:

Identifies potentially suspicious transactions.

Current Rule:

```text
Transaction Amount > 75000
```

Example:

```text
Show suspicious transactions
```

---

# Sample Questions

```text
Show me the database schema

Show customer details for customer 1

Show card details for customer 1

Show the last 10 transactions for customer 1

Show transactions above 50000

Show transactions for merchant Amazon

Which merchant category has the highest spend?

Show spend summary by merchant type

Show suspicious transactions

Find high value transactions
```

---

# Sensitive Data Masking Rules

The agent does not expose sensitive customer information.

Implemented protections:

### Card Number

Before:

```text
1234567890123456
```

After:

```text
**** **** **** 3456
```

### Phone Number

Before:

```text
9876543210
```

After:

```text
******3210
```

### Email

Before:

```text
johnsmith@gmail.com
```

After:

```text
jo***@gmail.com
```

### Security Information

The following fields are never returned:

* security_code
* password
* security_question
* security_answer

---

# Known Limitations

1. The database does not contain rewards data.

2. The database does not contain notification data.

3. The database does not contain statement data.

4. Suspicious transaction detection currently uses simple rule-based logic.

5. The agent depends on available database records and cannot answer questions for missing data.

---

# Future Improvements

1. Add reward tracking if reward tables become available.

2. Add notification analytics if notification data becomes available.

3. Improve suspicious transaction detection using multiple fraud detection rules.

4. Add Streamlit UI.

5. Add charts and visual summaries.

6. Add customer spend trend analysis.

7. Add export functionality for reports.

---

# Development Notes and Challenges

While building this project, I encountered several practical issues which helped me understand SQLite and database tool development better.

## Dynamic SQL Query Construction

While creating tools such as `get_customer_profile()`, I started with:

```sql
SELECT * FROM customer WHERE 1=1
```

and dynamically appended conditions based on user inputs.

One issue I encountered was accidentally writing:

```python
q += "AND phone = ?"
```

instead of:

```python
q += " AND phone = ?"
```

The missing space before `AND` caused SQLite query errors and helped me understand how carefully dynamic SQL queries need to be constructed.

---

## Understanding Database Schema

Before implementing tools, I inspected the database structure to understand available tables and columns.

I learned to use:

```sql
PRAGMA table_info(table_name)
```

which helped me view column information for each table and design tools based on the actual database schema.

---

## Reserved Keyword Issue

The database contains a table named:

```text
transaction
```

Since `transaction` is a reserved keyword in SQLite, queries failed when referenced directly.

To fix this, I used:

```sql
SELECT * FROM "transaction"
```

which correctly treats it as a table name.

---

## Understanding Table Relationships

While implementing transaction-related tools, I initially expected the transaction table to contain a customer ID.

After inspecting the schema, I realized that customer information is linked indirectly:

```text
customer
   ↓
card
   ↓
transaction
```

Because of this, JOIN operations were required to retrieve customer-specific transaction data.

This was one of the most important learnings during the project.

---

## Using Real Database Data

The project requirements mentioned examples such as rewards, statements, and notifications.

After inspecting the actual database, I found that those tables were not available.

Instead of generating artificial data, I implemented tools only for data that exists in the database so that all responses remain grounded in actual records.

---

# Participant

Mohammad Anas

