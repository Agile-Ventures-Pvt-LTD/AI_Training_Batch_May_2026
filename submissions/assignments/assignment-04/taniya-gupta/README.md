# Assignment 04 : E-Commerce Database Assistant using LangChain and SQLite

## Name
Taniya gupta

## Project Overview

This project is an AI-powered E-Commerce Database Assistant that allows users to query an SQLite database using natural language. Instead of writing SQL queries manually, users can ask business questions in plain English and receive accurate, business-friendly responses.


---

## Technology Stack

### Backend

* Python 3.11+
* SQLite

### AI & Agent Framework

* LangChain
* LangChain Community
* LangChain Groq
* Groq LLM API

### Utilities

* python-dotenv

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

## Project Structure

```text
assignment-04/taniya-gupta

├── README.md
├── .env.examples
├── requirements-legacy.txt
├── requirements-modern.txt

├── data/
│   └── ecommerce.db

├── scripts/
│   ├── create_database.py
│   └── seed_database.py

├── src/
│   ├── agents/
│   │   ├── legacy_agent.py
│   │   └── modern_agent.py
│   │
│   ├── db/
│   │   └── connection.py
│   │
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   ├── tools/
│   │   └── ecommerce_sql_tool.py
│   │
│   └── app.py

└── sample_queries.md
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Installation

### Clone Repository

```bash
git clone <repo_url>
cd assignment-04
```

---

## Legacy LangChain Setup

Create virtual environment:

```bash
python -m venv legacy
legacy\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements-legacy.txt
```

Run application:

```bash
python -m src.app legacy
```

---

## Modern LangChain Setup

Create virtual environment:

```bash
python -m venv modern
modern\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements-modern.txt
```

Run application:

```bash
python -m src.app modern
```

---

## Creating the Database

Create tables:

```bash
python scripts/create_database.py
```

Seed sample data:

```bash
python scripts/seed_database.py
```

This creates:

```text
data/ecommerce.db
```

---

## Sample Questions

* What is the total revenue from completed orders?
* Which customer has spent the most money?
* Show the top 5 products by quantity sold.
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
* Show total sales by product category.

---

## Future Improvements

* Streamlit UI
* LangSmith tracing
* Conversation memory

---

**NOTE:** All test cases mentioned in files in test folder have been passed succesfully. All requirements mentioned in the assignment have been implemented succesfully.

## Author

Taniya Gupta
