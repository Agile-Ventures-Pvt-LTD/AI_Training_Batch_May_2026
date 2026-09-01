# Model Context Protocol (MCP) Implementation

## 1. Configuration
- **Child Agent Attachment:** `M365 Guidance Specialist`
- **Server Name:** `Microsoft Learn MCP Server`
- **Endpoint URL:** `https://learn.microsoft.com/api/mcp`
- **Authentication:** `None`

---

## 2. Boundaries & Non-Blocking Fallback
- **Domain Boundary:** M365 Guidance Specialist operates strictly for technical/deployment guidance (Teams publishing, M365 Copilot configuration). It has 0% influence on Sleepsia quality severity or CAPA decisions.
- **Fallback Behavior:** If the MCP server is unreachable or offline, the agent responds: `"Microsoft guidance unavailable - manual review"`. Core quality assessment and incident intake workflows continue without interruption.
