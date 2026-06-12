# Ecommerce Database Agent using LangChain

## Project Overview

This project demonstrates the implementation of an AI-powered Ecommerce Database Agent capable of answering business questions using natural language.

The agent converts user questions into SQL queries, retrieves data from a SQLite database, and returns business-friendly insights.

The project showcases both:

* Legacy LangChain Agent Architecture
* Modern LangChain Agent Architecture

while enforcing SQL security and database safety.

---

## Objectives

The goal of this project is to:

* Query an Ecommerce SQLite database using natural language.
* Convert user questions into SQL statements.
* Execute only safe SELECT queries.
* Prevent destructive database operations.
* Demonstrate both older and newer LangChain agent implementations.
* Provide business-friendly responses based on database results.

---

## Features

### Natural Language to SQL

Users can ask questions such as:

* What is total revenue?
* Who is the highest spending customer?
* Show products with low stock.
* How many pending orders exist?

The agent automatically generates SQL and retrieves the required information.

---

### SQL Security Validation

The application prevents execution of dangerous SQL statements.

Blocked Operations:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE
* CREATE
* REPLACE

Additional Protections:

* Multiple SQL statement prevention
* SQL comment removal
* Read-only query execution
* Automatic LIMIT enforcement

---

### LangChain Implementations

#### Legacy Agent

Uses:

* initialize_agent()
* AgentType.ZERO_SHOT_REACT_DESCRIPTION

Demonstrates the traditional LangChain architecture.

---

#### Modern Agent

Uses:

* create_agent()
* Native Tool Calling
* Structured Agent Workflow

Demonstrates LangChain 1.x architecture.

---

## Technology Stack

| Component   | Technology |
| ----------- | ---------- |
| LLM         | Groq       |
| Framework   | LangChain  |
| Database    | SQLite     |
| Language    | Python     |
| Environment | dotenv     |
| Testing     | Python     |

---

## Project Structure

```text
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
│   │
│   ├── agents/
│   │   ├── modern_agent.py
│   │   └── legacy_agent.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   └── schema_description.py
│   │
│   ├── prompts/
│   │   └── system_prompt.py
│   │
│   ├── tools/
│   │   └── ecommerce_sql_tool.py
│   │
│   └── app.py
│
├── tests/
│   ├── test_database.py
│   ├── test_sql_tool.py
│   └── test_agent_queries.py
│
├── sample_queries.md
├── requirements.txt
├── .env
└── README.md
```

---

## Database Schema

The Ecommerce database contains four tables:

### customers

Stores customer information.

Columns:

* customer_id
* name
* email
* city
* signup_date

---

### products

Stores product information.

Columns:

* product_id
* name
* category
* price
* stock_quantity

---

### orders

Stores customer orders.

Columns:

* order_id
* customer_id
* order_date
* status
* total_amount

---

### order_items

Stores order line items.

Columns:

* order_item_id
* order_id
* product_id
* quantity
* unit_price

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ecommerce-agent-assignment
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Database Setup

### Create Database

```bash
python scripts/create_database.py
```

### Seed Database

```bash
python scripts/seed_database.py
```

---

## Running the Application

### Command Line Interface

```bash
python -m src.app
```

---

### Streamlit Interface

```bash
streamlit run streamlit_app.py
```

---

## Running Tests

### Database Tests

```bash
python -m tests.test_database
```

---

### SQL Tool Tests

```bash
python -m tests.test_sql_tool
```

---

### Agent Query Tests

```bash
python -m tests.test_agent_queries
```

---

## Sample Questions

### Customer Analysis

* How many customers exist?
* Show customers from Delhi.
* Which customer spent the most?

### Product Analysis

* Show products with low stock.
* List all Electronics products.
* Which products sell the most?

### Revenue Analysis

* What is total revenue?
* Show monthly revenue.
* Show revenue by category.

### Order Analysis

* Show pending orders.
* Show cancelled orders.
* What is the average order value?

More examples are available in:

```text
sample_queries.md
```

---

## Security Controls

The system implements the following protections:

### Allowed

```sql
SELECT * FROM customers
```

### Blocked

```sql
DELETE FROM customers
```

```sql
DROP TABLE orders
```

```sql
UPDATE products SET price = 0
```

```sql
ALTER TABLE customers ADD COLUMN age INTEGER
```

---

## Example Workflow

### User Question

```text
Who is the highest spending customer?
```

### Agent Action

1. Understands the question.
2. Generates SQL query.
3. Executes query through database tool.
4. Retrieves results.
5. Returns business-friendly response.

### Example Response

```text
Rohan Mehta is the highest spending customer with total purchases of ₹42,500.
```

---

## Key Learnings

This project demonstrates:

* LangChain Agent Development
* Tool Calling
* Natural Language to SQL
* SQLite Integration
* Prompt Engineering
* Agent Security Controls
* Legacy vs Modern LangChain Architectures

---

## Future Enhancements

* Query history tracking
* Visualization dashboards
* Multi-database support
* Authentication and access control
* Query explanation mode
* Advanced analytics capabilities

---

## Author

Ashish Sinha

