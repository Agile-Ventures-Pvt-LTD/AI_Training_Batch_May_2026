# MCP Implementation

## Microsoft Learn MCP Server

The Quality Intelligence Control Tower uses the Microsoft Learn MCP Server through Microsoft Copilot Studio.

### MCP Configuration

- MCP Server: Microsoft Learn MCP Server
- Endpoint: https://learn.microsoft.com/api/mcp
- Transport: Streamable HTTP
- Authentication: None
- Connected through: Microsoft Copilot Studio
- Assigned Agent: M365 Guidance Specialist

The Microsoft Learn MCP Server provides access to Microsoft documentation and code-sample search capabilities. Microsoft documents the endpoint as `https://learn.microsoft.com/api/mcp` and states that authentication is not required. :contentReference[oaicite:0]{index=0}

## Copilot Studio Configuration

The MCP server was added from the agent's **Tools** section using the Model Context Protocol option.

Configuration flow:

1. Open the M365 Guidance Specialist.
2. Select **Tools**.
3. Add the Microsoft Learn MCP Server.
4. Configure the MCP connection.
5. Enable the required MCP capabilities.
6. Add the MCP server to the agent.
7. Test the connection using Microsoft Learn-related questions.

Copilot Studio supports adding an existing MCP server through the Tools page and exposes the tools provided by the connected MCP server. :contentReference[oaicite:1]{index=1}

## Discovered MCP Tools

The Microsoft Learn MCP Server provides:

- `microsoft_docs_search`
- `microsoft_docs_fetch`
- `microsoft_code_sample_search`

These tools allow the M365 Guidance Specialist to search Microsoft documentation, retrieve documentation content, and search Microsoft code samples. :contentReference[oaicite:2]{index=2}

## Agent Instructions

The M365 Guidance Specialist is instructed to use the Microsoft Learn MCP Server when the request requires Microsoft 365, Copilot Studio, or related Microsoft product guidance.

## Testing Evidence

The MCP integration was tested from the Copilot Studio agent environment.

Validation included:

- MCP server connection availability.
- Tool discovery.
- Microsoft documentation search.
- Retrieval of relevant Microsoft Learn guidance.
- Agent use of MCP results for Microsoft 365/Copilot-related questions.

## Failure Behaviour

MCP is used for Microsoft documentation guidance and is not part of the core quality investigation decision path.

If the MCP service is unavailable, the Quality Supervisor's core quality investigation workflow can continue without relying on MCP results.

## Implementation Boundary

MCP is used for Microsoft Learn/Microsoft 365 guidance only.

Operational quality data remains in the configured Excel Online tools, while Word and Outlook are used for report generation and notification respectively.

Copilot Studio requires generative orchestration when using MCP tools. :contentReference[oaicite:3]{index=3}