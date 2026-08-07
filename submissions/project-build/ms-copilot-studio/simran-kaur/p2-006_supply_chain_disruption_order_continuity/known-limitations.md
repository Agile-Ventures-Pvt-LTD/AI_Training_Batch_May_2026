# Known Limitations — Multi-Agent Disruption Response System

This document outlines the architectural, platform, and connector limitations discovered during the implementation and testing of Project P2-006.

---

## 1. Copilot Studio Generative Orchestration Limits
* **Non-Deterministic Routing**: While generative orchestration allows flexible component discovery, it can occasionally misroute complex multi-intent requests. Deterministic custom topics (such as Intake Validation and Strategy Resolution) must be used to enforce business rules.
* **Topic Nesting Depth**: Copilot Studio has a maximum nesting limit of **8 levels** of sub-topics. Designing deep agent-to-agent-to-sub-topic hierarchies can trigger execution errors.
* **Variable Scope Isolation**: Passing large objects (like ranked order tables) between child agents can hit memory limits. Variables should be kept flat or structured in simple JSON arrays.
* **Transient Execution Timeouts**: Copilot Studio limits execution duration for a single trigger run to **120 seconds**. If multiple specialists experience slow connector responses, the orchestrator may timeout, triggering the fallback retry pattern.

---

## 2. Microsoft Excel Online (Business) Connector Limits
* **Row Locking & Race Conditions**: Excel Online does not support true database transaction locking. If two instances write to the same table simultaneously, writes can conflict. The Recurrence Trigger mitigates this by restricting ingestion to a single record per run.
* **Lack of Real-Time Webhooks**: The standard Excel trigger does not support instantaneous data modification triggers. It relies on polling, which creates a delay (determined by the recurrence interval, e.g. 5 minutes).
* **Delegation Limits**: The Excel connector has a delegation limit of **2,000 rows** for filter queries. For larger datasets, tables must be indexed, or data must be migrated to Dataverse/SQL Server.

---

## 3. Word Online (Business) Connector Limits
* **Premium Licensing Requirement**: The Word Online connector requires a premium license, which may restrict deployment in standard client environments.
* **Static Template Binding**: Generating reports relies on pre-defined content control fields in a template document. Dynamic addition of table columns or nested rows (e.g., looping through an arbitrary number of affected customer orders) is difficult to implement without complex JSON schemas.
* **File Overwrite Constraints**: Creating a document with an existing name will cause a failure unless explicit "Overwrite = Yes" flags or unique timestamps are appended to the file name.

---

## 4. Office 365 Outlook Connector Limits
* **Rate Limiting**: The connector enforces a limit of **300 emails per minute** per user connection. In high-volume disruption environments, this can lead to throttling.
* **Attachment Constraints**: If the Reporting Specialist attempts to attach the Word report directly to the Outlook email, the file size must not exceed **20 MB**.
* **HTML Formatting Differences**: Complex HTML layouts in the notification body render inconsistently across Outlook Desktop, Outlook Web, and mobile applications. The system uses plain markdown-like HTML tags (`<br>`, `<b>`, `<ul>`) to ensure cross-client compatibility.
