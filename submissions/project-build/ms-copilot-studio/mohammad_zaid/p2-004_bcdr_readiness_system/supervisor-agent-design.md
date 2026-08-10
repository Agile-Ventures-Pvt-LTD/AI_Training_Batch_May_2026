
# BCDR Supervisor Agent Design

## Overview

The BCDR Supervisor Agent is the central orchestrator of the Business Continuity & Disaster Recovery (BCDR) Readiness Assessment solution.

The agent is responsible for coordinating the complete assessment workflow by invoking specialist child agents, managing assessment context, consolidating assessment findings, updating assessment records, and initiating report generation and stakeholder communication.

The Supervisor Agent does not perform domain-specific analysis. Instead, it delegates specialized tasks to the appropriate child agents and consolidates their outputs into a final readiness assessment.

---

# Agent Information

| Property            | Value                     |
| ------------------- | ------------------------- |
| Agent Name          | BCDR Supervisor Agent     |
| Agent Type          | Parent (Supervisor) Agent |
| Platform            | Microsoft Copilot Studio  |
| Architecture Role   | Master Orchestrator       |
| Orchestration Model | Hub-and-Spoke             |

---

# Primary Responsibilities

The Supervisor Agent is responsible for:

- Receiving new BC/DR assessment requests.
- Retrieving application information.
- Maintaining assessment context.
- Delegating work to specialist child agents.
- Consolidating specialist findings.
- Calculating the overall BC/DR readiness.
- Updating the Assessment Register.
- Initiating report generation.
- Triggering stakeholder notifications.

---

# Agent Workflow

The Supervisor Agent executes the assessment using the following sequence.

```

New Assessment Request

↓

Retrieve Application Details

↓

Validate Application

↓

Application Criticality Specialist

↓

Recovery Requirements Specialist

↓

Technical Recovery Specialist

↓

Risk & Recovery Gap Specialist

↓

Remediation Planning Specialist

↓

Consolidate Assessment Results

↓

Update Assessment Register

↓

Reporting & Communication Specialist

↓

Assessment Complete

```

---

# Child Agent Delegation

The Supervisor Agent delegates work to the following child agents.

| Order | Child Agent                          | Responsibility                            |
| ----- | ------------------------------------ | ----------------------------------------- |
| 1     | Application Criticality Specialist   | Assess business criticality               |
| 2     | Recovery Requirements Specialist     | Evaluate RTO, RPO and recovery objectives |
| 3     | Technical Recovery Specialist        | Assess technical recovery capabilities    |
| 4     | Risk & Recovery Gap Specialist       | Identify recovery risks and gaps          |
| 5     | Remediation Planning Specialist      | Generate remediation recommendations      |
| 6     | Reporting & Communication Specialist | Generate report and notify stakeholders   |

The Supervisor Agent waits for each child agent to complete before proceeding to the next stage.

---

# Tools Used

## 1. Get Application Details

### Connector

Excel Online (Business)

### Purpose

Retrieve application information from the Application Inventory.

### Table

ApplicationInventoryTable

### Output

Application record containing:

- Application ID
- Application Name
- Business Function
- Business Owner
- Technical Owner
- Hosting Platform
- Azure Service
- Environment
- User Count
- Customer Facing
- Business Criticality
- Recovery Information

---

## 2. Update Assessment Register

### Connector

Excel Online (Business)

### Purpose

Store the completed assessment.

### Table

AssessmentRegisterTable

### Updates

- Assessment ID
- Application ID
- Overall Readiness
- Risk Rating
- Assessment Status
- Completion Date

---

# Input

The Supervisor Agent receives the following information from the trigger.

| Input          | Description                    |
| -------------- | ------------------------------ |
| Assessment ID  | Unique assessment identifier   |
| Application ID | Application to assess          |
| Request Date   | Assessment request date        |
| Requested By   | User requesting the assessment |

---

# Output

The Supervisor Agent produces:

- Overall BC/DR Readiness
- Consolidated Assessment
- Updated Assessment Register
- Report Generation Request
- Notification Request

---

# Decision Logic

The Supervisor Agent follows the assessment sequence defined in the PRD.

1. Validate the assessment request.
2. Retrieve application information.
3. Invoke each child agent in sequence.
4. Collect assessment findings.
5. Consolidate the assessment.
6. Determine the overall readiness status.
7. Update the Assessment Register.
8. Request report generation.
9. Request stakeholder notification.
10. Return the final assessment summary.

---

# Error Handling

The Supervisor Agent handles the following scenarios.

## Missing Application

If the application cannot be found:

- Stop the assessment.
- Return an error message.
- Do not invoke child agents.

---

## Missing Assessment Data

If required assessment information is unavailable:

- Continue only with available validated data.
- Identify missing information in the final assessment.

---

## Tool Failure

If an external connector fails:

- Stop the affected operation.
- Report the failure.
- Prevent incomplete assessment updates.

---

## Child Agent Failure

If a child agent cannot complete its task:

- Stop orchestration.
- Return the failure reason.
- Do not generate the final report.

---

# Assessment Context

The Supervisor Agent maintains a shared assessment context containing:

- Assessment ID
- Application Information
- Business Criticality
- Recovery Requirements
- Technical Recovery Findings
- Recovery Risks
- Recovery Gaps
- Remediation Recommendations
- Overall Readiness

This context is passed to child agents as required and consolidated after each assessment stage.

---

# Design Principles

The Supervisor Agent follows these principles.

## Orchestrator Only

The Supervisor coordinates specialist agents and does not perform specialist analysis.

---

## Sequential Execution

Child agents are executed in the order defined by the PRD.

---

## Single Source of Truth

The Supervisor maintains the complete assessment context throughout the workflow.

---

## Centralized Decision Making

The final readiness assessment is determined only after all specialist assessments have been completed.

---

## Auditability

Every assessment follows a repeatable and traceable workflow, ensuring consistency across evaluations.

---

# Implementation Summary

The BCDR Supervisor Agent acts as the central coordinator of the multi-agent system. It controls assessment execution, delegates work to specialist agents, manages assessment state, integrates external tools, and produces the final consolidated BC/DR readiness assessment in accordance with the project requirements.
