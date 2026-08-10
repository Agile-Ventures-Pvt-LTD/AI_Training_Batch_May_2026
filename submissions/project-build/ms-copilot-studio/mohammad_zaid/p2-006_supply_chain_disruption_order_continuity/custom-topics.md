
# Custom Topics Design

# Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System uses three deterministic custom topics to orchestrate the disruption assessment lifecycle. These topics divide the workflow into logical execution stages, ensuring predictable behaviour, deterministic business rule enforcement, and clear separation of responsibilities.

Each topic is executed by the **Supply Continuity Supervisor** and controls a specific phase of the orchestration lifecycle.

---

# Topic Architecture

```
                Supply Continuity Supervisor
                           │
                           ▼
        ┌────────────────────────────────────┐
        │ Disruption Intake & Validation     │
        └────────────────────────────────────┘
                           │
                           ▼
              Inventory Impact Specialist
                           │
                           ▼
          Alternate Supplier Specialist
                           │
                           ▼
        Customer & Order Impact Specialist
                           │
                           ▼
            Commercial Impact Specialist
                           │
                           ▼
        ┌────────────────────────────────────┐
        │ Recovery Strategy Resolution       │
        └────────────────────────────────────┘
                           │
                           ▼
            Recovery Planning Specialist
                           │
                           ▼
        ┌────────────────────────────────────┐
        │ Approval, Exception &             │
        │ Selective Reassessment            │
        └────────────────────────────────────┘
                           │
                           ▼
     Reporting & Communication Specialist
```

---

# Topic 1 — Disruption Intake & Validation

## Purpose

Validate the incoming disruption request before any specialist assessment begins.

This topic ensures only valid disruption requests proceed to the orchestration workflow.

---

## Trigger

Invoked automatically by the Supply Continuity Supervisor after the Recurrence Trigger identifies the oldest pending disruption.

---

## Workflow

```
Start
   │
   ▼
SUP - Get Pending Disruptions
   │
   ▼
Select Oldest Pending Record
   │
   ▼
Validate Mandatory Fields
   │
   ▼
All Fields Valid?
   │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
Status =   Status =
Insufficient  In Assessment
Evidence
 │         │
 ▼         ▼
End       Return Validated Context
```

---

## Validation Rules

The topic validates:

- Disruption ID
- Pending Status
- Supplier ID
- SKU
- Disruption Type
- Reported Date
- Affected Purchase Order
- Affected Quantity

---

## Variables

### Inputs

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- ReportedSeverity

### Outputs

- ValidationStatus
- CurrentDisruption
- WorkflowStatus

---

## Success Result

Returns a validated disruption to the Supervisor for specialist assessment.

---

## Failure Result

Updates the disruption state to **Insufficient Evidence** and terminates the workflow.

---

# Topic 2 — Recovery Strategy Resolution

## Purpose

Coordinate specialist assessments, consolidate domain findings, and determine the recommended recovery strategy.

---

## Trigger

Invoked after successful completion of the Disruption Intake & Validation topic and execution of the four specialist agents.

---

## Workflow

```
Start
   │
   ▼
Receive Specialist Outputs
   │
   ▼
Inventory Assessment
   │
   ▼
Alternate Supplier Assessment
   │
   ▼
Customer Impact Assessment
   │
   ▼
Commercial Assessment
   │
   ▼
Invoke Recovery Planning Specialist
   │
   ▼
Recovery Strategy Available?
   │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
No Viable  Return Recovery
Recovery   Recommendation
 │
 ▼
End
```

---

## Inputs

- InventoryAssessment
- SupplierAssessment
- CustomerAssessment
- CommercialAssessment

---

## Outputs

- RecoveryStrategy
- FinalRisk
- ResidualRisk
- ApprovalRequired
- RecoveryConfidence

---

## Decision Rules

The topic determines:

- Whether inventory alone is sufficient
- Whether alternate sourcing is required
- Whether customer commitments are protected
- Whether commercial approval is necessary
- Whether a viable recovery strategy exists

---

## Failure Handling

If no recovery strategy is available:

- Workflow status is set to **No Viable Recovery**
- Control returns to the Supervisor

---

# Topic 3 — Approval, Exception & Selective Reassessment

## Purpose

Evaluate approval requirements, manage workflow exceptions, and determine whether selective reassessment or escalation is required before final workflow completion.

---

## Trigger

Invoked after the Recovery Strategy Resolution topic returns a recommended recovery strategy.

---

## Workflow

```
Start
   │
   ▼
Receive Recovery Strategy
   │
   ▼
Approval Required?
   │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
Approved  Awaiting Approval
 │         │
 │     Approval Received?
 │         │
 │   ┌─────┴─────┐
 │   │           │
 │  Yes         No
 │   │           │
 │   ▼           ▼
 │ Approved   Reassessment?
 │               │
 │        ┌──────┴──────┐
 │        │             │
 │       No            Yes
 │        │             │
 │        ▼             ▼
 │ Manual Review   Reassessment Count < 2?
 │                      │
 │               ┌──────┴──────┐
 │               │             │
 │              Yes           No
 │               │             │
 ▼               ▼             ▼
End        Reassessment   Escalation
```

---

## Inputs

- RecoveryStrategy
- FinalRisk
- ResidualRisk
- ApprovalRequired
- RecoveryConfidence

---

## Outputs

- WorkflowStatus
- ApprovalStatus
- ReassessmentRequired
- EscalationRequired

---

## Approval Conditions

The topic evaluates:

- Commercial approval thresholds
- Recovery strategy risk
- Alternate supplier approval
- Customer priority
- Recovery feasibility

---

## Reassessment Logic

When reassessment is required:

- Re-run only affected specialist assessments.
- Preserve valid specialist outputs.
- Return control to the Supervisor.

Maximum reassessment attempts:

**2**

---

## Escalation Conditions

Escalation occurs when:

- No viable recovery exists.
- Approval cannot be obtained.
- Maximum reassessment limit is exceeded.
- Critical business constraints cannot be satisfied.

---

# Topic Variables Summary

| Topic                                        | Inputs             | Outputs                                            |
| -------------------------------------------- | ------------------ | -------------------------------------------------- |
| Disruption Intake & Validation               | Disruption Details | ValidationStatus, WorkflowStatus                   |
| Recovery Strategy Resolution                 | Specialist Outputs | RecoveryStrategy, FinalRisk, ApprovalRequired      |
| Approval, Exception & Selective Reassessment | Recovery Outputs   | WorkflowStatus, ApprovalStatus, EscalationRequired |

---

# Topic Execution Order

```
Recurrence Trigger
        │
        ▼
Disruption Intake & Validation
        │
        ▼
Supervisor
        │
        ▼
Inventory Specialist
        │
        ▼
Alternate Supplier Specialist
        │
        ▼
Customer Impact Specialist
        │
        ▼
Commercial Impact Specialist
        │
        ▼
Recovery Strategy Resolution
        │
        ▼
Recovery Planning Specialist
        │
        ▼
Approval, Exception &
Selective Reassessment
        │
        ▼
Supervisor Validation
        │
        ▼
Reporting & Communication
        │
        ▼
Workflow Completed
```

---

# Design Principles

The custom topics are designed according to the following principles:

- Deterministic execution
- Single responsibility per topic
- Clear separation of orchestration phases
- Supervisor-controlled workflow
- Policy-driven business decisions
- Explicit state transitions
- Structured inputs and outputs
- Modular and reusable orchestration

---

# Summary

The solution implements three deterministic custom topics that divide the disruption lifecycle into validation, recovery planning, and approval phases. Each topic has a clearly defined responsibility, structured variables, deterministic decision logic, and controlled handoff to the next orchestration stage, enabling a maintainable and enterprise-grade Microsoft Copilot Studio implementation.
