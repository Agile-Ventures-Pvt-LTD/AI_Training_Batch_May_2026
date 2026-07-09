# E-Commerce Agent Assignment

## Overview

This project contains **two implementations**:

### Modern Version

* LangChain >= 1.0
* Environment: `.venv`
* Entry File: `src/app.py`

### Legacy Version

* LangChain 0.3.27
* Python 3.11
* Environment: `v1`
* Entry File: `src/app_legacy.py`

---

# Project Structure

```text
ecommerce-agent-assignment/
│
├── .venv/                        # Modern Environment
├── v1/                           # Legacy Environment
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

# Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

# MODERN VERSION

## Activate Environment

Git Bash

```bash
source .venv/Scripts/activate
```

Verify Version

```bash
python -c "import langchain; print(langchain.__version__)"
```

Expected:

```text
1.x.x
```

Install Packages

```bash
uv pip install -r requirements-modern.txt
```

Run Application

```bash
python -m src.app
```

Exit Application

```text
exit
```

or

```text
quit
```

Deactivate

```bash
deactivate
```

---

# LEGACY VERSION

## Activate Environment

Git Bash

```bash
source v1/Scripts/activate
```

Verify Python Version

```bash
python --version
```

Expected:

```text
Python 3.11.x
```

Verify LangChain Version

```bash
python -c "import langchain; print(langchain.__version__)"
```

Expected:

```text
0.3.27
```

Install Packages

```bash
uv pip install -r requirements-legacy.txt
```

Run Application

```bash
python -m src.app_legacy
```

Exit Application

```text
exit
```

or

```text
quit
```

Deactivate

```bash
deactivate
```

---

# requirements-modern.txt

```txt
langchain>=1.0.0
langchain-community>=0.3.0
langchain-groq>=0.3.0

python-dotenv>=1.0.0
faker>=37.0.0

pandas>=2.2.0
tabulate>=0.9.0

pytest>=8.0.0
```

---

# requirements1.txt

```txt
langchain==0.3.27
langchain-community==0.3.27
langchain-core==0.3.72

langchain-groq>=0.3.0
groq>=0.31.0

python-dotenv>=1.0.0
faker>=37.0.0

pandas>=2.2.0
tabulate>=0.9.0

fastapi>=0.115.0
uvicorn>=0.35.0

pytest>=8.0.0
```

---

# Database Setup

Create Database

```bash
python scripts/create_database.py
```

Seed Database

```bash
python scripts/seed_database.py
```

---

# Sample Queries

```text
What is the total revenue from completed orders?

Which customer spent the most money?

Show top 5 products by quantity sold.

Show total sales by product category.

Which products have stock below 10?

What is the average order value?

Which city has the highest number of customers?

Which customers have placed more than 2 orders?

Show all cancelled orders.

Which product has never been ordered?
```

```

---

# Git Ignore

```gitignore
.venv/
v1/

__pycache__/
*.pyc

.env

logs/
```

---

# Version Summary

| Version | Environment | LangChain | Run Command              |
| ------- | ----------- | --------- | ------------------------ |
| Modern  | .venv       | >=1.0     | python -m src.app        |
| Legacy  | v1          | 0.3.27    | python -m src.app_legacy |

Both versions use the same:

* SQLite Database
* Database Tool
* Prompts
* Schema
* Seed Data

Only the Agent and App files differ between versions.
