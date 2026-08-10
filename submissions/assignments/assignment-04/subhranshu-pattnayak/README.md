# Assignment 04 - Database Query Agents

This repository contains two implementations of a natural language database query agent built using Large Language Models and SQL databases:

1. **Database Query Agent** - A modern implementation using an updated agent architecture.
2. **Legacy Database Query Agent** - A legacy implementation maintained for comparison and backward compatibility.

Both agents are designed to convert natural language questions into SQL queries and execute them against the Olist E-Commerce SQLite database.

---

## Repository Structure

```text
assignment-04
└── subhranshu-pattnayak
   ├── .gitkeep
   ├── README.md
   ├── ab.ipynb
   ├── database_query_agent
   │   ├── .env.example
   │   ├── .gitignore
   │   ├── .python-version
   │   ├── README.md
   │   ├── __init__.py
   │   ├── database
   │   │   ├── __init__.py
   │   │   ├── db_config.py
   │   │   ├── db_tools.py
   │   │   └── olist.sqlite (to be installed)
   │   ├── groq_client.py
   │   ├── pyproject.toml
   │   ├── requirements.txt
   │   ├── sql_agent.py
   │   ├── testing_agent.ipynb
   │   └── uv.lock
   │
   ├── legacy_database_query_agent
   │   ├── .env
   │   ├── .gitignore
   │   ├── .python-version
   │   ├── README.md
   │   ├── database
   │   │   ├── __init__.py
   │   │   ├── db_config.py
   │   │   ├── db_tools.py
   │   │   └── olist.sqlite (to be installed)
   │   ├── groq_client.py
   │   ├── legacy_sql_agent.py
   │   ├── pyproject.toml
   │   ├── requirements.txt
   │   ├── testing_agent.ipynb
   │   └── uv.lock
   ├── .gitkeep
   └── README.md
```

---

## Project Overview

The objective of this assignment is to explore how Large Language Models can interact with structured databases through agent-based workflows.

The repository contains two versions of a SQL agent:

### Modern Database Query Agent

Located in:

```text
database_query_agent/
```

Features:

* Modern agent architecture (langchain_groq v1).
* Natural language to SQL translation.
* Database tool integration.
* Modular design for extensibility.
* Designed for experimentation with contemporary agent patterns.

### Legacy Database Query Agent

Located in:

```text
legacy_database_query_agent/
```

Features:

* Legacy implementation of the SQL agent (langchain_groq below v1).
* Natural language query processing.
* SQL generation and execution.
* Useful for comparing architectural differences with the modern implementation.

---

## Dataset

Both projects use the **Olist E-Commerce SQLite Database**.

Download the dataset from:

https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database/data

After downloading:

1. Extract the database archive.
2. Copy `olist.sqlite` into the corresponding `database/` directory of each project if required.

Example:

```text
database_query_agent/database/olist.sqlite

legacy_database_query_agent/database/olist.sqlite
```

---

## Environment Setup

### Requirements

* Python 3.11 or lower (Python < 3.12 recommended)
* Groq API Key
* SQLite

### Install Dependencies

For either implementation:

```bash
pip install -r requirements.txt
```

or using UV:

```bash
uv add -r requirements.txt
```

---

## Running the Modern Agent

```python
from database_query_agent.sql_agent import SQLAgent

agent = SQLAgent(model_name)

response = agent(query)
print(response)
```

---

## Running the Legacy Agent

```python
from legacy_database_query_agent.legacy_sql_agent import SQLAgent

agent = SQLAgent(model_name)

response = agent(query)
print(response)
```

---

## Key Components

| Component             | Purpose                               |
| --------------------- | ------------------------------------- |
| `sql_agent.py`        | Modern SQL agent implementation       |
| `legacy_sql_agent.py` | Legacy SQL agent implementation       |
| `groq_client.py`      | LLM client integration                |
| `db_config.py`        | Database configuration                |
| `db_tools.py`         | Database utility functions and tools  |
| `testing_agent.ipynb` | Experimentation and testing notebooks |

---

## Learning Objectives

This assignment demonstrates:

* Natural Language to SQL conversion
* Agent-based database interaction
* Tool-calling workflows
* LLM integration with structured data
* Prompt engineering for database querying
* Comparison between legacy and modern agent architectures

---

## Additional Documentation

For implementation-specific details, refer to:

* `database_query_agent/README.md`
* `legacy_database_query_agent/README.md`

These documents contain setup instructions and implementation details specific to each agent.
