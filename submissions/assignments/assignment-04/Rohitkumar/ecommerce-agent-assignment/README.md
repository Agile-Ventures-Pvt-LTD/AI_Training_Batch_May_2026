# LangChain + SQLite E-commerce Agent Assignment

## 1. Project Overview
This project is an AI-powered E-commerce query system built using LangChain, SQLite, and Groq LLM. It allows users to ask natural language questions about an e-commerce database and get SQL-based analytical answers. The system supports both legacy and modern LangChain implementations.



## 2. Business Use Case
This system is designed for e-commerce analytics and business intelligence. It can be used to analyze revenue, track product stock, monitor order status, and extract customer insights using natural language queries instead of writing SQL manually.



## 3. Technology Stack
Python, SQLite, LangChain, Groq API, UV package manager, dotenv.


## 4. Database Schema
The database consists of the following tables:

customers(customer_id, name, email, city, signup_date)

products(product_id, name, category, price, stock_quantity)

orders(order_id, customer_id, order_date, status, total_amount)

order_items(order_item_id, order_id, product_id, quantity, unit_price)


## 5. Setup Instructions

Create virtual environments:

Legacy:
uv venv .venv-legacy
.\.venv-legacy\Scripts\activate
uv pip install -r requirements-legacy.txt

Modern:
uv venv .venv-modern
.\.venv-modern\Scripts\activate
uv pip install -r requirements-modern.txt



## 6. Create and Seed Database

Run the following commands:

python scripts/create_database.py
python scripts/seed_database.py

This will create and populate the SQLite database with sample data.


## 7. Run Legacy LangChain Version

The legacy version uses initialize_agent and AgentType.ZERO_SHOT_REACT_DESCRIPTION.
activate the legacy virtual environment: . venv-legacy\Scripts\activate   

Run:

uv run python -m src.app

Select:
legacy


## 8. Run Modern LangChain Version

The modern version uses create_tool_calling_agent with structured tool calling.
activate the modern virtual environment
Run:
uv run python -m src.app

Select:
modern



## 9. Environment Variables Required

Create a .env file with:

GROQ_API_KEY=your_groq_api_key_here



## 10. Sample Questions
supportive queries are mentioned at sample_queries.md
Here are some:

What is the total revenue from completed orders
Show top 5 products by sales
List customers from a specific city
Show products with stock below 10
Show pending orders

-

## 11. Known Limitations

Legacy agent may generate incorrect SQL if schema is not strictly followed. Groq model limitations may occasionally cause parsing issues. SQLite does not support advanced enterprise-level analytics. No authentication system is implemented.



## 12. Future Improvements

Add LangGraph-based agent architecture. Improve SQL validation and correction mechanism. Add caching for frequent queries. Build a frontend dashboard using Streamlit or React. Extend support for PostgreSQL and MySQL. Improve schema-aware prompting for better accuracy.