# Custom Topics

## Overview

The solution uses three custom topics to enforce deterministic business logic, validation controls, approval governance, conflict resolution, and reassessment management. These topics work alongside the Supervisor Agent and specialist child agents to ensure that recommendations are based on validated data and approved business rules rather than generative reasoning alone. 【1-cfe43d】

---

# Topic 1: Disruption Intake & Validation

## Purpose

The Disruption Intake & Validation topic performs all mandatory validation checks before specialist agents are invoked. This topic serves as the gateway into the assessment workflow and prevents invalid or incomplete disruption records from entering the orchestration process. 【1-cfe43d】

---

## Trigger Point

```text
Recurrence Trigger
        ↓
Supervisor Agent
        ↓
Disruption Intake & Validation Topic
```

This topic executes immediately after the Supervisor selects a pending disruption record. 

---

## Inputs

The topic receives disruption information from the selected record.

### Required Variables

```text
DisruptionID
SupplierID
SKU
DisruptionType
ReportedDate
ExpectedRecoveryDate
AffectedPO
AffectedQty
ReportedSeverity
ValidationStatus
DuplicateDetected
```


---

## Validation Rules

The topic validates the following conditions:

### Record Validation

- Disruption ID exists
- Disruption ID is unique
- Status equals Pending

### Supplier Validation

- Supplier ID exists
- Supplier exists in Suppliers Table

### SKU Validation

- SKU exists
- SKU exists in SKU Master

### Purchase Order Validation

- Purchase Order exists
- Purchase Order references the same supplier
- Purchase Order references the same SKU

### Quantity Validation

- Affected quantity is greater than zero

### Date Validation

- Reported Date exists
- Reported Date is valid

### Business Data Validation

- Disruption Type exists
- Mandatory fields are populated


---

## Processing Flow

```text
Receive Disruption
        ↓
Validate Required Fields
        ↓
Validate Supplier
        ↓
Validate SKU
        ↓
Validate PO Relationship
        ↓
Validate Quantity & Dates
        ↓
Validation Passed?
      ┌─────┴─────┐
      │           │
     No          Yes
      │           │
      ▼           ▼
Insufficient   Continue
Evidence       Assessment
```


---

## Failure Handling

If validation fails:

- Specialist agents are not invoked.
- Validation reason is recorded.
- Record is routed to:
  - Insufficient Evidence, or
  - Manual Review

The topic never fabricates missing values. 【1-cfe43d】

---

## Outputs

### Successful Validation

```text
ValidationStatus = Pass
DuplicateDetected = No
AssessmentEligible = Yes
```

### Failed Validation

```text
ValidationStatus = Fail
AssessmentEligible = No
FailureReason Recorded
```


---

# Topic 2: Recovery Strategy Resolution

## Purpose

The Recovery Strategy Resolution topic consolidates specialist outputs and resolves conflicts using deterministic policy rules. This topic is responsible for selecting the most appropriate recovery path while ensuring business constraints and approval requirements are respected. 【1-cfe43d】

---

## Trigger Point

```text
Specialist Fan-In Complete
          ↓
Recovery Strategy Resolution Topic
```

The topic executes only after all required specialist assessments are available. 【1-cfe43d】

---

## Inputs

The topic receives consolidated specialist outputs.

### Inventory Assessment

- ATP
- Inventory Risk
- Shortage Quantity

### Alternate Supplier Assessment

- Alternate Availability
- Supplier Approval Status
- Lead Time
- Capacity

### Customer Impact Assessment

- Strategic Orders at Risk
- SLA Orders at Risk
- Revenue Exposure
- Fulfillment Requirements

### Commercial Assessment

- Cost Premium
- Incremental Cost
- Approval Requirements

### Additional Inputs

- Recovery Rules
- Supply Continuity Policy


---

## Decision Precedence

When specialist recommendations conflict, the following order is enforced.

```text
1. Safety & Quality Restrictions
2. Strategic/SLA Customer Commitments
3. Supplier Approval Restrictions
4. Inventory Availability & Timing
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience
```

Conflicting recommendations are never averaged. 【1-cfe43d】

---

# Mandatory Decision Branches

## Branch A: Inventory Sufficient

### Condition

```text
ATP protects all demand
until supplier recovery
```

### Action

- Use existing inventory
- Avoid unnecessary premium sourcing
- Determine safety stock consumption

### Outcome

```text
Resolved With Existing Supply
```


---

## Branch B: Partial Inventory Coverage

### Condition

```text
ATP covers only part
of required demand
```

### Action

- Rank customer orders
- Protect priority demand
- Evaluate alternate sources
- Check partial fulfillment permissions

### Outcome

```text
Combined Recovery Strategy
```


---

## Branch C: Approved Alternate Available

### Condition

```text
Approved Supplier Available
AND
Can Meet Demand
```

### Action

- Calculate commercial impact
- Determine approval requirements
- Create sourcing recommendation

### Outcome

```text
Recovery Plan Proposed
```


---

## Branch D: Unapproved Alternate Only

### Condition

```text
Supplier Approved = No
```

### Action

- Block autonomous selection
- Route to manual qualification workflow

### Outcome

```text
Manual Review
or
Management Escalation
```


---

## Branch E: No Recovery Route

### Condition

```text
No Inventory
No Approved Supplier
No Viable Alternative
```

### Action

- Escalate immediately
- Classify risk accordingly

### Outcome

```text
Management Escalation
```


---

## Outputs

### Strategy Outputs

```text
ProposedStrategy
StrategyComponents
OrdersProtected
OrdersRemainingAtRisk
RequiredApprovals
ResidualRisk
RequiredCustomerAction
RequiredInternalActions
Rationale
Confidence
```

These outputs are passed to the Supervisor Agent for final validation. 【1-cfe43d】

---

# Topic 3: Approval, Exception & Selective Reassessment

## Purpose

This topic manages approvals, exceptions, reassessment cycles, retries, and escalation decisions. It ensures the solution respects human approval boundaries and supports controlled reassessment when underlying data changes. 【1-cfe43d】

---

## Trigger Point

```text
Recovery Strategy Resolution
              ↓
Approval, Exception &
Selective Reassessment Topic
```


---

# Approval Evaluation

The topic evaluates conditions requiring human approval.

## Approval Conditions

### Commercial Approval

```text
Cost Premium > 15%
```

### Executive Approval

```text
Expedite Premium > 10%
```

### Strategic Inventory Usage

```text
Strategic SLA Orders
Require Safety Stock
Consumption
```

### Supplier Governance

```text
No Approved Alternate Supplier
```

### Fulfillment Restrictions

```text
Partial Fulfillment Not Allowed
```

### Critical Demand Protection Risk

```text
No Strategy Protects
Critical Demand
```


---

# Approval Workflow

```text
Approval Required?
      ┌─────┴─────┐
      │           │
     No          Yes
      │           │
      ▼           ▼
 Continue     Awaiting
 Workflow     Approval
                  │
                  ▼
       Record Approval Reason
                  │
                  ▼
      Wait for Approval Update
```


---

## Human Approval Rules

The system must:

- Determine required approver
- Record approval reason
- Set status to Awaiting Approval
- Wait for approval decision
- Resume only after approval data changes

The system must not:

- Invent approvals
- Bypass approval workflows
- Auto-approve requests


---

# Selective Reassessment

## Purpose

Reassessment prevents unnecessary execution when only part of the disruption context changes.

Instead of rerunning the full workflow, only impacted specialists are reinvoked. 【1-cfe43d】

---

## Reassessment Logic

```text
Data Change Detected
          ↓
Identify Stale Findings
          ↓
Determine Impacted Specialists
          ↓
Re-run Impacted Specialists
          ↓
Fan-In Updated Results
          ↓
Recalculate Strategy
```


---

## Example 1

### Alternate Supplier Capacity Changes

Re-run:

```text
Alternate Supplier Specialist
Commercial Impact Specialist
```

Do Not Re-run:

```text
Inventory Specialist
Customer Impact Specialist
```

Unless their data also changed. 【1-cfe43d】

---

## Example 2

### Inventory Availability Changes

Re-run:

```text
Inventory Specialist
Customer Impact Specialist
```

Continue with fan-in and strategy recalculation. 【1-cfe43d】

---

# Retry and Fallback Management

## Retry Logic

If a specialist does not return a usable response:

```text
Attempt 1
    ↓
Failure
    ↓
Retry Once
    ↓
Success → Continue
```


---

## Escalation Logic

If both attempts fail:

```text
Attempt 1 Failed
        ↓
Attempt 2 Failed
        ↓
Insufficient Evidence
        ↓
Manual Review
```

Recommendations requiring unsupported evidence are blocked. 【1-cfe43d】

---

## Reassessment Limit

Maximum automated reassessment cycles:

```text
2
```

After two unresolved reassessment cycles:

```text
Manual Review
```

is automatically assigned. 【1-cfe43d】

---

# Topic Interaction Flow

```text
Disruption Intake & Validation
              ↓
      Specialist Assessments
              ↓
         Fan-In Stage
              ↓
 Recovery Strategy Resolution
              ↓
 Approval, Exception &
 Selective Reassessment
              ↓
     Supervisor Validation
              ↓
 Reporting & Communication
```


---

# Summary

The custom topics act as the deterministic control framework for the solution. The Disruption Intake & Validation topic guarantees data quality before processing begins, the Recovery Strategy Resolution topic resolves conflicts and determines recovery actions using policy-driven decision logic, and the Approval, Exception & Selective Reassessment topic enforces governance, approval controls, retry behavior, and reassessment workflows. Together, these topics ensure that all recommendations remain traceable, explainable, policy-compliant, and aligned with operational constraints. 【1-cfe43d】