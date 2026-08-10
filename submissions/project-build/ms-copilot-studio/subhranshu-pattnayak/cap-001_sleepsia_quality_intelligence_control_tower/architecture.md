# Architecture

## Overview

The Sleepsia Quality Intelligence Control Tower is implemented in Microsoft Copilot Studio using a supervisor-specialist architecture.

A Quality Supervisor orchestrates the investigation workflow while specialist agents perform focused analysis tasks. Investigation decisions are made through policy-driven decision topics.

---

## Architecture Flow
```text
Trigger
   │
   ▼
Quality Supervisor
   │
   ├─ Incident Intake & Validation
   │
   ├─ Complaint Pattern Specialist
   ├─ Returns Specialist
   ├─ Product/Batch Specialist
   ├─ Customer Impact Specialist
   │
   ▼
Quality Investigation Decision
   │
   ├─ CAPA Specialist
   ├─ CAPA Planning & Ownership
   ├─ Evidence Update & Selective Reassessment
   │
   ▼
Report Generation
   │
   ▼
Notifications
```
---

## Quality Supervisor

The Quality Supervisor acts as the central orchestration component of the system.

Responsibilities include:

- Complaint intake processing
- Specialist invocation
- Investigation orchestration
- Classification processing
- CAPA initiation
- Reassessment processing
- Report generation
- Notification management

The supervisor operates in:

- Autonomous Quality Investigation Mode
- Interactive Utilization Mode

---

## Specialist Agents

### Complaint Pattern Specialist

Analyzes complaint history, complaint patterns, and recurring complaint behavior.

### Returns Specialist

Analyzes return-related information and return-rate trends.

### Product/Batch Specialist

Validates product, batch, supplier, and incident-history information.

### Customer Impact Specialist

Analyzes customer-impact-related evidence associated with complaints.

### CAPA Specialist

Generates CAPA recommendations when required by investigation outcomes.

### M365 Guidance Specialist

Provides MCP-based information retrieval during Interactive Utilization Mode.

---

## Decision Topics

The solution uses dedicated decision topics for:

- Incident Intake & Validation
- Quality Investigation Decision
- CAPA Planning & Ownership
- Evidence Update & Selective Reassessment

---

## Knowledge Sources

The solution uses the following knowledge sources:

- Sleepsia Product Quality Policy
- Sleepsia Product Care and Usage Guide
- Sleepsia Customer Resolution Policy
- Approved Product Information Sources

---

## Data Sources

The solution uses workbook tables including:

- Customer Complaints
- Quality Incidents
- CAPA Register
- Product Master
- Batch Register
- Returns
- Sales Summary
- Owners

---

## Processing Flow

1. Retrieve complaint.
2. Validate complaint.
3. Execute specialist analysis.
4. Execute quality investigation decision.
5. Create or update incident records.
6. Execute CAPA processing when required.
7. Execute reassessment processing when required.
8. Generate investigation report.
9. Send notifications.
10. Mark complaint as processed.

The Quality Supervisor remains responsible for workflow orchestration and decision execution, while specialist agents provide focused evidence and analysis.