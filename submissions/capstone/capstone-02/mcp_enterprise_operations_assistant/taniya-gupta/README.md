# Capstone project 02 - MCP-Based Enterprise Operations Assistant

## Project overview

This project demonstrates the use of MCP servers, in this project we have used three mcp servers to build an operations AI assistant.

An enterprise operations team is responsible for monitoring business applications and responding to
service issues.
During an operational incident, engineers usually need to check information from different systems:
service health
active incidents
support tickets
recent application or configuration changes
The information is available, but it is spread across separate systems.

## Solution approach

The project contains four main components.

| Component                    | Purpose                                                         |
|------------------------------|-----------------------------------------------------------------|
| Service Health MCP Server    | Provides service health and active incident information         |
| Support Ticket MCP Server    | Provides support-ticket information                             |
| Change Management MCP Server | Provides recent change information                              |
| MCP Host                     | Contains the Groq LLM and uses tools from all three MCP servers |


- This project has four main components, Service Health MCP Server which provides service health and active incident information, Support Ticket MCP Server which provides support-ticket information, Change Management MCP Server which provides recent change information and MCP Host which contains the Groq LLM and uses tools from all three MCP servers.

## Architecture


```
                   User Query (CLI)
                         │
                         ▼
                MCP Host + Groq LLM
                         │
                MCP Client / mcp-use
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
Service Health     Support Ticket    Change Management
  MCP Server         MCP Server         MCP Server
      │                  │                  │
      ▼                  ▼                  ▼
service_health.json   tickets.db       changes.json
```

**MCP host**: MCP Host is the user-facing application that orchestrates interactions and provides the interface for users to engage with AI agents.

**MCP Client**: MCP Client is the component running within the host that manages 1:1 connections to external services, handling tool discovery, request routing, and maintaining the active session with servers.

**MCP Server**: MCP Server is an external service provider that exposes tools, resources, and capabilities in a standardized format, allowing the client to discover and execute functions like API calls or data retrieval.

**GROQ LLM**:Groq LLM refers to the large language models hosted on GroqCloud that utilize the Model Context Protocol (MCP) to interact with these external tools via Groq’s fast, low-latency inference engine. 

## MCP Servers

**Service Health MCP Server**: This server provides service health and active incident information, it has three tools - "list_services","get_service_health","get_active_incidents". This server uses `service_health.json ` file

**Support Ticket MCP Server**: This server provides support-ticket information, it has three tools - "search_tickets", "get_ticket_details", "get_high_priority_tickets". This server uses `tickets.db` file.

**Change Management MCP Server**: This server provides recent change information, it has four tools- "list_recent_changes",   "get_change_details",   "get_changes_for_service",   "get_changes_for_services", This server uses ` changes.json` file.

## Tools
**list_services**: This tool is under service-health server, it lists services and their current health status.
**get_service_health**: This tool is under service-health server, Return detailed health information for one service, input: service_name is required.
**get_active_incidents**: This tool is under service-health server, Return active operational incidents, the tool filters by services, input: service_name
**search_tickets**: This tool is under support-ticket server, Search tickets using predefined filters, also adding a max limit, input: service_name, priority, status, limit
**get_ticket_details**: This tool is under support-ticket server, Get full details of one support ticket, input: ticket id is required 
**get_high_priority_tickets**: This tool is under support-ticket server, Get open P1 and P2 tickets, input: service_name
**list_recent_changes**: This tool is under change-management server, List recent change records sorted by implemented_at in descending order, input: limit
**get_change_details**: This tool is under change-management server, Return details of a specific change, input: change_id
**get_changes_for_service**: This tool is under change-management server, Get recent changes for a service, it is sorted by implemented_at by descending order, input :service_name
**get_changes_for_services**: This tool returns get_changes_for_service tool

## Dataset
 
For the dataset, we have four files namely
-service_health.json
-tickets.db
-changes.json
-sample_queries.json

All operational data used for this project is local.

## Setup

Do 'uv init' to initialize uv, then create a venv and activate it

### 1. Installation
install the dependencies from requirements.txt:
```bash
uv add -r requirements.txt
```

### 2. Configuration
Copy the `.env.example` file to `.env` and add your Groq API Key and model

### 3. Run the app
```bash
uv run python src/host.py
```

### To run the batch mandatory questions
```bash
uv run python src/host.py --batch
```

## Execution flow

User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Additional Tool Call if required
→ Final Answer

--- 

Receive user question
 ↓
Use Groq LLM
 ↓
Understand the request
 ↓
Select MCP tool or tools
 ↓
Call MCP servers
 ↓
Receive operational data
 ↓
Combine the evidence
 ↓
Generate final answer


## MCP Tool Discovery

From `outputs/tool_discovery.json`,

```bash
{
  "service-health": [
    "list_services",
    "get_service_health",
    "get_active_incidents"
  ],
  "support-ticket": [
    "search_tickets",
    "get_ticket_details",
    "get_high_priority_tickets"
  ],
  "change-management": [
    "list_recent_changes",
    "get_change_details",
    "get_changes_for_service",
    "get_changes_for_services"
  ]
}
```

## Multi-Server Queries

Q1- This query has used two servers,  "service-health", "change-management"
Q2 - This query has used two servers, "service-health", "support-ticket"
Q3 - This query has used two servers, "service-health", "support-ticket"
Q4 - This query has used two servers,  "service-health", "change-management"

## Testing


========================================== 13 passed, 35 warnings in 60.87s (0:01:00) =========================================== 

All testcases have been paased by the implementation, the testcases have been created to implement Tool tests, MCP discovery tests and Host integration tests


## Mandatory Query Results

| Query | Servers Used                          | Status |
|-------|---------------------------------------|--------|
| Q1    | "service-health", "change-management" | PASS   |
| Q2    | "support-ticket", "service-health"    | PASS   |
| Q3    | "support-ticket", "service-health"    | PASS   |
| Q4    | "service-health", "change-management" | PASS   |
| Q5    | "support-ticket", "service-health"    | PASS   |
| Q6    | "service-health", "change-management" | PASS   |
| Q7    | "support-ticket", "service-health"    | PASS   |
| Q8    | "change-management"                   | PASS   |


## Challenges Faced

<!-- langgraph.errors.GraphRecursionError: Recursion limit of 20 reached without hitting a stop condition. You can increase the limit by setting the `recursion_limit` config key. -->
- This error was caused when used openai/gpt-oss-120b model of groq

- Tool prompt validation


## Known Limitations
-The project uses local operational data.
-Service health values are stored snapshots rather than live monitoring metrics.
-The project does not include application logs or distributed traces.
-Possible change correlation is based on available service and timing evidence.
-The assistant does not perform operational write actions.

## Future Improvements
-Live monitoring integration
-ITSM integration
-Deployment system integration
-Application log MCP server
-Distributed tracing integration
-Human approval for operational actions
-Persistent incident conversation memory
-UI or web interface integration

