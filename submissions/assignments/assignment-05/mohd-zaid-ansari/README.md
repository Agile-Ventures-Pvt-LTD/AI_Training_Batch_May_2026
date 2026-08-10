# Credit Card Management System AI Agent

# Participant Name

**Mohd Zaid Ansari**

# Project Overview

The project is AI-Powered credit card management system which helps companies that can interpert 
natural language questions, decide which database tools to call, execute those tools safely and 
return answer in clear format. It uses several tools to look for database to get relevant information 
and then Agent uses that information to give familiar natural language answers.

The Project contains two implementations:
1:Custom React Agent
2:Prebuilt React Agent

# Setup Instruction
1. Create virtual environmnet
```bash
uv venv
```
2. Activate environment
```bash
.venv/Scripts/activate
```
3.Install Required Libraries
```bash
uv add -r requirements.txt
```
4.Create .env file
```bash
GROQ_API_KEY=...
MODEL_NAME=...
```
# Run The Application
1.Run app.py file
```bash
python app.py
```
## 2.Select Agent

- custom_react_agent

- prebuilt_agent

## 3.Enter question

# Features

- View database schema
- Get customer details
- Get information quickly
- Ask query in Natural Language
- Get output in Natural Language 
- Save response in files

# Tech Stach

- Python
- LangGraph
- GroqAPI
- GroqLLM
- Sqlite Database

## Project Structure

```text
project/
│
├── app.py                     
├── prebuilt_agent.py          
├── custom_react_agent.py       
├── tools.py                    
├── db_utils.py                 
├── prompts.py                  
├── config.py                   
├── output_formatter.py         
├── requirements.txt            
│
├── data/
│   └── ccms.db                 
│
├── outputs/
│   ├── sample_prebuilt_agent_run.txt
│   └── sample_custom_agent_run.txt
│
└── tests/
    └── test_tools.py          
```

# Available Tools

Tools:
- inspect_schema
- customer_profile
- card_details
- transactions_search
- customer_transactions
- suspicious_transactions
- rewards_summary
- merchant_spend_summary

# Sample Question

- Show me the database schema.
- Show customer profile for customer 1.
- Show card details for customer 1.
- Which merchant type has the highest total spend?
- Show reward points for customer 1.

# Future Improvements

- Add more tools do get more information.
- Can use multi-agent Collaboration.

# Author

**Mohd Zaid Ansari**


