# E-Commerce SQL Agent using LangChain (Modern & Legacy Versions)

## Participant Name
Nandani Bisht

## Project Overview

This project implements an AI-powered E-Commerce Database Assistant that answers business questions by querying a SQLite database using natural language.

The application supports:

* LangChain Modern Version (>= 1.0)
* LangChain Legacy Version (< 1.0)
* SQLite Database
* Secure SQL Tool Execution
* Groq LLM Integration
* Automated Testing with Pytest

The same business logic, database, and tools are shared across both implementations while demonstrating the differences between modern and legacy LangChain agent architectures.

---

## Business Use Case

Business teams frequently need data from the e-commerce database but do not know SQL. This assistant lets anyone ask plain-English questions and receive accurate, business-friendly answers directly from the database — no SQL knowledge required.

---

## Features

* Natural Language to SQL Querying
* SQLite Database Integration
* Tool-Based Agent Architecture
* Secure SQL Execution (SELECT only)
* Support for Modern and Legacy LangChain Versions
* Unit Testing with Pytest
* Business-Friendly Responses

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
│   ├── app.py
│   ├── agents/
│   │   ├── modern_agent.py
│   │   └── legacy_agent.py
│   ├── db/
│   │   ├── connection.py
│   │   └── schema_description.py
│   ├── prompts/
│   │   └── system_prompt.py
│   └── tools/
│       └── ecommerce_sql_tool.py
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

```sql
customer_id INTEGER PRIMARY KEY
name TEXT
email TEXT
city TEXT
signup_date TEXT
```

### products

```sql
product_id INTEGER PRIMARY KEY
name TEXT
category TEXT
price REAL
stock_quantity INTEGER
```

### orders

```sql
order_id INTEGER PRIMARY KEY
customer_id INTEGER
order_date TEXT
status TEXT
total_amount REAL
```

### order_items

```sql
order_item_id INTEGER PRIMARY KEY
order_id INTEGER
product_id INTEGER
quantity INTEGER
unit_price REAL
```

---

## Technologies Used

* Python 3.11
* LangChain 1.x (Modern)
* LangChain 0.3.x (Legacy)
* Groq (llama-3.3-70b-versatile)
* SQLite
* Pytest
* python-dotenv

---

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

---

## Setup Instructions

### Step 1 — Clone and enter the project

```bash
cd ecommerce-agent-assignment
```

### Step 2 — Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key.

### Step 3 — Create and seed the database

```bash
python scripts/create_database.py
python scripts/seed_database.py
```

This creates `data/ecommerce.db` with all 4 tables and sample data:
- 10 customers across 7 cities
- 15 products across 5 categories
- 25 orders (completed, pending, cancelled)
- 50 order items

---

## Running the Application

### Modern LangChain Version (>= 1.0)

Create and activate the environment:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-modern.txt
```

Run the app:

```bash
python -m src.app
```

Or use the root entry point:

```bash
python main.py
```

---

### Legacy LangChain Version (< 1.0)

This implementation uses the older `initialize_agent` API and is provided to demonstrate backward compatibility with LangChain 0.3.x. It is the **legacy implementation**.

Create and activate a separate environment:

```bash
python -m venv legacy_env

# Windows
.\legacy_env\Scripts\Activate.ps1

# macOS / Linux
source legacy_env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-legacy.txt
```

Run the app (it auto-detects the installed LangChain version):

```bash
python -m src.app
```

---

## Testing

Run all tests:

```bash
pytest -v
```

Tests included:

* `test_database.py` — Database connection and table existence
* `test_sql_tool.py` — SQL tool security (SELECT-only, block unsafe queries, block multi-statement)
* `test_agent_queries.py` — Agent end-to-end query handling

---

## Tool Design and Safety Checks

The custom tool `query_ecommerce_database` is defined using LangChain's `@tool` decorator. It accepts a SQL query string and enforces the following safety rules before execution:

1. **SELECT-only check** — The query must start with `SELECT`. Any other statement is rejected immediately.
2. **Forbidden keyword scan** — The query is scanned for dangerous keywords: `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `REPLACE`. Any match triggers an error.
3. **Multi-statement prevention** — After stripping the trailing semicolon, the query is checked for any remaining semicolons. This prevents injection via stacked queries like `SELECT 1; DROP TABLE orders`.
4. **Output size limit** — Results are capped at 50 rows using `fetchmany(50)` to prevent large dumps.
5. **Graceful error handling** — All database errors are caught and returned as readable error strings. The application never crashes on a bad query or missing database file.

---

## Modern vs Legacy Implementation

### Modern LangChain (>= 1.0)

Uses `create_agent` from `langchain.agents` with a tool list and system prompt. The agent is invoked with:

```python
agent.invoke({"messages": [{"role": "user", "content": query}]})
```

### Legacy LangChain (< 1.0)

Uses `initialize_agent` with `AgentType.ZERO_SHOT_REACT_DESCRIPTION`. The agent is invoked with:

```python
agent.run(query)
```

The legacy implementation is clearly marked as a backward-compatibility demonstration. Both implementations share the same tool, database, and system prompt.

---

## Sample Questions

See [sample_queries.md](sample_queries.md) for 15 tested queries with actual SQL and expected responses.

Example:

> **User:** Which customer has spent the most money?
>
> **Agent:** The highest spending customer is Priya Sharma with a total completed purchase value of Rs. 11,500.

---

## Known Limitations

* The agent only answers questions that can be answered with a single SQL SELECT query. Complex multi-step reasoning across multiple tool calls may produce incomplete answers.
* The database uses text fields for dates. Date arithmetic (e.g., "last 30 days") depends on the LLM generating correct `strftime` syntax.
* The legacy implementation does not support streaming output.
* If the Groq API is unavailable or the rate limit is hit, the agent will return an error instead of an answer.

---

## Future Improvements

* Add a Streamlit web interface with a chat window and example queries sidebar.
* Support CSV export of tabular query results.
* Add LangSmith tracing for observability.
* Expand the database with more realistic data (hundreds of records).
* Add support for multi-table analytical queries with automatic query refinement if results are empty.
