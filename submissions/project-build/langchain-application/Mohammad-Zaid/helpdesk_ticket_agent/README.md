# AI Helpdesk Ticket Operations Agent

## Project Overview

This project is a simple AI-powered Helpdesk Ticket Operations Agent built using LangChain, Groq, SQLite, and custom tools.

The agent helps support teams perform common ticket operations such as:

* Searching tickets
* Viewing ticket details
* Checking ticket history
* Prioritizing work queues
* Updating ticket status
* Adding internal comments
* Saving user preferences
* Recalling previous preferences and conversations

The SQLite database acts as a mock helpdesk backend similar to systems like ServiceNow 

---

## Technologies Used

* Python
* LangChain
* Groq
* SQLite
* python-dotenv

---

## Project Structure

```text
helpdesk_ticket_agent/
│
├── app.py
├── agent.py
├── tools.py
├── db_utils.py
├── memory.py
├── prompts.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ └── helpdesk_agent.db
│
└── outputs/    
 └── sample_agent_run.txt
```

---

## Database

I have used the provided SQLite database:

```text
helpdesk_agent.db
```

Main tables used:

* tickets
* ticket_comments
* archival_memory
* conversation_logs

Views used:

* open_tickets
* overdue_tickets
* ticket_work_queue

---

## Tools Implemented

### 1. search_tickets

Searches tickets based on user requests such as open tickets, high-priority tickets, or overdue tickets.

### 2. get_ticket_details

Retrieves complete details for a specific ticket.

### 3. get_ticket_comments

Retrieves ticket history, comments, and internal notes.

### 4. prioritize_tickets

Returns the highest-priority tickets using the ticket_work_queue view.

### 5. update_ticket_status

Updates the status of a ticket.

### 6. add_ticket_comment

Adds an internal comment or work note to a ticket.

### 7. save_memory

Stores long-term user preferences in archival memory.

### 8. recall_memory

Retrieves previously stored preferences.

### 9. save_conversation

Stores user-agent conversations in the database.

### 10. recall_conversation

Retrieves previous conversations using keyword search.

---

## Memory Design

The project uses two simple memory mechanisms.

### Archival Memory

Stored in:

```text
archival_memory
```

Used for storing long-term preferences such as:

```text
Remember that I want to prioritize enterprise customer issues first.
```

### Conversation Memory

Stored in:

```text
conversation_logs
```

Used for saving and recalling previous interactions.

---

## Planning and Reflection

The agent follows a simple planning and reflection pattern through the system prompt.

Before answering:

* Creates a short plan
* Decides which tool to use

After tool execution:

* Reviews tool results
* Provides a short reflection
* Generates the final answer

---

## Setup Instructions

### Step 1

Clone or download the project.

### Step 2

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Step 3

Install dependencies.

```bash
pip install -r requirements.txt
```

### Step 4

Create a `.env` file.

```text
GROQ_API_KEY=your_groq_api_key
```

### Step 5

Place the database file inside the project folder.

```text
helpdesk_agent.db
```

### Step 6

Run the notebook and execute all cells.

---

## Sample Queries

```text
Show me all open high-priority tickets.

Which tickets are overdue?

Which tickets should I work on first today?

Summarize ticket TCK-00077.

Add a comment to TCK-00077 saying billing team is reviewing the issue.

Update TCK-00077 status to In Progress.

Remember that I want to prioritize enterprise customer issues first.

Based on my preference, which tickets should I handle first?

What did we discuss earlier about billing tickets?
```

---

## Limitations

* Uses a local SQLite database instead of a real helpdesk platform.
* Uses simple keyword-based conversation recall.
* No vector database or embeddings are used.
* Designed as a lightweight assignment project rather than a production system.

---


