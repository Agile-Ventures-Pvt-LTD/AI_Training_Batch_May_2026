# Known Limitations

## Overview

The Sleepsia Product Quality Intelligence System is designed to automate complaint investigation, incident classification, reassessment handling, CAPA planning, reporting, and notification workflows.

The system operates within defined business rules, available data sources, and configured Microsoft 365 capabilities.

---

## Data Dependency Limitations

The system depends on the accuracy and completeness of data stored in:

- Customer Complaints Table
- Returns Table
- Sales Summary Table
- Product Master Table
- Batch Register Table
- Quality Incidents Table
- CAPA Register Table
- Owners Table

Missing, incomplete, or inaccurate records may reduce investigation quality.

---

## Knowledge Base Dependency

Policy decisions rely on configured knowledge sources:

- Sleepsia Product Quality Policy
- Sleepsia Product Care and Usage Guide
- Sleepsia Customer Resolution Policy

If knowledge sources are outdated or incomplete, generated guidance may be affected.

---

## Investigation Scope

Specialist agents analyze only their assigned domains:

- Complaint Pattern Specialist
- Returns Specialist
- Product/Batch Specialist
- Customer Impact Specialist
- CAPA Specialist
- M365 Guidance Specialist

Specialists do not make final quality decisions.

Final decisions are performed by the Quality Supervisor.

---

## Reassessment Limitation

Reassessments are governed by configured reassessment rules.

When reassessment limits are exceeded, incidents are routed to Manual Review.

The system does not autonomously bypass reassessment controls.

---

## Tool Dependency

Workflow execution depends on successful operation of:

- Microsoft 365 Copilot Studio
- Excel Online Business connectors
- Word document generation
- Outlook email services
- MCP server integrations

Tool failures may prevent completion of individual workflow steps.

---

## Notification Limitation

Notification delivery depends on Microsoft Outlook availability and recipient configuration.

Successful workflow execution does not guarantee email delivery if external mail services fail.

---

## Report Generation Limitation

Investigation reports are generated from available evidence and workflow outputs.

Reports cannot include information that is not present in source systems.

---

## Interactive Mode Limitation

Interactive Utilization Mode is read-only.

The system cannot:

- Create incidents
- Create CAPAs
- Modify records
- Send notifications
- Trigger investigations

through interactive user requests.

---

## Human Oversight Requirement

Critical Escalation incidents and Manual Review outcomes may require human review and decision-making.

The system does not autonomously close Critical Escalation incidents.

---

## Auditability

All decisions are based on available evidence, policy rules, workflow outputs, and tool responses available at execution time.

The system does not fabricate evidence, tool results, or policy outcomes.