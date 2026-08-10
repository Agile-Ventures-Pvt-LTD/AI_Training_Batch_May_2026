## Project Overview

The MCP-Based Enterprise Operations Assistant is designed to help operations engineers investigate and resolve operational issues by providing a natural-language interface to query various operational data sources. The assistant connects to multiple MCP servers, each exposing tools for specific operational capabilities, and uses a Groq LLM to understand user queries and select the required tools.

## Project Objective

The objective of this project is to build an enterprise operations assistant using FastMCP, MCP tools, and Groq LLM. The assistant should allow operations engineers to ask natural-language questions and provide a clear response by combining information from different operational sources.

## Architecture

The architecture of the project consists of the following components:

* MCP Host: The central component that receives user queries, uses the Groq LLM to understand the request, and selects the required MCP tools.
* MCP Client: The component that connects to the MCP servers and calls the selected tools.
* MCP Servers: Three servers that expose tools for specific operational capabilities:
        + Service Health MCP Server: Provides service health and active incident information.
        + Support Ticket MCP Server: Provides support ticket information.
        + Change Management MCP Server: Provides recent change information.
* Groq LLM: The large language model used inside the MCP Host to understand user queries and select MCP tools.

## MCP Servers

The project consists of three MCP servers:

* Service Health MCP Server: Reads data from `service_health.json` and exposes tools for listing services, getting service health, and getting active incidents.
* Support Ticket MCP Server: Reads data from `tickets.db` and exposes tools for searching tickets, getting ticket details, and getting high-priority tickets.
* Change Management MCP Server: Reads data from `changes.json` and exposes tools for listing recent changes, getting change details, and getting changes for a service.

## Tools

The project exposes the following nine tools:

* `list_services`: Lists all services and their current health status.
* `get_service_health`: Returns detailed health information for a service.
* `get_active_incidents`: Returns active operational incidents.
* `search_tickets`: Searches support tickets using predefined filters.
* `get_ticket_details`: Returns full details of a support ticket.
* `get_high_priority_tickets`: Returns open P1 and P2 tickets.
* `list_recent_changes`: Returns recent change records.
* `get_change_details`: Returns details of a specific change.
* `get_changes_for_service`: Returns recent changes for a service.

## Dataset

The project uses local operational data files:

* `service_health.json`: Contains service health and active incident information.
* `tickets.db`: Contains support ticket information.
* `changes.json`: Contains recent change information.
* `sample_queries.json`: Contains sample user queries for testing.

## Setup

To set up the project, run the following commands:
```bash
uv sync
uv run python scripts/create_ticket_db.py
```
## Environment Variables

The project uses the following environment variables:

* `GROQ_API_KEY`: The API key for the Groq LLM.
* `GROQ_MODEL`: The model used for the Groq LLM.

## Running the MCP Host

To run the MCP Host, use the following command:
```bash
uv run python -m src.host
```
## Execution Flow

The execution flow of the project is as follows:

1. User Query: The user enters a natural-language question.
2. Host: The MCP Host receives the query and uses the Groq LLM to understand the request.
3. LLM: The Groq LLM selects the required MCP tools.
4. MCP Tool Selection: The MCP Host calls the selected tools.
5. MCP Server: The MCP server executes the tool and returns the result.
6. Tool Result: The MCP Host receives the result and decides whether to call another tool.
7. Final Answer: The MCP Host combines the results and generates a final answer.

## MCP Tool Discovery

The project demonstrates MCP tool discovery by connecting to each server and discovering its tools. The discovered tools are saved in `outputs/tool_discovery.json`.

## Multi-Server Queries

The project executes four queries that use more than one MCP server:

* Query 1: Why is the Payment API unhealthy and is there any recent change that may be related?
* Query 2: Show high-priority open tickets for services that are currently unhealthy or degraded.
* Query 3: Summarize the current Payment API incident and the related support ticket impact.
* Query 4: Was there any recent change for Checkout Service that may explain the current degradation?

## Testing

The project includes pytest tests for:

* Service Health MCP tools
* Support Ticket MCP tools
* Change Management MCP tools
* MCP tool discovery
* Host integration tests

## Test Results

The test results are documented in `outputs/test_results.txt`.

## Mandatory Query Results

The project executes all eight mandatory queries and saves the results in `outputs/mandatory_query_results.json`.

## Sample Run Documentation

The project documents all eight mandatory query runs in `outputs/sample_run_outputs.md`.

## Tool Discovery Documentation

The project documents the discovered tools in `outputs/tool_discovery.json`.

## README Requirements

The README contains the following sections:

1. Project Overview
2. Project Objective
3. Architecture
4. MCP Servers
5. Tools
6. Dataset
7. Setup
8. Environment Variables
9. Running the MCP Host
10. Execution Flow
11. MCP Tool Discovery
12. Multi-Server Queries
13. Testing
14. Test Results
15. Mandatory Query Results
16. Sample Run Documentation
17. Tool Discovery Documentation

## Known Limitations

The project has the following limitations:

* The project uses local operational data.
* Service health values are stored snapshots rather than live monitoring metrics.
* The project does not include application logs or distributed traces.
* Possible change correlation is based on available service and timing evidence.
* The assistant does not perform operational write actions.

## Future Improvements

The project can be improved by:

* Integrating live monitoring
* Integrating ITSM
* Integrating deployment systems
* Adding application log MCP servers
* Adding distributed tracing integration
* Implementing human approval for operational actions
* Implementing persistent incident conversation memory

## GitHub Upload Structure

The project should be uploaded to GitHub in the following structure:
```markdown
submissions/
└── capstone/
    └── capstone-02/
        └── mcp-enterprise-operations-assistant/
            └── mohammad-anas/
                ├── README.md
                ├── pyproject.toml
                ├── .env.example
                ├── .gitignore
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
## Submission Deliverables

The final submission should contain:

1. Complete source code
2. pyproject.toml
3. .env.example
4. .gitignore
5. README.md
6. All provided local data files
7. Ticket database recreation script
8. Service Health MCP Server
9. Support Ticket MCP Server
10. Change Management MCP Server
11. All nine mandatory MCP tools
12. MCP Host
13. Groq LLM integration
14. mcp-use MCP Agent integration
15. MCP multi-server configuration
16. MCP tool discovery implementation
17. pytest tests
18. outputs/tool_discovery.json
19. outputs/mandatory_query_results.json
20. outputs/sample_run_outputs.md
21. outputs/test_results.txt