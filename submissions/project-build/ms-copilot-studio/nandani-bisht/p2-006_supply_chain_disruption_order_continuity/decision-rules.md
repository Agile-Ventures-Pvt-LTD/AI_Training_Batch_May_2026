# decision-rules.md

# Decision Rules

## P2-006 – Supply Chain Disruption Order Continuity

---

# Overview

The Supply Chain Disruption Order Continuity solution uses a set of deterministic business rules to ensure that disruption handling remains consistent, auditable, and compliant with organizational policies.

These rules guide the Supervisor Agent and specialist child agents during validation, assessment, recovery planning, approvals, and reporting.

---

# Decision Categories

The business rules are grouped into the following categories:

- Validation Rules
- Inventory Rules
- Alternate Supplier Rules
- Customer Priority Rules
- Commercial Rules
- Recovery Planning Rules
- Approval Rules
- Escalation Rules
- Failure & Retry Rules
- Reporting Rules

---

# 1. Validation Rules

## Rule V-01

A disruption request must contain a valid Disruption ID.

**If invalid**

→ Reject the request.

---

## Rule V-02

Supplier ID must exist.

**If not found**

→ Validation Failed.

---

## Rule V-03

SKU must exist.

**If invalid**

→ Validation Failed.

---

## Rule V-04

Purchase Order must match both Supplier and SKU.

**If mismatch**

→ Validation Failed.

---

## Rule V-05

Only Pending disruptions can begin processing.

```text
Pending?

YES → Continue

NO → Stop
```

---

## Rule V-06

Duplicate disruption requests are not processed.

```text
Duplicate?

YES → Stop Workflow

NO → Continue
```

---

# 2. Inventory Rules

## Rule I-01

If available inventory completely satisfies demand:

→ Recommend **Use Existing Inventory**

---

## Rule I-02

If inventory partially satisfies demand:

→ Protect strategic customers first.

---

## Rule I-03

Quality-held inventory is excluded.

---

## Rule I-04

Safety stock cannot be consumed below policy limits.

---

## Rule I-05

Negative inventory values are invalid.

---

# 3. Alternate Supplier Rules

## Rule S-01

Only approved suppliers can be recommended.

---

## Rule S-02

Supplier capacity must meet required quantity.

---

## Rule S-03

Supplier lead time must satisfy required delivery date.

---

## Rule S-04

Unapproved suppliers cannot be automatically selected.

```text
Approved Supplier?

YES → Recommend

NO → Reject
```

---

# 4. Customer Priority Rules

## Rule C-01

Strategic customers have highest priority.

---

## Rule C-02

SLA commitments override normal customer priority.

---

## Rule C-03

Revenue-at-risk increases escalation priority.

---

## Rule C-04

Customer orders are ranked before allocation.

---

# 5. Commercial Rules

## Rule M-01

If alternate supplier premium exceeds **15%**:

→ Finance approval required.

---

## Rule M-02

High commercial exposure increases escalation priority.

---

## Rule M-03

Commercial approval is required before executing premium recovery options.

---

# 6. Recovery Planning Rules

Recovery Planning follows this precedence:

1. Use Existing Inventory
2. Reallocate Inventory
3. Approved Alternate Supplier
4. Expedite Existing Supply
5. Expedite Alternate Supply
6. Partial Fulfilment
7. Customer Delivery Negotiation
8. Manual Review
9. Management Escalation

---

# 7. Approval Rules

Recovery strategies requiring commercial or operational approval are routed accordingly.

### Finance Approval

Required when:

- Cost premium exceeds threshold
- Budget impact exceeds policy

---

### Supply Chain Approval

Required when:

- Inventory reallocation affects multiple locations
- Strategic supply decisions are needed

---

### Management Approval

Required when:

- No viable recovery exists
- High business risk
- Critical customer commitments

---

# 8. Escalation Rules

Escalation occurs when:

- No approved supplier exists
- Inventory unavailable
- Critical SKU affected
- Strategic customers cannot be protected
- Repeated assessment failures occur

Possible outcomes:

- Manual Review
- Management Escalation
- Operational Review

---

# 9. Failure & Retry Rules

If a specialist fails:

### First Failure

Retry once.

---

### Second Failure

Return:

```text
Insufficient Evidence
```

---

### Third Failure / Unresolved

Escalate for Manual Review.

---

# 10. Reporting Rules

Reports are generated only after:

- Validation completed
- Recovery strategy selected
- Required approvals obtained

The Reporting & Communication Specialist then:

- Generates Word report
- Updates Excel
- Sends Outlook email

---

# Recovery Strategy Decision Matrix

| Condition | Recommended Action |
|-----------|--------------------|
| Inventory Available | Use Existing Inventory |
| Partial Inventory | Allocate Strategic Orders |
| Approved Alternate Supplier | Recommend Supplier |
| Premium >15% | Finance Approval |
| Unapproved Supplier | Reject Recommendation |
| No Recovery Route | Management Escalation |
| Specialist Failure | Retry |
| Retry Failed | Manual Review |

---

# Approval Decision Matrix

| Scenario | Required Approval |
|----------|-------------------|
| Normal Recovery | None |
| Premium Cost | Finance |
| Strategic Supply Decision | Supply Chain Director |
| Critical Business Risk | Executive Management |

---

# Exception Handling Matrix

| Exception | Action |
|-----------|--------|
| Duplicate Request | Stop Workflow |
| Invalid Supplier | Validation Failed |
| Invalid SKU | Validation Failed |
| Excel Unavailable | Retry / Log Error |
| Word Generation Failure | Retry |
| Outlook Failure | Log Notification Failure |

---

# Rule Execution Flow

```text
Validate Request
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
Approval
        │
        ▼
Reporting
```

---

# Governance Principles

The decision rules ensure:

- Consistent business decisions
- Enterprise policy compliance
- Controlled approvals
- Explainable AI recommendations
- Reduced operational risk
- Improved auditability

---

# Summary

The decision rules provide the foundation for autonomous decision-making within the Supply Chain Disruption Order Continuity solution.

They ensure that every recommendation generated by the Supervisor Agent and specialist agents follows predefined business policies, maintains governance, and supports consistent supply chain operations.

---

# Version

**Version:** 1.0

**Status:** Completed
