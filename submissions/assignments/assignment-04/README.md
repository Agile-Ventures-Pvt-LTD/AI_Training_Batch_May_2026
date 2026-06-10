# E-Commerce AI Agent using LangChain and SQLite

## Project Overview

This project was developed as part of the LangChain + SQLite E-Commerce Agent assignment.

The goal of the project is to build an AI-powered assistant that can answer business-related questions using natural language and data stored in an SQLite database. Instead of writing SQL queries manually, users can ask questions in plain English, and the agent generates the required SQL query, retrieves data from the database, and presents the answer in a user-friendly format.

Examples:

* Which customers are from Delhi?
* How many pending orders are there?
* Which products have stock below 10?
* Which customer has spent the most money?
* Show top 5 products by price.

The project includes both Legacy and Modern LangChain implementations to understand and compare the evolution of LangChain agent architectures.

---

# Objective

The main objectives of this project are:

* Build an AI agent capable of interacting with an SQLite database.
* Convert natural language questions into SQL queries.
* Restrict unsafe database operations.
* Implement both legacy and modern LangChain approaches.
* Compare the behavior of different LangChain versions.
* Provide a simple command-line interface for interacting with the agent.

---

# Technology Stack

## Programming Language

* Python 3.11

## Database

* SQLite

## AI Framework

* LangChain

## LLM

* Groq
* Llama 3.3 70B Versatile

## Additional Libraries

* pandas
* python-dotenv
* langchain-community
* langchain-groq

---

# Data Generation

The database is populated using a custom seeding script.

Generated data includes:

* 10 customers
* 15 products
* 25 orders
* 40+ order items

The dataset was intentionally kept small for testing and demonstration purposes.

---

# SQL Security Measures

One of the key requirements of the assignment was preventing unsafe database access.

The custom SQL tool validates every generated query before execution.

The following operations are blocked:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE
* CREATE
* REPLACE

Only SELECT queries are allowed.

Multiple SQL statements are also blocked to reduce the risk of SQL injection attempts.

Example:

```sql
DROP TABLE customers;
```

Result:

```text
Only SELECT queries are allowed.
```

---

# LangChain Implementations

## 1. Modern Implementation

Environment:

```text
langchain >= 1.0
```

Key Feature:

Uses the modern LangChain agent architecture.

Main File:

```text
src/agents/modern_agent.py
```

Advantages:

* Current LangChain standard
* Better tool calling support
* Cleaner architecture
* Easier future maintenance

---

## 2. Legacy Implementation

Environment:

```text
langchain < 1.0
```

Main File:

```text
src/agents/legacy_agent.py
```

Purpose:

The assignment documentation discussed both legacy and modern LangChain approaches. To better understand the differences between the two architectures, both implementations were created and tested separately.

Challenges encountered included API differences, agent initialization changes, and model compatibility issues.

---


# Sample Queries Tested

The following queries were tested successfully.

1. Which customers are from Delhi?
2. Show top 5 products by price.
3. Which products have stock below 10?
4. How many pending orders are there?
5. Which customer has spent the most money?
6. Show all completed orders.
7. Show all cancelled orders.
8. Which products belong to Electronics category?
9. What is the average product price?
10. Which city has the most customers?
11. Show all orders placed in 2025.
12. What is the total revenue generated?
13. Show top-selling products.
14. Which customers signed up after March 2024?
15. Show products with stock less than 5.

---

# Challenges Faced

During development, several challenges were encountered:

1. Managing compatibility differences between LangChain legacy and modern versions.

2. Understanding changes in agent creation APIs across LangChain releases.

3. Configuring Groq models for tool calling.

4. Handling deprecation warnings in legacy implementations.

5. Ensuring generated SQL remained safe and read-only.

6. Managing multiple virtual environments for testing both implementations.

7. Debugging import path issues caused by project structure and package resolution.

These issues were resolved through testing, version-specific implementations, and incremental validation.

---

# Future Improvements

Some enhancements that can be added in future versions:

* Streamlit-based web interface
* User authentication
* Query history logging
* Support for PostgreSQL and MySQL
* Interactive dashboards
* Data visualization and analytics
* Role-based access control
* Export query results to CSV or Excel

---

# Learning Outcomes

Through this project, I gained practical experience with:

* LangChain agents
* Tool calling
* Prompt engineering
* SQLite integration
* SQL query validation
* Groq LLM integration
* Agent architecture differences across LangChain versions
* Virtual environment management
* Building AI-powered database applications

---

# Conclusion

This project demonstrates how Large Language Models can be integrated with structured databases to create natural language interfaces for business analytics.

By implementing both legacy and modern LangChain approaches, I was able to understand how agent architectures have evolved while maintaining the same business objective: enabling users to retrieve meaningful insights from an e-commerce database using simple natural language questions.
