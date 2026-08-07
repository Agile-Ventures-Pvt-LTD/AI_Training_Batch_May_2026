# Custom Topics

## Overview

The Supply Chain Disruption Order Continuity solution implements three reusable custom topics to modularize workflow orchestration within Microsoft Copilot Studio.

Each topic represents a distinct stage of the disruption assessment lifecycle and is invoked by the **Anas_Supply_Chain_Continuity_Governance** Supervisor Agent.

The topics do not independently determine disruption outcomes. Instead, they execute workflow responsibilities before returning control to the Supervisor.

---

# Topic Architecture

```text
                  Supply Chain Supervisor
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
Disruption Intake    Recovery Strategy    Approval &
 & Validation          Resolution      Exception Management
```

---

# Topic 1

## Disruption Intake & Validation

### Purpose

This topic prepares the disruption request for assessment.

It retrieves the oldest pending disruption, validates mandatory information, updates the disruption lifecycle, and prepares the disruption record for specialist assessment.

---

## Trigger Description

Retrieve the oldest pending disruption request, validate mandatory disruption information, update the disruption status to **In Assessment**, and return the disruption record for specialist assessment.

---

## Responsibilities

- Retrieve pending disruption requests.
- Select the oldest pending disruption.
- Retrieve the complete disruption record.
- Validate mandatory fields.
- Update disruption status.
- Return the disruption record.

---

## Tools Used

- /List Disruption Requests
- /Get Disruption Row
- /Update Disruption Status

---

## Validation Rules

Mandatory fields include:

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- SeverityReported

If mandatory information is missing:

- Stop execution.
- Return validation failure.
- Do not invoke specialist agents.

---

## Workflow

```text
Recurrence Trigger
        │
        ▼
List Disruption Requests
        │
        ▼
Pending Request Exists?
        │
 ┌──────┴───────┐
 │              │
No             Yes
 │              │
 ▼              ▼
End      Get Disruption Row
                  │
                  ▼
         Validate Required Fields
                  │
         ┌────────┴─────────┐
         │                  │
      Invalid             Valid
         │                  │
         ▼                  ▼
       End        Update Status
                       │
                       ▼
             Return Disruption Record
```

---

# Topic 2

## Recovery Strategy Resolution

### Purpose

Coordinate specialist assessments and prepare a consolidated recovery recommendation.

The topic delegates assessment work to specialist agents and returns the consolidated recovery recommendation to the Supervisor.

---

## Trigger Description

Coordinate all specialist assessments, consolidate their findings, validate the recommended recovery strategy, and prepare the disruption for approval or reporting.

---

## Responsibilities

- Invoke specialist agents.
- Collect structured assessments.
- Coordinate recovery planning.
- Return consolidated findings.

---

## Child Agents Used

- /Inventory Impact Specialist
- /Alternate Supplier Specialist
- /Customer & Order Impact Specialist
- /Commercial Impact Specialist
- /Recovery Planning Specialist

---

## Workflow

```text
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
Recovery Planning Specialist
        │
        ▼
Return Recommendation
```

---

## Returned Information

The topic returns:

- Inventory Assessment
- Supplier Assessment
- Customer Assessment
- Commercial Assessment
- Recovery Recommendation
- Recovery Risk
- Executive Approval Requirement

The Supervisor validates these findings before continuing.

---

# Topic 3

## Approval & Exception Management

### Purpose

Process executive approvals, policy exceptions, reporting authorization, and disruption lifecycle completion.

This topic executes only after the Recovery Strategy Resolution topic has completed successfully.

---

## Trigger Description

Process executive approvals, handle policy exceptions, perform selective reassessment when required, authorize report generation, notify stakeholders, and update the disruption lifecycle status.

---

## Responsibilities

- Determine whether executive approval is required.
- Handle policy exceptions.
- Perform selective reassessment.
- Authorize reporting.
- Generate stakeholder communication.
- Update disruption lifecycle.

---

## Child Agent Used

- /Reporting & Communication Specialist

---

## Tool Used

- /Update Disruption Status

---

## Decision Logic

### Approval Required

If executive approval is required:

- Continue approval workflow.
- Record approval requirement.
- Continue after approval validation.

---

### Approval Not Required

Proceed directly to reporting.

---

### Manual Review

If the Recovery Planning Specialist recommends Manual Review:

- Update disruption status.
- End workflow.
- Do not generate reports.
- Do not notify stakeholders.

---

## Workflow

```text
Recovery Recommendation
        │
        ▼
Executive Approval Required?
        │
 ┌──────┴────────┐
 │               │
Yes             No
 │               │
 ▼               ▼
Approval      Reporting
Workflow      Specialist
 │               │
 └──────┬────────┘
        ▼
Update Disruption Status
        │
        ▼
Workflow Complete
```

---

# Topic Interaction

The Supervisor invokes the topics in the following sequence.

```text
Recurrence Trigger
        │
        ▼
Topic 1

Disruption Intake & Validation
        │
        ▼
Topic 2

Recovery Strategy Resolution
        │
        ▼
Topic 3

Approval & Exception Management
        │
        ▼
Workflow Complete
```

---

# Topic Design Principles

All custom topics follow the same architectural principles.

### Reusable

Each topic performs a single orchestration responsibility and can be reused within future workflows.

---

### Independent

Topics do not perform specialist analysis.

---

### Supervisor Controlled

Topics always return control to the Supervisor.

---

### Modular

Each topic isolates one stage of the workflow.

---

### Policy Compliant

Topics support policy-driven workflow execution while leaving business decisions to the Supervisor.

---

# Benefits

The custom topic architecture provides:

- Modular orchestration
- Reduced workflow complexity
- Improved maintainability
- Reusable workflow components
- Clear separation of responsibilities
- Simplified debugging
- Improved enterprise scalability

---

# Summary

The three custom topics divide the disruption assessment lifecycle into logical orchestration stages. The first topic validates disruption requests, the second coordinates specialist assessments and recovery planning, and the third manages approvals, reporting, and lifecycle completion. Together they provide a structured, reusable orchestration layer that supports the Supervisor Agent while maintaining separation of concerns and compliance with the project workflow.