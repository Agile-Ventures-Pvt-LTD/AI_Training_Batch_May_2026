# AI Helpdesk Ticket Agent

## Participant Name
Nandani Bisht

## Project Overview

This project is an AI-powered Helpdesk Ticket Operations Agent built using LangChain, Groq, and SQLite.

The goal of this project is to help support teams work with tickets more efficiently by allowing natural language interaction for searching tickets, reviewing ticket history, checking SLA risk, updating ticket status, storing preferences, and maintaining conversation history.

The application uses SQLite as the source of truth and LangChain tools to safely perform operations.


## Features

### Ticket Operations

* Search tickets using multiple filters
* View complete ticket details
* Read ticket comments and work history
* Check SLA status
* Prioritize tickets

### Updates

* Update ticket status
* Add internal comments
* Track write actions through audit logs

### Memory

* Save conversation history
* Recall previous conversations
* Store long-term preferences
* Generate conversation summaries



## Project Structure

```plaintext
AI Helpdesk Ticket Agent/
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
├── README.md
├── .env
│
├── tests/
│   └── test_agent.py
│
├── outputs/
│
└── data/
    └── helpdesk_agent.db
```


## Tech Stack

* Python
* LangChain
* Groq
* SQLite
* dotenv

## Setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

Activate environment:

Windows

```bash
.venv\Scripts\Activate.ps1
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

---

## Run Application

```bash
python app.py
```

Example:

```text
Ask: show me open high priority tickets
```

---

## Testing

Run:

```bash
pytest tests/test_tools.py
```

## Example Capabilities

Examples of supported queries:

```text
Show open tickets

Summarize ticket TCK-1003

What happened so far on TCK-1001?

Update TCK-1001 status to In Progress

Add comment to TCK-1001 saying billing team is reviewing the issue

Prioritize tickets based on enterprise customers
```
