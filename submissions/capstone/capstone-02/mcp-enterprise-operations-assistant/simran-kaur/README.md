# Project Overview
An enterprise operations team is responsible for monitoring business applications and responding toservice issues.During an operational incident, engineers usually need to check information from differentsystems:servicehealthactiveincidentssupport ticketsrecent application or configuration changesThe information is available, but it is spread across separate systems

# Project Objective
The completed application must:
Build three MCP servers.
Run the MCP servers using STDIO.
Build one MCP Host.
Connect the MCP Host to all three MCP servers.Discover tools exposed by the MCP servers.
Use Groq LLM inside the MCP Host.
Accept natural-language operational questions.Allow the LLM to decide which MCP tools are required.
Support queries that require tools from more than one MCP server.
Combine tool results into a clear operational answer.
Test MCP tools and multi-server execution.Document actual execution results.
# Architecture

User
                              │                              ▼
                     MCP Host + Groq LLM
                              │
                 MCP Client / mcp-use
                              │            ┌─────────────────┼─────────────────┐            │                 │                 │            ▼                 ▼                 ▼
   Service Health MCP   Support Ticket MCP   Change Management MCP          Server              Server                Server
            │                 │                 │            ▼                 ▼                 ▼
 service_health.json       tickets.db          changes.json


# MCP Servers
1. service_health_server:  It contains the health related information
2. support_ticket_server: It provides ticket information
3. change_management_server : it provide change relate information


# use app using

```bash
python -m src.host.py
```

# Tools

service-health
├── list_services
├── get_service_health
└── get_active_incidentssupport-ticket
├── search_tickets
├── get_ticket_details
└── get_high_priority_ticketschange-management
├── list_recent_changes
├── get_change_details
└── get_changes_for_service

# Dataset

# Setup
Provide the exact setup commands.Example:
uv sync
# Environment Variables
Explain  .env  configuration.
50
# Running the MCP Host
Provide the exact run command.
# Execution Flow
Explain:
User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Additional Tool Call if required
→ Final Answer

# Multi-Server Queries
Service Health + Change Management

Why is the Payment API unhealthy and is there any recent change that may be related?

Service Health + Support Tickets
Show high-priority open tickets for services that are currently unhealthy or degraded.

# Mandatory Query Results
The structured quesries were used to get relevant operational results from the agent.

The result of Q1 :Why is the Payment API unhealthy and is there any recent change that may be related?

is as followed

```text
        {
        "user_query": "Why is the Payment API unhealthy and is there any recent change that may be related?",
        "servers_used": [
            "MCP servers"
        ],
        "tools_used": [
            "get_service_health",
            "get_changes_for_service"
        ],
        "evidence": {
            "services": [
                {
                    "service_name": "Payment API",
                    "status": "UNHEALTHY"
                }
            ],
            "incidents": [],
            "tickets": [],
            "changes": [
                {
                    "change_id": "CHG-2001",
                    "service_name": "Payment API",
                    "change_type": "APPLICATION_RELEASE",
                    "status": "COMPLETED",
                    "risk": "HIGH",
                    "implemented_at": "2026-07-08T09:10:00",
                    "implemented_by": "Payments Engineering",
                    "summary": "Released payment-service changes for timeout handling and retry logic.",
                    "rollback_available": true
                }
            ]
        }
```
# Known Limitations

-The project uses local operational data.
-Service health values are stored snapshots rather than live monitoring metrics.
-The project does not include application logs or distributed traces.
-Possible change correlation is based on available service and timing evidence.
-The assistant does not perform operational write actions.
# Future Improvements
Reasonable improvements:
-Live monitoring integrationITSM -integrationDeployment system -integrationApplication log MCP serverDistributed -tracing integrationHuman approval for operational -actionsPersistent incident conversation memory