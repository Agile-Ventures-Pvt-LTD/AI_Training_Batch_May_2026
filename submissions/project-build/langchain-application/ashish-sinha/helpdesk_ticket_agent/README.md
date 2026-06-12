# AI Helpdesk Ticket Operations Agent

## Overview

AI-powered Helpdesk Ticket Operations Agent built using:

* Python
* LangChain
* langchain-groq
* SQLite
* python-dotenv

The agent can search tickets, analyze SLA status, prioritize work queues, manage ticket updates, store user preferences, and recall conversation history.

---

## Features

### Ticket Operations

* Search tickets using filters
* Retrieve ticket details
* View ticket comments
* Calculate SLA status
* Prioritize ticket queues

### Ticket Updates

* Update ticket status
* Add internal comments
* Audit logging for write actions

### Memory

* Save conversation history
* Recall previous conversations
* Save archival memory/preferences
* Recall stored preferences
* Generate conversation summaries

---

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
├── tools.py
├── output_formatter.py
│
├── tests/
│   └── test_tools.py
│
├── outputs/
│   ├── sample_agent_run.txt
│   └── evaluation_outputs.json
│
├── evaluate.py
├── requirements.txt
└── .env
```

---

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

---

## Run Agent

```bash
python app.py
```

---

## Run Evaluation

```bash
python evaluate.py
```

Generated files:

```text
outputs/sample_agent_run.txt
outputs/evaluation_outputs.json
```

---

## Mandatory Capabilities

* Ticket Search
* SLA Analysis
* Ticket Prioritization
* Ticket Updates
* Comment Management
* Conversation Memory
* Preference Memory
* Conversation Summarization

---

## Tech Stack

* LangChain
* Groq LLM
* SQLite
* Pydantic
* Rich
* Tabulate
* Python Dotenv

---

## Sample Queries

```text
Show me all open high-priority tickets.

Which tickets should I work on first today?

Update TCK-1001 status to In Progress.

Add a comment to TCK-1001 saying billing team is reviewing the duplicate invoice.

Remember that I want to prioritize enterprise customer issues first.

What did we discuss earlier about billing tickets?

Summarize this conversation and store it in memory.
```
