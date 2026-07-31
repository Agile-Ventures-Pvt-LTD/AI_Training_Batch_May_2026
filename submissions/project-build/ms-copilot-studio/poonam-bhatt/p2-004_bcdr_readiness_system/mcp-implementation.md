# Model Context Protocol (MCP) Implementation

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

## 1. MCP Configuration Details
The **Technical Recovery Specialist** uses the manually configured **Microsoft Learn MCP Server** to ground its assessments in real-time Microsoft Learn documentation. This connection prevents the agent from hallucinating capabilities or referencing deprecated features.

| Parameter | Required Value | Actual Implementation |
| :--- | :--- | :--- |
| **Server Name** | Microsoft Learn MCP | `Microsoft Learn MCP` |
| **Server Description** | Retrieves official Microsoft Learn documentation using the Microsoft Learn MCP server to provide evidence-based technical guidance for Azure, backup, disaster recovery, and business continuity assessments. | Configured as the tool's usage description |
| **Endpoint** | `https://learn.microsoft.com/api/mcp` | `https://learn.microsoft.com/api/mcp` |
| **Transport Type** | Streamable HTTP | Streamable HTTP |
| **Authentication** | None / Unauthenticated | No Auth header required |
| **Primary Consumer** | Technical Recovery Specialist | Linked *only* to the `Technical Recovery Specialist` agent toolset |

---

## 2. Discovered MCP Tools
Upon completing the connection handshake, the Microsoft Learn MCP Server exposes the following dynamic tools in Copilot Studio:

1. **`microsoft_docs_search`**:
   - **Description**: Searches Microsoft Learn documentation for Resiliency, Disaster Recovery, Backup, and Azure architectural blueprints.
   - **Inputs**: `query` (String), `limit` (Integer, default=5).
   - **Outputs**: List of matching documentation articles with titles, summaries, and URLs.
2. **`microsoft_docs_fetch`**:
   - **Description**: Retrieves the full markdown content of a specific Microsoft Learn documentation page by URL.
   - **Inputs**: `url` (String).
   - **Outputs**: Detailed text body of the page.

---

## 3. Connection Manager Authorization & Configuration Steps
In Microsoft Copilot Studio (2026 Modern Experience), follow these steps to add and authorize the MCP server:

1. Open the **Technical Recovery Specialist** connected agent.
2. Navigate to the **Tools** tab $\rightarrow$ Click **+ Add a tool** $\rightarrow$ Choose **Model Context Protocol (MCP)**.
3. Select **Add existing MCP server** or configure a new server with the Endpoint `https://learn.microsoft.com/api/mcp`.
4. Leave Authentication as **None / Unauthenticated** and click **Discover Tools**.
5. Save the configuration.
6. **Connection Manager Authorization**:
   - When attempting to run the agent in the Test chat, the bot will prompt: *"Let's get you connected first, and then I can find that info for you. Open connection manager to verify your credentials."*
   - Click the **Open connection manager** link.
   - Click the **Create Connection** button.
   - Click **Allow** to authorize Copilot Studio to use the HTTP connection. The connection state will update to **Connected**.
   - Return to the test panel and click **Retry**.

---

## 4. Structured Output Format
The Technical Recovery Specialist is instructed to execute queries against the MCP tools and parse the results into the following strict structure:

```text
Technology Evaluated:
- <Technology>

Microsoft Documentation Retrieved:
- <Document 1>
- <Document 2>

Current Configuration:
- <Summary>

Technical Gaps:
- <Gap 1>
- <Gap 2>

Recommendations:
- <Recommendation 1>
- <Recommendation 2>

Evidence Status:
- Retrieved Successfully
or
- Technical Evidence Unavailable

Confidence Level:
- High / Medium / Low
```

---

## 5. Resilience & Failure Handling
The system handles three major failure modes:
1. **MCP Connection Timeout/Network Failure**: The agent fails gracefully, catches the connection error, and passes `Technical evidence unavailable` to the Supervisor instead of hallucinating instructions.
2. **No Documentation Found**: If a search query yields no articles, the specialist outputs `Technical Evidence Unavailable - manual technical review required` under the **Evidence Status** section.
3. **Missing Critical Evidence**: If documentation is found but the application inventory lacks technical metadata to make a comparison, it flags `Evidence Status: Technical Evidence Unavailable`.

> [!IMPORTANT]
> **No Hallucinated Fallback Rule**:
> The Technical Recovery Specialist is strictly prohibited from inventing Microsoft technical guidelines. If the connection fails, it must pass a clear status string (`Technical evidence unavailable`) to the Supervisor. The Supervisor then flags the assessment as `Insufficient Evidence` and escalates the task to a human architect.
