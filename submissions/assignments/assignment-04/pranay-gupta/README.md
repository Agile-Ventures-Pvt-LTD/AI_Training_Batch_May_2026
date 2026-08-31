# LangChain + SQLite E-Commerce Database Agent

## Project Overview

This project demonstrates how a Large Language Model (LLM) can interact with a relational database through LangChain agents and custom tools. The application enables business users to ask questions in natural language and receive accurate answers generated from an SQLite e-commerce database.

Instead of writing SQL queries manually, users can interact with the system using plain English. The agent determines when database access is required, generates a safe SQL query, retrieves the relevant data, and returns a business-friendly response.

---

## Business Use Case

Business teams often need insights from operational databases but may not have SQL knowledge.

This solution acts as an AI-powered database assistant capable of answering questions such as:

* What is the total revenue from completed orders?
* Which customer has spent the most money?
* Which products are running low on stock?
* Which product category generates the highest revenue?

The goal is to reduce dependency on technical teams for routine data requests.

---

## Technology Stack

| Component              | Technology              |
| ---------------------- | ----------------------- |
| Programming Language   | Python                  |
| Database               | SQLite                  |
| Agent Framework        | LangChain               |
| LLM Provider           | Groq                    |
| Model                  | Llama 3.3 70B Versatile |
| Environment Management | python-dotenv           |
| Testing                | pytest                  |

---

## Project Structure

```text
ecommerce-agent-assignment/
│
├── README.md
├── .env.example
├── requirements-legacy.txt
├── requirements-modern.txt
│
├── data/
│   └── ecommerce.db
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
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   ├── agents/
│   │   ├── modern_agent.py
│   │   └── legacy_agent.py
│   │
│   └── app.py
│
├── tests/
│   ├── test_database.py
│   ├── test_sql_tool.py
│   └── test_agent_queries.py
│
└── sample_queries.md
```

---

## Database Schema

### customers

| Column      | Type    |
| ----------- | ------- |
| customer_id | INTEGER |
| name        | TEXT    |
| email       | TEXT    |
| city        | TEXT    |
| signup_date | TEXT    |

### products

| Column         | Type    |
| -------------- | ------- |
| product_id     | INTEGER |
| name           | TEXT    |
| category       | TEXT    |
| price          | REAL    |
| stock_quantity | INTEGER |

### orders

| Column       | Type    |
| ------------ | ------- |
| order_id     | INTEGER |
| customer_id  | INTEGER |
| order_date   | TEXT    |
| status       | TEXT    |
| total_amount | REAL    |

### order_items

| Column        | Type    |
| ------------- | ------- |
| order_item_id | INTEGER |
| order_id      | INTEGER |
| product_id    | INTEGER |
| quantity      | INTEGER |
| unit_price    | REAL    |

---

## Database Safety Features

The custom database tool includes multiple security controls:

### Allowed Operations

* SELECT queries only

### Blocked Operations

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE
* CREATE
* REPLACE

### Additional Protections

* Multiple SQL statements are rejected
* Maximum row limit enforced
* Database connection validation
* Graceful exception handling
* Read-only query execution

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd ecommerce-agent-assignment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Modern Version:

```bash
pip install -r requirements-modern.txt
```

Legacy Version:

```bash
pip install -r requirements-legacy.txt
```

---

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Create and Seed Database

### Create Database

```bash
python scripts/create_database.py
```

### Seed Database

```bash
python scripts/seed_database.py
```

---

## Running Modern LangChain Version

Compatible with:

```text
langchain >= 1.0
```

Run:

```bash
python src/app.py
```

The application will launch a command-line interface where users can ask business questions.

---

## Running Legacy LangChain Version

Compatible with:

```text
langchain < 1.0
```

Example:

```python
from src.agents.legacy_agent import run_legacy_agent

response = run_legacy_agent(
    "Which customer has spent the most money?"
)

print(response)
```

---

## Example Questions

* What is the total revenue from completed orders?
* Which customer has spent the most money?
* Show top 5 products by quantity sold.
* Which product category generated the highest revenue?
* How many orders are pending?
* Show all cancelled orders with customer names.
* Which customers are from Delhi?
* Which products have stock below 10?
* What is the average order value?
* Show total revenue by month.
* Which city has the highest number of customers?
* Which customers have placed more than 2 orders?
* What are the top 3 most expensive products?
* Which product has never been ordered?
* Show total sales by category.

---

## Testing

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_sql_tool.py
```

---

## Tool Design

The solution uses a reusable custom LangChain tool called:

```text
query_ecommerce_database
```

Responsibilities:

1. Validate generated SQL.
2. Enforce read-only access.
3. Connect to SQLite.
4. Execute queries safely.
5. Return structured results.
6. Handle database errors gracefully.

---

## Known Limitations

* Supports SQLite only.
* Database schema is predefined.
* Very complex analytical questions may require additional prompt engineering.
* Query performance is dependent on database size.
* Results are limited to prevent excessive output.

---

## Future Improvements

* Streamlit-based web interface.
* SQL query visualization panel.
* CSV export functionality.
* LangSmith observability and tracing.
* Role-based access control.
* Multi-database support.
* Query caching for improved performance.
* Conversation memory for follow-up questions.

---

## Assignment Outcomes

This project demonstrates:

* LangChain agent development
* Tool calling workflows
* SQLite database integration
* SQL query generation
* Enterprise safety controls
* Natural language business analytics
* Modern and legacy LangChain implementations

The final system allows business users to retrieve actionable insights from an e-commerce database using natural language without requiring SQL knowledge.
