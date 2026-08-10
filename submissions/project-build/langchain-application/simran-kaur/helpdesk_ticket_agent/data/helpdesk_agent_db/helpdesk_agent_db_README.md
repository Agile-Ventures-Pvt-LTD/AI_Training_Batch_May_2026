# AI Helpdesk Ticket Operations Agent - SQLite Database

This SQLite database was created from `customer_support_tickets.csv` for a LangChain Agents project build.

## Main Database File

`helpdesk_agent.db`

## Training Reference Time

The database uses a fixed training reference time for deterministic SLA views:

`2026-06-12 09:00:00`

This means the `overdue_tickets` and `ticket_work_queue` views produce stable results during participant evaluation.

## Core Tables

| Table | Purpose |
|---|---|
| `tickets` | Main helpdesk tickets table |
| `customers` | Customer profile and account metadata |
| `ticket_comments` | Ticket history, customer messages, internal notes, and resolution notes |
| `sla_policies` | SLA hours by priority |
| `conversation_logs` | Stores user-agent conversation turns |
| `conversation_summaries` | Stores summarized conversation memory |
| `archival_memory` | Stores long-term memory such as preferences and business rules |
| `tool_audit_logs` | Stores agent tool call history |
| `raw_customer_support_tickets` | Original CSV data loaded as a reference table |

## Useful Views

| View | Purpose |
|---|---|
| `open_tickets` | All non-closed tickets |
| `overdue_tickets` | Non-closed tickets past the fixed SLA reference time |
| `ticket_work_queue` | Prioritized queue with SLA status and priority score |

## Example Agent Tool Ideas

Participants can create LangChain tools around these operations:

1. `search_tickets`
2. `get_ticket_details`
3. `get_ticket_comments`
4. `calculate_sla_status`
5. `prioritize_tickets`
6. `update_ticket_status`
7. `add_ticket_comment`
8. `save_conversation`
9. `recall_conversation`
10. `save_archival_memory`
11. `recall_archival_memory`
12. `summarize_conversation`

## Recommended Test Prompts

```text
Show me all open high-priority tickets.
Which tickets are overdue?
Which tickets should I work on first today?
Summarize ticket TCK-00077.
Add a comment to TCK-00077 saying billing team is reviewing the issue.
Update TCK-00077 status to In Progress.
Remember that I want to prioritize enterprise customer issues.
Based on my preference, which tickets should I handle first?
What did we discuss earlier about billing tickets?
Summarize this conversation and store it in memory.
```

## Files Provided

| File | Description |
|---|---|
| `helpdesk_agent.db` | Ready-to-use SQLite database |
| `helpdesk_agent_schema.sql` | Schema and views |
| `helpdesk_agent_sample_queries.sql` | Sample SQL queries for testing |
| `helpdesk_agent_db_summary.json` | Database summary and table counts |
| `helpdesk_agent_db_README.md` | This README |
