# MCP implementation

## Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower integrates **Microsoft Learn MCP (Model Context Protocol)** through the **M365 Guidance Specialist** child agent.

The MCP integration provides Microsoft documentation and operational guidance for **Copilot Studio, Microsoft 365, Teams, connectors, authentication, and deployment**.

## MCP architecture

```text
Quality Supervisor
        |
        v
M365 Guidance Specialist
        |
        v
Microsoft Learn MCP
        |
        v
Microsoft Learn Documentation
```

## Configuration

| Setting        | Value                               |
| -------------- | ----------------------------------- |
| Server name    | Microsoft Learn MCP                 |
| Server URL     | https://learn.microsoft.com/api/mcp |
| Authentication | None                                |

## Responsibilities

The M365 Guidance Specialist uses MCP to provide:

* Copilot Studio guidance
* Teams publishing guidance
* Connector configuration
* Microsoft 365 deployment
* Authentication and governance best practices

## Workflow

1. User requests Microsoft-related guidance.
2. Quality Supervisor invokes the M365 Guidance Specialist.
3. The specialist retrieves documentation from Microsoft Learn MCP.
4. A structured guidance response is returned.

## Safety boundary

The MCP integration **does not participate in quality investigations**.

It must never influence:

* quality classifications,
* safety decisions,
* CAPA planning,
* incident severity,
* supervisor decisions.

## Failure handling

If the MCP server is unavailable:

* retry once,
* return **“Microsoft guidance unavailable – manual review required.”**

The quality investigation workflow continues independently.

## Benefits

* Up-to-date Microsoft documentation
* Reduced maintenance
* Accurate deployment guidance
* Native Microsoft 365 integration
* Clear separation between operational guidance and quality decision-making
