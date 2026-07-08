# Project Name
# MCP-Based Enterprise Operations Assistant

## Business use case (Real world use case)
An enterprise operations team is responsible for monitoring business applications and responding to
service issues.
During an operational incident, engineers usually need to check information from different systems:
1. service health
2. active incidents
3. support tickets
4. recent application or configuration changes
The information is available, but it is spread across separate systems.

For example, when the Payment API becomes unhealthy, the operations team may need to answer:
1. What is wrong with the Payment API?
2. Is there an active incident?
3. Are customers reporting the same issue?
4. Are there any high-priority support tickets?
5. Was a recent change made to the Payment API?
6. Could the timing of a recent change be related to the current incident?

So, this is the real world need of building an MCP-Based Enterprise Operations Assistant.

The assistant allows an operations engineer to ask these questions in natural language.
The LLM-powered MCP Host must connect to multiple MCP servers, select the required tools, combine
information from different operational sources, and provide a clear response.

## Project Objective
The completed application must:
1. Build three MCP servers.
2. Run the MCP servers using STDIO.
3. Build one MCP Host.
4. Connect the MCP Host to all three MCP servers.
5. Discover tools exposed by the MCP servers.
6. Use Groq LLM inside the MCP Host.
7. Accept natural-language operational questions.
8. Allow the LLM to decide which MCP tools are required.
9. Support queries that require tools from more than one MCP server.
10. Combine tool results into a clear operational answer.
11. Test MCP tools and multi-server execution.
12. Document actual execution results.

## MCP Server-Host configuration
                                   User
                                    │
                                    ▼
                            MCP Host + Groq LLM
                                    │
                            MCP Client / mcp-use
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
       Service Health MCP Support Ticket MCP Change Management MCP
               Server             Server             Server
                  │                 │                 │
                  ▼                 ▼                 ▼
        service_health.json   tickets.db         changes.json

- These are the four main components of the project:

          Component                                     Purpose
Service Health MCP Server         Provides service health and active incident information
Support Ticket MCP Server         Provides support-ticket information
Change Management MCP Server      Provides recent change information
MCP Host                          Contains the Groq LLM and uses tools from all MCP servers.     

## Dataset provided
capstone_02_enterprise_operations_dataset.zip

The provided files are:
data/
├── service_health.json
├── tickets.db
├── changes.json
└── sample_queries.json
scripts/
└── create_ticket_db.py
README_dataset.md

## Data sources
       MCP Server                                  Data Source
Service Health MCP Server                    data/service_health.json
Support Ticket MCP Server                        data/tickets.db
Change Management MCP Server                    data/changes.json

## Input file descriptions
### data/service_health.json
This file contains:
1. services
{
"service_name": "Payment API",
"service_id": "SVC-PAY-01",
"status": "UNHEALTHY",
"region": "India-West",
"error_rate_percent": 38.0,
"average_latency_ms": 1850,
"cpu_usage_percent": 42,
"memory_usage_percent": 61,
"last_checked": "2026-07-08T10:00:00",
"active_incident_ids": [
"INC-OPS-101"
]
}

2. incidents
{
"incident_id": "INC-OPS-101",
"service_name": "Payment API",
"severity": "SEV-1",
"status": "ACTIVE",
"started_at": "2026-07-08T09:55:00",
"summary": "Payment processing requests are experiencing elevated timeout 
failures.",
"customer_impact": "Customers may be unable to complete card payments.",
"assigned_group": "Application Support"
}

### data/tickets.db
The SQLite database contains:
tickets

      Column                               Purpose
     ticket_id                       Unique ticket identifier
    service_name                         Related service
     priority                            P1, P2, P3, or P4
   status Ticket                            status
     subject                            Short ticket subject
   description                         Ticket description
   created_at                           Ticket creation time
  customer_impact                         Recorded impact

Example record:
Ticket ID: TKT-1001
Service: Payment API
Priority: P1
Status: OPEN
Subject: Card payment timeout
Assigned Group: Application Support

### data/changes.json
The file contains recent operational changes.

For example:
{
"change_id": "CHG-2001",
"service_name": "Payment API",
"change_type": "APPLICATION_RELEASE",
"status": "COMPLETED",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00",
"implemented_by": "Payments Engineering",
"summary": "Released payment-service changes for timeout handling and retry 
logic.",
"rollback_available": true
}

## Folder structure of the project
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

## Folders/files description 
## data folder
### service_health.json
- This file contains the data in .json format.
- The data is about the incidents and the services that takes place.

### tickets.db
- This is a database file which contains a table named as "tickets".
- This table consists of multiple columns like ticket_id etc.

### changes.json
- This file contains the data in .json format.
- The data is about the changes made in the data.

### sample_queries.json
- This file stores the sample queries that should be asked by the user to the system.

## scripts folder
### create_ticket_db.py
- This file contains the data about the ticket that is going to be stored in the database.

## servers
### service_health_server.py
- This server is about services provided to the user.
- It takes data from the service_health.json file.

### support_ticket_server.py
- This server works on the ticket data.
- It takes data from the tickets.db file.

### change_management_server.py
- This server works on the data that has some changes.
- It takes data from the changes.json file.

## src folder
### host.py
- This file contains both MCP Host as well as  MCP Server.
- It contains several functions or tasks:
1. Load environment variables.
2. Configure GroqLLM.
3. Connect 3 MCP servers.
4. Discover all the tools.
5. Create MCP Agent.
6. Accept user query.
7. Allow users to select tools.
8. Return answer.
9. Close the session.

### config.py
- Configure the environment variables.

### output_writer.py
- This file makes use of the pydantic package and configues input and output of every class in the whole project.

### prompts.py
- This file simply contains the system prompt.

### tool_discovery.py
- This file ensures that the host is connected to the all the 3 servers and all the tools of each server.

## tests folder
### test_change_tools.py
- This file contains multiple test cases that validates of tests any if any change occurs in tools.

### test_host_queries.py
- This file contains test cases about the about the user queries asked to the system.

### test_mcp_discovery.py
- This file contains test cases about the mcp connection of client, host, servers, tools etc.

### test_service_health_tools.py
- This file contains the test cases about the health service and validates them.

### test_ticket_tools.py
- This file contains test cases that validates and tests the ticket attribute saved in the database file.

### .env.example
- This file contains the secret variables that need not to be revealed everywhere in all the files.
for example, 
1. GROQ_API_KEY
2. GROQ_MPDEL

### requirements.txt
fastmcp>=2.11.0
mcp>=1.12.0
groq>=0.31.0
langchain>=0.3.27
langchain-core>=0.3.75
langchain-groq>=0.3.7
python-dotenv>=1.1.1
pydantic>=2.11.7
pytest>=8.4.2
pytest-mock>=3.15.0
typing-extensions>=4.15.0
pytest-asyncio>=0.24.0
- As we can see, this file contains all the required packages used in the project with the suitable versions.
- Command to install these packages:
cmd command- 
"uv add -r requirements.txt"

### README_dataset.md
- This file contains some information about the dataset and its columns and attributes.

### pyproject.toml
- This file gets created when "uv init" command runs in the cmd terminal.

## .venv folder
- This folder gets created by running a command in the terminal i.e,
"uv venv"
- Then, the venv has to be activated using the command:
".venv\Scripts\activate"
- This is the virtual environment on which the whole project runs.

### .gitignore file
- This file contains some files that need to be ignored if the whole project is going to be uploaded somewhere on a different platform.

## Execution flow of the project
User Query
→ Host
→ LLM
→ MCP Tool Selection
→ MCP Server
→ Tool Result
→ Additional Tool Call if required
→ Final Answer

## MCP Tool Discovery
Server                   Discovered                               Tool Purpose
service-health          list_services                           List service health
service-health          get_service_health                     Get one service's health
service-health          get_active_incidents                    Find active incidents
support-ticket          search_tickets                             Search tickets
support-ticket          get_ticket_details                       Get ticket details
support-ticket          get_high_priority_tickets               Find P1/P2 open tickets
change-management       list_recent_changes                       List recent changes
change-management       get_change_details                         Get change details
change-management       get_changes_for_service                 Find changes for a service

## Technical dependencies
fastmcp
mcp-use
langchain-groq
python-dotenv
pydantic
pytest
pytest-asyncio

## Query output
[
{
"query_id": "Q1",
"user_query": "Why is the Payment API unhealthy and is there any recent 
change that may be related?",
"servers_used": [
"service-health",
"change-management"
],
"tools_used": [
"get_service_health",
"get_active_incidents",
"get_changes_for_service"
],
"final_answer": "",
"status": "PASS"
}
]

## Author
Vaishnavi Gupta
