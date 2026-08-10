# System and Integration Limitations

This document outlines the known technical, tenant-level, and integration limitations of the **Sleepsia Quality Control Tower** implementation.

---

## 1. Tenant and IT Security Policy Limitations

- **Microsoft 365 Copilot Extensibility:** 
  - Access to the Microsoft 365 Copilot channel requires specialized enterprise licensing and tenant-wide administrator consent. If administrative sideloading policies block custom agents, the bot remains restricted to the standalone web chat and Teams channel.
- **Power Platform DLP Policies:** 
  - Strict Data Loss Prevention (DLP) rules in the host environment can block the HTTP connector used by the MCP server or the Microsoft Learn endpoint unless the environment administrator explicitly adds these hosts to the "Business Data" classification.
- **Environment Billing Lock:**
  - The Power Platform tenant environment (`Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359`) is currently subject to a billing quota limit. This blocks compiling and publishing the newest version of the bot to active channels, keeping the "Publish" button greyed out until additional AI Builder credits or licensing capacities are allocated by the IT administrator.

---

## 2. Connector and Tool Constraints

### Excel Online (Business)
- **Concurrency & Locking:** 
  - Excel files on OneDrive/SharePoint are subject to file locking during simultaneous write operations. While the recurrence trigger processes records in clusters to minimize locking conflicts, concurrent writes from interactive employee chats may result in transient "File Locked" errors.
- **Data Volume Limits:** 
  - Excel Online tables are not designed to serve as high-volume relational databases. A dataset exceeding 10,000 rows can experience latency during read/write queries. For enterprise scaling, the backend should be migrated to Microsoft Dataverse or Azure SQL.

### Word Online (Business)
- **Formatting and Sizing:** 
  - The "Populate a Microsoft Word template" action requires pre-defined plain text tags. Dynamic lists or variable-length tables (such as multiple incident histories) require complex nesting in Power Automate, which can degrade report generation performance.

### Office 365 Outlook
- **Rate Limits & Spam Filters:** 
  - The Outlook connector is bound by standard Office 365 sending limits. High-frequency recurrence triggers generating numerous alerts risk running into sending rate caps or triggering automated spam filters.

---

## 3. Agent and Platform Boundaries

- **MCP Endpoint Dependency:** 
  - The M365 Guidance Specialist depends entirely on the uptime of the Microsoft Learn MCP server. If this server goes offline, the child agent cannot retrieve live guidelines and falls back to a static "guidance unavailable" state.
- **Selective Reassessment Cap:** 
  - The reassessment loop is capped at a maximum of 2 cycles to prevent infinite looping and excessive API usage in the event of conflicting or cyclical updates. Any further changes require manual intervention by a human supervisor.
- **State Management:** 
  - Copilot Studio variables are session-bound. The bot cannot maintain persistent cross-session memory without reading from or writing to the Excel database on each turn.
