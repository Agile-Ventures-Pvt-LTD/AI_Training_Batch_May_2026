# LangChain + SQLite E-Commerce Agent

## Participant Name

Mohd Zaid Ansari

## Project Overview

This project implements an AI-powered E-Commerce Assistant that answers business questions using natural language and a SQLite database. The assistant converts user questions into SQL queries, retrieves data from the database, and returns business-friendly responses.

The project demonstrates both:

* **Legacy LangChain (< 1.0)** implementation
* **Modern LangChain (≥ 1.0)** implementation

using the Olist E-Commerce dataset stored in SQLite.

---

## Business Use Case

Business users often need answers such as:

* How many orders have been placed?
* What is the average review score?
* Which payment method is most frequently used?
* Who are the top sellers?

Instead of writing SQL manually, users can ask questions in plain English and receive clear answers.

---

## Technology Stack

* Python
* SQLite
* LangChain
* LangChain Community
* LangChain Groq
* Groq LLM
* SQLAlchemy
* Python Dotenv

---

## Database Schema

The database contains the following tables:

* customers
* geolocation
* leads_closed
* leads_qualified
* order_items
* order_payments
* order_reviews
* orders
* product_category_name_translation
* products
* sellers

Schema information is maintained in:

```text
src/db/schema_description.py
```

---

## Project Structure

```text
ecommerce-agent-assignment/
│
├── README.md
├── requirements-legacy.txt
├── requirements-modern.txt
│
├── data/
│   └── olist.sqlite
│
├── src/
│   ├── agents/
│   │   ├── legacy_agent.py
│   │   └── modern_agent.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   └── schema_description.py
│   │
│   ├── tools/
│   │   └── sql_tool.py
│   │
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   ├── app.py
│   └── moder_app.py
│
├── tests/
│   ├── test_database.py
│   ├── test_sql_tool.py
│   └── test_agent_queries.py
│
└── sample_queries.md
```

---

## Setup Instructions


### Create Virtual Environment

```bash
uv venv ven1
```
```bash
uv venv ven2
```

### Activate Environment

```bash
.venv1\Scripts\activate
```

```bash
.venv2\Scripts\activate
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## How to Run Legacy LangChain Version (< 1.0)

Install dependencies:

```bash
uv add -r requirements1.txt
```

```bash
pip install -r requirements2.txt
```

Run:

```bash
python src/app.py
```

```bash
python moder/app.py
```

---

## How to Run Modern LangChain Version (≥ 1.0)

Install dependencies:

```bash
pip install -r requirements-modern.txt
```

Run:

```bash
python src/moder_app.py
```

---

## How the Application Works

```text
User Question
      ↓
LangChain Agent
      ↓
Generate SQL Query
      ↓
SQLite Tool
      ↓
Execute SELECT Query
      ↓
Retrieve Result
      ↓
Business-Friendly Answer
```

---

## Safety Features

* Only SELECT queries allowed
* Multiple SQL statements blocked
* Dangerous operations rejected:

  * INSERT
  * UPDATE
  * DELETE
  * DROP
  * ALTER
  * CREATE
  * REPLACE
  * TRUNCATE
* Query results limited to prevent excessive output
* Graceful error handling

---

## Sample Questions

* How many orders are there?
* How many customers are there?
* What is the average review score?
* Which payment type is used most frequently?
* Show the top 5 sellers by number of orders.
* How many products are available?

---

## Libraries Used

### Legacy Version

* langchain==0.3.27
* langchain-community==0.3.27
* langchain-groq==0.3.8
* langchain-core==0.3.75
* python-dotenv
* pandas

### Modern Version

* langchain>=1.0.0
* langchain-community>=0.4.0
* langchain-core>=1.0.0
* langchain-groq>=1.0.0
* python-dotenv
* pandas

---

## Assumptions

* SQLite database file exists at `data/olist.sqlite`
* User provides business-related questions
* Groq API key is valid and active
* Database schema remains unchanged

---

## Output

Example:

**Question**

```text
How many orders are there?
```

**Generated SQL**

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

**Answer**

```text
There are 99,441 orders in the database.
```

---

## Known Limitations

* Depends on LLM-generated SQL accuracy
* Limited to available database schema
* Supports read-only database operations
* Large result sets are truncated

---

## Future Improvements

* Query caching
* SQL validation using parser libraries
* Visualization dashboards
* Conversation memory
* Multi-database support
* Streaming responses
* Advanced analytics and reporting
