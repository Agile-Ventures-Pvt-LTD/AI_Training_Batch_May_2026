# Project Overview

An enterprise operations team is responsible for monitoring business applications and responding to
service issues.
During an operational incident, engineers usually need to check information from different systems:
- service health
- active incidents
- support tickets
- recent application or configuration changes
The information is available, but it is spread across separate systems.
The problem leads to delay in resolving any incident that had occured which leads to operations delay, delay in incident solving,
problem in managing tickets and knowing recent changes becomes problematic

# Project Objective

- The main objective of the project is to build **an MCP-Based Enterprise Operations Assistant** that solves the problem occured during operational incidents.
- Here our MCP based assistant solves this problem by managing different servers for different tasks. It uses 3 servers each server have different number of tools that are specified to do some unique work to resolve the problem.
- For every server we had created different client so that correct client gets the correct server request and then pass it to Host to get the response.
- Our Architecture use LLM so it takes Natural Language query from user and Generate answer in Natural language for every user query this helps in better understanding of the Incidents that occured.
- The main objective of the whole build is that any Natural language query going to LLM must route to client so it can the specific server and use tools to get the query response and then our LLM generate a Natural Language summarized response.

# Architecture

The Architecture consists of 4 major components that helps in responding user query and also ensures security validation
1. **MCP HOST:** It is where our Agent and our all MCP Client are declared. MCP Host is important because here Agent is used to generate the response of user query in Natural Language and our Client also config with all the servers it needs.

2. **MCP CLIENT:** MCP Client is the important part of the architecture that helps to connect with the corresponding MCP Servers.
It takes user query from LLM and call the corresponding server it needs to connect to get the tools response from the servers.

3. **MCP SERVER:** Servers are the componets that give tools access to client and LLM so the answer generated is directly from the tools not from its knowledge base and It uses two methods to communicate with the client **STDIO** and **STREAMABLE HTTP** modes.

4. **GROQ LLM:** It is the model used to repond the query given by user using the tools response it gets from the client.


# MCP Server

**Service Health MCP Server(service_health_server.py):** It uses the document **service_health.json** file to the services from the data and its status.

**Support Ticket MCP Server(support_ticket_server.py):** It uses the **ticket.db** data to make tools to get ticket_id, priority and status of the tickets to resolve issues.

**Change Management MCP Server(change_management_server.py):** IT uses **changes.json** file to get the recent changes made in services to get latest information to solve issues.

# Tools

**service_health_server.py tools:**
1. list services:
- purpose: List all services and their current health status
- input: No mandatory input
2. get_service_health:
- purpose: Return detailed health information for one service.
- input: "service_name": "Payment API"
3. get_active_incidents
- purpose: Return active operational incidents.
- input: "service_name": "Payment API"

**support_ticket_server.py tools**
1. search_tickets:
- purpose:Search support tickets using predefined filters.
- input: 
"service_name": "Payment API",
"status": "OPEN",
"limit": 20
2. get_ticket_details:
- purpose:Get full details of one support ticket.
- input: "ticket_id": "TKT-1001"
3. get_high_priority_tickets:
- purpose: Return open P1 and P2 tickets
- input: "service_name": "Payment API"

**change_management_server.py tools**
1. list_recent_changes:
- purpose:Return recent change records.
- input: "limit": 10
2. get_change_details:
- purpose:Return details of a specific change.
- input: "change_id": "CHG-2001"
3. get_changes_for_service:
- purpose: Find recent changes for a service.
- input: "service_name": "Payment API"

# Dataset
Document:
- service_health.json
- tickets.db
- changes.json
- sample_queries.json

# Setup

```bash
uv venv
uv pip install -r requirements.txt
```

# Environments Variable
```bash
.env.example
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile
```

# Running the MCP HOST
```bash
python -m src.host
```

# Execution Flow
```text
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

# Project Structure
```
mcp_enterprise_operations_assistant/
│
├── README.md
├── .env.example
│
├── data/
│   ├── service_health.json
│   ├── tickets.db
│   ├── changes.json
│   └── sample_queries.json
│
├── scripts/
│   └── create_ticket_db.py
│
├── servers/
│   ├── service_health_server.py
│   ├── support_ticket_server.py
│   └── change_management_server.py
│
├── src/
│   ├── __init__.py
│   ├── host.py
│   ├── config.py
│   ├── prompts.py
│   ├── tool_discovery.py
│   └── output_writer.py
│
├── tests/
│   ├── test_service_health_tools.py
│   ├── test_ticket_tools.py
│   ├── test_change_tools.py
│   ├── test_mcp_discovery.py
│   └── test_host_queries.py
│
└── outputs/
├── tool_discovery.json
├── mandatory_query_results.json
├── sample_run_outputs.md
└── test_results.txt
```

# Multi-Server Queries

- Why is the Payment API unhealthy and is there any recent change that may be related
- Show high-priority open tickets for services that are currently unhealthy or degraded.
- Was there any recent change for Checkout Service that may explain the current degradation?
- Which recent changes were made to services that currently have active incidents?

# Testing
```bash
uv run pytest tests/test_service_health_tools.py
```

# Test Results

```
outputs/test_result.txt
```

#  Known Limitations

- The project uses local operational data.
- Service health values are stored snapshots rather than live monitoring metrics.
- The project does not include application logs or distributed traces.
- Possible change correlation is based on available service and timing evidence.
- The assistant does not perform operational write actions.

# Future Imporovement

- Human approval for operational actions.
- Persistent incident conversation memory.
- More server and tools can be integrated.

# Author 

**Mohd Zaid Ansari**


