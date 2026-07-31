
## Architecture Overview

The NovaSphere BC/DR Readiness System follows an autonomous multi-agent architecture implemented in Microsoft Copilot Studio.

The architecture uses the **NovaSphere BC/DR Supervisor** as the central orchestrator. It receives assessment requests through an autonomous trigger and coordinates specialist agents to perform individual BC/DR analysis activities.

---

## High-Level Architecture

```

Assessment Request File Created
|
↓
Copilot Studio Event Trigger
|
↓
NovaSphere BC/DR Supervisor
|
-------------------------
|          |            |
↓          ↓            ↓
Criticality  Recovery    Technical
Specialist  Specialist  Specialist
|
↓
Microsoft Learn MCP

```
  ↓          ↓            ↓
```

Risk & Gap  Remediation  Reporting &
Specialist  Specialist  Communication
|
--------------------
|                  |
↓                  ↓
Word Assessment      Outlook Notification
Report

```

---

## Core Components

## 1. Autonomous Trigger

The system starts automatically when a new assessment request file is created.

The trigger provides assessment details to the Supervisor Agent, eliminating the need for manual chatbot interaction.

---

## 2. NovaSphere BC/DR Supervisor

The Supervisor Agent is responsible for orchestration and decision management.

### Responsibilities

- Receive trigger payload.
- Retrieve application assessment information.
- Invoke required specialist agents.
- Pass relevant context to specialists.
- Collect specialist responses.
- Validate assessment completeness.
- Consolidate findings.
- Determine final readiness classification.
- Authorize report generation and notification.

### Tools Used

- Get Assessment Requests
- Get Application Details
- Get Risk Scoring Rules
- Update Assessment Register

### Knowledge Used

- NovaSphere_BCDR_Policy.docx

---

# Specialist Agent Layer

## Application Criticality Specialist

Evaluates business importance and recovery priority.

### Input

- Application details
- Business impact information
- Ownership information

### Output

- Business criticality classification
- Supporting rationale

### Knowledge

- NovaSphere_BCDR_Policy.docx

---

## Recovery Requirements Specialist

Evaluates recovery objectives and identifies recovery requirement gaps.

### Analysis

- RTO alignment
- RPO alignment
- Maximum tolerable downtime
- Recovery dependencies

### Output

- Recovery assessment
- Identified inconsistencies
- Recommended recovery requirements

### Knowledge

- NovaSphere_BCDR_Policy.docx

---

## Technical Recovery Specialist

Evaluates technical resilience using Microsoft Learn MCP Server.

### Responsibilities

- Review technical architecture.
- Retrieve Microsoft guidance.
- Compare current configuration with recommended practices.
- Identify technical recovery gaps.

### Knowledge

- NovaSphere_BCDR_Policy.docx

### MCP Integration

Server:

```

Microsoft Learn MCP Server

```

Endpoint:

```

[https://learn.microsoft.com/api/mcp](https://learn.microsoft.com/api/mcp)

```

Tools:

- microsoft_docs_search
- microsoft_docs_fetch
- microsoft_code_sample_search

---

## Risk & Recovery Gap Specialist

Consolidates findings from other specialists.

### Responsibilities

- Identify BC/DR gaps.
- Classify risk severity.
- Provide readiness recommendation.

### Knowledge

- NovaSphere_BCDR_Policy.docx

---

## Remediation Planning Specialist

Creates remediation actions based on identified gaps.

### Responsibilities

- Define remediation tasks.
- Assign priority.
- Identify owners.
- Define validation requirements.

### Knowledge

- NovaSphere_BCDR_Policy.docx

---

## Reporting & Communication Specialist

Creates final assessment artifacts and communication.

### Responsibilities

- Generate BC/DR assessment report.
- Send readiness-based notifications.

### Knowledge

- BCDR_Rediness_Assessment_Report_Template.docx

### Tools

- Generate BCDR Assessment Report
- Send BCDR Notification

---

# Data Flow

```

Assessment Request
|
↓
Supervisor Agent
|
↓
Application Data Retrieval
|
↓
Specialist Analysis
|
↓
Validated Findings
|
↓
Final Readiness Decision
|
↓
Report + Notification

```

---

# External Integrations

| Integration | Purpose |
|---|---|
| Microsoft Excel | Application data and assessment register management |
| Microsoft Learn MCP | Technical recovery guidance |
| Microsoft Word | BC/DR assessment report generation |
| Microsoft Outlook | Stakeholder notifications |

---

# Architecture Principles

- Autonomous execution without user conversation.
- Clear separation of specialist responsibilities.
- Evidence-based technical recommendations.
- Supervisor-controlled final decisions.
- Safe handling of missing evidence and failed specialist responses.

