# AI Helpdesk Ticket Agent

AI-powered Helpdesk Operations Assistant built with LangChain, Groq, and SQLite. The agent supports ticket management, SLA monitoring, memory, planning, reflection, and tool-calling workflows to assist support teams in handling customer support operations efficiently.

---

## Key Features

### Ticket Operations

* Search tickets with filters
* Retrieve ticket details and comments
* View customer ticket history
* Update ticket status
* Add ticket comments

### SLA Management

* Calculate SLA status
* Identify overdue tickets
* Monitor open tickets
* Prioritize support queues

### Agent Capabilities

* LangChain Tool Calling Agent
* Planning Pattern
* Reflection Pattern
* Session-based Memory
* Structured Responses

### Memory System

* Conversation Logs
* Conversation Summaries
* Archival Memory
* Tool Audit Logs

---

## Project Structure

```text
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
│
├── data/
│   └── helpdesk_agent.db
│
├── outputs/
│   ├── sample_agent_run.txt
│   └── evaluation_outputs.json
│
├── tests/
│   └── test_tools.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Architecture

```text
User Query
    ↓
Planning Layer
    ↓
LangChain Agent
    ↓
Tool Execution
    ↓
SQLite Database
    ↓
Response Generation
    ↓
Reflection Layer
    ↓
Memory Storage
```

---

## Tech Stack

| Component | Technology           |
| --------- | -------------------- |
| LLM       | Groq                 |
| Framework | LangChain            |
| Database  | SQLite               |
| Memory    | Custom SQLite Memory |
| Language  | Python 3.11+         |

---

## Database Tables

### Operational Tables

* customers
* tickets
* ticket_comments
* sla_policies

### Memory Tables

* conversation_logs
* conversation_summaries
* archival_memory
* tool_audit_logs

---

## Available Tools

| Tool                 | Purpose                  |
| -------------------- | ------------------------ |
| search_tickets       | Search tickets           |
| get_ticket_details   | Ticket information       |
| get_ticket_comments  | Ticket discussions       |
| calculate_sla_status | SLA evaluation           |
| prioritize_tickets   | Queue prioritization     |
| get_open_tickets     | Open ticket retrieval    |
| get_overdue_tickets  | Overdue ticket retrieval |
| update_ticket_status | Status updates           |
| add_ticket_comment   | Add comments             |
| get_customer_history | Customer history         |
| save_memory          | Store memory             |
| recall_memory        | Retrieve memory          |
| recall_conversation  | Retrieve conversations   |

---

## Planning & Reflection

### Planning

Before executing a request, the agent generates an execution plan including:

* User Goal
* Required Tools
* Reasoning
* Expected Output

### Reflection

After generating a response, the agent evaluates:

* Answer Completeness
* Missing Information
* Recommended Actions
* Confidence Level

---

## Installation

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

## Run Application

```bash
python app.py
```

### Commands

```text
/help
/show_plan
/show_reflection
/exit
```

---

## Example Queries

```text
Show me all critical open tickets

Get details for ticket TKT-1001

Show comments for ticket TKT-1001

Check SLA status for ticket TKT-1001

Prioritize my support queue

Find overdue critical tickets and recommend actions
```

---

## Run Tests

```bash
python tests/test_tools.py
```

---

## Generated Outputs

```text
outputs/sample_agent_run.txt
outputs/evaluation_outputs.json
```

---

## Requirement Coverage

| Requirement          | Status |
| -------------------- | ------ |
| LangChain Agent      | ✅      |
| Tool Calling         | ✅      |
| Planning Pattern     | ✅      |
| Reflection Pattern   | ✅      |
| Memory System        | ✅      |
| SQLite Database      | ✅      |
| Multi-Step Reasoning | ✅      |
| Audit Logging        | ✅      |
| CLI Interface        | ✅      |

---

## Author

**Pranay Gupta**
Agile Ventures – Module 2 Project 2
