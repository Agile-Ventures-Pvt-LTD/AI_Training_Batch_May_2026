# Project Structure

ecommerce-agent-assignment/
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
│   │
│   ├── agents/
│   │   ├── modern_agent.py
│   │   └── legacy-agent.py
│   │
│   ├── tools/
│   │   └── ecommerce_sql_tool.py
│   │
│   └── prompts/
│       └── system_prompt.py
│
├── requirements.txt
├── .env
├── README.md
│
├── .venv
└── .venv-legacy

#  Database Schema

## Prodcuts
customer_id
name
email
city
created_at

## Orders
order_id
customer_id
order_date
status
total_amount

## Order Items
order_item_id
order_id
product_id
quantity
unit_price

# Environment Setup
## Create Modern Environment
python -m venv .venv

## Activate moden environment
.venv-legacy\Scripts\activate

## Install modern dependencies
pip install -r requiremnents.txt

## Create legacy environment
python -m venv .venv-legacy

## Activate legacy environment
.venv-legacy\Scripts\activate

## Install legacy dependencies
pip install -r requiremnents-legacy.txt

## Install dependencies(Modern)
pip install langchain>=0.1
pip install langchain-community
pip install langchain-groq
pip install sqlalchemy
pip install faker

## Install legacy dependencies(Legacy)
pip install langchain<0.1
pip install langchain-community
pip install langchain-groq
pip install sqlalchemy
pip install faker

## Create a .env file
GROQ_API_KEY=your_groq_api_key

# Database Creation
## Create database
python scripts/create_database.py

## Seeding database
python scripts/seed_database.py

# Modern Agent (LangChain 1.x)
## Description

The modern implementation uses:

LangChain 1.x
create_agent()
Custom SQL Tool
Prompt-based control

The agent generates SQL queries and executes them through a secure custom database tool.

Advantages
More flexible
Easier tool customization
Better for production systems
Uses latest LangChain architecture
Security

Only SELECT queries are allowed.

# Legacy Agent (LangChain 0.3)
## Description

The legacy implementation uses:

LangChain 0.3
create_sql_agent()
SQLDatabase Toolkit
Automatic schema inspection

The agent automatically:

Discovers tables
Reads schema
Generates SQL
Executes SQL
Returns Answer

# Key Learnings

Difference between modern and legacy LangChain agents
Natural language to SQL generation
Secure database access with LLMs
Tool calling architecture
SQL Agent Toolkit usage
Groq LLM integration
SQLite database operations

# Author

Vaishnavi Gupta

AI / GenAI Developer Project – Ecommerce SQL Agent using LangChain and Groq.