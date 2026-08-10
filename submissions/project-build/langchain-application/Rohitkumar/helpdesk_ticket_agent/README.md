
## AI Helpdesk Ticket Operations Agent

## Overview

AI-powered Helpdesk Ticket Operations Agent built using:

* LangChain
* Groq LLM
* SQLite
* Tool Calling Agents

The agent can search tickets, prioritize work queues, update ticket status, add comments, manage memory, and summarize conversations.

---

## Features

- Search Tickets
- View Ticket Details
- Retrieve Ticket Comments
- SLA Analysis
- Overdue Ticket Detection
- Ticket Prioritization
- pdate Ticket Status
- Add Internal Comments
- Conversation Recall
- User Preference Memory Conversation Summaries
 

---

## Project Structure

helpdesk_ticket_agent/
│
├── app.py
├── agent.py
├── config.py
├── db_utils.py
├── tools.py
├── memory.py
├── prompts.py
├── output_formatter.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ └── helpdesk_agent.db
│
├── outputs/
│ ├── sample_agent_run.txt
│ └── evaluation_outputs.json
│
└── tests/
 └── test_tools.py

---

## Setup

Create virtual environment:


uv venv


Activate:


.venv\Scripts\activate


Install dependencies:

uv pip install -r requirements.txt




## Run Agent


uv run app.py


or

uv run agent.py
```


## Sample Queries

Show me all open high-priority tickets.

Which tickets should I work on first today?

Summarize ticket TCK-00002.

Update TCK-00001 status to In Progress.

Add a comment to TCK-00001 saying customer confirmed resolution.

Remember that I want enterprise tickets prioritized first.

What did we discuss earlier about billing tickets?

Summarize this conversation and store it in memory.

---

## Expected Behaviors

### Ticket Search

Search tickets using status, priority, category, assignee, customer tier, and keywords.

### Ticket Prioritization

Ranks tickets using:

* Priority
* SLA Status
* Customer Tier
* Business Impact

### Memory

Stores:

* User preferences
* Conversation logs
* Conversation summaries

### Ticket Updates

Supports:

* Status changes
* Internal comments
* Audit logging

---

## issue found while evaluation with the given queries



### 1. Groq Rate Limit Error (429)

When using the model repeatedly, Groq may return:

```text
Rate limit reached for model llama-3.3-70b-versatile
```


```python
llama-3.1-8b-instant
```
but generated some ouput for some queries


-- output saved in output file

