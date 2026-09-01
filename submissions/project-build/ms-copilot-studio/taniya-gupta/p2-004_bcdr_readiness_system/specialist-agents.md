# Specialist Agents Specification (`specialist-agents.md`)

## Overview
The system employs **6 Child Specialist Agents**, each dedicated to a distinct functional domain of BC/DR analysis. 

---

## 1. Application Criticality Specialist
- **Purpose**: Evaluates operational dependencies, user count, customer impact, revenue, and compliance obligations to assign business criticality.
- **Classification Categories**: `Mission Critical`, `Business Critical`, `Important`, `Standard`.
- **Classification Rules**:
  - *Mission Critical*: `CustomerFacing = Yes` AND (`RevenueImpact = High` OR `RegulatoryImpact = High`) AND `UserCount > 500`.
  - *Business Critical*: Core internal/external operations with significant downstream dependencies.
  - *Important*: Non-revenue generating internal tools with moderate user counts and manual workarounds.
  - *Standard*: Routine internal utility services with low urgency.

---

## 2. Recovery Requirements Specialist
- **Purpose**: Validates documented RTO/RPO against business criticality baseline expectations.
- **Target Matrix**:
  - *Mission Critical*: Expected RTO <= 1h, Expected RPO <= 15m.
  - *Business Critical*: Expected RTO <= 4h, Expected RPO <= 1h.
  - *Important*: Expected RTO <= 24h, Expected RPO <= 4h.
  - *Standard*: Expected RTO <= 72h, Expected RPO <= 24h.
- **Gap Detection Rules**: Flags RTO > target, RPO > target, missing values, `RTO > MaximumTolerableDowntime`, or missing manual workarounds.

---

## 3. Technical Recovery Specialist
- **Purpose**: Audits backup, DR, and high-availability technical configurations using real-time grounding via MCP.
- **MCP Tool**: `microsoft_docs_search` on `https://learn.microsoft.com/api/mcp`.
- **Target Technologies**: Azure App Service, Azure SQL Database, Azure Virtual Machines, Azure Storage.
- **Fallback Rule**: If MCP is unreachable, sets `MCPEvidenceStatus = "Unavailable"` and proceeds with available inventory data.

---

## 4. Risk and Gap Specialist
- **Purpose**: Consolidates findings across all domains into a structured gap catalog evaluating 15 specific gap categories.
- **Severity Grading**: `Critical`, `High`, `Medium`, `Low`.
- **Readiness Ratings**: `Ready`, `Ready with Minor Gaps`, `Remediation Required`, `High Risk`, `Insufficient Evidence`.

---

## 5. Remediation Planning Specialist
- **Purpose**: Converts identified gaps into actionable remediation tasks with priorities (`P1-Immediate` to `P4-Low`), suggested owners, and target completion categories (`Immediate`, `Short-term`, `Medium-term`, `Long-term`).

---

## 6. Reporting and Communication Specialist
- **Purpose**: Executes report generation and notification dispatches upon receiving authorization from the Supervisor.
- **Tool Actions**:
  - *Word Online*: Creates executive report `BCDR_Assessment_Report_[AppID].docx` using template content controls (`<w:sdt>`).
  - *Excel Online*: Appends assessment outcome row to `AssessmentRegisterTable`.
  - *Outlook 365*: Sends email notification to resolved address `Taniya.Gupta@agileventures.net`.
