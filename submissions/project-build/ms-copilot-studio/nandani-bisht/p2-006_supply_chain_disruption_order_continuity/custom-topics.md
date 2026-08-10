# custom-topics.md

# Custom Topics Design

## P2-006 – Supply Chain Disruption Order Continuity

---

# Overview

The solution uses three custom topics to organize the autonomous workflow within Microsoft Copilot Studio. Each topic has a well-defined responsibility and ensures that the disruption management process remains modular, maintainable, and easy to extend.

The topics work together with the Supervisor Agent and specialist child agents to execute the complete disruption lifecycle.

---

# Topic Architecture

```text
Disruption Request
        │
        ▼
Topic 1
Disruption Intake & Validation
        │
        ▼
Recovery Planning Specialist
        │
        ▼
Topic 2
Recovery Strategy Resolution
        │
        ▼
Topic 3
Approval, Exception & Selective Reassessment
        │
        ▼
Reporting & Communication Specialist
```

---

# Topic 1 – Disruption Intake & Validation

## Purpose

This topic validates incoming disruption requests before any business assessment begins.

---

## Responsibilities

- Validate disruption request
- Verify mandatory information
- Prevent duplicate processing
- Validate Supplier ID
- Validate SKU
- Validate Purchase Order
- Confirm request status is Pending

---

## Inputs

- Disruption ID
- Supplier ID
- SKU
- Purchase Order
- Status
- Expected Recovery Date

---

## Outputs

- Validation Status
- Duplicate Detected
- Validation Reason
- Supplier ID
- SKU
- Purchase Order

---

## Variables

- DisruptionID
- SupplierID
- SKU
- PurchaseOrder
- ValidationStatus
- DuplicateDetected
- ValidationReason

---

## Workflow

```text
Start
   │
   ▼
Validate Disruption
   │
   ▼
Status = Pending?
   │
 ┌─┴─────────┐
 │           │
Yes         No
 │           │
 ▼           ▼
Validation  Validation
Passed      Failed
```

---

## Connected Agent

Recovery Planning Specialist

---

## Success Path

Validation Passed

↓

Continue to Recovery Planning

---

## Failure Path

Validation Failed

↓

End Workflow

---

# Topic 2 – Recovery Strategy Resolution

## Purpose

Determine the best recovery strategy using specialist recommendations.

---

## Responsibilities

- Receive specialist outputs
- Consolidate recommendations
- Apply business rules
- Resolve conflicts
- Recommend recovery strategy

---

## Inputs

- Inventory Assessment
- Supplier Assessment
- Customer Assessment
- Commercial Assessment

---

## Outputs

- Proposed Strategy
- Strategy Components
- Required Approvals
- Residual Risk
- Recommended Actions

---

## Decision Flow

```text
Receive Assessments
        │
        ▼
Inventory Available?
        │
 ┌──────┴──────┐
 │             │
Yes            No
 │             │
 ▼             ▼
Use Stock   Check Alternate
                 │
                 ▼
         Approved Supplier?
                 │
        ┌────────┴────────┐
        │                 │
       Yes               No
        │                 │
        ▼                 ▼
Recommend          Management
Supplier           Escalation
```

---

## Business Rules

- Prefer existing inventory
- Use only approved suppliers
- Protect strategic customers
- Respect commercial approval rules
- Escalate when no recovery exists

---

## Connected Topic

Approval, Exception & Selective Reassessment

---

# Topic 3 – Approval, Exception & Selective Reassessment

## Purpose

Handle approvals, reassessment, workflow exceptions, and final completion.

---

## Responsibilities

- Route approvals
- Retry failed assessments
- Handle reassessment
- Escalate unresolved cases
- Complete workflow

---

## Inputs

- Recovery Strategy
- Required Approval
- Specialist Results

---

## Outputs

- Final Status
- Approval Status
- Escalation Status
- Workflow Status

---

## Workflow

```text
Approval Required?
        │
 ┌──────┴───────┐
 │              │
Yes             No
 │              │
 ▼              ▼
Route        Complete
Approval
 │
 ▼
Approved?
 │
 ┌──────┴───────┐
 │              │
Yes             No
 │              │
 ▼              ▼
Reporting   Reassessment
```

---

## Connected Agent

Reporting & Communication Specialist

---

## Failure Handling

If a specialist fails:

- Retry once
- Retry twice
- Return "Insufficient Evidence"
- Manual Review
- Management Escalation

---

# Topic Communication

```text
Topic 1
      │
      ▼
Recovery Planning Specialist
      │
      ▼
Topic 2
      │
      ▼
Topic 3
      │
      ▼
Reporting Specialist
```

---

# Topic Integration

| Topic | Connected Components |
|--------|----------------------|
| Topic 1 | Recovery Planning Specialist |
| Topic 2 | Recovery Strategy Resolution |
| Topic 3 | Reporting & Communication Specialist |

---

# Best Practices

The custom topics follow these design principles:

- Single responsibility
- Modular workflow
- Clear decision boundaries
- Reusable logic
- Controlled routing
- Enterprise governance
- Explainable AI decisions

---

# Benefits

Using custom topics provides:

- Better workflow organization
- Easier maintenance
- Improved scalability
- Simplified debugging
- Better orchestration
- Reusable business logic

---

# Summary

The three custom topics form the backbone of the Supply Chain Disruption Order Continuity solution.

Each topic performs a dedicated function while collaborating with the Supervisor Agent and specialist child agents to deliver an autonomous, enterprise-grade disruption management workflow.

---

# Version

Version: **1.0**

Status: **Completed**