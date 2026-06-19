# IT Troubleshooting Agent with Tool Using Workflow Using Langgraph

In this project, we have used different tools to get relevant information about the user query especially in IT Troubleshooting.I have built a working LangGraph-based IT troubleshooting assistant that uses both document retrieval and tools to diagnose common IT issues and recommend next actions.

# Project Context
An enterprise IT support team receives frequent tickets for issues such as VPN failure, Outlook sync problems, password reset issues, slow laptops, network connectivity problems, and printer access problems.

The goal of this project is to build an IT Troubleshooting Agent that uses LangGraph, Groq, RAG, and custom tools to perform structured diagnosis.

The assistant should not behave like a generic chatbot. It should classify the issue, retrieve relevant troubleshooting steps, call tools to inspect operational data, branch conditionally based on the issue type and missing information, and generate a safe resolution or escalation plan

#  Product Goal

Build an IT Troubleshooting Agent that can:
1. Understand the user’s IT issue.
2. Classify the issue type.
3. Retrieve relevant troubleshooting guidance using RAG.
4. Use tools to inspect users, devices, known incidents, tickets, and diagnostics.
5. Execute a sequential diagnostic workflow.
6. Run selected diagnostic checks in parallel where useful.
7. Branch conditionally based on issue type, severity, missing data, and tool 
results.
8. Generate a safe troubleshooting plan
9. Recommend escalation when required.
10. Generate ticket summaries for support handoff.
11. Avoid unsafe requests for passwords, OTPs, MFA codes, or secrets


# Dataset Description
## Knowledge-Base Documents
- vpn_troubleshooting_guide.md
- email_outlook_troubleshooting_guide.md
- laptop_performance_guide.md
- password_reset_guide.md
- network_connectivity_guide.md
- printer_troubleshooting_guide.md


## SQLite Operational Database
The database file is:

data/database/it_support.db

It contains these tables:
users
devices
tickets
known_incidents
diagnostic_snapshots

The SQLite database simulates operational IT support data.

# Target Users
Primary User: IT Support Engineer

Uses the agent to diagnose user issues and recommend next steps.

Secondary User: Helpdesk Agent
Uses the agent to summarize tickets and follow troubleshooting playbooks.

Optional User: IT Support Lead
Uses the agent to identify incidents, escalation patterns, and operational risks

# Required Implementation Choices
## Choice 1: LangGraph Pre-built ReAct Agent
The pre-built agent should be able to select from registered tools and produce a 
final answer based on tool outputs

## Choice 2: Custom LangGraph Agent
Required custom nodes:
- classify_issue_node
- retrieve_kb_node
- tool_diagnostics_node
- diagnostic_decision_node
- resolution_planner_node
- safety_review_node
- final_response_node

Recommended optional nodes:
- clarification_node
- escalation_node
- ticket_summary_node
- known_incident_node

# Required LangGraph Workflow Patterns
1. Sequential Pattern
2. Parallelization Pattern
3. Conditional Pattern

# Functional Requirements
FR-1: Knowledge-Base Loading

FR-2: Chunking and Indexing

FR-3: SQLite Database Connection

FR-4: Issue Classification

FR-5: Troubleshooting Retrieval Tool

FR-6: User Profile Tool

FR-7: Device Status Tool

FR-8: Known Incident Tool

FR-9: Diagnostic Check Tool

FR-10: Ticket Lookup Tool

FR-11: Resolution Plan Generation

FR-12: Safety Review

FR-13: Clarification Handling

FR-14: Ticket Summary Generation

# Required Tools
Mandatory tools:
1. retrieve_troubleshooting_steps
2. get_user_profile
3. get_device_status
4. check_known_incidents
5. run_diagnostic_check
6. get_ticket_details
7. create_resolution_plan

Recommended additional tools:
8. classify_issue_type
9. create_ticket_summary
10. check_escalation_required
11. search_tickets
12. get_active_incidents

# Recommended System Prompt
You are an enterprise IT Troubleshooting Agent.

You help IT support engineers diagnose user issues using troubleshooting guides and operational tools.

Rules:
- Use tools for user, device, ticket, incident, and diagnostic information.
- Use retrieved troubleshooting guides as the knowledge source for 
resolution steps.
- Do not invent user, device, incident, or ticket data.
- Do not ask for passwords, OTPs, MFA codes, private keys, or security 
tokens.
- If user identity or issue details are missing, ask a clarification 
question.
- If known incident exists, include it in the diagnosis.- If device metrics show high risk, recommend escalation.
- If issue requires Identity Access Management, Network Support, 
Messaging Support, Endpoint Support, or Workplace IT, mention the 
correct group.
- Keep final answers clear, operational, and safe.

# Suggested Graph State
```python
from typing import TypedDict, List, Dict, Optional
class TroubleshootingState(TypedDict):
    user_query: str
    issue_type: str
    user_identifier: Optional[str]
    retrieved_guidance: List[Dict]
    user_profile: Dict
    device_status: Dict
    known_incidents: List[Dict]
    diagnostic_snapshot: Dict
    resolution_plan: Dict
    safety_review: Dict
    final_response: str
```

# Author

Vikash Kumar