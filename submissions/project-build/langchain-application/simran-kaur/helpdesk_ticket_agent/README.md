# AI Helpdesk Ticket Agent

This is a small LangChain + Groq agent that answers questions about a local helpdesk SQLite database.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DB_PATH=data/helpdesk_agent_db/helpdesk_agent.db
```

## Run

```bash
python app.py
```

If you are using the included virtual environment on Windows:

```bash
.\.venv\Scripts\python.exe app.py
```

## What It Can Do

- Count tickets by status
- Search tickets
- Show ticket details
- Show ticket comments
- List overdue tickets
- Show the work queue
- Update a ticket status
