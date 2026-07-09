# MCP-Based Enterprise Operations Assistant
## Project Overview
This project is an MCP-Based Enterprise Operations Assistant designed to help operations teams monitor business applications and respond to service issues. It aggregates information from service health, active incidents, support tickets, and recent application changes spread across separate systems.

## Project Objective
The assistant uses FastMCP to expose operational tools, mcp-use to orchestrate multi-server client sessions, and Groq's LLM to interpret natural language queries. The LLM autonomously selects the appropriate MCP tools to combine evidence across distinct data sources and deliver clear, actionable operational summaries.

## Architecture
- MCP Host: Central interface containing the Groq LLM, receiving user queries, interpreting intent, selecting MCP tools via mcp-use agent, combining evidence, and generating final outputs.
- MCP Client: Bridges the Host and Servers using mcp-use managing STDIO sessions.
- MCP Servers: FastMCP implementations exposing tools over STDIO for specific domains (Service Health, Support Tickets, Change Management).
- Groq LLM: The intelligence inside the Host mapping natural language to multi-step tool calls.

## MCP Servers
- Service Health MCP Server: Reads from data/service_health.json.
- Support Ticket MCP Server: Reads from SQLite database data/tickets.db.
- Change Management MCP Server: Reads from data/changes.json.

## Tools

- **list_services** – List enterprise services and current health status.
- **get_service_health** – Return detailed health information for a service.
- **get_active_incidents** – Return active operational incidents.
- **search_tickets** – Search support tickets using predefined filters.
- **get_ticket_details** – Get full details of one support ticket.
- **get_high_priority_tickets** – Return high priority open status tickets.
- **list_recent_changes** - Return recent changes records.
- **get_change_details** - Return details of a specific change.
- **get_changes_for_service** - Find recent changes for a service.

## DataSet
Documents:
```
service_health.json
tickets.db
changes.json
sample_queries.json
```

## Setup
Clone the repository.

```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd mcp-enterprise-operations-assistant
```
Initialize **uv** Package in current directory
```
uv init
```

Create a virtual environment using uv package & activate the environment.

### Windows

```bash
uv venv 
.venv\Scripts\activate
```
Install the dependencies through toml file using uv package.

```bash
uv sync
```
---
## Environment variable setup

Create a `.env` file using the provided `.env.example`.
```env
GROQ_API_KEY= <your-groq-api-key>
GROQ_MODEL=llama-3.3-70b-versatile
```

## Running MCP Host
Run **host.py** using this command.
```bash
uv run python -m src.host
```
Then give user_query to the agent.

## Execution Flow
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
              │              ├── Yes → Call another MCP tool
              │              └── No
                   ↓
           Combine operational evidence
                   ↓
          Generate final operations answer
                   ↓
              Display response
```
## MCP Tool Discovery

| Servers | Discovered Tool | Purpose |
|---|---|---|
| service-health | list_services | List service health |
| service-health | get_service_health | Get one service's health |
| service-health | get_active_incidents | Find active incidents |
| support-ticket | search_tickets | Search tickets |
| support-ticket | get_ticket_details | Get ticket details |
| support-ticket | get_high_priority_tickets | Find P1/P2 open tickets |
| change-management | list_recent_changes | List recent changes |
| change-management | get_change_details | Get change details |
| change-management | get_changes_for_service | Find changes for a service |

## Multi-Server Queries
For a multi-server question, the flow may look like:
```
User:Why is the Payment API unhealthy and is there any recent change that may be related?
              ↓
get_service_health
Service Health MCP Server
              ↓
get_active_incidents
Service Health MCP Server
              ↓
get_changes_for_service
Change Management MCP Server
              ↓
Groq LLM combines evidence
              ↓
Final operational answer
```
## testing
Running testing command for complete suite:
```bash
uv run pytest tests/ -v
```
For saving Testing result in .txt file use this command:
```bash
uv run pytest tests/ -v > outputs/test_results.txt
```

## Test Results
```
Unit, MCP and Integration tests executed: 11
Passed: 8
Failed: 3
```

## Mandatory Query Results

| Query | Servers Used | Tools Used | Status |
|---|---|---|---|
| Q1 | service-health, change-management | 3 tools | PASS |
| Q2 | service-health, support-ticket | 3 tools | PASS |
| Q3 | database-cluster | 5 tools | PASS |
| Q4 | inventory-management | 5 tools | PASS |
| Q5 | analytics-pipeline, notification-engine, inventory-management | 4 tools | PASS |
| Q6 | inventory-management | 1 tool | PASS |
| Q7 | change-management, notification-engine | 1 tool | PASS |
| Q8 | database-cluster, authentication, payment-gateway | 3 tools | PASS |


## Know Limitations
The project uses local operational data.
Service health values are stored snapshots rather than live monitoring metrics.
The project does not include application logs or distributed traces.
The assistant does not perform operational write actions.

## Future Improvements
```
Live monitoringintegration
Deployment system integration
Application log MCP server
Persistent incident conversation memory
```

## Author 
**Ashish Sinha**