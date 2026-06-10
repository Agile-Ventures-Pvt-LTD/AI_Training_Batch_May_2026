# Natural Language E-commerce Database Agent

## Project Overview

Natural Language E-commerce Database Agent is an AI-powered database assistant that allows business users to query an e-commerce database using plain English instead of SQL.

The application uses LangChain Agents, SQLite, and Groq LLMs to translate natural language questions into SQL queries, execute them safely, and return business-friendly responses.

Example:

**User Query:**

> Which customer has spent the most money?

**Agent Response:**

> Priya Sharma is the highest spending customer with a total completed purchase value of ₹38,900.

---

# Business Use Case

Business teams often depend on developers or data analysts to retrieve information from databases.

This project enables non-technical users to:

* Ask questions in plain English
* Retrieve information from an SQLite database
* Generate business insights without writing SQL
* Access customer, product, order, and revenue analytics

---

# Features

### Database Features

* SQLite Database
* Automated Database Creation Script
* Automated Data Seeding Script
* Realistic E-commerce Sample Data

### AI Features

* Natural Language Querying
* SQL Generation Using LangChain Agents
* Groq LLM Integration
* Business-Friendly Responses

### Security Features

* Only SELECT queries allowed
* Blocks INSERT statements
* Blocks UPDATE statements
* Blocks DELETE statements
* Blocks DROP statements
* Blocks ALTER statements
* Prevents multiple SQL statements
* Handles invalid queries gracefully

### Logging Features

* SQL Query Logging
* Query Result Logging
* Timestamp Tracking

---

# Technology Stack

| Component              | Technology                 |
| ---------------------- | -------------------------- |
| Language               | Python                     |
| Database               | SQLite                     |
| Framework              | LangChain                  |
| LLM                    | Groq                       |
| Data Generation        | Faker                      |
| Testing                | Pytest                     |
| Environment Management | Python Virtual Environment |

---

# Project Structure

```text
Natural Language E-commerce Database Agent/

├── data/
│   └── ecommerce.db
│
├── logs/
│   └── query_logs.txt
│
├── scripts/
│   ├── create_database.py
│   └── seed_database.py
│
├── src/
│   ├── db/
│   │   ├── connection.py
│   │   └── schema_description.py
│   │
│   ├── tools/
│   │   └── ecommerce_sql_tool.py
│   │
│   ├── agents/
│   │   ├── modern_agent.py
│   │   └── legacy_agent.py
│   │
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   ├── logger.py
│   ├── app.py
│   └── legacy_app.py
│
├── tests/
│   ├── test_database.py
│   ├── test_sql_tool.py
│   └── test_legacy_tool.py
│
├── requirements-modern.txt
├── requirements-legacy.txt
├── README.md
└── .env
```

---

# Database Schema

## Customers

| Column      | Type    |
| ----------- | ------- |
| customer_id | INTEGER |
| name        | TEXT    |
| email       | TEXT    |
| city        | TEXT    |
| signup_date | TEXT    |

---

## Products

| Column         | Type    |
| -------------- | ------- |
| product_id     | INTEGER |
| name           | TEXT    |
| category       | TEXT    |
| price          | REAL    |
| stock_quantity | INTEGER |

---

## Orders

| Column       | Type    |
| ------------ | ------- |
| order_id     | INTEGER |
| customer_id  | INTEGER |
| order_date   | TEXT    |
| status       | TEXT    |
| total_amount | REAL    |

---

## Order Items

| Column        | Type    |
| ------------- | ------- |
| order_item_id | INTEGER |
| order_id      | INTEGER |
| product_id    | INTEGER |
| quantity      | INTEGER |
| unit_price    | REAL    |

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd Natural-Language-Ecommerce-Agent
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

### Modern LangChain

```bash
pip install -r requirements-modern.txt
```

### Legacy LangChain

```bash
pip install -r requirements-legacy.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Database Setup

Create database:

```bash
python scripts/create_database.py
```

Seed sample data:

```bash
python scripts/seed_database.py
```

---

# Running Modern Agent

```bash
python -m src.app
```

---

# Running Legacy Agent

```bash
python -m src.legacy_app
```

---

# Sample Questions

* How many customers are there?
* What is the total revenue from completed orders?
* Which customer spent the most money?
* Show top 5 products by quantity sold.
* Which city has the highest number of customers?
* Which products have stock below 10?
* Show all cancelled orders.
* Which customers are from Delhi?
* What is the average order value?
* Show total revenue by month.

---

# Query Logging

All executed database queries are automatically logged.

Location:

```text
logs/query_logs.txt
```

Logged Information:

* Timestamp
* Generated SQL Query
* Query Result

---

# Safety Controls

The application includes multiple database protection mechanisms:

* Only SELECT queries allowed
* Multiple SQL statements blocked
* Dangerous SQL operations blocked
* Graceful error handling
* Database remains read-only

---

# Testing

Run database tests:

```bash
python -m tests.test_database
```

Run SQL tool tests:

```bash
python -m tests.test_sql_tool
```

Run legacy tool tests:

```bash
python -m tests.test_legacy_tool
```

---

# Future Improvements

* Streamlit Chat Interface
* LangSmith Tracing
* SQL Visualization
* CSV Export
* Authentication Layer
* Multi-Database Support
* Dashboard Analytics
* Query History UI

---

# Author

Priyanshi Garg

AI Engineer Intern Project

Natural Language E-commerce Database Agent
