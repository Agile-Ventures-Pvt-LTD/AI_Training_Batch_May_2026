## Project Build: Credit Card Management System Agent Using LangGraph, Groq, Tools, and SQLite

# 1. Project Title
AI Credit Card Management Agent Using LangGraph, Groq, Tools, and SQLite

# 2. Project Objective
The objective of this project is to build an AI-powered Credit Card Management System Agent using LangGraph, Groq, SQLite, and custom tools that can answer both operational and analytical questions about credit card data stored in the ccms.db database.

# 3. Project File Structure

ccms_langgraph_agent/
│
├── app.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── prebuilt_agent.py
├── custom_react_agent.py
├── output_formatter.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ └── ccms.db
│
├── outputs/
│ ├── sample_prebuilt_agent_run.txt
│ └── sample_custom_agent_run.txt
│
└── tests/
 └── test_tools.py


# 4. Implementation Approch

This project provides two implementation choices for building the AI Credit Card Management System Agent:

### Choice 1: LangGraph Pre-built ReAct Agent

A LangGraph pre-built ReAct agent that leverages LangGraph's built-in tool-calling capabilities to automatically perform reasoning, select appropriate tools, execute database operations, and generate final responses.

### Choice 2: Custom LangGraph ReAct Agent

A custom ReAct workflow built using LangGraph's StateGraph architecture, where agent behavior is explicitly defined through states, nodes, edges, and conditional routing between the agent, tools, and reflection components.

For this project, both implementation approaches were developed and evaluated. The same SQLite database (ccms.db), Groq LLM, and custom database tools were used across both implementations to ensure a fair comparison.


# 5. Setup Instruction
 
## Create Virtual Environment

uv venv --python 3.11

## Activate Virtual Environment

.venv\Scripts\activate

## Install Dependencies

uv pip install -r requirements.txt

## Configure Environment Variables

create .env

.env contains :-
GROQ_API_KEY=your_groq_api_key 
GROQ_MODEL=llama-3.1-8b-instant
DB_PATH=data/ccms.db

# 6. Database Setup

Place the provided database file inside:

data/ccms.db

Verify the database exists before running the application.

# 7. Running the Application

# 1--> for prebuilt react agent
   run "python app.py" command on terminal

   outputs will be saved in :
      outputs/sample_prebuilt_agent_run.txt


# 2--> custom react agent
   run "python app1.py" command on terminal

   outputs will be saved in :
      outputs/sample_custom_agent_run.txt

# 8. Available Tools

inspect_database_schema

    Returns database tables and schema information.

get_customer_profile

    Retrieves customer details using customer ID, email, phone, or name.

get_card_details

    Returns masked card information for a customer.

search_transactions

    Searches transactions using filters such as amount, merchant, or date range.

get_customer_transactions

    Returns recent transactions for a customer.

get_statement_summary

    Provides statement and dues information.

get_rewards_summary

    Returns reward points and related transactions.

get_merchant_spend_summary

    Aggregates spending by merchant or merchant type.

# 9. Sample Questions

Show me the database schema.
Show customer profile for customer CUST-1001.
Show card details for customer CUST-1001.
Show the last 5 transactions for customer CUST-1001.
Which customers have the highest amount due?
Show statement summary for customer CUST-1001.
Which merchant type has the highest total spend?
Show reward points for customer CUST-1001.
Identify potentially suspicious transactions.
Which cards are expiring in the next 60 days?

# 10. Sensitive Data Handling

The system follows strict security rules:

Full card numbers are never displayed.
CVV/security codes are never exposed.
Passwords are never exposed.
Security questions and answers are never exposed.
Sensitive customer information is masked when required.
Parameterized SQL queries are used throughout the application.

Example:

**** **** **** 1234

# 11. Sample Output

QUESTION:
show the card details of cust-1

RESPONSE:
{
    "user_question": "show the card details of cust-1",
    "implementation_choice": "prebuilt_react_agent",
    "tools_used": [
        "get_card_details"
    ],
    "records_found": 1,
    "answer": "The card details for cust-1 are:\n\n- Card Number: **** **** **** 1697\n- Valid From: 2013-06-01\n- Expiry: 2023-06-01\n- Security Code: ***\n- X-coordinate: 55.33711897497719\n- Y-coordinate: 50.313247255154\n- Mean Amount: 23.42\n- Standard Deviation of Amount: 11.71\n- Mean Number of Transactions per Day: 3.44",
    "sensitive_data_masked": true,
    "limitations": []
}

# 12. Dataset Limitations

The following tools were implemented according to the PRD requirements but could not be fully validated due to missing or limited data in the provided database:

* get_statement_summary
* get_notification_summary
* get_rewards_summary

The tool implementations are complete; however, the available dataset did not contain sufficient records to demonstrate all expected scenarios. The agent therefore returns appropriate "No records found" responses when relevant data is unavailable.

# 13. Challenge Faced

One challenge encountered during development was inconsistent agent behavior. In some cases, the same user query would return the correct answer, while on other attempts the agent would fail to produce the expected response despite no changes to the query or underlying data. This issue appears to be related to the agent's reasoning and tool-calling process and remains an area for further investigation.

# 14. Conclusion

This project demonstrates how LangGraph agents can safely interact with enterprise databases through controlled tools, enabling natural language access to credit card management data while maintaining security, reliability, and explainability.
