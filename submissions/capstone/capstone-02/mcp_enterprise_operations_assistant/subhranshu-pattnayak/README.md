# **`CAPSTONE PROJECT BUILD – 2`**
# **`MCP-Based Enterprise Operations Assistant`**

This is a MCP-Based Enterprise Operations Assistant.

The assistant should allows an operations engineer to ask questions in natural language and  provides a clear response using combined information from different operational sources.


---

## 1. Project Overview

Enterprise operations teams are usually responsible for monitoring business applications and responding to
service issues. During an operational incident, engineers usually need to check information from different systems:

- service health
- active incidents
- support tickets
- recent application or configuration changes

The assistant allows an operations engineer to ask these questions in natural language.

The LLM-powered MCP Host connects to multiple MCP servers, selects the required tools, combines information from different operational sources, and provide a clear response.


---

## 2. Project Objective

The enterprise operations assistant uses:

- FastMCP
- MCP tools
- MCP Host
- mcp-use
- Groq LLM
- Python
- local JSON files
- SQLite
- pytest

The application does:

- Build three MCP servers.
- Run the MCP servers using STDIO.
- Build one MCP Host.
- Connect the MCP Host to all three MCP servers.
- Discover tools exposed by the MCP servers.
- Use Groq LLM inside the MCP Host.
- Accept natural-language operational questions.
- Allow the LLM to decide which MCP tools are required.
- Support queries that require tools from more than one MCP server.
- Combine tool results into a clear operational answer.
- Test MCP tools.

---

## 3. Architecture

```
subhranshu-pattnayak
├── .env.example
├── .gitignore
├── .pytest_cache
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v
│       └── cache
│           ├── lastfailed
│           └── nodeids
├── .python-version
├── README.md
├── data
│   ├── changes.json
│   ├── sample_queries.json
│   ├── service_health.json
│   └── tickets.db
├── outputs
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── scripts
│   └── create_ticket_db.py
├── servers
│   ├── __init__.py
│   ├── change_management_server.py
│   ├── confserver.py
│   ├── service_health_server.py
│   └── support_ticket_server.py
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── host.py
│   ├── output_writer.py
│   ├── prompts.py
│   ├── server.ipynb
│   └── tool_discovery.py
├── tests
│   ├── test_change_tools.py
│   ├── test_service_health_tools.py
│   └── test_ticket_tools.py
└── uv.lock
```

The project contains four main components.
|Component | Purpose|
|Service Health MCP Server | Provides service health and active incident information|
|Support Ticket MCP Server | Provides support-ticket information|
|Change Management MCP Server | Provides recent change information|
|MCP Host | Contains the Groq LLM and uses tools from all three MCP servers|

- LLM is inside the MCP Host.
- MCP servers expose tools.
- MCP Host Receives user question, Uses Groq LLM, Understands the request, Selects MCP tool or tools, Calls MCP servers, Receives operational data, Combines the evidence, Generates final answer

---

## 4. MCP Servers

```
servers                                                                                                                           
├── __init__.py                        
├── change_management_server.py
├── confserver.py
├── service_health_server.py
└── support_ticket_server.py
```

|Service Health MCP Server | Provides service health and active incident information|
|Support Ticket MCP Server | Provides support-ticket information|
|Change Management MCP Server | Provides recent change information|

---

## 5. Setup

```
uv venv
uv sync
```

---

## 6. Environment Variables

Create file .env and paste:

```
GROQ_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=...

OUTPUT_PATH=outputs
SRC_PATH=src
DATA_PATH=data
SERVER_PATH=servers
COLLECTION_NAME=logistics-rtickets.dbule-collection

tickets=tickets.db
changes=changes.json
sample_queries=sample_queries.json
service_health=service_health.json
```

Change groq key.

---

## 7. Running the MCP Host

```
uv run python src/host.py
```

---

## 8. Execution Flow

```
User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Additional Tool Call if required
→ Final Answer
```

---

## 9. Testing

Test all tools:

```
pytest -v
```
---

## 10. Known Limitations

Examples:

```
The project uses local operational data.
Service health values are stored snapshots rather than live monitoring metrics.
The project does not include application logs or distributed traces.
Possible change correlation is based on available service and timing evidence.
The assistant does not perform operational write actions.
No documentation available.
Some of the test are unavailable.
```

---

## 11. Future Improvements

Reasonable improvements:

```
Proper documentation
Complete Tests.
Live monitoring integration
ITSM integration
Deployment system integration
Application log MCP server
Distributed tracing integration
Human approval for operational actions
Persistent incident conversation memory
```

---

