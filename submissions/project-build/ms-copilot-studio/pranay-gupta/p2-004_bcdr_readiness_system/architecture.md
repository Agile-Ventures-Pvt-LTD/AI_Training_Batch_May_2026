# Solution Architecture

## Overview

The BCDR Readiness Assessment System follows a multi-agent architecture implemented in Microsoft Copilot Studio. A central Supervisor Agent coordinates the assessment process by delegating specialized tasks to dedicated child agents, validating their outputs, and producing the final BC/DR readiness assessment.

---

# Architecture Components

## Supervisor Agent

The **BCDR Supervisor Agent** acts as the central orchestrator of the solution. It is responsible for:

* Receiving BC/DR assessment requests.
* Retrieving application information from Excel.
* Invoking the appropriate specialist agents.
* Consolidating specialist outputs.
* Validating assessment results.
* Determining the final readiness classification.
* Updating the assessment register.
* Initiating report generation and stakeholder communication.

---

## Specialist Agents

The solution includes six specialist agents:

### Application Criticality Specialist

Evaluates the business criticality of the application and determines its criticality classification.

### Recovery Requirements Specialist

Assesses recovery objectives, including RTO, RPO, and recovery requirement gaps.

### Technical Recovery Specialist

Uses the Microsoft Learn MCP Server to evaluate the application's technical recovery capabilities and compare them with Microsoft guidance.

### Risk and Recovery Gap Specialist

Consolidates assessment findings to identify recovery gaps, assign risk levels, and recommend an overall readiness status.

### Remediation Planning Specialist

Creates remediation actions for identified gaps and recommends priorities and ownership.

### Reporting and Communication Specialist

Generates the BC/DR Readiness Assessment Report and prepares stakeholder notifications after Supervisor approval.

---

# System Workflow

The solution follows the workflow below:

```text
Assessment Request
        │
        ▼
BCDR Supervisor Agent
        │
        ├── Retrieve Assessment Request (Excel)
        ├── Retrieve Application Details (Excel)
        │
        ▼
Application Criticality Specialist
        │
        ▼
Recovery Requirements Specialist
        │
        ▼
Technical Recovery Specialist
(Microsoft Learn MCP)
        │
        ▼
Risk and Recovery Gap Specialist
        │
        ▼
Remediation Planning Specialist
        │
        ▼
Supervisor Validation
        │
        ├── Update Assessment Register (Excel)
        │
        ▼
Reporting and Communication Specialist
        ├── Microsoft Word
        └── Microsoft Outlook
```

---

# Microsoft Integrations

The solution integrates with the following Microsoft services:

* Microsoft Excel
* Microsoft Learn MCP Server
* Microsoft Word
* Microsoft Outlook

Each integration supports a specific stage of the BC/DR readiness assessment process.

---

# Architecture Summary

The architecture separates orchestration from specialist analysis by assigning dedicated responsibilities to each agent. The Supervisor Agent manages the overall workflow, while specialist agents focus on individual assessment activities. This design enables a structured, modular, and consistent BC/DR readiness assessment process.
