# Credit Card Management System Agent

## Overview

Credit Card Management System Agent is an AI-powered assistant built using **LangGraph, LangChain, Groq LLM, and SQLite**.

The system follows a **Custom ReAct Agent architecture**, where the LLM understands user queries, selects the required tool, retrieves information from the database, and generates a final response.

The final response is also stored in JSON format for evaluation.

---

# Features

The agent supports the following operations:

- Inspect database schema
- Retrieve customer profile
- Retrieve card details
- Search transactions
- Get customer transaction history
- Generate statement summary
- Get reward summary
- Generate merchant spending summary
- Save final responses in JSON format

---

# Technology Stack

- **Programming Language:** Python
- **LLM Framework:** LangChain
- **Agent Framework:** LangGraph
- **LLM Provider:** Groq
- **Database:** SQLite
- **Environment Management:** python-dotenv

---

# Project Structure

ccms_langgraph_agent/

│
├── app.py
│ └── Main application file
│
├── custom_react_agent.py
│ └── Custom ReAct agent implementation using LangGraph
│
├── tools.py
│ └── Database tools used by the agent
│
├── db_utils.py
│ └── SQLite connection and query execution utilities
│
├── prompts.py
│ └── System prompt for agent behavior
│
├── config.py
│ └── Application configuration
│
├── database/
│ └── ccms.db
│
├── outputs/
│ ├── final_response.json
│ └── tool_outputs/
│
├── tests/
│ └── test_tools.py
│
├── requirements.txt
│
└── .env



---

# Agent Architecture

The agent follows a Custom ReAct workflow:

            User Query
                |
                v
          Agent Node
                |
      -------------------
      |                 |
      v                 v
   Tool Call        Final Response
      |
      v
 Tool Execution
      |
      v
Database Response
      |
      v
  Agent Node
      |
      v
  Final Answer

---

# Available Tools

## 1. Database Schema Inspection

Tool:


inspect_database_schema


Purpose:

- Retrieve database tables
- Retrieve column information
- Understand database structure


Example:


User:
Show database schema


---

## 2. Customer Profile

Tool:


get_customer_profile


Purpose:

Fetch customer details.

Input:


cust_id


Returns:

- Name
- Email
- Phone
- Address

---

## 3. Card Details

Tool:


get_card_details


Purpose:

Retrieve card information.

Input:


card_number


Returns:

- Card expiry
- Card type
- Security information

---

## 4. Transaction Search

Tool:


search_transactions


Purpose:

Search card transactions.

Input:


card_id
limit


Returns:

- Transaction ID
- Transaction date
- Amount

---

## 5. Customer Transactions

Tool:


get_customer_transaction


Purpose:

Retrieve customer transaction history.

---

## 6. Statement Summary

Tool:


get_statement_summary


Purpose:

Generate customer statement summary.

Returns:

- Spending information
- Transaction summary

---

## 7. Rewards Summary

Tool:


get_rewards_summary


Purpose:

Retrieve reward information.

Returns:

- Reward summary
- Spending based rewards

---

## 8. Merchant Spending Summary

Tool:


get_merchant_spend_summary


Purpose:

Analyze customer spending by merchant.

---


Create Virtual Environment
uv venv

Activate environment:

Windows
.venv\Scripts\activate

Install Dependencies
uv pip install -r requirements.txt
Environment Configuration

Create a .env file:

GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=llama-3.3-70b-versatile
Running the Application

Start the agent:

python app.py

Example:

==============================
 Credit Card Management Agent
 Type exit to stop
==============================


User:
Show database schema


Assistant:
The database contains customer, card, transaction tables...
Output Generation

Every query generates a JSON response.

Output location:

outputs/final_response.json

Example:

{
    "user_question": "show database schema",

    "implementation_choice":
    "custom_react_agent",

    "tools_used":
    [
        "inspect_database_schema"
    ],

    "records_found": 0,

    "answer":
    "Database contains 9 tables...",

    "sensitive_data_masked": true,

    "limitations": []
}
Database Schema

The system uses SQLite database containing:

customer

netbanking

card_type

card

transaction_type

transaction_terminal

merchant_type

merchant

transaction
Testing

Tool testing can be performed separately.

Run:

python -m tests.test_tools

The test files validate:

Tool execution
Database queries
Tool responses
Error Handling

The system handles:

Invalid inputs
Database errors
Missing parameters
Tool execution failures

Example:

Invalid customer id.
Please provide a valid customer id.
Security

The application follows basic security practices:

API keys stored using environment variables
Sensitive information masking
Parameterized SQL queries
Input validation

