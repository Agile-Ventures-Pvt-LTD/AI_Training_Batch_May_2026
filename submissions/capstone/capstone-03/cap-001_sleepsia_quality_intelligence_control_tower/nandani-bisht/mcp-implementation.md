# Model Context Protocol (MCP) Integration

This document defines the configuration, tooling interface, and exception boundaries for the **Microsoft Learn MCP Server** integration in the **Sleepsia Quality Control Tower**.

---

## 1. MCP Server Configuration Settings

The **M365 Guidance Specialist** child agent uses the Model Context Protocol to query live documentation and deployment guidelines.

| Configuration Field | Value |
| :--- | :--- |
| **Server Name** | Microsoft Learn MCP Server |
| **Endpoint URL** | `https://learn.microsoft.com/api/mcp` |
| **Authentication Type** | None (Public API) |
| **Parent Agent** | Quality Supervisor |
| **Child Agent Owner** | M365 Guidance Specialist |
| **Operational Impact** | Non-blocking to core quality assessments |

---

## 2. Copilot Studio Integration Steps

The MCP server is added as an external tool inside Copilot Studio:

1. **Access Settings:** Navigate to the **M365 Guidance Specialist** agent configuration canvas.
2. **Tool Creation:** Go to **Tools** -> **Add a tool** -> **New tool** -> Select **Model Context Protocol**.
3. **Register Endpoint:** Enter `Microsoft Learn MCP Server` as the name, add a descriptive summary, and set the URL to `https://learn.microsoft.com/api/mcp`. Set Authentication to `None`.
4. **Tool Discovery:** Save the configuration. Copilot Studio queries the server's manifest and exposes the following tools:
   - `search_documentation(query: String)`: Searches Microsoft Learn database for Copilot Studio and Teams deployment topics.
   - `get_article_content(articleUrl: String)`: Retrieves the raw markdown content of a documentation page.
   - `verify_connector_status(connectorName: String)`: Returns authentication requirements and limits for standard enterprise connectors.

---

## 3. Discovered Tools Interface

The M365 Guidance Specialist interacts with the following schema mappings:

### `search_documentation`
- **Purpose:** Resolves deployment queries.
- **Parameters:**
  - `query` (required): Terms relating to Power Platform, Teams publishing, or Copilot Studio administration.
- **Returns:** List of articles with URLs and snippet highlights.

### `get_article_content`
- **Purpose:** Grounding content extraction.
- **Parameters:**
  - `articleUrl` (required): Target URL returned by search.
- **Returns:** Fully formatted document text.

---

## 4. Boundary and Failure Handling

The MCP connection is configured to prevent system crashes during Microsoft API outages:

- **Graceful Degradation:** The MCP tool call is wrapped inside a try-catch block in the Power Automate calling flow.
- **Outage Fallback Status:** If the endpoint `https://learn.microsoft.com/api/mcp` returns a `500`, `503`, or `404` status, or if the request times out (limit set to 5000ms):
  1. The system catches the error.
  2. The specialist returns the string: `"Microsoft guidance unavailable - manual review"`.
  3. The Quality Supervisor logs the exception details in the incident record.
  4. The Supervisor continues the core Sleepsia quality workflow.
- **No Hallucination Rule:** Under no circumstances should the system fabricate Microsoft documentation or invent connector guidelines if the MCP server is down.
