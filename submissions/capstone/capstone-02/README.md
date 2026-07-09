## MCP-Based Enterprise Operations Assistant
Business Scenario
An enterprise operations team is responsible for monitoring business applications and responding to
service issues.
During an operational incident, engineers usually need to check information from different systems:
service health
active incidents
support tickets
recent application or configuration changes
## 2. Project Objective
Build an enterprise operations assistant using:
FastMCP
MCP tools
MCP Host
mcp-use
Groq LLM
Python
local JSON files
SQLite
pytest
## 5. Project Scope
This project is focused on read-only enterprise operations investigation.
##  Technical Dependencies
fastmcp
mcp-use
langchain-groq
python-dotenv
pydantic
pytest
pytest-asyncio
## Environment Configuration
.env
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
## Dataset Provided
```
The provided files are:
data/
├── service_health.json
├── tickets.db
├── changes.json
└── sample_queries.json
scripts/
└── create_ticket_db.py
README_dataset.md
```
## Required MCP Server
1. service_health_server
2. support_ticket_server
3. change_management_server
## MCP Tool Discovery
```
service-health
├── list_services
├── get_service_health
└── get_active_incidents
support-ticket
├── search_tickets
├── get_ticket_details
└── get_high_priority_tickets
change-management
├── list_recent_changes
├── get_change_details
└── get_changes_for_servic
```
## Application Execution Flow
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
 ##  Project Structure
 ```
 mcp_enterprise_operations_assistant/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│ ├── service_health.json
│ ├── tickets.db
│ ├── changes.json
│ └── sample_queries.json
│
├── scripts/
│ └── create_ticket_db.py
│
├── servers/
│ ├── service_health_server.py
│ ├── support_ticket_server.py
│ └── change_management_server.py
│
├── src/
│ ├── __init__.py
│ ├── host.py
34
│ ├── config.py
│ ├── prompts.py
│ ├── tool_discovery.py
│ └── output_writer.py
│
├── tests/
│ ├── test_service_health_tools.py
│ ├── test_ticket_tools.py
│ ├── test_change_tools.py
│ ├── test_mcp_discovery.py
│ └── test_host_queries.py
│
└── outputs/
 ├── tool_discovery.json
 ├── mandatory_query_results.json
 ├── sample_run_outputs.md
 └── test_results.txt
 ```
 