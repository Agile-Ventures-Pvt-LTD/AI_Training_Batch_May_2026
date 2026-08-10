# Autonomous Trigger Design

## Overview

The Autonomous Trigger is the entry point of the Supply Chain Disruption & Order Continuity Response System. It enables the solution to operate without requiring user interaction by automatically detecting and processing disruption requests on a recurring schedule.

A Microsoft Copilot Studio **Recurrence Event Trigger** is used to periodically scan disruption records, identify pending disruptions, and initiate the multi-agent assessment workflow. The trigger ensures that disruptions are processed in a controlled and deterministic manner while preventing duplicate or concurrent assessments. 【1-5e8f0c】

---

# Objective

The purpose of the autonomous trigger is to:

- Enable fully autonomous execution
- Detect new disruption requests
- Select disruptions awaiting assessment
- Prevent duplicate processing
- Initiate the Supervisor Agent workflow
- Maintain controlled processing order
- Support continuous monitoring of supply disruptions


---

# Trigger Configuration

## Trigger Type

**Recurrence Event Trigger**

The trigger is configured directly within Microsoft Copilot Studio and runs automatically based on a predefined schedule.

### Sample Configuration

```text
Trigger Type: Recurrence
Frequency: Every 5 Minutes (Testing)
Production Frequency: As Required
Execution Mode: Automated
Generative Orchestration: Enabled
```

During project testing, a shorter recurrence interval may be used to quickly validate orchestration behavior. 

---

# Trigger Execution Flow

```text
Recurrence Trigger Fires
          │
          ▼
Read Disruption Requests
          │
          ▼
Pending Records Exist?
          │
    ┌─────┴─────┐
    │           │
   No          Yes
    │           │
    ▼           ▼
 Safe Exit   Select Oldest
                 Pending
                   │
                   ▼
      Change Status to
        In Assessment
                   │
                   ▼
     Invoke Supervisor
                   │
                   ▼
      Begin Multi-Agent
         Assessment
```



---

# Operational Workflow

## Step 1: Trigger Activation

The recurrence trigger executes according to its configured schedule.

### Actions

- Start autonomous workflow
- Establish connection to Excel data source
- Retrieve disruption request records


---

## Step 2: Read Disruption Requests

The trigger reads records from the disruption management table.

### Data Source

```text
DisruptionRequestsTable
```

### Storage Location

- OneDrive for Business
- SharePoint Online

The solution uses Excel Online (Business) connectors to access operational data. 【1-5e8f0c】

---

## Step 3: Identify Pending Records

The trigger searches for disruption requests where:

```text
Status = Pending
```

Only records meeting this requirement qualify for processing. 【1-5e8f0c】

---

## Step 4: Select Oldest Pending Record

If multiple pending disruptions exist, only one disruption is processed during each trigger cycle.

### Selection Rule

```text
Choose Oldest Pending Record
```

This ensures:

- Predictable execution
- Fair processing order
- Reduced concurrency conflicts
- Simplified state management


---

## Step 5: Prevent Duplicate Processing

Before assessment begins, the selected disruption record is immediately updated.

### Status Update

```text
Pending
    ↓
In Assessment
```

This prevents:

- Multiple trigger cycles processing the same disruption
- Duplicate specialist execution
- Conflicting recommendations
- Data inconsistencies


---

## Step 6: Invoke Supervisor Agent

Once the record is marked **In Assessment**, control passes to the Supply Continuity Supervisor Agent.

### Supervisor Responsibilities Following Invocation

- Execute validation
- Determine scope
- Identify affected SKU
- Identify affected purchase orders
- Identify affected customer orders
- Trigger specialist assessments
- Coordinate workflow execution


---

# Trigger Inputs

The trigger consumes disruption request information from the operational dataset.

## Key Fields

```text
Disruption ID
Supplier ID
SKU
Disruption Type
Reported Date
Expected Recovery Date
Affected PO
Affected Quantity
Severity
Status
```

These values are passed into the validation stage following trigger execution. 【1-5e8f0c】

---

# Trigger Decision Logic

## Decision Rule 1

### Pending Record Exists

```text
If Pending Records Found
    Continue Processing
Else
    Exit Safely
```


---

## Decision Rule 2

### Duplicate Protection

```text
If Status = In Assessment
    Skip Record
Else
    Continue Processing
```


---

## Decision Rule 3

### Single Record Processing

```text
One Trigger Run
        ↓
One Disruption Processed
```

Multiple pending records are intentionally not processed within a single trigger execution cycle. 

---

# State Transition Management

The trigger is responsible for initiating the first valid workflow state transition.

## Initial State Flow

```text
Pending
   ↓
In Assessment
```

Subsequent state transitions are handled by the Supply Continuity Supervisor.

### Valid Downstream States

- Awaiting Approval
- Recovery Plan Proposed
- Customer Action Required
- Management Escalation
- Insufficient Evidence
- Manual Review
- Completed


---

# Error Handling

The trigger layer includes protective handling for startup failures.

## Scenario 1: No Pending Disruptions

### Behavior

```text
No Matching Records
        ↓
Log Result
        ↓
Exit Safely
```

No assessment workflow is started. 【1-5e8f0c】

---

## Scenario 2: Excel Read Failure

### Behavior

```text
Read Failure
      ↓
Record Error
      ↓
Stop Execution
```

The system does not assume data was successfully retrieved. 【1-5e8f0c】

---

## Scenario 3: Status Update Failure

### Behavior

```text
Unable to Mark
"In Assessment"
          ↓
Do Not Continue
          ↓
Stop Processing
```

Processing is blocked to prevent duplicate execution. 【1-5e8f0c】

---

# Integration Points

## Excel Online (Business)

Used for:

- Reading disruption requests
- Updating disruption status
- Maintaining workflow state

### Relevant Table

```text
DisruptionRequestsTable
```



---

## Supply Continuity Supervisor

The trigger's only orchestration responsibility is initiating the Supervisor Agent.

The trigger does not:

- Perform specialist assessments
- Resolve conflicts
- Generate reports
- Send notifications
- Determine recovery strategies

Those responsibilities belong to downstream agents and topics. 【1-5e8f0c】

---

# Non-Functional Requirements

The trigger implementation supports:

### Reliability

- Controlled execution
- Duplicate protection
- Safe failure handling

### Scalability

- Supports recurring autonomous operation
- Decouples trigger logic from assessment logic

### Traceability

- State transition recorded in Excel
- Supervisor invocation auditable

### Data Integrity

- Status updated before assessment begins
- Prevents concurrent processing conflicts


---

# Testing Scenarios

## TC-01: Valid Pending Disruption

**Expected Result**

```text
Pending Record Found
      ↓
Validation Invoked
      ↓
Assessment Continues
```


---

## TC-02: Duplicate In Assessment Record

**Expected Result**

```text
Duplicate Processing Blocked
```


---

## TC-24: No Pending Disruption

**Expected Result**

```text
Safe Exit
Without Errors
```


---

# Summary

The Autonomous Trigger provides the event-driven foundation of the solution by continuously monitoring disruption requests and initiating workflow execution without human intervention. Through recurrence scheduling, pending-record selection, duplicate-processing safeguards, and controlled Supervisor invocation, the trigger establishes a reliable and scalable entry point for the complete multi-agent supply continuity orchestration process. 【1-5e8f0c】