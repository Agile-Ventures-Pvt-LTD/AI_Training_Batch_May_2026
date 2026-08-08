# Custom Topics

## Purpose

Custom Topics implement deterministic business governance within Microsoft Copilot Studio.

These topics act as workflow control components that enforce validation, recovery strategy selection, approval routing, escalation handling, and reassessment limits.

The topics are invoked by the Supply Continuity Supervisor during workflow execution.

---

# Topic Overview

| Topic | Purpose |
|---------|---------|
| Disruption Intake & Validation | Validate disruption requests before assessment begins |
| Recovery Strategy Resolution | Select the appropriate recovery path based on specialist findings |
| Approval, Exception & Selective Reassessment | Govern approval routing, reassessment limits, and manual review decisions |

---

# Disruption Intake & Validation

## Purpose

Provides deterministic validation before specialist assessment execution.

The topic validates disruption request completeness and basic business rules.

---

## Inputs

| Input | Type |
|---------|---------|
| DisruptionID | String |
| SupplierID | String |
| SKU | String |
| DisruptionType | String |
| ReportedDate | Date |
| ExpectedRecoveryDate | Date |
| AffectedPO | String |
| AffectedQty | Number |
| ReportedSeverity | String |
| Status | String |

---

## Validation Rules

The topic validates:

- Disruption ID exists
- Supplier ID exists
- SKU exists
- Disruption Type exists
- Reported Date exists
- Expected Recovery Date exists
- Reported Date < Expected Recovery Date
- Affected PO exists
- Affected Quantity > 0
- Severity exists
- Status = Pending

---

## Outputs

| Output | Type |
|---------|---------|
| ValidationStatus | String |
| DuplicateDetected | Boolean |

---

## Possible Outcomes

### PASS

All validation requirements satisfied.

### FAIL

One or more validation requirements failed.

Workflow terminates.

---

# Recovery Strategy Resolution

## Purpose

Selects a recovery branch using specialist findings received from the Supervisor.

The topic does not perform analysis.

The topic only applies deterministic business rules.

---

## Inputs

| Input | Type |
|---------|---------|
| InventoryRisk | String |
| InventoryRecommendation | String |
| AlternateAvailable | Boolean |
| ApprovedStatus | String |
| ApprovalRequired | String |
| RequiredApprover | String |

---

## Branch Selection Logic

### Branch A

Conditions:

- InventoryRisk = Low

OR

- InventoryRecommendation = Use Existing Inventory

Result:

- Use Existing Inventory

---

### Branch B

Conditions:

- InventoryRisk = Medium

Result:

- Partial Fulfillment

---

### Branch C

Conditions:

- AlternateAvailable = True
- ApprovedStatus = Yes
- ApprovalRequired = Yes

Result:

- Approved Alternate Supplier

---

### Branch D

Conditions:

- AlternateAvailable = True
- ApprovedStatus = No

Result:

- Unapproved Alternate Supplier
- Escalation Required

---

### Branch E

Conditions:

- AlternateAvailable = False
- InventoryRisk = Critical

OR

- No prior branch matched

Result:

- Management Escalation

---

## Outputs

| Output | Type |
|---------|---------|
| SelectedRecoveryBranch | String |
| SelectedRecoveryStrategy | String |
| EscalationRequired | Boolean |

---

# Approval, Exception & Selective Reassessment

## Purpose

Controls approval routing and reassessment governance.

The topic does not rerun specialists.

The Supervisor remains responsible for reassessment execution.

---

## Inputs

| Input | Type |
|---------|---------|
| ApprovalRequired | String |
| RequiredApprover | String |
| ReassessmentCycleCount | Number |

---

## Governance Logic

### Manual Review

Condition:

ReassessmentCycleCount >= 2

Result:

- CaseStatus = Manual Review
- ManualReviewRequired = True

No further reassessment cycles permitted.

---

### Approval Route

Condition:

ApprovalRequired = Yes

Result:

- CaseStatus = Awaiting Approval

---

### Approved Route

Condition:

ApprovalRequired = No

Result:

- CaseStatus = Approved Route

---

### Reassessment Tracking

If manual review threshold is not exceeded:

UpdatedReassessmentCycleCount =
ReassessmentCycleCount + 1

---

## Outputs

| Output | Type |
|---------|---------|
| CaseStatus | String |
| ManualReviewRequired | Boolean |
| UpdatedReassessmentCycleCount | Number |
| ApprovalRequiredOrNot | String |
| RequiredApproverName | String |

---

# Topic Integration

Execution order within the workflow:

1. Disruption Intake & Validation
2. Inventory Impact Specialist
3. Alternate Supplier Specialist
4. Customer Impact Specialist
5. Commercial Impact Specialist
6. Recovery Planning Specialist
7. Recovery Strategy Resolution
8. Approval, Exception & Selective Reassessment
9. Reporting & Communication Specialist

---

# Design Principles

The custom topics are intentionally deterministic.

Topics:

- Do not perform specialist analysis
- Do not retrieve workbook data
- Do not make business approvals
- Do not override policy rules
- Do not execute operational actions

Their purpose is to provide governance and routing decisions that support the Supervisor's orchestration responsibilities.

---