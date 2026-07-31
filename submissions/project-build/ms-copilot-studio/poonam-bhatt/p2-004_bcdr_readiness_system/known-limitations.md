# Known Limitations

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

## 1. Overview
This document describes the known limits and operational boundaries of the **P2-004 Autonomous BC/DR Readiness System** built in Microsoft Copilot Studio (2026 Modern Experience).

Documenting these boundaries ensures that IT architects, business owners, and operations teams understand where the automation stops and where human oversight is required.

---

## 2. Functional & Architecture Limitations

### 2.1 Multi-Agent Loop Scoping
- Copilot Studio limits connected agent depth. The system uses a flat hub-and-spoke multi-agent topology (1 Supervisor, 6 Specialists). Nested calling of specialists by other specialists is disabled to avoid runtime infinite loops.
- Context data size: Large JSON strings passed between agents can exceed slot parameters, so input context variables are trimmed to keep only key fields.

### 2.2 Conflict Resolution Override
- If specialists return conflicting assessments, the Supervisor overrides the final score to the highest risk option. This prevents system downtime but may flag false-positive high-risk warnings for minor configuration issues.

---

## 3. Platform & Connector Constraints

### 3.1 Microsoft Excel Online (Business) Connector
- **Row/Table Locking**: If a user is actively editing `P2-004_BCDR_Lab_Data.xlsx` in Excel Desktop or Web while the OneDrive trigger runs, the file lock may prevent Copilot Studio from reading/writing values. This causes a transient trigger exception.
- **Trigger Sync Latency**: Power Platform connector sync intervals can take from 30 seconds to several minutes to fire after a file modification is saved in OneDrive for Business, which might introduce minor assessment delay. Frequent background updates on massive tables may consume high Power Platform API request quotas.

### 3.2 Microsoft Word Template Connector
- **Formatting Constraints**: The Word report generator uses content control field mapping. Complex visual formatting (like dynamic tables of varying row sizes for remediation actions) is limited by basic Word templates.

### 3.3 Microsoft Outlook Email Connector
- **Send Rates**: Tenant policies limit the number of automated emails sent. During large-scale application inventory batch imports, notifications are queued to prevent rate-limit blocks.

---

## 4. Tenant & MCP Network Limitations

### 4.1 Connection Manager Authorization
- **Manual Hands-On Verification**: In Copilot Studio 2026, external MCP HTTP servers create connection objects that require manual authorization via the Connection Manager (Create Connection $\rightarrow$ Allow). The agent cannot self-authorize, preventing fully hands-off environment deployment.
- **Description Limits**: Some tenants enforce strict character limit constraints on tool descriptions, requiring a compressed description format for the MCP search and fetch capabilities.

### 4.2 MCP Server Routing Policies
- **Direct IP Restrictions**: Organizations with strict Data Loss Prevention (DLP) rules might block outbound Streamable HTTP requests to external endpoints like `https://learn.microsoft.com/api/mcp`.
- **Latency Overheads**: Large doc searches via the MCP server take between 1.5 to 3 seconds. The Technical Recovery Specialist has a 5-second connection timeout, which could result in a transient `Technical evidence unavailable` state during network congestion.

---

## 5. Future Improvement Opportunities
- **Automated Service Tickets**: Integrating the Remediation Specialist with Azure DevOps or Jira to auto-generate development tickets.
- **Enhanced Data Parsing**: Using AI Hub document processing to read PDF network topology diagrams and verify single-region dependency configurations.
- **Self-Healing Triggers**: Adding auto-retry configurations on trigger locks.
