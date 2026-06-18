# **`Credit Card Management System Agent`**
---
# **1. Project overview**
**_A LangGraph-based AI agent that interacts with a SQLite credit card management database through StructuredTools._**

**_The agent supports:_**

- Customer profile lookup
- Card detail retrieval
- Transaction search
- Customer transaction history
- Merchant spend analytics
- Suspicious transaction detection
- Database schema inspection
---
# **2. How to place ccms.db**

> ccms_langgraph_agent\
> ├── .env\
> ├── README.md\
> ├── agents\
> │   ├── __init__.py\
> │   └── prebuilt_agent.py\
> ├── app.py\
> ├── data\
> │   ├── __init__.py\
> │   └── ccms.db << --- here ---- >>\
> ├── db_utils\
> │   ├── __init__.py\
> │   └── db_connection.py\
> ├── logs\
> │   └── conversation_log.json\
> ├── outputs\
> │   ├── test_agent_output.json\
> │   └── test_tools_output.json\
> ├── prompts.py\
> ├── requirements.txt\
> ├── tests\
> │   ├── __init__.py\
> │   ├── queries_for_test.py\
> │   ├── test_agent.py\
> │   └── test_tools.py\
> ├── tools\
> │   ├── __init__.py\
> │   ├── analytics_tools.py\
> │   ├── card_tools.py\
> │   ├── init.py\
> │   ├── inspect_database_schema.py\
> │   ├── profile_tools.py\
> │   ├── security_tools.py\
> │   └── transaction_tools.py\
> └── utils\
>     ├── __init__.py\
>     ├── config.py\
>     ├── gClient.py\
>     ├── logger.py\
>     ├── response_formatter.py\
>     └── tool_utils.py

### Place the ccms.db in the directory: `ccms_langgraph_agent > data > ccms.db`
---
# **3. Setup instructions**
### Run the following commands in the terminal
For uv usage:
```
uv venv
.venv/Scripts/activate
uv pip install -r requirements.txt
```
For pip usage:
```
python -m venv <name>
.\<name>\Scripts\activate
pip install -r requirements.txt
```
---
# **4. Environment variable setup**

> In the root directory, create a `.env` file

> Write `GROQ_API_KEY=...` and replace `...` by you groq api key.
---
# **5. How to run pre-built agent**
For uv usage:
`uv run app.py`

For pip usage
`python -m app`
---
# **6. Tool list and purpose**
| Tool | Purpose |
| -------------------------------- | ------------------------------------------------------------------------------------------------- |
| `inspect_database_schema`| Retrieve database tables and column information to understand the available data model.|
| `get_customer_profile`| Retrieve customer profile information using a customer ID.|
| `get_card_details` | Retrieve customer card information with sensitive card data masked.|
| `search_transactions`| Search transactions using filters such as amount, merchant, date, transaction type, and locality. |
| `get_customer_transactions`| Retrieve recent transaction history for a specific customer. |
| `detect_suspicious_transactions` | Identify potentially suspicious transactions using rule-based anomaly detection.|
| `get_merchant_spend_summary`| Generate aggregated spending summaries by merchant or merchant category.|
---
# **7. Sample questions**
**_The agent can answer questions such as:_**

- Show me the database schema.
- Show customer profile for customer 132.
- Show card details for customer 131.
- Show the last 5 transactions for customer 113.
- Search transactions above $100.
- Show transactions made on 5th June 2022.
- Which merchant type has the highest total spend?
- Show spend summary by merchant category.
- Identify potentially suspicious transactions.
- Show all debit transactions for a specific merchant.
---
# **8. Sensitive data masking rules**
To protect customer privacy and comply with secure data handling practices, the following rules are applied:

- Security codes, Net banking passwords, Security question answers and Full card number are never returned or exposed.
- Card numbers are displayed in masked format (e.g., ************1234).
- Agent responses only include information necessary to answer the user's request.
---
# **9. Future improvements**

Potential enhancements for future versions include:

- Implement a custom LangGraph ReAct agent in addition to the prebuilt agent.
- Introduce Pydantic schemas for stronger validation.
- Add conversation memory.
- Improve suspicious transaction detection using machine learning models or better rules such as z-index.
- Add support for additional banking operations such as rewards, statements, and notification management.

---
# **10. Important Notes**

The project requirement document explicitly told us to design three more functions relating to notifications, rewards, and statements which according to the ER Diagrahm and the PRD, should be having tables related to them but tables relating to notifications, rewards and statements are missing from the provided database ccms.db.

For reference check test_tools_output.json and search for tool test result for tool inspect_database_schema.

---
# **Thanks!**
---