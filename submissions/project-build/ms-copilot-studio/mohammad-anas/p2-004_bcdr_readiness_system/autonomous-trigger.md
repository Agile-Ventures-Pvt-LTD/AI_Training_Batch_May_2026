# Autonomous Trigger

## Overview

The Autonomous Multi-Agent Business Continuity & Disaster Recovery (BC/DR) Readiness System is designed to operate without manual intervention once an assessment request is submitted.

The automation begins when a predefined trigger detects a change in the assessment workbook stored in Microsoft OneDrive. This event initiates the Supervisor Agent, which coordinates the complete assessment workflow by invoking specialist agents, updating business records, and generating assessment reports.

The trigger mechanism enables event-driven execution, allowing the system to respond automatically to new or updated assessment requests.

---

# Objective

The autonomous trigger is responsible for:

- Detecting assessment requests.
- Starting the BC/DR assessment workflow automatically.
- Eliminating manual execution.
- Passing execution context to the Supervisor Agent.
- Ensuring consistent workflow initiation.

---

# Trigger Technology

The solution uses the following Microsoft Copilot Studio trigger.

| Component | Technology |
|----------|------------|
| Platform | Microsoft Copilot Studio |
| Trigger Type | Event Trigger |
| Connector | OneDrive |
| Event | When a file is modified |

---

# Trigger Configuration

## Connector

Microsoft OneDrive

---

## Event

```
When a file is modified
```

---

## Monitored File

```
P2-004_BCDR_Lab_Data.xlsx
```

---

## Purpose

Monitor the assessment workbook for changes and automatically initiate the BC/DR readiness assessment workflow.

---

# Trigger Workflow

The trigger initiates the assessment using the following sequence.

```text
Assessment Workbook Updated
             │
             ▼
OneDrive Detects File Modification
             │
             ▼
Copilot Studio Event Trigger Fires
             │
             ▼
Supervisor Agent Starts
             │
             ▼
Retrieve Assessment Data
             │
             ▼
Execute Specialist Agents
             │
             ▼
Update Assessment Register
             │
             ▼
Generate Word Report
             │
             ▼
Send Outlook Notification
             │
             ▼
Workflow Complete
```

---

# Execution Sequence

## Step 1

A user updates the assessment workbook stored in Microsoft OneDrive.

Typical updates include:

- Adding a new application.
- Updating recovery information.
- Creating a new assessment request.
- Modifying application details.

---

## Step 2

The OneDrive connector detects that the monitored file has been modified.

The trigger automatically activates.

---

## Step 3

Microsoft Copilot Studio starts the Supervisor Agent.

The trigger itself does not perform any business logic.

Its sole responsibility is to initiate workflow execution.

---

## Step 4

The Supervisor Agent retrieves business information from Microsoft Excel using configured connectors.

Tables accessed include:

- AssessmentRequestsTable
- ApplicationInventoryTable

---

## Step 5

The Supervisor coordinates the Connected Agents.

Execution order:

1. Application Criticality Specialist
2. Recovery Requirements Specialist
3. Technical Recovery Specialist
4. Risk & Recovery Gap Specialist
5. Remediation Planning Specialist
6. Reporting & Communication Specialist

---

## Step 6

After all specialists complete successfully, the Supervisor Agent updates the Assessment Register.

Updated fields may include:

- Assessment Status
- Readiness Classification
- Completion Date
- Assessment Summary

---

## Step 7

The Reporting & Communication Specialist:

- Generates the Microsoft Word assessment report.
- Drafts the stakeholder email.
- Sends the Outlook notification.

---

## Trigger Responsibilities

The trigger is intentionally lightweight.

Its responsibilities are limited to:

- Monitoring the assessment workbook.
- Detecting modifications.
- Starting the Supervisor Agent.
- Passing execution context.

The trigger does **not**:

- Read Excel data.
- Execute business logic.
- Perform assessments.
- Generate reports.
- Communicate with specialist agents.
- Update business records.

These responsibilities belong to the Supervisor Agent.

---

# Design Considerations

The trigger follows an event-driven architecture.

Key design principles include:

- Automatic execution.
- Minimal trigger logic.
- Clear separation of concerns.
- Stateless execution.
- Supervisor-controlled orchestration.

This keeps the trigger simple while allowing the Supervisor Agent to manage workflow complexity.

---

# Error Handling

Several scenarios are considered during trigger execution.

## Workbook Not Found

**Cause**

The monitored workbook is unavailable or has been moved.

**System Response**

- Trigger execution fails.
- Workflow is not started.
- Failure is logged.

---

## OneDrive Connection Failure

**Cause**

The OneDrive connector cannot access the workbook.

**System Response**

- Workflow execution stops.
- Supervisor Agent is not invoked.

---

## Supervisor Agent Failure

**Cause**

The trigger executes successfully, but the Supervisor Agent cannot start.

**System Response**

- Workflow terminates.
- Error is recorded for investigation.

---

## Excel Data Retrieval Failure

**Cause**

The Supervisor cannot retrieve assessment information.

**System Response**

- Assessment is not executed.
- Error is returned to the workflow.

---

# Advantages of Event-Driven Execution

The autonomous trigger provides several operational benefits.

## Reduced Manual Effort

No user interaction is required once an assessment request has been entered into the workbook.

---

## Faster Processing

Assessments begin immediately after a qualifying workbook modification.

---

## Consistent Workflow

Every assessment follows the same execution sequence, reducing variability.

---

## Improved Reliability

Automatic initiation minimizes the risk of missed or delayed assessments.

---

## Scalable Design

The same trigger mechanism can support additional assessment workflows or specialist agents without changes to the overall architecture.

---

# Current Implementation

The implemented trigger uses the following configuration.

| Property | Value |
|----------|-------|
| Platform | Microsoft Copilot Studio |
| Trigger Type | Event |
| Connector | OneDrive |
| Event | When a file is modified |
| Monitored File | P2-004_BCDR_Lab_Data.xlsx |
| Next Component | BC/DR Supervisor Agent |

---

# Future Enhancements

Potential improvements include:

- Monitoring multiple assessment workbooks.
- Trigger filtering based on specific worksheets or tables.
- Scheduled assessment execution.
- Support for SharePoint document libraries.
- Dataverse event triggers.
- Approval-based workflow initiation.
- Duplicate assessment detection.
- Retry mechanisms for transient failures.

---

# Summary

The Autonomous Trigger provides the entry point for the BC/DR Readiness System by automatically detecting changes to the assessment workbook and initiating the Supervisor Agent. By adopting an event-driven architecture, the solution eliminates manual workflow initiation while ensuring every assessment follows a consistent, automated, and repeatable execution process.