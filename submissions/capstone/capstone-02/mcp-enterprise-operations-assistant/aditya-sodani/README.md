# MCP-Based Enterprise Operations Assistant
## 1. Project Overview
The MCP-Based Enterprise Operations Assistant helps enterprise operations teams investigate service issues using natural language.
During incidents, engineers normally check multiple systems such as:
- Service health monitoring
- Active incidents
- Support tickets
- Recent operational changes
This project combines these systems using MCP servers and allows an LLM-powered MCP Host to automatically select tools, collect evidence, and generate operational summaries.

---
# 2. Project Objective
The objective of this project is to build an enterprise assistant using:
- FastMCP
- MCP Tools
- MCP Host
- mcp-use
- Groq LLM
- Python
- SQLite
- JSON data sources
- pytest
The assistant can:
- Connect with multiple MCP servers
- Discover available MCP tools
- Accept natural-language queries
- Allow Groq LLM to choose required tools
- Execute multi-server workflows
- Combine operational evidence into a final response

---
# 3. Architecture

User
↓
MCP Host + Groq LLM
↓
mcp-use MCP Agent
↓
MCP Client
↓
--------------------------------
Service Health MCP Server
Support Ticket MCP Server
Change Management MCP Server
--------------------------------
↓
Local Data Sources

Data:
Service Health Server
→ service_health.json
Support Ticket Server
→ tickets.db
Change Management Server
→ changes.json

---
# 4. Project Structure

mcp-enterprise-operations-assistant/
├── data/
│   ├── service_health.json
│   ├── tickets.db
│   ├── changes.json
│   └── sample_queries.json
│
├── servers/
│   ├── service_health_server.py
│   ├── support_ticket_server.py
│   └── change_management_server.py
│
├── src/
│   ├── host.py
│   ├── config.py
│   ├── prompts.py
│   ├── output_writer.py
│   ├── mcp_logger.py
│   └── tool_discovery.py
│
│
├── outputs/
│   ├── tool_discovery.json
│   ├── mandatory_query_results.json
│   └── test_results.txt
│
├── README.md
├── pyproject.toml
├── .env.example
└── .gitignore

---
# 5. MCP Servers

## Service Health MCP Server
File:
servers/service_health_server.py

Data Source:
data/service_health.json

Tools:
| Tool | Purpose |
|-|-|
| list_services | Lists all services and health status |
| get_service_health | Gets detailed health of a service |
| get_active_incidents | Returns active incidents |

---
## Support Ticket MCP Server
File:
servers/support_ticket_server.py

Data Source:
data/tickets.db

Tools:
| Tool | Purpose |
|-|-|
| search_tickets | Search tickets using filters |
| get_ticket_details | Get complete ticket details |
| get_high_priority_tickets | Returns open P1/P2 tickets |

---
## Change Management MCP Server

File:
servers/change_management_server.py

Data Source:
data/changes.json

Tools:

| Tool | Purpose |
|-|-|
| list_recent_changes | Lists latest changes |
| get_change_details | Gets change information |
| get_changes_for_service | Finds changes for a service |

---
# 6. Dataset

All operational data is local.

## service_health.json
Contains:
- Services
- Health metrics
- Active incidents

## tickets.db
SQLite database containing:
- ticket id
- service
- priority
- status
- customer impact

## changes.json
Contains:
- change records
- deployment details
- rollback information

---
# 7. Environment Setup

Create virtual environment:
uv init

Install dependencies:
uv add fastmcp mcp-use langchain-groq python-dotenv pydantic

Install testing packages:
uv add --dev pytest pytest-asyncio

---
# 8. Environment Variables

Create:
.env

Add:

GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile

Example file:
.env.example

contains:

GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile

---
# 9. Running MCP Servers

Each MCP server can run independently.

Service Health:

uv run python servers/service_health_server.py

Support Ticket:

uv run python servers/support_ticket_server.py

Change Management:

uv run python servers/change_management_server.py

---
# 10. Running MCP Host

Run:

uv run python -m src.host

Example:

Enterprise Operations Assistant
Enter Question:
Why is the Payment API unhealthy and is there any recent change?

Flow:

User Query
↓
Groq LLM
↓
MCP Agent
↓
Tool Selection
↓
MCP Server
↓
Tool Response
↓
Final Operational Answer

---
# 11. MCP Tool Discovery

Run:

uv run python -m src.tool_discovery

Generated file:

outputs/tool_discovery.json

Example:

{
   "service-health":[
       "list_services",
       "get_service_health",
       "get_active_incidents"
   ],
   "support-ticket":[
       "search_tickets",
       "get_ticket_details",
       "get_high_priority_tickets"
   ],
   "change-management":[
       "list_recent_changes",
       "get_change_details",
       "get_changes_for_service"
   ]
}

---
# 12. Multi Server Query Examples

## Query 1

Why is the Payment API unhealthy and is there any recent change?

Servers Used:
- Service Health
- Change Management

Tools:
- get_service_health
- get_active_incidents
- get_changes_for_service

---

## Query 2

Show high priority tickets for unhealthy services

Servers Used:
- Service Health
- Support Ticket

Tools:
- list_services
- get_high_priority_tickets

---

## Query 3

Show ticket TKT-1001 and related service health

Servers Used:
- Support Ticket
- Service Health

Tools:
- get_ticket_details
- get_service_health

---
# 13. Output Files

## current_tool_execution.json

It stores the tools, servers,evidences for current user query.

{
    "servers_used": [],
    "tools_used": [],
    "evidence": {
        "services": [],
        "incidents": [],
        "tickets": [],
        "changes": []
    }
}

## mandatory_query_results.json

Stores:

{
"user_query":"",
"servers_used":[],
"tools_used":[],
"evidence":{
"services":[],
"incidents":[],
"tickets":[],
"changes":[]
},
"operations_summary":"",
"possible_change_correlation":"",
"recommended_next_actions":[],
"limitations":[]
}

Values are generated from actual MCP execution.

---
# 14. Known Limitations

- Uses local JSON and SQLite data
- Does not connect to live monitoring
- No application logs available
- No distributed tracing
- Change correlation is based only on available evidence
- Assistant does not perform write operations

---
# 15. Future Improvements

- Live monitoring integration
- ServiceNow/Jira integration
- Deployment pipeline integration
- Application log MCP server
- Distributed tracing support
- Persistent incident memory
- Human approval workflow

---
# 16. Technologies Used

- Python
- FastMCP
- MCP
- mcp-use
- Groq LLM
- LangChain Groq
- SQLite
- JSON
- Pytest