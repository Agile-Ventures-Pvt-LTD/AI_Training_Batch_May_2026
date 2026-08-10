# AI Helpdesk Ticket Operations Agent

## 1. Participant Name
**Mohd Zaid Ansari**
---

## 3. Description

This project is an AI-powered helpdesk ticket management system built using **LangChain agents**, **Groq LLM**, and a **SQLite database backend**.
The system acts as an intelligent support assistant capable of:

- Searching and filtering helpdesk tickets
- Checking SLA status (overdue, due today, within SLA)
- Updating ticket status safely with validation
- Adding internal comments to tickets
- Prioritizing tickets based on business rules
- Maintaining short-term and long-term memory
- Recalling past conversations and user preferences
- Summarizing conversations into structured memory

The agent follows a strict workflow:

**Planning → Tool Execution → Reflection → Final Answer → Memory Update**
---

## 4. Key Features

### Ticket Operations
- Search tickets by status, priority, customer tier, and keywords
- Fetch detailed ticket information
- Update ticket status (Open, In Progress, Pending, Resolved, Closed, Escalated)
- Add internal comments to tickets
---
### SLA Management
- Detect overdue tickets
- Identify SLA breach conditions
- Classify tickets as:
  - BREACHED
  - DUE_TODAY
  - WITHIN_SLA
---
### Ticket Prioritization
- Prioritizes tickets using:
  - Priority level
  - SLA status
  - Customer tier (Enterprise priority)
  - Business rules (billing/security/compliance urgency)
---
###  Memory System
- Conversation logs stored in SQLite
- Archival memory for long-term preferences
- Recall memory for past conversations
- Summary memory for compressing conversation history
---
### AI Agent Behavior
The agent follows:
1. **Planning Phase**
   - Creates a short step-by-step plan before using tools
2. **Tool Execution Phase**
   - Uses SQLite-backed tools only (no hallucinated data)
3. **Reflection Phase**
   - Validates whether tool output is sufficient
4. **Memory Update Phase**
   - Stores conversation logs, summaries, and preferences
---

## 5. How to Run the Project

### Step 1: Install Dependencies
```bash
uv add -r requirements.txt
