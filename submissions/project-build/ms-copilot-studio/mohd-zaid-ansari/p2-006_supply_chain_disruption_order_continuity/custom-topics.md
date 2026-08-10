# Custom Topics Design

## Overview

The solution uses three mandatory custom topics in Microsoft Copilot Studio to control validation, recovery decisions, approvals, and reassessment.

These topics provide deterministic business logic while the Supervisor Agent manages overall orchestration.

---

# 1. Disruption Intake & Validation Topic

## Purpose

Validate disruption requests before specialist agents are executed.

## Trigger

Called by:

**Mohd Zaid Supply Continuity Supervisor**

after the recurrence trigger identifies a pending disruption.

---

## Responsibilities

Validates:

* Disruption ID exists
* Duplicate processing check
* Status is Pending
* Supplier exists
* SKU exists
* Disruption type exists
* Report date is valid
* Purchase order exists
* PO matches supplier and SKU
* Affected quantity is valid

---

## Inputs

* DisruptionID
* SupplierID
* SKU
* DisruptionType
* ReportedDate
* ExpectedRecoveryDate
* AffectedPO
* AffectedQty
* Severity

---

## Outputs

* ValidationStatus
* DuplicateDetected
* ValidationReason

---

## Routing

### Valid Record

```
Pending
   ↓
In Assessment
   ↓
Specialist Analysis
```

### Invalid Record

```
Validation Failed
        ↓
Manual Review / Insufficient Evidence
```

Specialists are not called when validation fails.

---

# 2. Recovery Strategy Resolution Topic

## Purpose

Resolve competing specialist recommendations and select the appropriate recovery path.

---

## Inputs

Receives:

* Inventory assessment
* Alternate supplier assessment
* Customer impact assessment
* Commercial impact assessment
* Recovery rules

---

## Decision Precedence

Conflicts are resolved using:

1. Safety and quality restrictions
2. Strategic/SLA customer commitments
3. Supplier approval restrictions
4. Inventory availability and timing
5. Commercial approval requirements
6. Cost optimization
7. Lower priority convenience

---

# Decision Branches

## Branch A — Inventory Sufficient

Condition:

ATP protects demand until recovery.

Action:

* Prefer existing supply
* Avoid unnecessary premium sourcing
* Check safety stock impact

---

## Branch B — Partial Inventory

Condition:

ATP covers only part of demand.

Action:

* Rank customer orders
* Protect priority customers
* Evaluate alternate supply
* Check fulfilment rules

---

## Branch C — Approved Alternate Available

Condition:

Approved supplier can meet demand.

Action:

* Evaluate cost impact
* Check approvals
* Recommend alternate supply if valid

---

## Branch D — Unapproved Alternate Only

Action:

* Do not select supplier automatically
* Route for supplier qualification/manual review

---

## Branch E — No Recovery Option

Action:

* Set Critical risk where required
* Escalate to management

---

## Output

* SelectedStrategy
* RiskClassification
* ApprovalRequired
* RequiredApprover
* FinalRecommendation

---

# 3. Approval, Exception & Selective Reassessment Topic

## Purpose

Control approval routing, failure handling, and selective reassessment.

---

# Approval Conditions

Requires approval when:

* Alternate supplier premium >15%
* Expedite premium >10%
* Strategic SLA order requires safety stock usage
* No approved alternate supplier exists
* Partial fulfilment is not allowed
* Critical demand cannot be protected

---

# Approval Workflow

```
Decision Requires Approval
            |
            ▼
Set Status = Awaiting Approval
            |
            ▼
Record Approval Reason
            |
            ▼
Wait For Approval State Change
```

The system never fabricates human approval.

---

# Selective Reassessment

When data changes:

1. Identify stale specialist results.
2. Re-run only impacted specialists.
3. Preserve valid previous findings.
4. Perform fan-in consolidation again.
5. Recalculate strategy.

---

## Example

If alternate supplier capacity changes:

Re-run:

* Alternate Supplier Specialist
* Commercial Impact Specialist

Do not rerun unaffected inventory/customer analysis.

---

# Reassessment Limit

Maximum automated reassessment cycles:

**2**

After limit reached:

```
Manual Review
```

---

# Error Handling

Topics handle:

* Missing disruption data
* Duplicate disruptions
* Invalid PO relationships
* Missing approvals
* Specialist failures
* Conflicting recommendations
* No recovery route

---

# Topic Design Principles

* Deterministic business rules override AI judgement.
* Validation occurs before analysis.
* Supervisor controls topic execution.
* Approval boundaries are enforced.
* Unsupported decisions are prevented.
* All outcomes are traceable.

These topics provide the governance layer required for autonomous supply disruption response.
