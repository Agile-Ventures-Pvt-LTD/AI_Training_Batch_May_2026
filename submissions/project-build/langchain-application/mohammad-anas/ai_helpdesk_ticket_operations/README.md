# Project Build 2: AI Helpdesk Ticket Operations Agent

**Participant:** Mohammad Anas

This is my submission for the AI Helpdesk Agent. It uses LangChain (specifically LangGraph for the ReAct architecture), Groq (Llama-3), and a local SQLite database to manage support tickets.

## How to run the project
1. Create a virtual environment using uv: `uv venv`
2. Install the required packages: `uv pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and paste your `GROQ_API_KEY`.
4. Make sure `helpdesk_agent.db` is inside the `data/` folder.
5. Run the main file: `python app.py`

## Development Notes & Approach
I chose to use LangGraph's `create_react_agent` because the PRD required the agent to plan and reflect before acting. This allowed me to pass in 11 custom SQLite tools.

**A challenge I faced:** While building the tools, the agent kept crashing with an `Error code: 400 (invalid_request_error)` when calling the database. I realized this was because the SQLite wrapper was returning Python lists/dictionaries, but the Groq API strictly requires tool outputs to be strings. I resolved this by importing the `json` module and wrapping all my database returns in `json.dumps()` inside `tools.py`.

## Memory Implementation
To handle the memory requirements without blowing up the context window, I built specific tools:
* **Archival:** `save_archival_memory` and `recall_archival_memory` write directly to the DB so the agent can check preferences (like prioritizing Enterprise customers).
* **Conversation Summary:** Instead of passing the whole chat history, the `summarize_conversation` tool uses a secondary Groq call to compress the chat logs and save them into the `conversation_summaries` table.

## Safety
I did not give the LLM raw SQL execution access. All queries are parameterized inside `db_utils.py` to prevent SQL injection, and every write operation (like updating a status or adding a comment) automatically logs an entry into the `tool_audit_logs` table.

## Testing
You can find my full test run for the 10 mandatory prompts inside `outputs/sample_agent_run.txt`.