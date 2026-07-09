# CAPSTONE PROJECT BUILD – 2
## MCP-Based Enterprise Operations Assistant
## Submitted by: Palak



### Project Overview
An enterprise operations team is responsible for monitoring business applications and responding to
service issues.
During an operational incident, engineers usually need to check information from different systems:
- service health
- active incidents
- support tickets
- recent application or configuration changes
The information is available, but it is spread across separate systems.
It is difficult and time consuming to search for every incidents, tickets and changes

---


### Project Objective
Objective of this project is to help enterprise operations team in monitoring business applications and responding to service issues with the help of **MODEL CONTEXT PROTOCOL**

This project recieves natural language input and get data from various required sources to respond to user. it helps user in fetching information on time and with ease.

---


### Architecture
There are various components in this Architecture as defined
```
MCP Host
MCP Client
MCP Server
Groq LLM
```
1. **MCP HOST** -> This is the main application that act as interface between user and the system.
- it takes user query 
- pass query to agent (llm with tools) 
- agent fetches all the tools from server with the help of client
- Execute the required tool and get data
- produces final response for the user

2. **MCP CLIENT** -> this is the interface between MCP Host and MCP Server
- it connects the host with server
- it exposes all server tools to agent in the host

3. **MCP SERVER** ->This is like a system that has all tools, prompts and resources
- There are three servers in this project 
  - Service Health MCP Server
  - Support Ticket MCP Server
  - Change Management MCP Server


---


### MCP Servers
There are three servers in this project 
```
- Service Health MCP Server
- Support Ticket MCP Server
- Change Management MCP Server
```


1. Service Health MCP Server ->
```
servers/service_health_server.py
```
DATA FILE ```servers/service_health_server.py```

To run mcp server, use command
```
uv run python servers/service_health_server.py
```
TOOLS in this server
- list_services
- get_service_health
- get_active_incidents



2. Support Ticket MCP Server ->
```
servers/service_health_server.py
```
DATA FILE ```data/tickets.db```

To run mcp server, use command
```
uv run python servers/support_ticket_server.py
```
TOOLS in this server
- search_tickets
- get_ticket_details
- get_high_priority_tickets



3. Change Management MCP Server ->
```
servers/service_health_server.py
```
DATA FILE ```data/changes.json```

To run mcp server, use command
```
uv run python servers/change_management_server.py
```
TOOLS in this server
- list_recent_changes
- get_change_details
- get_changes_for_service

---

### Tools
There are total 9 tools in the system that are used to get data from files and database
- list_services
- get_service_health
- get_active_incidents
- search_tickets
- get_ticket_details
- get_high_priority_tickets
- list_recent_changes
- get_change_details
- get_changes_for_service

---

###  Requirements
```
fastmcp>=3.1.0
ipython>=9.10.0
requests>=2.32.5
python-dotenv>=1.2.2
mcp-use>=1.6.0
langchain-groq>=1.1.2
pydantic-ai>=1.78.0
```

---

### Setup instructions

Steps for set-up are as follows:
1. initialize uv
```bash
uv init
```

2. create Environment 
```bash
uv venv
```
3. install requirements
```bash
uv add -r requirements.txt
```

**set-up part is completed!!!**

---


### Environment Variables setup 

To set any Environment variable, do the following:
1. first create Environment file named **.env**
2. add your api key here 
```python
GROQ_API_KEY=...

```

---
### Running the MCP Host
To run the main application use the below command:
```
uv run -m src.host
```

---

### Execution Flow
User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Additional Tool Call if required
→ Final Answer

- User query is passed to host that has the agent
- agent get invoked and connects to mcp servers with the help of client
- Discovers all available tool
- Based on requirements of user query, it call tools with valid input 
- Based on all tool call results it generates the final response

---

###  MCP Tool Discovery
This is the method that is used to connect to server by the agent to get information about all available tools
Output of tool discovery for this agent is
```
[
    [
        {
            "tool": "list_services",
            "tool_disc": "List enterprise services and current health status."
        },
        {
            "tool": "get_service_health",
            "tool_disc": "Return detailed health information for a service."
        },
        {
            "tool": "get_active_incidents",
            "tool_disc": "This tool is use to get active incidents based on service name"
        }
    ],
    [
        {
            "tool": "search_tickets",
            "tool_disc": "Search support tickets using predefined filters such as service name, priority, status\ninput optional arg:\nservice_name: str\npriority: str\nstatus: str"
        },
        {
            "tool": "get_ticket_details",
            "tool_disc": "Get full details of one support ticket"
        },
        {
            "tool": "get_high_priority_tickets",
            "tool_disc": "get high priority tickets that can be filter by service_name as well"
        }
    ],
    [
        {
            "tool": "list_recent_changes",
            "tool_disc": "Return all recent change records."
        },
        {
            "tool": "get_change_details",
            "tool_disc": "Return details of a specific recent change by id."
        },
        {
            "tool": "get_changes_for_service",
            "tool_disc": "This tool is use to Find recent changes for a service bsed on its service name"
        }
    ]
]
```
- To test tool discovery, run command as **uv run -m src.tool_discovery payh-to-server**

Example: ``` uv run -m src.tool_discovery servers/change_management_server.py```

---

###  Testing
There are multiple test cases defined 
- test_list_services_returns_services
- test_get_service_health_payment_api
- test_get_service_health_unknown_service
- test_get_active_incidents_payment_api
- test_search_open_payment_tickets
- test_get_ticket_details_valid_ticket
- test_get_ticket_details_invalid_ticket
- test_high_priority_tickets_only_returns_p1_p2
- test_get_changes_for_payment_api
- test_get_change_details_valid_change
- test_host_payment_api_change_query

To run test cases run command as below
```
python -m pytest tests -v 
```
**OR**
```
python -m pytest tests -v > outputs/test_results.txt
```

---


### Test Results
Pytest results were
```
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Palak\Desktop\capstone-2\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Palak\Desktop\capstone-2
configfile: pyproject.toml
plugins: anyio-4.14.1, langsmith-0.9.8, logfire-4.37.0
collecting ... collected 11 items

tests/test_change_tools.py::test_get_changes_for_payment_api PASSED      [  9%]
tests/test_change_tools.py::test_get_change_details_valid_change PASSED  [ 18%]
tests/test_host_queries.py::test_host_payment_api_change_query PASSED    [ 27%]
tests/test_service_health_tools.py::test_list_services_returns_services PASSED [ 36%]
tests/test_service_health_tools.py::test_get_service_health_payment_api PASSED [ 45%]
tests/test_service_health_tools.py::test_get_service_health_unknown_service PASSED [ 54%]
tests/test_service_health_tools.py::test_get_active_incidents_payment_api PASSED [ 63%]
tests/test_ticket_tools.py::test_search_open_payment_tickets PASSED      [ 72%]
tests/test_ticket_tools.py::test_get_ticket_details_valid_ticket PASSED  [ 81%]
tests/test_ticket_tools.py::test_get_ticket_details_invalid_ticket PASSED [ 90%]
tests/test_ticket_tools.py::test_high_priority_tickets_only_returns_p1_p2 PASSED [100%]
```

---

###  Known Limitations
- The project uses local operational data.
- Service health values are stored snapshots rather than live monitoring metrics.
- The project does not include application logs or distributed traces.
- Possible change correlation is based on available service and timing evidence.
- The assistant does not perform operational write actions.


---

###  Future Improvements
Live monitoring integration
ITSM integration
Deployment system integration
Application log MCP server
Distributed tracing integration
Human approval for operational actions
Persistent incident conversation memory

---


