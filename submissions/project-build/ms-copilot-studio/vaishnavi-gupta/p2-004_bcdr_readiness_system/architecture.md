# Architecture

## Overview

The Autonomous Multi-Agent BC/DR Readiness Assessment System is built using Microsoft Copilot Studio and follows a multi-agent architecture. A central Supervisor Agent coordinates multiple specialist agents to perform Business Continuity (BC) and Disaster Recovery (DR) readiness assessments. The system is event-driven and executes automatically when the configured trigger is activated.

---

## Architecture Components

### 1. Trigger Layer

- File Modified Trigger
- Monitors the designated folder containing the BC/DR assessment workbook.
- Automatically starts the assessment workflow when the workbook is modified.

---

### 2. Supervisor Agent

The BC/DR Supervisor Agent acts as the central orchestrator of the system.

Responsibilities include:
- Reading assessment requests.
- Retrieving application details from Excel.
- Delegating tasks to specialist agents.
- Consolidating assessment results.
- Determining the overall BC/DR readiness.
- Initiating report generation and notifications.

---

### 3. Specialist Agents

#### Application Criticality Specialist
- Determines business criticality.
- Evaluates operational, financial, and customer impact.

#### Recovery Requirements Specialist
- Validates Recovery Time Objective (RTO) and Recovery Point Objective (RPO).
- Identifies recovery objective gaps.

#### Technical Recovery Specialist
- Uses the Microsoft Learn MCP Server.
- Retrieves official Microsoft guidance.
- Compares current recovery architecture with Microsoft best practices.

#### Risk & Recovery Gap Specialist
- Identifies BC/DR risks and recovery gaps.
- Assigns risk severity levels.
- Recommends overall readiness status.

#### Remediation Planning Specialist
- Converts identified gaps into remediation actions.
- Prioritizes corrective activities.
- Suggests ownership and validation requirements.

#### Reporting & Communication Specialist
- Generates the BC/DR Readiness Assessment Report.
- Updates the Assessment Register.
- Sends stakeholder notifications through Outlook.

---

## Data Sources

The solution uses the following data sources:

- Excel Workbook
  - Application_Inventory
  - Assessment_Requests
  - Assessment_Register
  - Risk_Scoring_Rules
  - Technology_Mapping

- Knowledge Sources
  - NovaSphere BC/DR Policy
  - BC/DR Readiness Assessment Report Template

- Microsoft Learn MCP Server
  - Official Microsoft technical documentation
  - Azure disaster recovery guidance
  - Backup and resiliency recommendations

---

## Workflow

1. The File Modified Trigger detects changes in the monitored folder.
2. The Supervisor Agent starts the assessment process.
3. Pending assessment requests are retrieved.
4. Application details are read from the Excel workbook.
5. Specialist agents independently analyze their respective domains.
6. The Technical Recovery Specialist retrieves Microsoft guidance using MCP.
7. The Supervisor validates and consolidates all findings.
8. The Reporting & Communication Specialist generates the final report.
9. The Assessment Register is updated.
10. Outlook notifications are sent to stakeholders.

---

## Architecture Diagram

```text
                 File Modified Trigger
                         │
                         ▼
              BC/DR Supervisor Agent
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     ▼                   ▼                   ▼
Application        Recovery           Technical Recovery
Criticality        Requirements        Specialist
Specialist         Specialist                │
                                             ▼
                                  Microsoft Learn MCP
                                             │
                                             ▼
                             Risk & Recovery Gap Specialist
                                             │
                                             ▼
                              Remediation Planning Specialist
                                             │
                                             ▼
                     Reporting & Communication Specialist
                         │                │
                         ▼                ▼
                 Assessment Report   Outlook Notification
                         │
                         ▼
                 Assessment Register
```

---

## Technologies Used

- Microsoft Copilot Studio
- Microsoft Learn MCP Server
- Excel Online
- Microsoft Word
- Microsoft Outlook
- OneDrive / SharePoint
- Autonomous Triggers

---

## Design Principles

- Multi-agent architecture with clear separation of responsibilities.
- Centralized orchestration through the Supervisor Agent.
- Evidence-based technical validation using Microsoft Learn MCP.
- Autonomous execution through event-driven triggers.
- Standardized reporting and assessment process.
- Modular design for scalability and future enhancements.