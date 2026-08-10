
# Autonomous Trigger Design

# Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System is initiated through a Microsoft Copilot Studio **Recurrence Event Trigger**. This trigger enables the solution to operate autonomously without requiring a conversational user prompt.

At every scheduled execution, the trigger monitors the disruption register, identifies new disruption requests awaiting assessment, and initiates the complete multi-agent orchestration workflow.

---

# Trigger Information

| Property            | Value                        |
| ------------------- | ---------------------------- |
| Trigger Name        | Supply Disruption Monitoring |
| Trigger Type        | Recurrence Event Trigger     |
| Platform            | Microsoft Copilot Studio     |
| Execution Mode      | Autonomous                   |
| Invocation          | Scheduled                    |
| Orchestration Owner | Supply Continuity Supervisor |

---

# Business Objective

The recurrence trigger eliminates the need for manual workflow initiation by continuously monitoring operational disruption records.

Its primary objectives are:

- Detect new disruption requests automatically
- Identify pending disruption records
- Start orchestration without user intervention
- Prevent duplicate processing
- Process disruptions in chronological order

---

# Trigger Workflow

```
Recurrence Trigger
        │
        ▼
Read DisruptionRequestsTable
        │
        ▼
Pending Record Available?
        │
   ┌────┴─────┐
   │          │
 No          Yes
   │          │
   ▼          ▼
 End     Select Oldest Pending
              │
              ▼
      Invoke Supervisor
              │
              ▼
 Disruption Intake & Validation
```

---

# Trigger Configuration

## Trigger Type

```
Recurrence
```

---

## Execution Frequency

For demonstration purposes:

```
Every 5 Minutes
```

For production deployments:

```
Configurable according to business requirements
```

---

# Trigger Responsibilities

At every execution cycle the trigger performs the following activities:

1. Connect to Microsoft Excel Online (Business).
2. Read the Disruption Requests table.
3. Search for records where Status is Pending.
4. Select the oldest pending disruption.
5. Process only one disruption during the current execution.
6. Invoke the Supply Continuity Supervisor.
7. Allow the Supervisor to continue orchestration.
8. Complete the execution cycle.

---

# Trigger Instructions

The recurrence trigger follows these execution instructions:

```
You are responsible for autonomously monitoring the disruption register.

At each scheduled execution:

1. Retrieve all disruption requests.
2. Identify records with Status = Pending.
3. If no pending disruptions exist, terminate the execution.
4. If pending disruptions exist, select the oldest pending record.
5. Process only one disruption during each execution cycle.
6. Invoke the Supply Continuity Supervisor.
7. Do not process completed, cancelled, or closed disruptions.
8. Do not modify disruption data directly.
9. Allow the Supervisor to manage all workflow state transitions.
10. Record execution outcome for monitoring and auditing purposes.
```

---

# Trigger Inputs

The trigger retrieves information from:

- DisruptionRequestsTable

Primary fields include:

- DisruptionID
- SupplierID
- SKU
- Status
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- ReportedSeverity

---

# Trigger Outputs

The trigger provides the Supervisor with:

- Current Disruption Record
- Disruption Context
- Execution Timestamp
- Workflow Initiation Request

---

# Decision Logic

```
Pending Records?

      │
 ┌────┴─────┐
 │          │
No         Yes
 │          │
 ▼          ▼
End     Select Oldest Record
              │
              ▼
Invoke Supervisor
```

---

# Processing Rules

The trigger follows these business rules:

- Process only one disruption per execution.
- Ignore disruptions already under assessment.
- Ignore completed disruptions.
- Never process duplicate disruptions.
- Always process the oldest pending disruption first.
- Never bypass the Supervisor.

---

# Integration

The trigger integrates with:

## Microsoft Copilot Studio

Provides scheduled autonomous execution.

---

## Excel Online (Business)

Reads operational disruption data.

---

## Supply Continuity Supervisor

Starts the orchestration lifecycle.

---

# Error Handling

The trigger safely handles the following conditions:

## No Pending Disruptions

Action:

- End execution without invoking the Supervisor.

---

## Excel Connection Failure

Action:

- Record the failure.
- Stop execution.
- Retry during the next scheduled recurrence.

---

## Missing Workbook

Action:

- Abort execution.
- Prevent invalid orchestration.

---

## Invalid Dataset

Action:

- Log the issue.
- Skip execution.

---

# Security

The trigger follows these safety principles:

- Read-only access to identify pending disruptions.
- No direct modification of operational data.
- All workflow updates are delegated to the Supervisor.
- Only authenticated Microsoft 365 connectors are used.

---

# Benefits

The autonomous trigger provides:

- Fully automated workflow initiation
- Continuous disruption monitoring
- Reduced manual effort
- Consistent execution
- Controlled processing
- Improved operational responsiveness

---

# End-to-End Trigger Lifecycle

```
Recurrence Schedule
        │
        ▼
Read Excel
        │
        ▼
Identify Pending Disruption
        │
        ▼
Select Oldest Record
        │
        ▼
Invoke Supervisor
        │
        ▼
Execute Custom Topics
        │
        ▼
Complete Orchestration
```

---

# Summary

The Autonomous Recurrence Trigger enables continuous monitoring of supply disruption requests and automatically initiates the multi-agent orchestration workflow. By selecting the oldest pending disruption and delegating execution to the Supply Continuity Supervisor, it ensures deterministic, repeatable, and policy-compliant processing without requiring manual user interaction.
