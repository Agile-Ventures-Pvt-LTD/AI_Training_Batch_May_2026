## MCP-Based Enterprise Operations Assistant

## 1. Project Overview
An MCP-Based Enterprise Operations Assistant for Handling responsible for monitoring bussinees application and service issue so that this  allows  an operations engineer to ask query and The LLM-powered MCP Host must connect to multiple MCP servers, select the required tools, combine information from different operational sources such as service health,active incidents,support tickets,recent application or configuration changes and provide a clear response.

## 2. Project Objective
To build an MCP-Based Enterprise Operations Assistant.
The assistant should allow an operations engineer to ask these questions in natural language.
The LLM-powered MCP Host must connect to multiple MCP servers, select the required tools, combine
information from different operational sources, and provide a clear response


## 3. Architecture
 
```
Receive user question
        ↓
Use Groq LLM
        ↓
Understand the request
        ↓
Select MCP tool or tools(9 tools mentioned)
        ↓
Call MCP servers( 3 server: Change Management MCP Server,Support Ticket MCP Server,Service Health MCP Server)
        ↓
Receive operational data
        ↓
Combine the evidence
        ↓
Generate final answer

```

## 4. MCP Servers
1. Change management MCP Sever:
expose 3 tools such as list_recent_changes, get_changes_details, get_changes_for_service

run:
```bash
uv run -m servers.support_ticket_server

```

2. Support Ticket MCP Server:
expose 3 tools such as search_tickets, get_tickets_details, get_high_priority_tickets

run:
```bash
uv run -m servers.support_ticket_server

```
3. Service Health MCP server:
expose 3 tools such as list_services, get_service_health, get_active_incidents
Run:
```bash
uv run -m servers.service_health_server

```

## 5. Tools ( 9 tools )
1. Change management MCP Sever:3 tools-
 - list_recent_changes:
 ```
Purpose: Return recent change records.
Input;{"limit": 10}
Expected Output:
{
"count": 5,
"changes": [
{
"change_id": "CHG-2001",
"service_name": "Payment API",
"change_type": "APPLICATION_RELEASE",
"status": "COMPLETED",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00"
}]}
 ```
 - get_changes_details:
 
 ```Purpose: Return details of a specific change.
 Input:{"change_id": "CHG-2001"}
Expected Output:
{
"found": true,
"change": {
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
}

 ```
 - get_changes_for_service: 

 ```
 Purpose:Find recent changes for a service.
Input: {"service_name": "Payment API"}
Expected Output:
{
"service_name": "Payment API",
"count": 1,
"changes": [
{
"change_id": "CHG-2001",
"change_type": "APPLICATION_RELEASE",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00",
"summary": "Released payment-service changes for timeout handling and 
retry logic.",
"rollback_available": true
}]}

 ```
2. Service Health MCP server: 3 tools -
 - list_services: 
```
Purpose : List all services and their current health status.
Input: No mandatory input.
Expected Output
{
"count": 5,
"services": [
{
"service_name": "Payment API",
"status": "UNHEALTHY",
"region": "India-West"
},
{
"service_name": "Checkout Service",
"status": "DEGRADED",
"region": "India-West"
}
]
}
```
 - get_service_health: 
```
Purpose: Return detailed health information for one service.
Input:{"service_name": "Payment API"}
Expected Output:
{
"found": true,
"service": {
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
]}}

```

 - get_active_incidents:

 ```
 Purpose: Return active operational incidents.

Input Example: {"service_name": "Payment API"}
Expected Output:
{
"count": 1,
"incidents": [
{
"incident_id": "INC-OPS-101",
"service_name": "Payment API",
"severity": "SEV-1",
"status": "ACTIVE",
"summary": "Payment processing requests are experiencing elevated timeout 
failures.",
"customer_impact": "Customers may be unable to complete card payments.",
"assigned_group": "Application Support"
}
]
}
 ```
3. Support Ticket MCP Server: 3 tools - 
 - search_tickets: 
 ```
Purpose: Search support tickets using predefined filters.
Supported Filters:service_name, priority, status,limit
Input Example:{
"service_name": "Payment API","status": "OPEN","limit": 20
}
Expected Output:{
"count": 4,
"tickets": [
{
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout",
"customer_impact": "High",
"assigned_group": "Application Support"
}]}

 ```
 - get_tickets_details

 ```
    Purpose:get_ticket_details Get full details of one support ticket.
    Input:{"ticket_id": "TKT-1001"}
    Expected Output:{
"found": true,
"ticket": {
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout",
"description": "Customers report payment failures and timeout errors.",
"created_at": "2026-07-08T09:58:00",
"customer_impact": "High",
"assigned_group": "Application Support"

}}

 ```
 - get_high_priority_tickets

 ```
Purpose:Return open P1 and P2 tickets.The tool may optionally filter by service.
Input Example:{"service_name": "Payment API"}
Expected Output:
{
"count": 3,
"tickets": [
{
"ticket_id": "TKT-1001",
"service_name": "Payment API",
"priority": "P1",
"status": "OPEN",
"subject": "Card payment timeout
}]}

 ```

## 6. Dataset
the provided files saved in data and added README_dataset.md also

```
data/
├── service_health.json
├── tickets.db
├── changes.json
└── sample_queries.json

```

## 7. Setup

1. Create a virtual environment:
activate 
```
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt

```
4. requirements:
```
fastmcp
mcp-use
langchain-groq
python-dotenv
pydantic
pytest
pytest-asyncio
```
5. Folder_structure:
```
mcp_enterprise_operations_assistant/
│
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
## 8. Environment Variables
Set up environment variables:
```
 .env.example  or .env

```
`.env` with your API keys:
```
GROQ_API_KEY= your_groq_API_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## 9. Running the MCP Host
Run your MCP host 
```bash
uv run -m src.host

```
## 10. Execution FLOW

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

## 11. MCP Tool Discovery
Host can connect to each server and discover its tools
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
└── get_changes_for_service

```
here is the structure output save as outputs\tool_discovery.json
```
{
  "service-health": [
    "list_recent_changes",
    "get_change_details",
    "get_changes_for_service"
  ],
  "support-ticket": [
    "search_tickets",
    "get_ticket_details",
    "get_high_priority_tickets"
  ],
  "change-management": [
    "list_recent_changes",
    "get_change_details",
    "get_changes_for_service"
  ]
}
```

## 12. Multi-Server Queries
1. Service health + change management : why is the Payment API unhealthy and is there any recent change that may be related?
2. Service Health + Support Tickets: Show high-priority open tickets for services that are currently unhealthy or degraded.
3. Support Ticket + Service Health : Show the details of ticket TKT-1001 and check the health of its related service.

## 13. Testing
test service health tool
```bash 
uv run -m tests.test_service_health_tools
```
test ticket tools
```bash 
uv run -m tests.test_ticket_tools.py
```
test change tools
```bash 
uv run -m tests.change_tools.py
```
MCP dicovery tests
```bash 
uv run -m tests.test_mcp_discovery

```
Host integration tests

```bash 
uv run -m tests.test_host_queries
```

## 14. Test Results

## 15. Mandontory Query Results
```
{
"user_query":"Why is the Payment API unhealthy and is there any recent change that may be related?",
"servers_used": [
                "service-health","change-management"],
"tools_used": ["get_service_health","get_active_incidents","get_changes_for_service"],
"evidence": {
              "services": [
    {
"service_name": "Payment API",
"status": "UNHEALTHY",
"error_rate_percent": 38.0,
"average_latency_ms": 1850
}
],

"incidents": [
{
"incident_id": "INC-OPS-101",
"severity": "SEV-1",
"status": "ACTIVE"
}
],
"tickets": [],
"changes": [
{
"change_id": "CHG-2001",
"risk": "HIGH",
"implemented_at": "2026-07-08T09:10:00"
}

]
},
"operations_summary": "The Payment API is unhealthy with a 38 percent error rate and elevated
latency. A SEV-1 incident is active for payment timeout failures.",
"possible_change_correlation": "A high-risk Payment API release was completed 
before the incident began. The service and timing indicate a possible 
correlation, but the available data does not confirm the release as the root 
cause.",
"recommended_next_actions": [
"Review CHG-2001 with Payments Engineering.",
"Compare the release changes with current timeout failures.",
"Review rollback readiness because rollback information is available.",
"Continue SEV-1 incident handling with Application Support."
],
"limitations": [
"The dataset does not contain application logs or distributed traces."
]
}

```

## 16. Known Limitations

- The project uses local operational data
- Service health values are stored snapshots
- rather than live monitoring metrics.
- The project does not include application logs or distributed traces.
- Possible change correlation is based on      available service and timing evidence.
- The assistant does not perform operational write actions

## 17. Future Improvements

- Live monitoring integration
- ITSM integration
- Deployment system integration
- Application log MCP server
- Distributed tracing integration
- Human approval for operational actions
- Persistent incident conversation memory


