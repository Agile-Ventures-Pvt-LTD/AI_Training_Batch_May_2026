# Database Query Agent

This project implements a query agent for interacting with a library. The agent is designed to accept natural language queries and translate them into database actions or SQL queries that can retrieve the requested information from modern systems.

## Overview

- Uses an modern agent-based approach to interpret user intents and execute database operations.
- Intended as an assignment project for exploring database integration and query automation.

## Project Structure

├── .env\
├── .python-version\
├── README.md\
├── database\
│&emsp;   ├── __init__.py\
│&emsp;   ├── db_config.py\
│&emsp;   ├── olist.sqlite(to be installed)\
│&emsp;   └── db_tools.py\
├── groq_client.py\
├── .gitignore\
├── sql_agent.py\
├── pyproject.toml\
├── requirements.txt\
└── testing_agent.ipynb\

- `README.md` - project overview, setup, and usage instructions.
- `groq_client.py` - client module for querying with the legacy library and handling llm client actions.
- `sql_agent.py` - agent logic for converting natural language requests into SQL queries.
- `main.py` - application entrypoint for running the legacy database query agent.
- `requirements.txt` - list of Python dependencies required by the project.
- `database/` - helper modules for database configuration and database tools that could be accessed by the agent.
- Configuration or environment files - modern database connection settings and environment variables.

## Setup

1. Before setup make sure python is below v3.12, then install required dependencies for the project.

&emsp;&emsp;&emsp;`pip install -r requirements.txt`

&emsp;&emsp;&emsp;or for uv ecosystem:

&emsp;&emsp;&emsp;`uv add -r requirements.txt`

2. Go to 'https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database/data' and download the .sqlite database as zip into database directory and then extract it there.

3. Run the agent.

&emsp;&emsp;&emsp;`from database_query_agent.sql_agent import SQLAgent`

&emsp;&emsp;&emsp;`agent = SQLAgent(model_name)`

&emsp;&emsp;&emsp;`response = agent(query)`

## Usage

- Use the agent entrypoint to submit natural language queries.
- The agent parses requests and generates appropriate database commands.

## Notes

- This README is based on the project intent and typical structure of a database query agent.
- Adjust configuration and usage sections based on the actual implementation files in the repository.
