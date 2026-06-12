# AI Helpdesk Ticket Operations Agent

## Overview

AI-powered Helpdesk Ticket Operations Agent built using LangChain, LangGraph, Groq LLM, and SQLite. The agent can search tickets, retrieve ticket details, analyze ticket history, check SLA status, prioritize work queues, update ticket status, and manage conversation memory.

## Features

* Search support tickets
* Retrieve ticket details
* View ticket comments/history
* Check SLA status
* Prioritize ticket queues
* Update ticket status
* Add internal ticket comments
* Conversation memory
* Archival memory (user preferences)
* Conversation summarization
* Tool audit logging

## Tech Stack

* Python
* LangChain
* LangGraph
* Groq (Llama 3.1)
* SQLite
* python-dotenv

## Project Structure

```text
helpdesk_ticket_agent/
│
├── app.py
├── agent.py
├── config.py
├── db_utils.py
├── memory.py
├── prompts.py
├── schema.py
├── sql_router.py
├── tools.py
│
├── data/
│   └── helpdesk_agent.db
│
├── requirements.txt
└── README.md
```

## Setup

1. Create virtual environment

```bash
uv venv --python 3.11
```

2. Activate environment

```bash
# Windows
.venv\Scripts\activate
```

3. Install dependencies

```bash
uv pip install -r requirements.txt
```

4. Configure environment variables

Create `.env`

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
DB_PATH=data/helpdesk_agent.db
```

## Run Application

```bash
python app.py
```

## Example Queries

* Show me all open high-priority tickets
* Which tickets are overdue?
* Summarize ticket TCK-1003
* Show comments for TCK-1003
* Prioritize my ticket queue
* Update ticket TCK-1003 to Resolved
* Add comment to TCK-1003

## Output

* Conversation logs stored in SQLite
* User-friendly responses displayed in terminal


