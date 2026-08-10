
# Autonomous Trigger Design

## Overview

The Business Continuity & Disaster Recovery (BCDR) Readiness Assessment solution uses an Autonomous Trigger to automatically initiate the assessment workflow.

The trigger continuously monitors the configured location for new or updated assessment requests. When a valid assessment request is detected, the trigger invokes the BCDR Supervisor Agent to begin the assessment process.

This removes the need for manual intervention and enables an event-driven assessment workflow.

---

# Trigger Information

| Property      | Value                        |
| ------------- | ---------------------------- |
| Trigger Name  | New BC/DR Assessment Request |
| Trigger Type  | Autonomous Trigger           |
| Platform      | Microsoft Copilot Studio     |
| Event Source  | OneDrive for Business        |
| Trigger Event | When a file is modified      |

---

# Trigger Purpose

The trigger is responsible for:

- Monitoring incoming assessment requests.
- Detecting updates to the assessment request dataset.
- Starting the BCDR assessment workflow.
- Passing assessment information to the Supervisor Agent.

The trigger only starts the workflow. It does not perform any assessment logic.

---

# Trigger Configuration

## Connector

OneDrive for Business

## Event

When a file is modified

## Monitored Folder

```
/BCDR_Documents
```

---

# Trigger Source

The assessment request is stored in:

```
Assessment_Requests.csv
```

This dataset contains the assessment requests that initiate the workflow.

---

# Trigger Workflow

```

Assessment_Requests.csv Updated

↓

OneDrive Trigger Activated

↓

Validate Trigger Event

↓

Invoke BCDR Supervisor Agent

↓

Retrieve Application Details

↓

Begin Assessment Workflow

```

---

# Supervisor Integration

Once triggered, the workflow is handed over to the BCDR Supervisor Agent.

The Supervisor Agent is responsible for:

- Retrieving application information.
- Coordinating specialist agents.
- Maintaining assessment context.
- Consolidating assessment results.
- Updating assessment records.
- Initiating report generation.
- Triggering stakeholder notifications.

---

# Assessment Context

The trigger provides the starting point for the assessment.

The assessment context includes information such as:

- Assessment Identifier
- Application Identifier
- Request Date
- Request Origin

The Supervisor Agent uses this information to retrieve the complete application details from the Application Inventory.

---

# Trigger Responsibilities

The Autonomous Trigger is responsible for:

- Detecting assessment requests.
- Starting the assessment workflow.
- Invoking the Supervisor Agent.
- Passing the initial assessment context.

The trigger does not:

- Perform assessments.
- Invoke specialist agents.
- Generate reports.
- Update assessment records.
- Send notifications.

These responsibilities belong to the Supervisor Agent and the specialist agents.

---

# Event Flow

```

Assessment Request Received

↓

OneDrive for Business

↓

Autonomous Trigger

↓

BCDR Supervisor Agent

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

Reporting & Communication Specialist

↓

Assessment Completed

```

---

# Design Considerations

The trigger has been designed with the following principles:

## Event Driven

The assessment starts automatically when a qualifying event occurs.

---

## Single Entry Point

All assessment requests enter the system through a single autonomous trigger, ensuring a consistent execution path.

---

## Decoupled Architecture

The trigger is responsible only for detecting events and initiating the workflow. Business logic is delegated entirely to the Supervisor Agent.

---

## Scalability

The trigger can process multiple assessment requests over time without requiring changes to the orchestration logic.

---

# Current Implementation

The following trigger components have been configured:

- OneDrive for Business trigger.
- Monitoring of the `/BCDR_Documents` folder.
- Autonomous invocation of the BCDR Supervisor Agent.
- Integration with the multi-agent orchestration workflow.

---

# Future Enhancements

Potential improvements include:

- Trigger validation to process only `Assessment_Requests.csv`.
- Duplicate assessment detection.
- Scheduled batch processing.
- Additional validation of incoming assessment requests.
- Enhanced error logging and monitoring.

These enhancements are outside the scope of the current PRD implementation.

---

# Summary

The Autonomous Trigger serves as the entry point of the BC/DR Readiness Assessment solution. By automatically initiating the Supervisor Agent upon receiving an assessment request, it enables a fully event-driven workflow while maintaining a clear separation between event detection and business logic orchestration.
