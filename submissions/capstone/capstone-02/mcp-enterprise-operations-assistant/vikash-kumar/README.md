# MCP-Based Enterprise Operations Assistant

We have built an MCP-Based Enterprise Operations Assistant which will help the user to decision and information at the one platform without routing to multiple servers for health, ticket, management related problem. We have used FastMCP, mcp-use to connect the client to the server and get the required information for the user.

# Technology Used
- FastMCP
- MCP tools
- MCP Host
- mcp-use
- Groq LLM
- Python
- local JSON files
- SQLite
- pytest
- langchain-groq
- pytest

# Workflow
```bash
                             User
                              │                              ▼
                     MCP Host + Groq LLM
                              │
                 MCP Client / mcp-use
                              │            ┌─────────────────┼─────────────────┐            │                 │                 │            ▼                 ▼                 ▼
   Service Health MCP   Support Ticket MCP   Change Management MCP          Server              Server                Server
            │                 │                 │            ▼                 ▼                 ▼
 service_health.json       tickets.db          changes.json

 ```

 # Flow of the project
```bash

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

# Technical Dependencies

- fastmcp
- mcp-use
- langchain-groq
- python-dotenv
- pydantic
- pytest
- pytest-asyncio

# Setup Instructions
1. Create the virtual environment

```python
uv venv
```

2. Activate the environment

```python
.venv\Scripts\activate
```

3. Install the packages/dependencies

```python
uv pip install -r requirements.txt
```

# Environment Configuration
```python
.env

GROQ_API_KEY=<your_groq_api_key>

GROQ_MODEL=llama-3.1-8b-instant #llama-3.3-70b-versatile 

```

# MCP Server

1. Service Health MCP Server: data/service_health.json

2. Support Ticket MCP Server: data/tickets.db

3. Change Management MCP Server: data/changes.json


# To recreate the database

```python
uv run python scripts/create_ticket_db.py
```

# Server run independently

```python

uv run python servers/service_health_server.py

uv run python servers/support_ticket_server.py

uv run python servers/change_management_server.py

```

# FastMCP Server

```python

from fastmcp import FastMCP

mcp = FastMCP("Service Health MCP Server")

@mcp.tooldef list_services() -> dict:
"""List enterprise services and current health status."""...

@mcp.tooldef get_service_health(service_name: str) -> dict:
"""Return detailed health information for a service."""...

if __name__ == "__main__":
    mcp.run()

```

# MCP Host

```python
src/host.py
```

# MCP Tools Used
```bash
service-health
├── list_services
├── get_service_health
└── get_active_incidentssupport-ticket

search_tickets
├── get_ticket_details
└── get_high_priority_tickets

change-management
├── list_recent_changes
├── get_change_details
└── get_changes_for_service
```
```python
python -m src.tool_discovery

uv run python src/tool_discovery.py
```

# Application Execution Flow

```bash
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

# User Input

Why is the Payment API unhealthy and is there any recent change that may be related?

# Expected Output

```bash
{"user_query":"Why is the Payment API unhealthy and is there any recent change that may be related?",
"servers_used": ["service-health","change-management"],
"tools_used": ["get_service_health","get_active_incidents","get_changes_for_service"],
"evidence": {"services": 
[{"service_name": "Payment API","status": "UNHEALTHY","error_rate_percent": 38.0,"average_latency_ms": 1850}],
"incidents": [{"incident_id": "INC-OPS-101","severity": "SEV-1","status": "ACTIVE"}],"tickets": [],
"changes": [{"change_id": "CHG-2001","risk": "HIGH","implemented_at": "2026-07-08T09:10:00"}
30
]},
"operations_summary": "The Payment API is unhealthy with a 38 percent error rate and elevated latency. A SEV-1 incident is active for payment timeout failures.",
"possible_change_correlation": "A high-risk Payment API release was completed before the incident began. The service and timing indicate a possible correlation, but the available data does not confirm the release as the root cause.",
"recommended_next_actions": ["Review CHG-2001 with Payments Engineering.","Compare the release changes with current timeout failures.","Review rollback readiness because rollback information is available.","Continue SEV-1 incident handling with Application Support."],
"limitations": ["The dataset does not contain application logs or distributed traces."]}
```

# Running the Application

```python

uv run python -m src.host

```


# Testing

```python
uv run pytest -v

uv run pytest -v > outputs/test_results.txt
```

# Test Results & Incident Execution Results
```bash

(project) PS C:\Users\Vikash Kumar\Desktop\project> uv run pytest -v
========================================== test session starts ==========================================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Vikash Kumar\Desktop\project\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Vikash Kumar\Desktop\project
configfile: pytest.ini
testpaths: test, tests
plugins: anyio-4.14.1, langsmith-0.9.8, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 14 items                                                                                       

test/test_change_tools.py::test_list_recent_changes PASSED                                         [  7%]
test/test_change_tools.py::test_get_change_details_valid PASSED                                    [ 14%]
test/test_change_tools.py::test_get_changes_for_service PASSED                                     [ 21%]
test/test_host_queries.py::test_orchestrator_execution_flow PASSED                                 [ 28%]
test/test_host_queries.py::test_orchestrator_unmatched_query FAILED                                [ 35%]
test/test_mcp_discovery.py::test_export_tool_manifest_keys FAILED                                  [ 42%]
test/test_mcp_discovery.py::test_export_tool_manifest_contents FAILED                              [ 50%]
test/test_service_health_tools.py::test_list_services PASSED                                       [ 57%]
test/test_service_health_tools.py::test_get_service_health_valid FAILED                            [ 64%]
test/test_service_health_tools.py::test_get_service_health_invalid PASSED                          [ 71%]
test/test_service_health_tools.py::test_get_active_incidents_all PASSED                            [ 78%]
test/test_ticket_tools.py::test_search_tickets_all PASSED                                          [ 85%]
test/test_ticket_tools.py::test_get_ticket_details_valid PASSED                                    [ 92%]
test/test_ticket_tools.py::test_get_high_priority_tickets PASSED                                   [100%]

=============================================== FAILURES ================================================
___________________________________ test_orchestrator_unmatched_query ___________________________________

    @pytest.mark.asyncio
    async def test_orchestrator_unmatched_query():
        agent = MCPOperations()
        res = agent.execute_workflow("Ping generic server check echo status")
>       assert res["tool_used"] == "None"
E       AssertionError: assert 'call_list_se...ervice_health' == 'None'
E         
E         - None
E         + call_list_services, call_get_service_health

test\test_host_queries.py:16: AssertionError
____________________________________ test_export_tool_manifest_keys _____________________________________

    @pytest.mark.asyncio
    async def test_export_tool_manifest_keys():
        export_fn = getattr(discovery, "export_tool_manifest", getattr(discovery, "export_manifest", None))
>       assert export_fn is not None
E       assert None is not None

test\test_mcp_discovery.py:7: AssertionError
__________________________________ test_export_tool_manifest_contents ___________________________________

    @pytest.mark.asyncio
    async def test_export_tool_manifest_contents():
        export_fn = getattr(discovery, "export_tool_manifest", getattr(discovery, "export_manifest", None))
>       manifest = await export_fn()
                         ^^^^^^^^^^^
E       TypeError: 'NoneType' object is not callable

test\test_mcp_discovery.py:17: TypeError
_____________________________________ test_get_service_health_valid _____________________________________

    def test_get_service_health_valid():
        res = json.loads(get_service_health("payment-gateway"))
>       assert res["found"] is True
E       assert False is True

test\test_service_health_tools.py:12: AssertionError
======================================== short test summary info ========================================
FAILED test/test_host_queries.py::test_orchestrator_unmatched_query - AssertionError: assert 'call_list_se...ervice_health' == 'None'
FAILED test/test_mcp_discovery.py::test_export_tool_manifest_keys - assert None is not None
FAILED test/test_mcp_discovery.py::test_export_tool_manifest_contents - TypeError: 'NoneType' object is not callable
FAILED test/test_service_health_tools.py::test_get_service_health_valid - assert False is True
===================================== 4 failed, 10 passed in 4.79s ======================================
(project) PS C:\Users\Vikash Kumar\Desktop\project> uv run pytest -v > outputs/test_results.txt
(project) PS C:\Users\Vikash Kumar\Desktop\project> 
```

# Future Improvements

We can connect with multiple servers to have more tools access and can make better decision. We can improve the logic of the python functions so that the latency should be less.

# Author

Vikash Kumar
