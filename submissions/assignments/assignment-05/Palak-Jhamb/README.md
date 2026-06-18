# Assignment-05 (A005)
## Project Title
### AI Credit Card Management Agent Using LangGraph, Groq, Tools, and SQLite
### Submitted By: Palak
### 1. Project overview:

Build an AI agent that can answer operational and analytical questions from a credit card management database. This agent is build to help user or any one in credit card management team.
Here an LLM is converted into agent by adding extra functionality to llm. This method help llm answer based on its knowledge or based on databse .

Method used:
1.  LangGraph Pre-built ReAct Agent
2.  Custom LangGraph ReAct Agent

Database schema:
```json
{
'tables':[
'customer',
'netbanking',
'card_type',
'card',
'transaction_type',
'transaction_terminal',
'merchant_type',
'merchant',
'transaction'
],
'schema':{
'customer':[
'cust_id',
'first_name',
'last_name',
'email',
'phone',
'address',
'city',
'state',
'zip'
],
'netbanking':[
'username',
'password',
'expiry_date',
'security_question',
'security_answer',
'cust_id'
],
'card_type':[
'card_type_id',
'card_type',
'card_network',
'privilege'
],
'card':[
'card_number',
'valid_from',
'expiry',
'security_code',
'x-coordinate',
'y-coordinate',
'mean_amount',
'std_amount',
'mean_nb_tx_per_day',
'cust_id',
'card_type_id'
],
'transaction_type':[
'txn_type_id',
'debit_credit',
'lcl_intnl'
],
'transaction_terminal':[
'TERMINAL_ID',
'x_terminal_id',
'y_terminal_id'
],
'merchant_type':[
'id',
'merchant_type'
],
'merchant':[
'id',
'merchant',
'merchant_type'
],
'transaction':[
'Unnamed: 0',
'TXN_ID',
'TX_DATETIME',
'CARD_ID',
'TERMINAL_ID',
'TX_AMOUNT',
'TX_TIME_SECONDS',
'TX_TIME_DAYS',
'TXN_TYPE_ID',
'M_ID'
]
}
}
```


---

### 2.Setup instructions

Steps for set-up are as follows:
1. initialize uv
```bash
uv init
```

2. create Environment 
```bash
uv venv
```
3. install requirements
```bash
uv add -r requirements.txt
```

**set-up part is completed!!!**

---

### 3.How to place ccms.db

To add databse to project folder, first create folder name data
- if databse is present on your local devide simply drag it into this project folder
- if database is from third party source then download it and move it to  project folder

---

### 4.Environment variable setup

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
API_KEY=zws2.....
```
3. Load the api in any folder or file with the help of os
```bash
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")
```

---

### 5.How to run pre-built agent

To run the agent run file named as app.py
```bash
python app.py
```
This will run the main application that will end only when user says exit or quit.

---

### 6.How to run Custom agent

To run the agent run file named as custom_app.py
```bash
python custom_app.py
```
This will run the main application that will end only when user says exit or quit.

---

### 7.Tool list and purpose
There are total 9 tools that are provided to llm .

Detail about tools:
1. **inspect_database_schema:** this is a tool that helps agent to retrieve database schema
2. **get_customer_profile:** this tool helps agent get details about customer based on provided details
3. **get_card_details:** this tool help agent get details regarding card
4. **search_transactions:** this is a tool that is used by agent to retrive transactions  based on diffrent filters provided
5. **get_customer_transactions:** this is another transaction related tool that help agent get transactions done by particular customer
6. **get_statement_summary:** this is used to get summary of transactions
7. **get_rewards_summary:** this function helps agent define reward points based on transaction amount
#as tere was no column related to rewards, i have added a logic to gnerate reward points
8. **get_merchant_spend_summary:** based on merchant or merchaint type this tool helps to get information regarding them
9. **detect_suspicious_transactions:** it is defined as rule based tool that detect suspicious transactions based on transaction amount

---

### 7.Sample questions
```
1. Show me the database schema.
2. Show customer profile for customer CUST-1001.
3. Show card details for customer CUST-1001.
4. Show the last 5 transactions for customer CUST-1001.
5. Which customers have the highest amount due?
6. Show statement summary for customer CUST-1001.
7. Which merchant type has the highest total spend?
8. Show reward points for customer CUST-1001.
9. Identify potentially suspicious transactions
```
---

### 8.Sensitive data masking rules
To hide the card details , an masked number was formed that stores only last 4 digits.
```python 
card_no = str(card_detail["card_number"])
masked_card = f"**** **** **** {card_no[-4:]}"
```

---
### 9. Known limitations
As number of data in databse are huge, sometimes it becomes imposible for llm to process all records because of token limit error.
for example- to get all transaction in table

```
User: give me reward summary for customer id one

Error: Error code: 400 - {'error': {'message': 'Tool call validation failed: tool call validation failed: parameters for tool get_rewards_summary did not match schema: errors: [`/cust_id`: expected string, but got number]', 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '{"name": "get_rewards_summary", "arguments": {"cust_id": 1}}'}}
```

---
### 10. Testing

Based on sample queries in PRD , **tests/test.py** is designed.
It runs all sample question provided one by one and save its output at **"outputs"** folder 

- To run Testing file :
```python
python -m tests.test_tools
```

### 11. Final Workflow
1.  LangGraph Pre-built ReAct Agent
```
            user input
                |
               agent
            (need tool)
                |
                /\
       (yes)   /   \  (no)
              /     \   
       Tool call     llm respond by self
            |           |
            \           /
              \       /   
     Repeat until user enter exit or quit
      
```

2. Custom LangGraph ReAct Agent
```
              START
                |
            user input
                |
               agent
            (need tool)
                |
                /\
       (yes)   /   \  (no)
              /     \   
       Tool call     Reflection
            |           |
    Back to agent      END
                        
                             
      
```