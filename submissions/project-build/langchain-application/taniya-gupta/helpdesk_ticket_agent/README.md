# AI Helpdesk Ticket Operations Agent

An assistant that helps team manage, prioritize, and update customer tickets.

## Name
Taniya Gupta


## Project Structure
```bash
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

## Tools Implemented
1.  **`search_tickets`**: Filters tickets by status, priority, tier, and category.
2.  **`get_ticket_details`**: Retrieves full information for a specific ticket.
3.  **`get_ticket_comments`**: Fetches the latest internal comments.
4.  **`calculate_sla_status`**: Determines if a ticket is BREACHED, DUE_TODAY, or WITHIN_SLA.
5.  **`get_overdue_tickets`**: Lists all tickets that have breached their SLA.
6.  **`prioritize_tickets`**: Ranks tickets based on a priority score.
7.  **`update_ticket_status`**: Safely updates ticket status with validation.
8.  **`add_ticket_comment`**: Adds internal work notes to tickets.
9.  **`save_archival_memory`**: Stores long-term user preferences (e.g., "Prioritize Enterprise first").
10. **`recall_archival_memory`**: Retrieves saved preferences.
11. **`save_conversation`**: Logs user-agent interactions.
12. **`recall_conversation`**: Searches past logs using keywords.
13. **`summarize_conversation`**: Generates and stores a concise summary of the session.

## Memory Design
- **Recall Memory**: Uses keyword-based search on the `conversation_logs` table to help the agent remember past discussions.
- **Archival Memory**: Stores facts and business rules in the `archival_memory` table, which the agent checks.
- **Summary Memory**: Summarizes chat history into key decisions and open items, stored in `conversation_summaries` for an overview of work completed.

## Setup and Installation
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables**: Create a `.env` file (by copying .env.example then add your groqapi key) with your Groq API key:
    ```env
    GROQ_API_KEY=your_api_key_here
    GROQ_MODEL=openai/gpt-oss-120b
    DB_PATH=data/helpdesk_agent.db
    ```

3.  **Run the App**:
    ```bash
    python app.py
    ```

## Mandatory Test Prompts
The agent has been verified against the following prompts (results available in `outputs/sample_agent_run.txt`):
1.  Show me all open high-priority tickets.
2.  Which tickets are overdue?
3.  Which tickets should I work on first today?
4.  Summarize ticket TCK-00019.
5.  Add a comment to TCK-00019 saying billing team is reviewing the duplicate invoice.
6.  Update TCK-00019 status to In Progress.
7.  Remember that I want to prioritize enterprise customer issues first.
8.  Based on my preference, which tickets should I handle first?
9.  What did we discuss earlier about billing tickets?
10. Summarize this conversation and store it in memory.

## Limitations & Future Improvements
- **Keyword Search**: Currently uses basic SQL `LIKE` for memory recall.
- **Concurrency**: The current CLI is session-based; a multi-user web UI (Streamlit/FastAPI) would be better 
- **No real ServiceNow**: This project was implemented with Mock data, future improvement includes implementation with Real ServiceNow incidents.