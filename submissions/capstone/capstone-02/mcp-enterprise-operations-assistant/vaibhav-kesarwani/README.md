# Capstone Build 02 - MCP-Based Enterprise Operations Assistant 

## Participant Name

**Vaibhav Kesarwani**

## Capstone Title

### MCP-Based Enterprise Operations Assistant

## Project Overview

This is an MCP-Based enterprise operations assistant which will assist the operations teams to identify the multiple operational incidents which checks for the different systems:

- service health
- active incidents
- support tickets
- recent application or configuration changes

The MCP host is connected with these MCP servers:

- Service Health server
- Support Ticket server
- Change Management server

which will helps the operations teams to ask the question in natural language to the assistant and give them the proper response according to the reports.

---

## Business Use Case

An enterprise operations team is responsible for monitoring business applications and responding to service issues.

During an operational incident, engineers usually need to check information from different systems:
 
- service health
- active incidents
- support tickets
- recent application or configuration changes

The information is available, but it is spread across separate systems.

The task is to build an MCP-Based Enterprise Operations Assistant.

The assistant should allow an operations engineer to ask these questions in natural language.

The LLM-powered MCP Host must connect to multiple MCP servers, select the required tools, combine information from different operational sources, and provide a clear response.

---

## Project Objective

This assistant will help the operations team to save there time and answer those questions which required more time to find and answer between spreaded documents. This assistant will make that task easier to understand.

Because it have the multiple MCP server connected to that assistant which allow the agent to perform those task easily using the tools which are assign to that agent.

---

## Architecture

The architecture of this assistant is as follow firstly it recieves the user input and than process the input and give to the MCP host which is connected with the Groq LLM whcih starts processing the user query.

And, than after that it goes to the MCP client to know how many tools are connected with it than there are three tools currently connected with the MCP Client are:

- Service Health MCP Server
    - tools
        - list_services
        - get_service_health
        - get_active_incidents

- Support Ticket MCP Server
    - tools
        - search_tickets
        - get_ticket_details
        - get_high_priority_tickets

- Change Management MCP Server
    - tools 
        - list_recent_changes
        - get_change_details
        - get_changes_for_service

And, than after getting the response back from the tools agent gives the response on the basis of that tool response.

---

## MCP Servers

The MCP Servers which are connected with the agent to give the response for that user query

#### 1. Service Health MCP Server

This server have the status of service health and incidents for those services which will show the current health status of those services.

```json
{
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
},
```

This server contain three tools:

- list_services
- get_service_health
- get_active_incidents

#### 2. Support Ticket MCP Server

This server have the tools related to the support ticket database which will help the agent to connect with those tools and use the tool output to give the response

Database link: [`Database link`](./data/tickets.db)

This server contains exactly three tools:

- search_tickets
- get_ticket_details
- get_high_priority_tickets

#### 3. Change Management MCP Server

This server have the tools related to the changes which are made in the required services and this mcp server have the changes data for all the services.

```json
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
},
```

This server had exactly three tools:

- list_recent_changes
- get_change_details
- get_changes_for_service

---

## Tools

### 1. list_services

It is present inside the `Service Health server`

#### Purpose:
List all services and their current health status

#### Input:
No mandatory input.

#### Output:

```json
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
        ... // more
    ]
}
```

### 2. get_service_health

It is present inside the `Service Health server`

#### Purpose:
Return detailed health information for one service.

#### Input:
```json
{
    "service_name": "Payment API"
}
```

#### Output:
```json
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
```

### 3. get_active_incidents

It is present inside the `Service Health server`

#### Purpose:
Return active operational incidents. The tool may optionally filter by service.

#### Input:
```json
{
    "service_name": "Payment API"
}
```

#### Output:
```json
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

### 4. search_tickets

It is present inside the `Support Ticket server`

#### Purpose:
Search support tickets using predefined filters.

#### Supported Filters:
- service_name
- priority
- status
- limit

#### Input:
```json
{
    "service_name": "Payment API",
    "status": "OPEN",
    "limit": 20
}
```

#### Output:
```json
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
```

### 5. get_ticket_details

It is present inside the `Support Ticket server`

#### Purpose:
Get full details of one support ticket.

#### Input:
```json
{
    "ticket_id": "TKT-1001"
}
```

#### Output:
```json
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
```

#### Invalid Ticket Output:
```json
{
    "found": false,
    "message": "Ticket not found."
}
```

### 6. get_high_priority_tickets

It is present inside the `Support Ticket server`

#### Purpose:
Return open P1 and P2 tickets.
The tool may optionally filter by service.

#### Input:
```json
{
    "service_name": "Payment API"
}
```

#### Output:
```json
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
```

High-priority tickets are:

- P1
- P2

Only open tickets should be returned by this tool

### 7. list_recent_changes

It is present inside the `Change Management server`

#### Purpose:
Return recent change records.

#### Input:
```json
{
    "limit": 10
}
```

#### Output:
```json
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
```
Changes should be returned with the most recent first

### 8. get_change_details

It is present inside the `Change Management server`

#### Purpose:

Return details of a specific change.

#### Input:
```json
{
    "change_id": "CHG-2001"
}
```

#### Output:
```json
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

### 9. get_changes_for_service

It is present inside the `Change Management server`

#### Purpose:

Find recent changes for a service.

#### Input:
```json
{
    "service_name": "Payment API"
}
```

#### Output:
```json
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

---

## Dataset

Document:

- service_health.json
- tickets.db
- changes.json
- sample_queries.json

The data files present inside the `/data` folder.

---

## Setup

## Setup Instructions

---

## Setup `.env`

```bash
GROQ_API_KEY=...
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
uv venv
```

Activate the environment:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
uv pip install -r requirements.txt
```

## Running the MCP Host

Use the below command to run the script.

```bash
uv run src/host.py
```

---

## Execution Flow

```bash
User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Final Answer
```

---

## MCP Tool Discovery

Tool discovery is made in the `tool_discovery.py` file which is inside the `src/` folder.

```json
[
    {
        "server": "service-health",
        "tools": [
            "list_services",
            "get_service_health",
            "get_active_incidents"
        ]
    },
    {
        "server": "support-ticket",
        "tools": [
            "search_tickets",
            "get_ticket_details",
            "get_high_priority_tickets"
        ]
    },
    {
        "server": "change-management",
        "tools": [
            "list_recent_changes",
            "get_change_details",
            "get_changes_for_service"
        ]
    }
]
```

---

## Testing Results

To see the testing result you look for the [`test_file`](./outputs/test_results.txt)

### Commands Used

```bash
uv run pytest tests/-v-m "not integration"
uv run pytest tests/-v-m integration
```

### Result Summary

```bash
Unit and MCP tests executed: 12
Passed: 12
Failed: 0

Integration tests executed: 3
Passed: 3
Failed: 0
```

### Components Tested

```bash
- Service Health MCP tools
- Support Ticket MCP tools
- Change Management MCP tools
- Invalid service handling
- Invalid ticket handling
- MCP server connectivity
- MCP tool discovery
- Multi-server host query
- Groq MCP agent integration
```

---

## Query Results

The summary table of all 8 queries is: 

| Query|Serves used|Tools Used|Status|
| - | - | - | - |
|Q1|service_health, change_management|list_recent_changes|PASS|
|Q2|service_health, recent_changes|list_recent_changes, list_services, get_service_health|PASS|
|Q3|service_health, support_ticket|list_services, get_high_priority_tickets, get_service_health|PASS|
|Q4|service_health, support_ticket|list_services, serach_tickets, get_service_health|PASS|
|Q5|service_health, change_management|list_services, list_recent_changes|PASS|
|Q6|service_health, change_management|list_services, list_recent_changes|PASS|
|Q7|service_health, support_ticket|list_services, get_ticket_DETAILS, get_service_health|PASS|
|Q8|service_health, change_management|list_recent_changes|PASS|
---


## Known Limitations

- The project uses local operational data.
- Service health values are stored snapshots rather than live monitoring metrics.
- The project does not include application logs or distributed traces.
- Possible change correlation is based on available service and timing evidence.
- The assistant does not perform operational write actions.

---

## Future Improvements

- Live monitoring integration
- Deployment system integration
- Application log MCP server
- Distributed tracing integration
- Human approval for operational actions
- Persistent incident conversation memory