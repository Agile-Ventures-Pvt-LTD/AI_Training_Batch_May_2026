# Credit Card Management System Agent

## Project Overview

This project implements an AI-powered Credit Card Management System Agent using:

- LangGraph
- LangChain
- Groq
- SQLite

The agent answers user questions using database-backed tools.
The database is the source of all the responses given by the System.


## Implementation Choice: Choice 1-LangGraph Prebuilt ReAct Agent

## Features

### Customer Profile Lookup

Example: Show customer profile for customer cust_id: 1.

### Card Details Lookup

Example: Show card details for customer cust_id: 1.

### Transaction Search

Example: Show last 5 transactions for customer cust_id: 1.

### Statement Summary

Example: Show statement summary for customer cust_id: 1.

### Rewards Summary

Example: Show reward points for customer cust_id: 1.

### Merchant Spend Summary

Example: Which merchant type has the highest spend?

### Suspicious Transaction Detection

Example: Identify potentially suspicious transactions.

### Database Schema Inspection

Example: Show database schema.

## Folder Structure

ccms_langgraph_agent/

├── app_choice1.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── prebuilt_agent.py
├── output_formatter.py
├── requirements.txt
├── .env
├── README.md

├── data/
│   └── ccms.db

└── tests/
    └── test_tools.py


### app.py
- Main file of the whole application, accepts user input or queries, invoke agent and displays the output.

### config.py
- Contains all the configuration details such as model_name, api_key ( as a variable), database file path etc.

### db_utils.py
- Provides reusable database utility functions for connecting to SQLite like, executing queries, retrieving records, and fetching database schema information.

### tools.py
- Contains all the 8 tools which perform various fucntions such as customer lookup, schema inspection etc.

### prompts.py
- Contains the system prompt given to the system to control its behaviour and output generation.

### prebuilt_agent.py
- Creates and configures the LangGraph Prebuilt ReAct Agent using the selected LLM, tools, and system prompt. It serves as the core orchestration layer of the application.

### output_formatter.py
- Formats agent responses into a user-friendly structure containing:

Question
Tool Used
Records Found
Answer
Sensitive Data Masked

### requirements.txt
- Contains all the requirements(packages) like langchain, langGraph, python-dotenv etc. as per system requirements.

### .env
- Contains the confidential information like api-key etc.

### ccms.db
- The database file from where all the data is being fetched.

### test_tools.py
- This file verifies that each tool executes successfully, returns data in the expected format, and maintains proper integration with the database layer.

### sample_prebuilt_agent_run.txt
- Contains all the sample queries that should be tested.

## Setup

### Create Virtual Environment

python -m venv .venv

### Activate virtual environment

.venv\Scripts\activate

### Create requirements.txt file
Add:
langchain==0.3.27
langchain-core==0.3.74
langchain-groq==0.3.7
langgraph==0.6.6
python-dotenv==1.1.1
pandas==2.3.2
tabulate==0.9.0
rich==14.1.0
pydantic==2.11.7
pytest==8.4.1

### Install Dependencies

pip install -r requirements.txt

### Configure Environment

Add your Groq API key in .env file.

Example: GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx

### Place Database

Copy: ccms.db

into: data folder(data/ccms.db)

## Run Application

python app_choice1.py

## Sample Questions

- Show me the database schema

- Show customer profile for customer CUST-1001

- Show card details for customer CUST-1001

- Show last 5 transactions for customer CUST-1001

- Show statement summary for customer CUST-1001

- Show reward points for customer CUST-1001

- Identify suspicious transactions

- Which merchant category has highest spend?

- Which cards are expiring soon?

- Which customers have highest dues?

## Sensitive Data Rules

Never expose confidential information of the user, like:

- Full card numbers
- CVV values
- Security codes
- Passwords
- Security answers

Card numbers are masked like this: **** **** **** 1234

## Known Limitations

- Relies on available database records.
- Suspicious transaction detection is rule-based.
- Does not perform fraud confirmation.
- No write/update operations.

## Future Improvements

- Streamlit UI
- Customer dashboard
- PDF report generation
- Advanced fraud detection
- Hybrid RAG architecture
- Role-based access control

## Implementation Choice: Choice 1-LangGraph Prebuilt ReAct Agent

## Features
Almost all the files for implementation of Choice 2 are same i.e,
- Same .venv is used.
- Same check_schema.py is used.
- Same config.py is used.
- Same db_utils.py is used.
- Same prompts.py is used.
- Same requirements.txt is used.
- In tools.py, two extra tools are added i.e, get_statement_summary & get_rewards_summary.

## Extra files in Choice 

### router.py
 - Implements conditional routing logic for the graph. It examines the LLM output and determines whether a tool should be executed next, or the workflow should proceed to the reflection stage and terminate.
This enables dynamic decision-making within the graph.

### state.py
- Defines the shared state used by the LangGraph workflow. The state stores conversation messages, tool execution information, and reflection data that is passed between graph nodes during execution.

### nodes.py
- Contains the core graph nodes i.e, 

Agent Node – Uses the LLM to analyze user queries and decide whether tools need to be called.
Tool Node – Executes the selected tool and returns the result to the workflow.
Reflection Node – Reviews the execution flow, tracks tools used, and prepares the final response.

### custom_agent.py
- Builds and compiles the custom LangGraph workflow using:
StateGraph
Nodes
Conditional Edges
Routing Logic
It orchestrates the complete ReAct cycle.

### app_choice2.py
- Console-based application entry point for the Custom StateGraph Agent. It:

Accepts user questions
Invokes the custom graph workflow
Formats responses
Saves sample outputs to sample_custom_agent_run.txt

### Sample_custom_agent_run.txt
- Contains sample execution logs and outputs generated by the Custom StateGraph Agent. This file serves as evidence of successful execution and testing of Choice 2 requirements.

## Execution of Choice 2
python app_choice2.py

# Difference between Choice 1 and Choice 2

Choice 1                                                Choice 2

Uses create_react_agent                                 Uses StateGraph
Prebuilt Workflow                                       Custom workflow
Faster implementation                                   Greater control and flexibility


# For evaluation
- I have implemented CHoice 1 firstly, and then have also done Choice 2 for understanding a different method for getting the same results.

- As mentioned in the PRD, for excellent evaluation, I have performed both the methods but if the evaluation will be done on the basis of only one method, I will prefer Choice 1 i.e, LangGraph prebuilt ReAct agent.
