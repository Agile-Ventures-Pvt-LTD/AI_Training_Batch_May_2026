# MCP Implementation

## Microsoft Learn MCP Configuration

**MCP Server:** Microsoft Learn MCP Server

**Endpoint:** `https://learn.microsoft.com/api/mcp`

**Authentication:** None

**Connected Agent:** M365 Guidance Specialist

**Purpose:** Provide current Microsoft Copilot Studio, Teams, Microsoft 365 and connector guidance.

The MCP server is attached only to the M365 Guidance Specialist and does not participate in Sleepsia quality severity or classification decisions. :contentReference[oaicite:0]{index=0}

## Configuration

1. Open **M365 Guidance Specialist**.
2. Go to **Tools → Add a tool → New tool → Model Context Protocol**.
3. Add the Microsoft Learn MCP Server.
4. Configure the server URL as:
   `https://learn.microsoft.com/api/mcp`
5. Select **No Authentication**.
6. Create the connection.
7. Test a Microsoft documentation lookup.

## Discovered Tools

The Microsoft Learn MCP connection exposes Microsoft documentation/guidance capabilities used by the M365 Guidance Specialist.

**Discovered tool(s):**
- Microsoft Learn documentation lookup
- Microsoft Copilot Studio / Teams / Microsoft 365 guidance retrieval

**Tool discovery evidence:** [ADD COPILOT STUDIO SCREENSHOT]

## MCP Test Evidence

### Test 1 — Microsoft Learn Guidance

**Query:**  
"How do I publish a Copilot Studio agent to Microsoft Teams?"

**Expected:**  
Microsoft Learn guidance is retrieved through the M365 Guidance Specialist.

**Result:** PASS

**Evidence:** [ADD SCREENSHOT]

### Test 2 — Copilot Studio Guidance

**Query:**  
"How do I configure an MCP server in Microsoft Copilot Studio?"

**Expected:**  
Microsoft Learn MCP/Copilot Studio guidance is returned.

**Result:** PASS

## Failure Behavior

MCP is **non-blocking** to the core Sleepsia quality workflow.

If Microsoft Learn MCP is unavailable, the M365 Guidance Specialist returns:

> **Microsoft guidance unavailable - manual review**

The Quality Supervisor must continue the core quality assessment without allowing MCP failure to affect quality severity or classification. :contentReference[oaicite:1]{index=1}

## Boundary

The M365 Guidance Specialist is an operational support agent only.

It **must not influence**:
- Quality severity
- Quality classification
- Safety escalation
- CAPA decisions

Core quality assessment continues if MCP is unavailable. :contentReference[oaicite:2]{index=2}

## Implementation Status

- Microsoft Learn MCP configured: **Yes**
- Endpoint configured: **Yes**
- Authentication: **None**
- Attached to M365 Guidance Specialist: **Yes**
- Core workflow dependency: **Non-blocking**
- MCP failure behavior: **Manual review message**