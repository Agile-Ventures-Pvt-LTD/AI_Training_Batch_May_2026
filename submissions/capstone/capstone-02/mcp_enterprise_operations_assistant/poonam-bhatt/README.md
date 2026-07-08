# MCP Enterprise operations assistant:

1. ## Project Overview:

```
An enterprise operations team is responsible for monitoring business applications and responding to
service issues.

During an operational incident, engineers usually need to check information from different systems:
- service health
- active incidents
- support tickets
- recent application or configuration changes

The information is available, but it is spread across separate systems.

For example, when the Payment API becomes unhealthy, the operations team may need to answer:

- What is wrong with the Payment API?
- Is there an active incident?
- Are customers reporting the same issue?
- Are there any high-priority support tickets?
- Was a recent change made to the Payment API?
- Could the timing of a recent change be related to the current incident.

```


2. ##  Project Objective:

```
We are building an MCP-Based Enterprise Operations Assistant.

The assistant should allow an operations engineer to ask these questions in natural language.

The LLM-powered MCP Host must connect to multiple MCP servers, select the required tools, combine
information from different operational sources, and provide a clear response.

```

3. ##  Architecture:

```

                           User
                            │
                            ▼
                   MCP Host + Groq LLM
                            │
                   MCP Client / mcp-use
                            │
 ┌──────────────────────────┼──────────────────────────┐
 │                          │                          │
 ▼                          ▼                          ▼
 Service Health     MCP Support Ticket MCP       Change Management MCP
 Server                  Server                    Server
 │                          │                          │
 ▼                          ▼                          ▼
 service_health.json      tickets.db               changes.json


 ```

 4. ## MCP Servers: 



- Service Health MCP Server

File:
```
servers/service_health_server.py
```
Data source:
```
data/service_health.json
```
The server expose exactly these three mandatory tools:
1. list_services
2. get_service_health
3. get_active_incidents


- Support Ticket MCP Server

File:
```
servers/support_ticket_server.py
```
Data source:
```
data/tickets.db
```
The server must expose exactly these three mandatory tools:
1. search_tickets
2. get_ticket_details
3. get_high_priority_tickets


- Change Management MCP Server

File:
```
servers/change_management_server.py
```
Data source:
```
data/changes.json
```
The server expose exactly these three mandatory tools:
1. list_recent_changes
2. get_change_details
3. get_changes_for_service

5. ## Tools: 

5.1 Tool – list_services
```
Purpose: List all services and their current health status.
Input: No mandatory input.
Expected Output: 
{
"count": 5,
"services": [
{
"service_name": "Payment API",
"status": "UNHEALTHY",
"region": "India-West"
},
{
"service_name": "Checkout Service",
"status": "DEGRADED",
"region": "India-West"
}
]
}
The actual output must come from service_health.json .
```

5.2 Tool – get_service_health
```
Purpose: Return detailed health information for one service.
Input: 
{
"service_name": "Payment API"
}
Expected Output: 
{
"found": true,
"service": {
"service_name": "Payment API",
"service_id": "SVC-PAY-01",
"status": "UNHEALTHY",
"region": "India-West",
"error_rate_percent": 38.0,
"average_latency_ms": 1850,
"cpu_usage_percent": 42,
"memory_usage_percent": 61,
"last_checked": "2026-07-08T10:00:00",
"active_incident_ids": [
"INC-OPS-101"
]
}
}
Invalid Service Output
{
"found": false,
"message": "Service not found."
}
```

5.3 Tool – get_active_incidents
```
Purpose: Return active operational incidents.
The tool may optionally filter by service.
Input Example: 
{
"service_name": "Payment API"
}
Expected Output: 
{
"count": 1,
"incidents": [
{
"incident_id": "INC-OPS-101",
"service_name": "Payment API",
"severity": "SEV-1",
"status": "ACTIVE",
"summary": "Payment processing requests are experiencing elevated timeout 
failures.",
"customer_impact": "Customers may be unable to complete card payments.",
"assigned_group": "Application Support"
}
]
}
```

5.4 Tool – search_tickets
```
Purpose: Search support tickets using predefined filters.
Supported Filters: 
service_name
priority
status
limit
Input Example: 
{
"service_name": "Payment API",
"status": "OPEN",
"limit": 20
}
Expected Output: 
{
"count": 4,
"tickets": [
{
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout",
"customer_impact": "High",
"assigned_group": "Application Support"
}
]
}
Apply a reasonable maximum result limit.
Recommended maximum: 50
```


5.5 Tool – get_ticket_details
```
Purpose: Get full details of one support ticket.
Input:
{
"ticket_id": "TKT-1001"
}
Expected Output:
{
"found": true,
"ticket": {
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout",
"description": "Customers report payment failures and timeout errors.",
"created_at": "2026-07-08T09:58:00",
"customer_impact": "High",
"assigned_group": "Application Support"
}
}
Invalid Ticket Output
{
"found": false,
"message": "Ticket not found."
}
```

5.6 Tool – get_high_priority_tickets
```
Purpose: Return open P1 and P2 tickets.
The tool may optionally filter by service.
Input Example:
{
"service_name": "Payment API"
}
Expected Output:
{
"count": 3,
"tickets": [
{
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout"
}
]
}
High-priority tickets are:
P1
P2
Only open tickets should be returned by this tool.
```

5.7 Tool – list_recent_changes
```
Purpose: Return recent change records.
Input:
{
"limit": 10
}
Expected Output:
{
"count": 5,
"changes": [
{
"change_id": "CHG-2001",
"service_name": "Payment API",
"change_type": "APPLICATION_RELEASE",
"status": "COMPLETED",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00"
}
]
}
Changes should be returned with the most recent first.
```

5.8 Tool – get_change_details
```
Purpose: Return details of a specific change.
Input: 
{
"change_id": "CHG-2001"
}
Expected Output: 
{
"found": true,
"change": {
"change_id": "CHG-2001",
"service_name": "Payment API",
"change_type": "APPLICATION_RELEASE",
"status": "COMPLETED",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00",
"implemented_by": "Payments Engineering",
"summary": "Released payment-service changes for timeout handling and retry 
logic.",
"rollback_available": true
}
}
```

5.9 Tool – get_changes_for_service
```
Purpose: Find recent changes for a service.
Input:
{
"service_name": "Payment API"
}
Expected Output:
{
"service_name": "Payment API",
"count": 1,
"changes": [
{
"change_id": "CHG-2001",
"change_type": "APPLICATION_RELEASE",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00",
"summary": "Released payment-service changes for timeout handling and 
retry logic.",
"rollback_available": true
}
]
}
```

6. ## Dataset:

1. Service Health

File:
```
data/service_health.json
```

The file contains:
services
incidents

A service record contains fields such as:
```
{
}
"service_name": "Payment API",
"service_id": "SVC-PAY-01",
"status": "UNHEALTHY",
"region": "India-West",
"error_rate_percent": 38.0,
"average_latency_ms": 1850,
"cpu_usage_percent": 42,
"memory_usage_percent": 61,
"last_checked": "2026-07-08T10:00:00",
"active_incident_ids": [
"INC-OPS-101"
]
```

An incident record contains fields such as:

```
{
"incident_id": "INC-OPS-101",
"service_name": "Payment API",
"severity": "SEV-1",
"status": "ACTIVE",
"started_at": "2026-07-08T09:55:00",
"summary": "Payment processing requests are experiencing elevated timeout 
failures.",
"customer_impact": "Customers may be unable to complete card payments.",
"assigned_group": "Application Support"
}
```

This file is the source of truth for service and incident information.

2. Support Tickets

File:
```
data/tickets.db
```
The SQLite database contains:
tickets

The table contains:
Column
ticket_id            :      Unique ticket identifier
service_name         :      Related service
priority             :      P1, P2, P3, or P4
status               :      Ticket status
subject              :      Short ticket subject
description          :      Ticket description
created_at           :      Ticket creation time
customer_impact      :      Recorded impact
assigned_group       :      Support group

Example record:
```
Ticket ID: TKT-1001
Service: Payment API
Priority: P1
Status: OPEN
Subject: Card payment timeout
Assigned Group: Application Support
```
The dataset contains multiple tickets across different services and priorities.

A recreation script is provided:
```
scripts/create_ticket_db.py
```
To recreate the database:

```bash
uv run python scripts/create_ticket_db.py
```

3. Change Management

File:
```
data/changes.json
```
The file contains recent operational changes.
```
Example:
{
"change_id": "CHG-2001",
"service_name": "Payment API",
"change_type": "APPLICATION_RELEASE",
"status": "COMPLETED",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00",
"implemented_by": "Payments Engineering",
"summary": "Released payment-service changes for timeout handling and retry 
logic.",
"rollback_available": true
}
```

This file is the source of truth for change information.
The agent may identify a possible correlation between a change and an incident.
The agent must not claim that a change is the confirmed root cause unless the data explicitly proves it.


7. ## Setup: 

Exact Setup using uv.
```bash
uv init
```
```bash
uv venv
```
```bash
.venv\Scripts\activate
```

8. ## Environment Variables:

Created .env file.
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

9. ## Running the MCP Host:

To run MCP Host use the following command:

```bash
python -m src.host
```

10. ## Execution Flow: 

```
User enters an operations question
              ↓
MCP Host receives the question
              ↓
Groq LLM interprets the request
              ↓
MCP Agent reviews available MCP tools
              ↓
LLM selects required MCP tool
              ↓
MCP Client calls the correct MCP server
              ↓
MCP server reads local operational data
              ↓
Structured tool result returned
              ↓
LLM decides whether another tool is required
              │
              ├── Yes → Call another MCP tool
              │
              └── No
                   ↓
           Combine operational evidence
                   ↓
          Generate final operations answer
                   ↓
              Display response
```

11. ## MCP Tool Discovery
 
Tools created under tool_discovery are: 
- list_services
- get_service_health
- get_active_incidents
- search_tickets
- get_ticket_details
- get_high_priority_tickets
- list_recent_changes
- get_change_details
- get_changes_for_service

12. ## Multi-Server Queries:

Following are the queries that uses multiple server: 

Service Health + Change Management
```
- Why is the Payment API unhealthy and is there any recent change that may be 
related?
Expected server usage:
Service Health MCP Server
Change Management MCP Server
```
Service Health + Support Tickets
```
- Show high-priority open tickets for services that are currently unhealthy or 
degraded.
Expected server usage:
Service Health MCP Server
Support Ticket MCP Server
```
Support Ticket + Service Health
```
- Show the details of ticket TKT-1001 and check the health of its related service.
Expected server usage:
Support Ticket MCP Server
Service Health MCP Server
```
13. ## Testing:
Explain:
Tool tests
MCP discovery tests
Host integration tests
14. ## Test Results

To run all the test cases at once use following command:

```bash
pytest tests/
```

15. ## Mandatory Query Results

16. ## Known Limitations

```
The project uses local operational data.
Service health values are stored snapshots rather than live monitoring metrics.
The project does not include application logs or distributed traces.
Possible change correlation is based on available service and timing evidence.
The assistant does not perform operational write actions.
```

17. ## Future Improvements: 

Reasonable improvements:
```
Live monitoring integration
ITSM integration
Deployment system integration
Application log MCP server
Distributed tracing integration
Human approval for operational actions
Persistent incident conversation memory
```