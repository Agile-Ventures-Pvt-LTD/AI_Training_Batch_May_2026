## Submitted By

**Name:** Palak Jhamb

---

## Assignment Name

**LangChain + SQLite E-commerce Agent Assignment**

---

## Project Description

This project implements an AI-powered E-commerce Database Assistant using LangChain and SQLite.

The assistant is capable of:

* Understanding user questions in natural language.
* Converting user questions into SQL queries using a Large Language Model (LLM).
* Querying a local SQLite database containing e-commerce data.
* Retrieving relevant information from the database.
* Returning business-friendly responses based on the retrieved data.

The project demonstrates both:

1. **Legacy LangChain Agent Implementation (< 1.0)**
2. **Modern LangChain Agent Implementation (>= 1.0)**

The database contains the following tables:

* customers
* products
* orders
* order_items

The agent dynamically receives the database schema and uses it to generate valid SQL queries.

---

## Project Structure

```text
Palak-Jhamb/
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
│   ├── agents/
│   │   ├── legacy_agent.py
│   │   └── modern_agent.py
│   │
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   └── app.py
│
├── tests/
│   ├── test_database.py
│   ├── test_sql_tool.py
│   └── test_agent_queries.py
│
├── requirements-legacy.txt
├── requirements-modern.txt
└── README.md
```

---

## Architecture

```text
User Question
      ↓
LLM Agent
      ↓
Generate SQL Query
      ↓
SQLite Tool
      ↓
Execute Query
      ↓
Database Result
      ↓
LLM
      ↓
Business-Friendly Answer
```

---

## Steps to Run the Project

### 1. Clone the Repository

```bash
git clone <repository_url>
cd Palak-Jhamb
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:


```bash
.venv\Scripts\activate
```


---

### 3. Install Dependencies

For Legacy LangChain:

```bash
pip install -r requirements-legacy.txt
```

For Modern LangChain:

```bash
pip install -r requirements-modern.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

### 5. Create Database

```bash
python scripts/create_database.py
```

---

### 6. Populate Sample Data

```bash
python scripts/seed_database.py
```

---

### 7. Run the Application

Legacy Agent:

```bash
python -m src.app
```

Modern Agent:

```bash
python -m src.app_modern
```



## Required Libraries

### Core Libraries

* langchain
* langchain-community
* langchain-groq
* groq
* python-dotenv

### Database

* sqlite3 (built-in)

### Testing

* pytest

---

## Assumptions Made

1. Only **SELECT** queries are allowed.
2. Database modification queries are prohibited:

   * INSERT
   * UPDATE
   * DELETE
   * DROP
   * ALTER
   * TRUNCATE
3. Database schema remains fixed during execution.
4. User asks business-related questions about the e-commerce database.
5. The LLM has access to the database schema through the system prompt.
6. The SQLite database file exists in the `data/` folder.

---

## Example 

```text
How many customers are registered?
```

Example Response:

```text
There are 10 registered customers in the database.
```



## Output Explanation

The agent performs the following steps:

1. Receives a user query.
2. Uses the database schema provided in the system prompt.
3. Generates a valid SQLite SELECT query.
4. Executes the query through a custom database tool.
5. Retrieves results from the SQLite database.
6. Generates a business-friendly response.

Example execution:

```text
User:
Is there any order for Amit Verma?

Generated SQL:
SELECT o.order_id, o.order_date, o.status, o.total_amount
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
WHERE c.name = 'Amit Verma';

Database Result:
[(2, '2025-12-25', 'cancelled', 3189.16)]

Assistant:
Yes, Amit Verma has placed orders in the system.
```

---

## Features Implemented

* SQLite database integration
* Dynamic schema extraction
* Custom SQL execution tool
* SQL query validation
* Legacy LangChain agent implementation
* Modern LangChain agent implementation
* Business-friendly response generation
* Modular project structure
* Secure read-only database access

