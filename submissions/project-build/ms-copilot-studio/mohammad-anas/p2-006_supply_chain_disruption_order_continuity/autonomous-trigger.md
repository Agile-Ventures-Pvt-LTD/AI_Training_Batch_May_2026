# Autonomous Trigger

## Overview

The Supply Chain Disruption Order Continuity solution is initiated through an autonomous **Recurrence Trigger** configured in Microsoft Copilot Studio.

Unlike user-driven conversational agents, this solution operates without manual interaction. The trigger periodically executes the Supply Chain Continuity workflow, retrieves pending disruption requests, and begins the complete assessment lifecycle automatically.

The trigger serves as the entry point for the Supervisor Agent and ensures continuous monitoring of operational disruptions.

---

# Trigger Type

**Recurrence Trigger**

Execution Mode:

Autonomous

Execution Frequency:

Configured within Microsoft Copilot Studio Recurrence Trigger settings.

---

# Purpose

The Recurrence Trigger is responsible for:

- Automatically monitoring disruption requests.
- Starting the Supply Chain Continuity workflow.
- Invoking the Supervisor Agent.
- Processing one pending disruption request per execution.
- Preventing unnecessary executions when no pending disruptions exist.

---

# Trigger Description

The trigger invokes the following workflow:

> You are being invoked by the Recurrence Trigger to start the **Anas_Supply_Chain_Continuity_Governance** workflow.
>
> Retrieve the oldest supply chain disruption request that is currently in the **Pending** status.
>
> If no pending disruption request exists, terminate the execution without performing any additional actions.
>
> If a pending disruption request exists, retrieve its complete details and initiate the Supply Chain Continuity Assessment according to the configured workflow.
>
> Invoke **/Disruption Intake & Validation** to validate the disruption information and prepare it for specialist assessment.
>
> After successful validation, continue the workflow by invoking **/Recovery Strategy Resolution** to coordinate specialist assessments and determine the recommended recovery strategy.
>
> If executive approval, policy exceptions, or selective reassessment are required, invoke **/Approval & Exception Management** before authorizing reporting.
>
> Generate the Supply Chain Continuity Assessment Report, update the disruption lifecycle status, and notify stakeholders only after the Supervisor validates the final disruption outcome.
>
> Process only one pending disruption request during each execution.

---

# Trigger Workflow

```text
Recurrence Trigger
        │
        ▼
Supply Chain Supervisor
        │
        ▼
Retrieve Pending Disruption
        │
        ▼
Pending Exists?
        │
 ┌──────┴───────┐
 │              │
No             Yes
 │              │
 ▼              ▼
End       Disruption Intake &
          Validation
                  │
                  ▼
     Recovery Strategy Resolution
                  │
                  ▼
 Approval & Exception Management
                  │
                  ▼
 Reporting & Communication
                  │
                  ▼
 Update Disruption Status
                  │
                  ▼
 Workflow Complete
```

---

# Trigger Responsibilities

The trigger performs the following responsibilities.

### Automatic Execution

Starts the workflow according to the configured schedule without requiring user interaction.

---

### Workflow Initialization

Invokes the Supervisor Agent responsible for orchestration.

---

### Pending Request Detection

Ensures that only disruption requests with **Status = Pending** are processed.

---

### Single Record Processing

Processes only the oldest pending disruption request during each execution.

This prevents duplicate assessments and simplifies lifecycle tracking.

---

### Safe Termination

If no pending disruption exists, the workflow exits safely without invoking specialist agents or modifying operational data.

---

# Interaction with the Supervisor

After execution begins, the trigger transfers control to:

**Anas_Supply_Chain_Continuity_Governance**

The Supervisor becomes responsible for:

- Workflow orchestration
- Topic execution
- Specialist coordination
- Recovery validation
- Approval handling
- Reporting authorization
- Lifecycle management

The trigger performs no business analysis.

---

# Interaction with Custom Topics

The trigger indirectly initiates all custom topics through the Supervisor.

Execution sequence:

```text
Recurrence Trigger

↓

Supervisor

↓

/Disruption Intake & Validation

↓

/Recovery Strategy Resolution

↓

/Approval & Exception Management
```

---

# Trigger Constraints

The trigger follows several operational constraints.

- Executes autonomously.
- Processes one disruption per execution.
- Never skips validation.
- Never performs specialist analysis.
- Never updates disruption data directly.
- Never generates reports.
- Never communicates with stakeholders.

These responsibilities remain with the Supervisor Agent.

---

# Error Handling

The trigger safely terminates under the following conditions.

## No Pending Disruptions

Result

Workflow exits successfully.

---

## Invalid Disruption Record

Result

Supervisor terminates workflow after validation.

---

## Workflow Failure

Result

Supervisor records failure and returns appropriate workflow status.

---

# Design Principles

The trigger implementation follows these enterprise principles.

## Autonomous Execution

No manual intervention required.

---

## Lightweight Initialization

Only starts workflow execution.

Business logic remains inside the Supervisor.

---

## Controlled Processing

Processes only one disruption request per execution.

---

## Separation of Concerns

The trigger initializes execution.

The Supervisor performs orchestration.

Specialists perform business analysis.

---

# Benefits

The autonomous trigger provides:

- Continuous monitoring
- Automatic workflow initiation
- Consistent disruption processing
- Reduced manual intervention
- Improved operational responsiveness
- Controlled workload execution
- Enterprise-ready automation

---

# Summary

The Recurrence Trigger serves as the autonomous entry point for the Supply Chain Disruption Order Continuity solution. It continuously monitors pending disruption requests and initiates the Supervisor-controlled workflow while ensuring that only one disruption request is processed during each execution. By separating workflow initialization from business orchestration, the trigger supports a scalable, reliable, and policy-driven automation architecture within Microsoft Copilot Studio.