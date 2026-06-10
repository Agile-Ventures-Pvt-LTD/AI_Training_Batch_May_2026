# Assignment 04-LangChain + SQLite E-commerce Agent Assignment

## Participant Name

Simran Kaur

## Assignment / Project Title

LangChain + SQLite E-commerce Agent

## Description

This project demonstrates the development of an AI-powered SQL Agent using LangChain, Groq LLM, and SQLite.

The agent accepts natural language questions from users, automatically understands the database schema, generates SQL queries using an LLM, executes those queries on an SQLite database, and returns human-readable answers.

The project uses the Olist Brazilian E-commerce Dataset and implements both:

* Legacy Agent using LangChain 0.3.x
* Modern Agent using LangChain 1.x

The solution follows a modular architecture consisting of database utilities, schema extraction, SQL execution tools, prompts, agents, and tests.

## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ecommerce-agent-assignment
```

### 2. Create Virtual Environment

#### Legacy Agent Environment

```bash
uv venv .venv-legacy
```

Activate:

```bash
.venv-legacy\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements-legacy.txt
```

#### Modern Agent Environment

```bash
uv venv .venv-modern
```

Activate:

```bash
.venv-modern\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements-modern.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Application

```bash
python -m src.app
```

### 5. Run Tests

```bash
pytest
```

or

```bash
pytest tests/test_database.py
pytest tests/test_sql_tool.py
pytest tests/test_agent_queries.py
```

## Libraries / Packages Required

### Legacy Agent

```text
python-dotenv>=1.2.2
ipykernel>=7.2.0
groq>=0.30.0,<1.0.0
langchain==0.3.27
langchain-core>=0.3.75,<1.0.0
langchain-groq==0.3.8
langchain-experimental==0.3.4
pandas>=2.2.2
kagglehub>=0.3.13
pytest>=8.0.0
```

### Modern Agent

```text
python-dotenv>=1.2.2
ipykernel>=7.2.0
groq>=0.30.0,<1.0.0
langchain>=1.0.0
langgraph>=1.0.0
langchain-groq>=1.0.0
pandas>=2.2.2
kagglehub>=0.3.13
pytest>=8.0.0
```

## Assumptions Made

* The SQLite database file is available inside the `data/` directory.
* The database schema is extracted automatically from the SQLite database.
* The LLM generates valid SQL queries based on the provided schema.
* Users ask questions that can be answered using the available database tables and columns.
* A valid Groq API key is available through environment variables.
* The database is treated as read-only for analytical queries.

## Output Explanation

### Example User Query

```text
How many customers exist?
```

### Agent Workflow

```text
User Question
      |
      v
Schema-Aware LLM
      |
      v
Generated SQL Query
      |
      v
SQL Execution Tool
      |
      v
SQLite Database
      |
      v
Query Result
      |
      v
Final Answer
```

### Example Output

```text
There are 99,441 customers in the database.
```

The agent automatically converts the natural language question into SQL, executes it against the database, and presents the result in a human-readable format.
