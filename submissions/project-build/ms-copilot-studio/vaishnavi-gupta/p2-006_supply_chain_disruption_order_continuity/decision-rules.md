# Decision Rules

## Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System applies deterministic decision rules to ensure that all recommendations align with organizational policy, supply continuity requirements, approval governance, and customer commitments.

These rules are used by the Supervisor Agent, specialist agents, and custom topics to evaluate disruptions, resolve conflicts, classify risk, determine approvals, and recommend recovery strategies. Deterministic rules always take precedence over generative reasoning. 【1-ce2a94】

---

# Decision Framework

The solution follows a layered decision-making approach:

```text
Validation Rules
        ↓
Assessment Rules
        ↓
Recovery Rules
        ↓
Conflict Resolution Rules
        ↓
Approval Rules
        ↓
Risk Classification Rules
        ↓
Final Status Determination
```


---

# Validation Rules

## Rule VR-01: Disruption ID Validation

### Condition

```text
Disruption ID is missing
```

### Decision

```text
Validation Failed
```

### Outcome

```text
Insufficient Evidence
```


---

## Rule VR-02: Duplicate Record Detection

### Condition

```text
Duplicate Disruption ID Exists
OR
Record Already In Assessment
```

### Decision

```text
Do Not Process
```

### Outcome

```text
Prevent Duplicate Processing
```


---

## Rule VR-03: Supplier Validation

### Condition

```text
Supplier Does Not Exist
```

### Decision

```text
Validation Failed
```

### Outcome

```text
Insufficient Evidence
```


---

## Rule VR-04: SKU Validation

### Condition

```text
SKU Not Found
```

### Decision

```text
Validation Failed
```

### Outcome

```text
Manual Review
```


---

## Rule VR-05: Purchase Order Validation

### Condition

```text
Purchase Order Missing
OR
PO Does Not Match Supplier/SKU
```

### Decision

```text
Validation Failed
```

### Outcome

```text
Insufficient Evidence
```


---

# Inventory Decision Rules

The Inventory Impact Specialist evaluates stock availability using the Available-to-Promise formula.

## ATP Formula

```text
Available To Promise (ATP)
=
On Hand
- Reserved
+ Inbound Within 7 Days
- Quality Hold
```


---

## Rule INV-01: Inventory Sufficient

### Condition

```text
ATP >= Demand Until Recovery
```

### Decision

```text
Inventory Can Protect Demand
```

### Recommended Action

```text
Use Existing Inventory
```

### Strategy Status

```text
Resolved With Existing Supply
```


---

## Rule INV-02: Inventory Partially Sufficient

### Condition

```text
ATP < Demand Until Recovery
AND
ATP > 0
```

### Decision

```text
Partial Demand Coverage
```

### Recommended Action

```text
Protect High Priority Orders
Evaluate Alternate Supply
```


---

## Rule INV-03: Inventory Shortage

### Condition

```text
ATP <= 0
```

### Decision

```text
Inventory Cannot Protect Demand
```

### Recommended Action

```text
Alternate Sourcing
or
Escalation
```


---

## Rule INV-04: Quality Hold Restriction

### Condition

```text
Inbound Quantity On Quality Hold
```

### Decision

```text
Do Not Count As Available Inventory
```

### Rationale

Quality-restricted inventory cannot be treated as usable supply.


---

# Customer Priority Rules

## Order Priority Hierarchy

```text
Strategic + SLA Protected
        ↓
Priority
        ↓
Standard
```


---

## Rule CUS-01: Strategic Order Protection

### Condition

```text
Strategic Order At Risk
```

### Decision

```text
Protect Strategic Order First
```

### Override

Customer protection takes precedence over lower-priority demand.


---

## Rule CUS-02: SLA-Protected Orders

### Condition

```text
SLA Order At Risk
```

### Decision

```text
Prioritize Fulfillment
```

### Outcome

Higher fulfillment priority than standard orders.


---

## Rule CUS-03: Order Ranking

### Condition

```text
Multiple Orders Competing
For Limited Supply
```

### Decision

```text
Rank Orders Based On:
- Strategic Status
- SLA Commitments
- Required Date
- Revenue Exposure
- Customer Tier
```


---

## Rule CUS-04: Partial Fulfillment Restriction

### Condition

```text
Partial Fulfillment Not Allowed
```

### Decision

```text
Do Not Split Order
```

### Outcome

Alternative recovery strategy required.


---

# Alternate Supplier Rules

## Rule ALT-01: Approved Alternate Supplier

### Condition

```text
Approved Supplier Exists
AND
Capacity Available
AND
Can Meet Required Date
```

### Decision

```text
Approved For Strategy Evaluation
```


---

## Rule ALT-02: Unapproved Supplier Restriction

### Condition

```text
Approved Status = No
```

### Decision

```text
Cannot Be Selected Autonomously
```

### Outcome

```text
Manual Qualification Required
```


---

## Rule ALT-03: Capacity Validation

### Condition

```text
Supplier Capacity
< Required Quantity
```

### Decision

```text
Supplier Cannot Fully Protect Demand
```

### Outcome

Combined recovery strategy may be required.


---

## Rule ALT-04: Delivery Schedule Validation

### Condition

```text
Lead Time Exceeds Required Date
```

### Decision

```text
Supplier Cannot Meet Customer Need
```

### Outcome

Alternative strategy required.


---

# Commercial Rules

## Rule COM-01: Cost Premium Approval

### Condition

```text
Cost Premium > 15%
```

### Decision

```text
Approval Required
```

### Required Approver

```text
Finance Business Partner
```


---

## Rule COM-02: Expedite Premium Approval

### Condition

```text
Expedite Premium > 10%
```

### Decision

```text
Approval Required
```

### Required Approver

```text
Supply Chain Director
```


---

## Rule COM-03: Acceptable Premium

### Condition

```text
Premium Within Threshold
```

### Decision

```text
Approval Not Required
```

### Outcome

Continue processing.


---

# Recovery Strategy Rules

## Rule REC-01: Existing Inventory Strategy

### Condition

```text
ATP Covers All Demand
```

### Strategy

```text
Use Existing Inventory
```


---

## Rule REC-02: Inventory + Alternate Supplier

### Condition

```text
ATP Covers Partial Demand
AND
Approved Alternate Available
```

### Strategy

```text
Combined Recovery Strategy
```


---

## Rule REC-03: Approved Alternate Supplier

### Condition

```text
Inventory Insufficient
AND
Approved Alternate Can Meet Demand
```

### Strategy

```text
Alternate Supplier Recovery
```


---

## Rule REC-04: Customer Negotiation

### Condition

```text
Supply Cannot Meet Required Date
```

### Strategy

```text
Customer Date Negotiation
```


---

## Rule REC-05: No Recovery Route

### Condition

```text
No Inventory
No Approved Supplier
No Viable Alternative
```

### Strategy

```text
Management Escalation
```


---

# Conflict Resolution Rules

When specialist recommendations conflict, the Supervisor applies the following precedence model.

## Conflict Priority Order

```text
1. Safety & Quality Restrictions
2. Strategic/SLA Commitments
3. Supplier Approval Restrictions
4. Inventory Availability
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience
```


---

## Conflict Example 1

### Scenario

```text
Inventory Appears Sufficient
But Strategic SLA Order
Is Due Earlier
```

### Decision

```text
Protect Strategic Customer
```

### Winning Rule

```text
SLA Commitment Priority
```


---

## Conflict Example 2

### Scenario

```text
Alternate Supplier Available
But Cost Premium = 18%
```

### Decision

```text
Technically Feasible
Approval Required
```

### Winning Rule

```text
Commercial Approval Rule
```


---

## Conflict Example 3

### Scenario

```text
Alternate Supplier Has Capacity
But Supplier Not Approved
```

### Decision

```text
Do Not Select Automatically
```

### Winning Rule

```text
Supplier Approval Restriction
```


---

# Approval Rules

## Approval State Trigger

The disruption is moved to:

```text
Awaiting Approval
```

when any approval condition exists.


---

## Approval Conditions

- Cost premium exceeds 15%
- Expedite premium exceeds 10%
- Safety stock required for strategic demand
- Unapproved supplier identified
- Partial fulfillment restricted
- Critical demand remains unprotected


---

## Approval Constraints

The system must not:

- Invent approvals
- Assume approval completion
- Continue restricted actions without approval


---

# Selective Reassessment Rules

## Rule REA-01: Supplier Data Change

### Re-run

```text
Alternate Supplier Specialist
Commercial Impact Specialist
```


---

## Rule REA-02: Inventory Change

### Re-run

```text
Inventory Specialist
Customer Impact Specialist
```


---

## Rule REA-03: Preserve Valid Results

### Decision

```text
Do Not Re-run
Unaffected Specialists
```

### Benefit

Reduces unnecessary processing.


---

## Rule REA-04: Reassessment Limit

### Condition

```text
More Than Two
Unresolved Reassessments
```

### Outcome

```text
Manual Review
```


---

# Risk Classification Rules

## Low Risk

```text
Demand Protected
No Escalation
No Major Constraints
```


---

## Medium Risk

```text
Minor Constraints
Recovery Available
Limited Business Impact
```


---

## High Risk

```text
Strategic Exposure
Significant Shortage
Approval Required
```


---

## Critical Risk

```text
No Viable Recovery
Major Customer Exposure
Severe Supply Impact
Management Escalation
```


---

# Final Status Rules

Exactly one primary status must be assigned.

## Possible Status Values

```text
Resolved With Existing Supply
Recovery Plan Proposed
Awaiting Approval
Customer Action Required
Management Escalation
Insufficient Evidence
Manual Review
Completed
```


---

## Completion Rule

### Condition

```text
Reporting Completed
Notifications Sent
No Outstanding Approvals
```

### Final Status

```text
Completed
```

### Restriction

Cases awaiting approval cannot be marked as Completed.


---

# Summary

The decision framework ensures that every recommendation produced by the solution is policy-driven, explainable, and auditable. Validation rules protect data quality, inventory and customer rules prioritize operational continuity, supplier and commercial rules enforce governance, conflict-resolution rules ensure consistent decision-making, and approval controls maintain required human oversight. Together, these rules enable autonomous disruption assessment while preserving business control and compliance requirements. 【1-ce2a94】