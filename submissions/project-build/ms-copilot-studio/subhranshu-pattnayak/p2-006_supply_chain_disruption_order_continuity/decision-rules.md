# Decision Rules

## Purpose

The Supply Continuity Supervisor uses deterministic governance rules to ensure that recovery recommendations remain compliant with policy, customer commitments, and operational constraints.

The Supervisor does not perform specialist analysis.

All decisions must be based on specialist findings and policy guidance.

---

# Policy Precedence Order

When findings conflict, the Supervisor applies the following precedence sequence:

1. Safety or Quality Restriction
2. Strategic / SLA-Protected Customer Commitment
3. Supplier Approval Restriction
4. Inventory Availability and Timing
5. Commercial Approval Requirement
6. Cost Optimization
7. Lower-Priority Customer Convenience

Higher-priority rules always override lower-priority rules.

---

# Validation Rules

Processing may proceed only when:

- Disruption ID exists
- Supplier ID exists
- SKU exists
- Affected Quantity > 0
- Reported Date exists
- Expected Recovery Date exists
- Reported Date < Expected Recovery Date
- Status = Pending
- Severity exists

If any validation rule fails:

- ValidationStatus = FAIL
- Workflow stops
- No specialist execution occurs

---

# Recovery Strategy Rules

## Branch A – Use Existing Inventory

Selected when:

- Inventory Risk = Low

OR

- Inventory Recommendation = Use Existing Inventory

Result:

- SelectedRecoveryBranch = A
- SelectedRecoveryStrategy = Use Existing Inventory

---

## Branch B – Partial Fulfillment

Selected when:

- Inventory Risk = Medium

Result:

- SelectedRecoveryBranch = B
- SelectedRecoveryStrategy = Partial Fulfillment

---

## Branch C – Approved Alternate Supplier

Selected when:

- AlternateAvailable = True
- ApprovedStatus = Yes
- ApprovalRequired = Yes

Result:

- SelectedRecoveryBranch = C
- SelectedRecoveryStrategy = Approved Alternate Supplier

---

## Branch D – Unapproved Alternate Supplier

Selected when:

- AlternateAvailable = True
- ApprovedStatus = No

Result:

- SelectedRecoveryBranch = D
- EscalationRequired = True

---

## Branch E – Management Escalation

Selected when:

- AlternateAvailable = False
- InventoryRisk = Critical

OR

- No previous branch matches

Result:

- SelectedRecoveryBranch = E
- EscalationRequired = True

---

# Reassessment Rules

The Approval & Reassessment Topic controls reassessment governance.

## Manual Review Threshold

If:

ReassessmentCycleCount >= 2

Then:

- CaseStatus = Manual Review
- ManualReviewRequired = True

No additional reassessment cycles are permitted.

---

## Approval Route

If:

ApprovalRequired = Yes

Then:

- CaseStatus = Awaiting Approval

---

## Approved Route

If:

ApprovalRequired = No

Then:

- CaseStatus = Approved Route

---

# Escalation Rules

Escalation is required when:

- Unapproved supplier is the only available source
- No viable recovery strategy exists
- Required specialist evidence is unavailable
- Reassessment limit is exceeded
- Policy restrictions cannot be satisfied
- Recovery planning returns Management Escalation
- Recovery planning returns Manual Review

---

# Supervisor Governance Rules

The Supervisor must never:

- Create Purchase Orders
- Approve Suppliers
- Approve Expenditure
- Commit Inventory
- Promise Customer Delivery Dates
- Override Policy Rules
- Fabricate Missing Evidence

The Supervisor may only make recommendations based on specialist findings and policy guidance.