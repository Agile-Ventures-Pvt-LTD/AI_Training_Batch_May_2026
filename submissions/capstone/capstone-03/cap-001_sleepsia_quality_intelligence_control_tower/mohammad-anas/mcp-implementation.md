# MCP Implementation

## Server configuration

| Setting | Value |
|---|---|
| Server name | Microsoft Learn MCP |
| Server URL | https://learn.microsoft.com/api/mcp |
| Authentication | None |
| Attached agent | M365 Guidance Specialist only |
| Transport | Streamable (Copilot Studio default) |

## Setup steps performed
1. Opened M365 Guidance Specialist agent → Tools tab.
2. Selected Add a tool → Model Context Protocol → New tool (server not present in the pre-listed catalog).
3. Entered server name, description, and URL as above; authentication set to None.
4. Created the connection and added the server to the agent.
5. Verified at least one lookup tool/resource was listed on the MCP server's settings page.

## Discovered tools/resources
[FILL IN — list the actual tool names shown on the MCP server settings page after connecting, e.g. documentation search, page fetch, etc.]

## Test evidence

| Test query | Result | Grounded in MCP response? |
|---|---|---|
| "How do I publish a Copilot Studio agent to Teams?" | Yes It gives step by step implementations. |  Yes|

## Failure boundary
Per PRD Section 15.1/22, MCP failure is non-blocking to the core quality workflow. The M365 Guidance Specialist's instructions require it to respond "Microsoft guidance unavailable — manual review" if the MCP tool is unreachable or returns no result, rather than inventing Microsoft product guidance from memory. This agent is explicitly excluded from influencing FinalClassification, CAPA decisions, or any quality-severity output (enforced in both its own instructions and the Quality Supervisor's instructions).
