# Credit Card Management System AI Agent

This project is for managing credit card data, transactions and customer profiles using LangChain and LangGraph.

### Project Overview
I implemented both a prebuilt ReAct workflow and a custom LangGraph agent to compare flexibility and development effort.

### Setup Instructions
1. Clone the repo.
2. Create a venv: `uv venv`
3. Activate it (Windows): `.venv\Scripts\activate`
4. Install dependencies: ` uv pip install -r requirements.txt`

### Place ccms.db
Place the database file in a folder named `data` at the root of the project:
`../data/ccms.db`

### Environment Variable Setup
Create a `.env` file(copying from .env.example) and add your Groq API key:
```
GROQ_API_KEY=your_api_key
```

### To run pre-built agent
Run `python app.py` and select option **1**. 

### To run custom agent
Run `python app.py` and select option **2**. 

### Tools
- `get_database_schema`
- `get_customer_profile`
- `get_card_details`
- `search_transactions`
- `get_merchant_spend_summary`
- `get_statement_summary`
- `get_rewards_summary`
- `get_notifications`
- `detect_suspicious_transactions`

### Sensitive Data Masking Rules
- **Card Numbers**: Only the last 4 digits are shown, starting digits are masked with asterisks.
- **Security**: PINs and Security Codes columns are dropped during runtime.
- **Passwords**: passwords and security answers are never displayed.

### Known Limitations
- SQLite is used, so it's not meant for high-concurrency production.
- Complex queries may require multiple tool calls.

### Future Improvements
- To implement a web interface using Streamlit.

### Project structure
```bash
ccms_langgraph_agent/
│
├── app.py
├── config.py
├── db_utils.py
├── tools.py
├── prompts.py
├── prebuilt_agent.py
├── custom_agent.py
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
```

### Comparing the two agents:
**Pre Built agent:**
- Logic : Standard React Loop
- Control : High
- Speed : Faster than Custom agent
- Reliability : Good for standard tasks

**Custom agent:**
- Logic : State graph with reflection node
- Control : Maximum since fully customizable
- Speed : Slightly slower
- Reliability : Better for complex analysis

### Challenges Faced

- Tool outputs occasionally exceeded context limits.
- Mapping natural language queries to structured filters.
- Handling multiple customer identifiers increased tool complexity.