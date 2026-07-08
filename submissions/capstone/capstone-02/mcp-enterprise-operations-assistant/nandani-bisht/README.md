## Project Name:
MCP-Based Enterprise Operations Assistant

## Project Overview:
An enterprise operations team is responsible for monitoring business applications and responding to service isssues.

During the incident, engineers usually need to check information from different systems:
.service health
.active incidents
.support tickets
.recent application or configuration changes

## Participation Name:
Nandani Bisht

## Project Objective
The objective of the project is we have to build an enterprise opeartions assistant using the 
```
* FastMCP
* MCP tools
* MCP Host
* mcp-use
* Groq LLM
* python
* local JSON files
* SQLite
* pytest
```

## Architecture of the Project:
The LLM must be inside the MCP Host.
The responsibility of the MCP Host is to:

```
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
```

## MCP Servers:
Document:
**Service Health MCP Server** 

**Support Ticket MCP Server**

**Change Management MCP Server**

## Tools:
Tool name 
MCP server
Purpose
Input
Output

## Dataset:
**service_health.json**
**tickets.db**
**changes.json**
**sample_queries.json**



## Setup:

```
uv init
uv venv
uv add -r requirements.txt
```
## Environment Variables:

GROQ_API_KEY = "your_api_key"
GROQ_MODEL = llama-3.3-70b-versatile

## Running the MCP Host:
``` uv run python -m src.host```

## Limitations:
1. The project uses local operational data.
2. Service health values are stored snapshots rather than live monitoring metrics.
3. The project does not include application logs or distributed traces.
4. Possible change correlation is based on available service and timing evidence.
5. The assistant does not perform operational write actions

## Future improvements:
1. Live monitoring integration
2. ITSM integration
3. Deployment system integration
4. Application log MCP server
5. Distributed tracing integration
6. Human approval for operational actions
7. Persistent incident conversation memory



