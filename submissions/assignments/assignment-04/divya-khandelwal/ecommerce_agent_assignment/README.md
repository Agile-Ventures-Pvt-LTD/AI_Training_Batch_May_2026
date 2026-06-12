# Ecommerce AI Agent Assignment

## Overview

This project demonstrates the implementation of an AI-powered Ecommerce Analytics Agent using LangChain.

The agent accepts natural language business questions from users, converts them into SQL queries, executes them on an Ecommerce SQLite database, and returns business-friendly responses.

The project contains two implementations:

1. Legacy LangChain Implementation (< 1.0)
2. Modern LangChain Implementation (>= 1.0)

---

# Project Architecture

User Question

↓

AI Agent

↓

SQL Generation

↓

Database Query Execution

↓

Business-Friendly Response

---

# Features

* Natural Language to SQL Conversion
* SQLite Database Integration
* SQL Safety Validation
* Business-Friendly Response Generation
* Legacy LangChain Implementation
* Modern LangChain Agent Implementation
* Tool Calling Architecture
* Modular Project Structure

---

# Database Schema

## customers

| Column      | Type    |
| ----------- | ------- |
| customer_id | INTEGER |
| name        | TEXT    |
| email       | TEXT    |
| city        | TEXT    |
| signup_date | DATE    |

---

## products

| Column         | Type    |
| -------------- | ------- |
| product_id     | INTEGER |
| name           | TEXT    |
| category       | TEXT    |
| price          | REAL    |
| stock_quantity | INTEGER |

---

## orders

| Column       | Type    |
| ------------ | ------- |
| order_id     | INTEGER |
| customer_id  | INTEGER |
| order_date   | DATE    |
| status       | TEXT    |
| total_amount | REAL    |

---

## order_items

| Column        | Type    |
| ------------- | ------- |
| order_item_id | INTEGER |
| order_id      | INTEGER |
| product_id    | INTEGER |
| quantity      | INTEGER |
| unit_price    | REAL    |

---

# Folder Structure

```text
ecommerce_agent_assignment/

│
├── app.py
├── app_modern.py
│
├── requirements-legacy.txt
├── requirements-modern.txt
│
├── data/
│   └── ecommerce.db
│
├── src/
│
│   ├── agents/
│   │   ├── legacy_agent.py
│   │   └── modern_agent.py
│
│   ├── db/
│   │   ├── connection.py
│   │   ├── schema_description.py
│   │   └── modern_schema_description.py
│
│   ├── prompts/
│   │   ├── system_prompt.py
│   │   └── modern_system_prompt.py
│
│   ├── tools/
│   │   ├── ecommerce_sql_tool.py
│   │   └── ecommerce_sql_tool_modern.py
│
└── .env
```

---

# Legacy Implementation

## Technologies Used

* LangChain 0.3.27
* LLMChain
* PromptTemplate
* ChatGroq
* SQLite
* Pandas

## Workflow

User Question

↓

SQL Generation Chain

↓

Generated SQL

↓

Database Tool

↓

SQL Result

↓

Answer Generation Chain

↓

Final Response

### Main Components

* legacy_agent.py
* ecommerce_sql_tool.py
* system_prompt.py

---

# Modern Implementation

## Technologies Used

* LangChain 1.x
* create_agent()
* Tool Calling
* ChatGroq
* SQLite
* Pandas

## Workflow

User Question

↓

Agent

↓

Tool Call

↓

Database Query

↓

Result

↓

Final Response

### Main Components

* modern_agent.py
* ecommerce_sql_tool_modern.py
* modern_system_prompt.py

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd ecommerce_agent_assignment
```

---

# Legacy Environment Setup

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

```bash
.\.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements-legacy.txt
```

Run application

```bash
python app.py
```

---

# Modern Environment Setup

Create virtual environment

```bash
python -m venv venv_modern
```

Activate environment

```bash
.\venv_modern\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements-modern.txt
```

Run application

```bash
python app_modern.py
```

---

# Sample Questions

## Product Queries

```text
Which products have stock below 10?
```

```text
Show all products in Electronics category.
```

```text
Which product is the most expensive?
```

---

## Order Queries

```text
How many pending orders exist?
```

```text
Show all completed orders.
```

```text
What is the total revenue generated from completed orders?
```

---

## Customer Queries

```text
How many customers are registered?
```

```text
Which customer placed the most orders?
```

---

## Join Queries

```text
Which customer spent the highest amount on orders?
```

```text
Show customer names along with their order count.
```

```text
What are the top 5 best-selling products?
```

---

# Security Features

* Only SELECT queries are allowed.
* Multiple SQL statements are blocked.
* Dangerous SQL operations are prohibited.

Blocked Operations:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* CREATE
* TRUNCATE

---

# Legacy vs Modern Comparison

| Feature           | Legacy               | Modern             |
| ----------------- | -------------------- | ------------------ |
| LangChain Version | < 1.0                | >= 1.0             |
| Core API          | LLMChain             | create_agent       |
| Tool Usage        | Manual               | Automatic          |
| Execution Method  | .run()               | .invoke()          |
| Workflow Control  | Developer Controlled | Agent Controlled   |
| Architecture      | Chain Based          | Tool Calling Agent |

