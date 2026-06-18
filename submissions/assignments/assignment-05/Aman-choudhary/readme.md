## Project Build: Credit Card Management System
## Agent Using LangGraph, Groq, Tools, and SQLite

his project implements an AI-powered Credit Card Management System Agent using LangGraph, LangChain, Groq LLM, and SQLite.

The agent can answer customer-related questions by interacting with a Credit Card Management System database through a set of tools.

-- Prebuilt ReAct Agent using       LangGraph's create_react_agent
-- Custom ReAct Agent built using a custom LangGraph workflow

## Features
Database schema inspection
Customer profile retrieval
Card details lookup
Customer transaction history
Merchant spending analysis
Statement summary support
Reward summary support
Sensitive data masking
Structured JSON output
Prebuilt ReAct Agent implementation
Custom ReAct Agent implementation
Error handling and graceful failure responses


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

## Setup Instructions

1.Clone
git clone url 
cd Aman-choudhary
## Create Virtual Environment
python -m venv .venv
## Activate Virtual Environment
venv\Scripts\activate
source .venv/bin/activate
## Install Dependencies
pip install -r requirements.txt
## Configure Environment Variables
create .env
.env---> GROQ_API_KEY=your_groq_api_key GROQ_MODEL=llama-3.3-70b-versatile DB_PATH=data/ccms.db
## Running the Application
for prebuilt react agent 
python app.py
2--> custom react agent 
python app1.py

## Sample Queries
show me the database schema
show customer profile for customer 100
show card details for customer 100
show the last five transactions for customer 100
show reward point for customer 100
show statement summary for customer 100
which merchant type has the highest total spend identify potentially suspicious transaction
