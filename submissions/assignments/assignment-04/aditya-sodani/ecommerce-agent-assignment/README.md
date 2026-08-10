# E-Commerce AI Database Agent

## Overview

This project implements an AI-powered E-Commerce Database Agent that allows users to interact with an e-commerce database using natural language queries.

The system leverages Large Language Models (LLMs), LangChain agents, SQL tools, and SQLite to convert business questions into SQL queries and provide meaningful insights from the database.

The project contains two implementations:

* **Legacy Agent** – Built using traditional LangChain Agent architecture.
* **Modern Agent** – Built using the latest LangChain agent patterns and best practices.

---

## Features

* Natural language querying of e-commerce data
* Automated SQL query generation
* Database schema awareness
* Business analytics and reporting
* Legacy and Modern agent implementations
* Conversation logging
* SQLite-based data storage
* Modular and extensible architecture

---

## Project Structure

```text
ecommerce-agent-assignment/
│
├── .venv/                        # Legacy Environment
├── v1/                           # Modern Environment
│
├── requirements-modern.txt
├── requirements-legacy.txt
├── .env
│
├── data/
│   └── ecommerce.db
│
├── logs/
│
├── scripts/
│   ├── create_database.py
│   └── seed_database.py
│
└── src/
    │
    ├── app.py
    ├── app_legacy.py
    │
    ├── agents/
    │   ├── modern_agent.py
    │   └── legacy_agent.py
    │
    ├── db/
    │   ├── connection.py
    │   └── schema_description.py
    │
    ├── tools/
    │   └── ecommerce_sql_tool.py
    │
    └── prompts/
        └── system_prompt.py
```

---

## Technology Stack

* Python 3.11
* LangChain
* SQLite
* OpenAI / LLM Provider
* SQL Database Toolkit
* Python Dotenv

---

## Setup Instructions

### 1. Create Virtual Environment

Using uv:

```bash
uv venv --python 3.11     #legacy_agent
uv venv v1 --python 3.11    #modern_agent
```

Activate environment:

#### Windows

```bash
.venv\Scripts\activate
v1\Scripts\activate
```

---

### 3. Install Dependencies

For Modern Agent:

```bash
uv pip install -r requirements-modern.txt
```

For Legacy Agent:

```bash
uv pip install -r requirements-legacy.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Replace with your actual API key.

---

## Database Setup

### Create Database

```bash
python scripts/create_database.py
```

### Seed Sample Data

```bash
python scripts/seed_database.py
```

This creates and populates the SQLite database located at:

```text
data/ecommerce.db
```

---

## Running the Application

### Modern Agent

```bash
python -m src.app_modern
```

### Legacy Agent

```bash
python -m src.app_legacy
```

---

## Example Queries

Users can ask questions such as:

```text
Show the top 5 products by quantity sold.
```

```text
What are the highest revenue generating products?
```

```text
Which customers placed the most orders?
```

```text
Show monthly sales trends.
```

```text
What is the total revenue generated?
```

---

## Components

### Agents

#### Modern Agent

Located in:

```text
src/agents/modern_agent.py
```

Uses modern LangChain patterns for improved maintainability and performance.

#### Legacy Agent

Located in:

```text
src/agents/legacy_agent.py
```

Implements the traditional LangChain Agent architecture.

---

### SQL Tool

Located in:

```text
src/tools/ecommerce_sql_tool.py
```

Responsible for:

* Executing SQL queries
* Returning database results
* Serving as the bridge between the agent and SQLite database

---

### Database Layer

Located in:

```text
src/db/
```

Provides:

* Database connection management
* Schema descriptions
* Query execution support

---

## Logs

Conversation history and execution logs are stored inside:

```text
logs/
```

This helps with debugging and auditing agent interactions.

---

##
