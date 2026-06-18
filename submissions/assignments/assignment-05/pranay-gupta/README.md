# Credit Card Management System AI Agent

This project is an AI-powered Credit Card Management Assistant built using LangGraph, Groq LLM, and SQLite. It allows users to ask credit card-related questions in natural language. The agent selects the required database tools, fetches information from the database, and generates user-friendly responses.

The project contains two implementations:
- Prebuilt ReAct Agent using LangGraph's built-in agent
- Custom ReAct Agent built using custom nodes, tool handling, and reflection

---

## Features

- View customer information
- Retrieve customer card details
- Check recent transactions
- Search transaction history
- Generate customer spending summary
- Calculate reward details
- Analyze merchant spending
- View database schema
- Save agent responses into text files

---

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- SQLite Database

---

## Project Structure

```
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

---

## Setup Instructions


1. Create a virtual environment:

```
python -m venv .venv
```

Activate environment:

**Windows**
```
.venv\Scripts\activate
```

2. Install required packages:

```
pip install -r requirements.txt
```

3. Create a `.env` file and add:

```
GROQ_API_KEY=your_api_key
MODEL_NAME=your_model_name
DB_PATH=data/ccms.db
```

---

## Running the Application

Run:

```
python app.py
```

Choose an agent:

```
1 - Prebuilt ReAct Agent
2 - Custom ReAct Agent
```

Enter your question and the response will be displayed in the terminal and saved inside the `outputs` folder.

---

## Available Tools

Tool: 
```
inspect_database_schema 
get_customer_profile
get_card_details 
get_customer_transactions 
search_transactions 
get_statement_summary 
get_reward_summary 
get_merchant_spend_summary 
```
---

## Sample Questions

- Show the database schema.
- Show customer details for customer 1.
- Show card details for customer 1.
- Show last 5 transactions for customer 1.
- Show spending summary for customer 1.
- Show reward details for customer 1.

---

## Testing

Run the tool test file:

```
python tests/test_tools.py
```

---

## Future Improvements

- Add better fraud detection features.
- Improve custom agent planning and reflection.
- Add a web interface for easier interaction.

---

## Author

Pranay Gupta