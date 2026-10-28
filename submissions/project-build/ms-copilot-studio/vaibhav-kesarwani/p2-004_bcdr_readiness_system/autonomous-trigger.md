# Autonomous trigger

## P2-004 Autonomous Multi-Agent BC/DR Readiness System

Microsoft Copilot Studio | Event-driven assessment orchestration | Supervisor-triggered execution

## Overview

The BC/DR Readiness System is designed to operate autonomously using an event-driven trigger mechanism in Microsoft Copilot Studio.

A new assessment request automatically initiates the BC/DR Supervisor Agent, which coordinates the complete assessment workflow without requiring manual conversational interaction.

The trigger architecture enables the system to continuously monitor incoming assessment requests and execute the full multi-agent BC/DR readiness assessment process.

## Trigger objective

The autonomous trigger is responsible for:

* detecting new assessment requests,
* validating request completeness,
* initiating the Supervisor Agent,
* providing assessment context,
* starting the multi-agent assessment workflow,
* enabling unattended BC/DR assessment execution.

## Trigger architecture

```text
Assessment Request
        |
        v
Excel / OneDrive Trigger
        |
        v
Copilot Studio Trigger
        |
        v
BC/DR Supervisor Agent
        |
        +-----------------------------+
        |                             |
        +--> Child Agent Orchestration
        |
        +--> Report Generation
        |
        +--> Assessment Register Update
        |
        +--> Outlook Notification
```

The trigger initiates only the Supervisor Agent.

All child agents are invoked through Supervisor orchestration.

## Trigger source

The implemented trigger uses **Excel Online (Business)** with **OneDrive for Business**.

Primary trigger file:

Assessment_Requests.xlsx

The workbook contains incoming BC/DR assessment requests.

## Trigger event

The trigger activates when a **new assessment request is added** to the Assessment Requests table.

Monitored event:

When a new row is added.

This event starts autonomous assessment execution.

## Assessment request structure

Each assessment request contains:

* Request_ID
* Request_Date
* Requestor_Name
* Requestor_Email
* Application_ID
* Application_Name
* Assessment_Reason
* Priority
* Status

Example:

| Field             | Value               |
| ----------------- | ------------------- |
| Request_ID        | REQ-20260731-001    |
| Application_ID    | APP1001             |
| Application_Name  | NovaCRM             |
| Assessment_Reason | Annual BC/DR Review |
| Priority          | High                |
| Status            | New                 |

## Trigger configuration

The Copilot Studio trigger is configured to monitor the Assessment Requests workbook stored in OneDrive for Business.

Configuration:

| Component      | Value                   |
| -------------- | ----------------------- |
| Trigger source | Excel Online (Business) |
| Storage        | OneDrive for Business   |
| Event          | New row added           |
| Target table   | Assessment_Requests     |
| Execution mode | Automatic               |

## Trigger validation

When a trigger event is received, the Supervisor Agent performs validation before starting the assessment.

Required fields:

* Application_ID or Application_Name
* Request_ID
* Request_Date

Validation rules:

If Application_ID is available:

Use Application_ID.

Else if Application_Name is available:

Use Application_Name.

Else:

Stop execution and classify as Insufficient Evidence.

## Trigger execution workflow

### Stage 1 – Trigger received

The Excel trigger detects a new assessment request.

### Stage 2 – Supervisor initialization

The BC/DR Supervisor Agent receives:

* request metadata,
* application identifier,
* requestor information,
* assessment reason.

### Stage 3 – Assessment ID generation

The Supervisor generates:

BCDR-YYYYMMDD-XXXX

Example:

BCDR-20260731-0001

### Stage 4 – Application retrieval

The Supervisor retrieves application information from:

P2-004_BCDR_Lab_Data.xlsx

### Stage 5 – Child-agent orchestration

The Supervisor invokes:

1. Application Criticality Specialist
2. Recovery Requirements Specialist
3. Technical Recovery Specialist
4. Risk & Recovery Gap Specialist
5. Remediation Planning Specialist
6. Reporting & Communication Specialist

### Stage 6 – Assessment completion

The Supervisor:

* validates findings,
* determines readiness,
* authorizes report generation,
* updates the assessment register,
* authorizes Outlook notifications.

## Context passed by the trigger

The trigger provides the initial assessment context.

Example:

```json
{
  "Request_ID": "REQ-20260731-001",
  "Request_Date": "2026-07-31",
  "Application_ID": "APP1001",
  "Application_Name": "NovaCRM",
  "Assessment_Reason": "Annual BC/DR Review",
  "Priority": "High"
}
```

The Supervisor enriches this context using Excel application data.

## Autonomous execution boundaries

The trigger automatically starts:

* application retrieval,
* specialist delegation,
* technical assessment,
* report generation,
* assessment register updates,
* notification preparation.

The trigger does not autonomously:

* approve assessments,
* modify infrastructure,
* change Azure configuration,
* execute disaster recovery,
* perform failover operations.

## Duplicate request handling

Before starting a new assessment, the Supervisor validates whether an active assessment already exists.

Validation:

* Application_ID
* Assessment status
* Assessment date

If a duplicate assessment is detected:

* merge with the active assessment,
* reject the duplicate,
* or escalate for manual review.

## Failure handling

### Missing application identifier

Result:

Assessment not started.

### Application not found

Result:

Insufficient Evidence.

### Excel unavailable

Result:

Assessment suspended.

### Child agent failure

Result:

Supervisor retry logic executed.

### MCP unavailable

Result:

Technical evidence limitation recorded.

Assessment continues when possible.

## Trigger retry behavior

The Supervisor supports limited retry behavior for transient failures.

Retry scenarios:

* temporary connector failure,
* temporary Excel access failure,
* temporary child-agent failure.

Persistent failures are recorded and escalated.

## Status management

The Assessment Requests workbook is updated during execution.

Status progression:

New

↓

In Progress

↓

Assessment Completed

or

Assessment Failed

or

Additional Information Required

This provides operational visibility into autonomous execution.

## Trigger monitoring

The following events are monitored:

* assessment started,
* assessment completed,
* assessment failed,
* report generated,
* notification sent,
* escalation triggered.

These events support operational monitoring and auditability.

## Security considerations

The trigger operates using Microsoft 365 connectors.

Access is governed by:

* OneDrive permissions,
* Excel permissions,
* Copilot Studio permissions,
* Outlook permissions.

The trigger processes only authorized assessment requests.

## PRD compliance

The autonomous trigger satisfies the PRD requirements by:

* initiating assessments automatically,
* invoking the Supervisor Agent,
* enabling multi-agent orchestration,
* integrating with Excel,
* supporting autonomous execution,
* handling failures safely,
* supporting auditability,
* supporting enterprise BC/DR workflows.

## Conclusion

The autonomous trigger transforms the BC/DR assessment process from a manual conversational workflow into an event-driven enterprise assessment pipeline.

By automatically initiating the Supervisor Agent whenever a new assessment request is received, the system enables unattended multi-agent orchestration, evidence-grounded technical assessment, automated reporting, operational record updates, and structured stakeholder communication while maintaining governance controls and safe failure handling.
