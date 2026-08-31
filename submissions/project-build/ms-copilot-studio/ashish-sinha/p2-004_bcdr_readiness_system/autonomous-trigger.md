# Autonomous Trigger

## Overview

The BC/DR Readiness Assessment System is designed to execute autonomously without requiring a user to start the assessment manually. An autonomous trigger initiates the assessment workflow, invokes the Supervisor Agent, and coordinates the complete multi-agent assessment process.

This approach enables scheduled or event-driven BC/DR assessments across enterprise applications.

---

# Objectives

The autonomous trigger is responsible for:

- Automatically initiating BC/DR assessments
- Passing the required assessment context to the Supervisor Agent
- Starting the multi-agent orchestration workflow
- Recording assessment execution
- Supporting scheduled and event-driven execution

---

# Trigger Architecture

```text
                 Trigger Event
                      │
                      ▼
          Autonomous Trigger Workflow
                      │
                      ▼
             BC/DR Supervisor Agent
                      │
                      ▼
          Multi-Agent Assessment Flow
                      │
                      ▼
         Reporting & Communication Agent
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Word Report   Excel Update   Outlook Notification
```

---


## 1. Text-Based Trigger

The assessment begins when a new assessment request is added to the Application Inventory or Assessment Register.

Example Event:

```
New Assessment Request Added or modified
```

---


# Trigger Input

The autonomous trigger passes the following information to the Supervisor Agent.

| Field | Description |
|---------|-------------|
| AssessmentID | Unique assessment identifier |
| ApplicationID | Target application identifier |
| TriggerType | Scheduled, Excel, SharePoint, Dataverse |
| TriggerTime | Date and time of execution |
| RequestedBy | System or requesting user |
| Priority | Assessment priority |


---

# Supervisor Invocation

After receiving the trigger event, the workflow invokes the BC/DR Supervisor Agent.

The Supervisor is responsible for:

1. Reading application data from text
2. Building the assessment context
3. Invoking specialist agents
4. Validating assessment results
5. Determining overall readiness
6. Triggering report generation
7. Updating the assessment register
8. Sending notifications

---

# Execution Flow

```text
Trigger Fired
      │
      ▼
Create Assessment Context
      │
      ▼
Invoke Supervisor Agent
      │
      ▼
Read Application Inventory
      │
      ▼
Application Criticality Specialist
      │
      ▼
Recovery Requirements Specialist
      │
      ▼
Technical Recovery Specialist
      │
      ▼
Risk & Recovery Gap Specialist
      │
      ▼
Remediation Planning Specialist
      │
      ▼
Supervisor Validation
      │
      ▼
Reporting & Communication Specialist
      │
      ▼
Assessment Completed
```

---

# Assessment Context

The autonomous trigger creates the initial assessment context.

Typical fields include:

- AssessmentID
- ApplicationID
- TriggerType
- TriggerTime
- RequestedBy

The Supervisor enriches this context with application metadata retrieved from the Excel Application Inventory.

---

# Trigger Validation

Before invoking the Supervisor Agent, the trigger validates:

- Assessment request exists
- Application ID is present
- Duplicate assessments are avoided
- Required data source is available

If validation fails, the workflow terminates and records the failure.

---

# Error Handling

The trigger supports graceful failure handling.

Examples include:

## Missing Application ID

Action:

- Stop execution
- Record failure
- Notify assessment owner (optional)

---

## Duplicate Assessment

Action:

- Ignore duplicate request
- Log duplicate detection

---

## Excel Unavailable

Action:

- Record data source failure
- Do not invoke the Supervisor

---

## Supervisor Invocation Failure

Action:

- Retry once
- Record failure if retry is unsuccessful

---

# Logging

Each execution records:

- Assessment ID
- Application ID
- Trigger Type
- Trigger Time
- Execution Status
- Completion Time
- Failure Reason (if applicable)

This information supports auditability and operational monitoring.

---

# Security Considerations

The autonomous trigger should:

- Run under a managed service account
- Use least-privilege permissions
- Avoid hardcoded credentials
- Validate all incoming trigger data
- Log execution events for auditing

---

# Best Practices

- Use scheduled execution for recurring assessments.
- Validate trigger inputs before starting the workflow.
- Prevent duplicate assessment execution.
- Log all trigger events.
- Retry transient failures once before terminating.
- Pass only the required context to the Supervisor Agent.

---

# Example End-to-End Flow

```text
OneDrive Modify text Trigger
            │
            ▼
Generate Assessment Request
            │
            ▼
Invoke Supervisor Agent
            │
            ▼
Execute Multi-Agent Assessment
            │
            ▼
Generate Word Report
            │
            ▼
Update Excel Register
            │
            ▼
Send Outlook Notification
            │
            ▼
Assessment Complete
```

---

# Summary

The Autonomous Trigger provides the entry point for the BC/DR Readiness Assessment System. It enables automated execution, supplies the initial assessment context, invokes the Supervisor Agent, and ensures that the assessment workflow begins consistently and reliably without manual intervention.