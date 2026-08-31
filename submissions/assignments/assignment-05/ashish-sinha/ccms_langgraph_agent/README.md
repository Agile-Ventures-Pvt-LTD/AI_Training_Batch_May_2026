# Credit Card Management System Agent

## Overview

It is an AI-powered customer support system built using LangGraph, LangChain, Groq LLM, and SQLite.

The agent can answer customer service queries by retrieving information from ccms.db database through a set of specializes tools as we used in this project.

The project demonstrates two implementations:
1. Custom ReAct Agent 
2. Prebuilt ReAct Agent

---

## Tech Stack

* Python 3.12+
* LangChain
* LangGraph
* Groq API
* SQLite
* python-dotenv

---

## Project Structure

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

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd ccms_langgraph_agent
```

### 2. Create Virtual Environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=data/ccms.db
```

---

## Running the Application

```bash
python app.py
```

You will be prompted to choose:

1. Custom ReAct Agent
2. Prebuilt ReAct Agent

The selected implementation will be used throughout the session.

---

## Available Tools

### inspect_database_schema
Returns database schema information.

### get_customer_profile
Returns customer details.

### get_card_details
Returns customer card information with masked card number.

### search_transactions
Search transactions using filters:

* cust_id
* card_last4
* merchant_name
* merchant_type
* min_amount
* max_amount
* from_date
* to_date
* transaction_type
* limit

### get_customer_transactions
Returns customer transaction history.

### get_statement_summary
Returns statement information and risk level.

### get_reward_points
Returns reward points and related transactions.

### get_merchant_spend_summary
Provides spend aggregation by merchant or merchant type.

### detect_suspicious_transactions
Detects potentially risky transactions using rule-based logic.

---

## Example Queries

```text
These are the uestions mentioned in the PRD:
1. Show me the database schema.
2. Show customer profile for customer 1
3. Show card details for customer 1
4. Show the last 5 transactions for customer 1
5. Which customers have the highest amount due?
6. Show statement summary for customer 1.
7. Which merchant type has the highest total spend?
8. Show reward points for customer 1.
9. Identify potentially suspicious transactions.
10. Which cards are expiring in the next 60 days?
```

## Output Example
User Query: Show me the database schema.

Agent Response:
Question: Show me the database schema.
Implementation: custom_react_agent
Tools Used: inspect_database_schema
Records Found: 0
Answer:
The database schema consists of 9 tables: card, card_type, customer, merchant, merchant_type, netbanking, transaction, transaction_terminal, and transaction_type. Each table has several columns, which are listed in the schema.

For example, the card table has columns such as card_number, valid_from, expiry, security_code, and cust_id, among others. Similarly, the customer table has columns such as cust_id, first_name, last_name, email, phone, address, city, state, and zip. The transaction table has columns such as TXN_ID, TX_DATETIME, CARD_ID, TERMINAL_ID, TX_AMOUNT, TX_TIME_SECONDS, TX_TIME_DAYS, TXN_TYPE_ID, and M_ID. The schema provides a detailed structure of the database, which can be useful for querying and analyzing the data.
Sensitive Data Masked: True

---

## Testing

Run tool tests:

```bash
python -m tests.test_tools
```

---

## Output Logs

Agent responses are saved in the following file output directories.

Custom Agent Output Directory:
```text
outputs/custom_agent_run.txt
```

Prebuilt Agent Output Directory:
```text
outputs/prebuilt_agent_run.txt
```

---

## Security Features

* Card numbers are masked before display.
* Only relevant customer information is returned.
* No sensitive financial information is exposed unnecessarily.

---

## Agent Implementations

### Custom ReAct Agent

Built manually using:

* StateGraph
* ToolNode
* Custom routing
* Reflection node
* Output formatter

### Prebuilt ReAct Agent

Built using:

```python
create_react_agent()
```

with the same set of tools and LLM.

---

## Future Enhancements

* Streamlit UI
* FastAPI deployment
* Authentication and authorization
* Conversation memory
* Advanced fraud detection
* RAG integration with policy documents

---

## Author
Ashish Sinha
