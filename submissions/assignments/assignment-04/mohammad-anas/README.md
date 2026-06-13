# LangChain + SQLite E-commerce Agent

**Paricipant - Mohammad Anas**

## Project Overview
This project is an AI-powered database assistant built using Python and LangChain. It allows users to query an SQLite e-commerce database using natural language. The agent translates plain English questions into safe SQL queries, executes them, and returns business-friendly answers. 

## Business Use Case
In an e-commerce company, business teams often need data (like total revenue, top customers, or low stock products) but they do not know SQL. They usually have to wait for developers to fetch this data. This AI agent solves that problem by acting as a bridge between the business users and the database.

## Technology Stack
- **Language:** Python
- **Framework:** LangChain (Both `<1.0` Legacy and `>=1.0` Modern approaches are implemented)
- **Database:** SQLite3
- **LLM:** Groq / openai/gpt-oss-120b
- **Libraries:** python-dotenv, langchain-community, langchain-groq, langchain_classic

## Database Schema
The SQLite database (`ecommerce.db`) consists of 4 tables:
1. **customers:** `customer_id`, `name`, `email`, `city`, `signup_date`
2. **products:** `product_id`, `name`, `category`, `price`, `stock_quantity`
3. **orders:** `order_id`, `customer_id`, `order_date`, `status`, `total_amount`
4. **order_items:** `order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price`

## Setup Instructions
1. Clone this repository to your local machine.
2. It is recommended to create two separate virtual environments to test both LangChain versions:
   - `python -m venv legacy_env`
   - `python -m venv modern_env`

## Environment Variables Required
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## How to Create and Seed the Database

Before running the agent, you need to generate the database and fill it with sample data.
Run these commands from the root directory:

```bash
python scripts/create_database.py
python scripts/seed_database.py
```

This will create ``ecommerce.db`` inside the ``data/`` folder.

## How to Run the Agents
Running the Modern Agent (LangChain >= 1.0)
Activate your modern virtual environment and install dependencies:

```bash
uv add -r requirements-modern.txt
python src/agents/modern_agent.py
```

## Using the Main App Menu 
You can easily switch between both versions using the main app interface:
```bash
python src/app.py
```

## Sample Questions

1. You can ask the agent questions like:

2. What is the total revenue from completed orders?

3. Which customer has spent the most money?

4. Which products have stock below 10?

5. Show total sales by product category.

## Security and Safety Checks

The custom tool ``(ecommerce_sql_tool.py)`` includes safety measures:

Only ``SELECT`` queries are allowed. ``INSERT``, ``DROP``, ``DELETE`` will be blocked.

Results are limited to ``50 rows`` to prevent context window overflow.

Database errors are caught and handled gracefully without crashing the app.

## Known Limitations

1. The agent currently cannot handle very complex multi-table joins if the schema relationship is not clearly understood by the LLM.

2. It does not remember chat history (memory is not implemented yet).

## Future Improvements

1. Add memory to allow follow-up questions.

2. Build a web interface using Streamlit.

3. Implement logging and LangSmith tracing for better debugging.