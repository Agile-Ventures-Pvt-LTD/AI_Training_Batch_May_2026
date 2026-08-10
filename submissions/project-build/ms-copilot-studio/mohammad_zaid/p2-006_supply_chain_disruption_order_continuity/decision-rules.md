
# Decision Rules

# Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System follows deterministic business rules to ensure every recommendation is consistent, explainable, auditable, and aligned with the NovaSphere Supply Continuity Policy.

Unlike traditional AI systems, the solution does not rely solely on generative reasoning. Instead, explicit business rules, operational data, and policy constraints govern every decision made throughout the orchestration lifecycle.

---

# Decision Hierarchy

The solution follows the following decision hierarchy.

```
Business Policy
       │
       ▼
Data Validation
       │
       ▼
Inventory Assessment
       │
       ▼
Supplier Assessment
       │
       ▼
Customer Assessment
       │
       ▼
Commercial Assessment
       │
       ▼
Recovery Planning
       │
       ▼
Supervisor Validation
       │
       ▼
Final Decision
```

---

# Rule Category 1 — Disruption Validation

Before any specialist assessment begins, the system validates the disruption request.

Validation Rules:

- Disruption ID must exist.
- Status must be Pending.
- Supplier ID must exist.
- SKU must exist.
- Disruption Type must exist.
- Reported Date must be valid.
- Affected Purchase Order must exist.
- Affected Quantity must be greater than zero.
- Duplicate disruption requests are rejected.

Failure Action:

- Status = Insufficient Evidence
- Workflow terminates.

---

# Rule Category 2 — Inventory Rules

The Inventory Impact Specialist evaluates inventory using deterministic calculations.

Rules:

- Calculate Available-to-Promise (ATP).
- Exclude reserved inventory.
- Exclude quality-held inventory.
- Include valid inbound inventory.
- Compare ATP against affected demand.
- Determine shortage quantity.
- Recommend inventory action.

Possible Outcomes:

- Inventory sufficient
- Partial inventory available
- Inventory shortage

---

# Rule Category 3 — Alternate Supplier Rules

The Alternate Supplier Specialist evaluates alternate sourcing options.

Rules:

- Only approved suppliers may be recommended.
- Supplier capacity must satisfy required quantity.
- Lead time must support recovery.
- Supplier risk must be acceptable.
- Supplier approval status is mandatory.

Restrictions:

- Unapproved suppliers cannot be selected automatically.
- Unapproved suppliers may only be suggested for manual qualification.

---

# Rule Category 4 — Customer Priority Rules

Customer commitments are prioritized according to business importance.

Priority Order:

1. Strategic Customers with SLA Protection
2. Priority Customers
3. Standard Customers

Additional Factors:

- Required delivery date
- Revenue exposure
- Customer tier
- Partial fulfilment permission

---

# Rule Category 5 — Commercial Rules

Commercial approval is determined using recovery cost.

Rules:

- Calculate recovery cost.
- Calculate alternate supplier premium.
- Evaluate expedite premium.
- Determine approval requirement.
- Assess commercial risk.

Approval Thresholds:

- Cost Premium > 15%
- Expedite Premium > 10%

These thresholds trigger mandatory approval workflows.

---

# Rule Category 6 — Recovery Strategy Rules

The Recovery Planning Specialist recommends only permitted recovery strategies.

Allowed Strategies:

- Use Existing Inventory
- Reallocate Inventory
- Approved Alternate Supplier
- Expedite Existing Supply
- Expedite Alternate Supply
- Partial Fulfilment
- Customer Date Negotiation
- Combined Recovery Strategy
- Management Escalation
- Manual Review

Restricted Actions:

- Place Purchase Orders
- Approve Suppliers
- Cancel Customer Orders
- Promise Delivery Dates
- Approve Commercial Spend

---

# Rule Category 7 — Decision Precedence

When specialist findings conflict, the Supervisor applies the following precedence order.

1. Safety and Quality Restrictions
2. Strategic / SLA Customer Commitments
3. Supplier Approval Restrictions
4. Inventory Availability
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience

The Supervisor never averages conflicting recommendations.

---

# Rule Category 8 — Approval Rules

Approval is required when one or more of the following conditions are met.

- Commercial premium exceeds threshold.
- Expedite premium exceeds threshold.
- Strategic demand requires safety stock consumption.
- No approved alternate supplier exists.
- Partial fulfilment is not allowed.
- Critical demand cannot be protected.

If approval is required:

- Workflow Status = Awaiting Approval.

---

# Rule Category 9 — Selective Reassessment Rules

The system minimizes unnecessary reassessment.

Rules:

- Reassess only affected business domains.
- Preserve valid specialist outputs.
- Re-run only stale assessments.
- Return to Recovery Strategy Resolution.

Maximum reassessment cycles:

2

After two unsuccessful reassessments:

Workflow Status = Manual Review.

---

# Rule Category 10 — Exception Rules

The solution handles exceptional situations deterministically.

| Scenario                     | Decision              |
| ---------------------------- | --------------------- |
| Missing Supplier             | Insufficient Evidence |
| Missing SKU                  | Insufficient Evidence |
| Missing Purchase Order       | Insufficient Evidence |
| Invalid PO–SKU Relationship | Manual Review         |
| No Recovery Strategy         | Management Escalation |
| Missing Specialist Output    | Retry Once            |
| Retry Failure                | Insufficient Evidence |
| Approval Failure             | Awaiting Approval     |
| Reassessment Limit Reached   | Manual Review         |

---

# Workflow State Rules

Valid workflow transitions are:

```
Pending
      │
      ▼
In Assessment
      │
      ▼
Recovery Plan Proposed
      │
      ▼
Awaiting Approval
      │
      ▼
Completed
```

Additional terminal states:

- Insufficient Evidence
- Manual Review
- Management Escalation
- Customer Action Required

Invalid transitions are not permitted.

---

# Supervisor Decision Rules

Only the Supervisor may:

- Validate disruption requests.
- Invoke specialist agents.
- Determine recovery strategy.
- Resolve conflicting recommendations.
- Determine approval requirements.
- Authorize reporting.
- Authorize stakeholder notification.
- Update final workflow state.

Specialists never make the final business decision.

---

# Risk Classification Rules

The Supervisor classifies every disruption into one of four risk levels.

- Low
- Medium
- High
- Critical

Risk classification considers:

- Inventory availability
- Customer impact
- Commercial impact
- Supplier risk
- Recovery feasibility
- Policy constraints

Every High and Critical classification must include a business rationale.

---

# Final Decision Logic

```
Validate Disruption
        │
        ▼
Specialist Assessments
        │
        ▼
Recovery Planning
        │
        ▼
Supervisor Validation
        │
        ▼
Approval Required?
        │
   ┌────┴─────┐
   │          │
 No          Yes
   │          │
   ▼          ▼
Complete   Await Approval
   │          │
   ▼          ▼
Reporting  Reassessment
        │
        ▼
Workflow Complete
```

---

# Design Principles

The decision engine follows these principles:

- Deterministic execution
- Policy-first reasoning
- Explainable recommendations
- Structured validation
- Human approval boundaries
- Conflict-aware orchestration
- Controlled reassessment
- Auditable workflow execution

---

# Summary

The decision engine combines deterministic business rules, structured specialist assessments, organizational policy, and Supervisor-controlled orchestration to ensure every recovery recommendation is transparent, repeatable, and compliant with enterprise supply chain governance. The explicit decision hierarchy prevents unsupported autonomous actions while maintaining operational efficiency and business resilience.
