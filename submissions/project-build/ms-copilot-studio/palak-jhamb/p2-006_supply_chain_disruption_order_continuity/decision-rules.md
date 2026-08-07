# Decision Rules

## Overview

The Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System follows a set of deterministic business rules to ensure that disruption assessments are consistent, policy-compliant, and evidence-based. These rules are enforced by the **Supply Continuity Supervisor** and the specialist agents throughout the workflow.

---

# 1. Disruption Validation Rules

Every disruption request must pass validation before assessment begins.

## Validation Criteria

The disruption request must satisfy all of the following:

- Disruption ID exists.
- Supplier ID exists.
- SKU exists.
- Purchase Order exists.
- Affected Quantity is greater than zero.
- Status equals **Pending**.
- Expected Recovery Date exists.
- Expected Recovery Date is not in the past.

If any validation fails:

- Stop the assessment.
- Mark the disruption as **Manual Review** or **Insufficient Evidence**.
- Do not invoke specialist agents.

---

# 2. Inventory Decision Rules

The Inventory Impact Specialist evaluates whether current inventory can satisfy customer demand.

### Rule 1

If Available-to-Promise (ATP) is greater than or equal to the required quantity:

- Inventory is considered sufficient.
- Existing inventory is preferred.

### Rule 2

If ATP is less than the required quantity:

- Calculate the shortage quantity.
- Continue with alternate supplier evaluation.

### Rule 3

Inventory on Quality Hold must never be considered available.

### Rule 4

Safety stock should be preserved whenever possible.

---

# 3. Alternate Supplier Rules

Alternate suppliers are evaluated using structured supplier information.

### Rule 1

Only suppliers with:

```
Approved = Yes
```

may be recommended as autonomous recovery options.

### Rule 2

If no approved supplier exists:

- Recommend Manual Supplier Qualification.
- Escalate for approval if required.

### Rule 3

Supplier evaluation considers:

- Available Capacity
- Lead Time
- Expedite Lead Time
- Unit Cost
- Supplier Risk

---

# 4. Customer Priority Rules

Customer commitments are prioritized using business rules.

Priority order:

1. Strategic Customer with SLA Protection
2. Strategic Customer
3. SLA Protected Customer
4. Priority Customer
5. Standard Customer

Higher-priority customer commitments should be protected whenever possible.

---

# 5. Commercial Decision Rules

Commercial assessments determine whether financial approvals are required.

### Rule 1

If the alternate supplier cost premium exceeds the defined business threshold:

- Finance approval is required.

### Rule 2

If the expedite premium exceeds the defined business threshold:

- Supply Chain Director approval is required.

### Rule 3

Commercial assessments must never fabricate costs or approval requirements.

---

# 6. Recovery Strategy Rules

The Recovery Planning Specialist recommends recovery strategies based on consolidated specialist assessments.

Possible strategies include:

- Use existing inventory
- Source from an approved alternate supplier
- Expedite existing supply
- Expedite alternate supply
- Partial fulfillment
- Customer delivery negotiation
- Combined recovery strategy
- Manual review
- Management escalation

Recovery recommendations must follow the NovaSphere Supply Continuity Policy.

---

# 7. Approval Rules

The Supervisor determines whether additional approvals are required.

Approval may be required when:

- Commercial premium exceeds policy thresholds.
- Expedite premium exceeds policy thresholds.
- Manual supplier qualification is required.
- Management escalation is recommended.

No recovery strategy requiring approval should proceed until approval has been obtained.

---

# 8. Conflict Resolution Rules

When specialist recommendations conflict, the Supervisor applies the following precedence:

1. Safety and Quality
2. Strategic Customer Commitments
3. SLA Obligations
4. Approved Supplier Restrictions
5. Inventory Availability
6. Commercial Constraints
7. Cost Optimization

These rules ensure that business-critical priorities are protected before cost optimization.

---

# 9. Retry Rules

If a child agent fails:

1. Retry once.
2. If the retry succeeds, continue processing.
3. If the retry fails:
   - Mark the assessment as **Insufficient Evidence**.
   - Continue if the remaining evidence is sufficient.
4. Escalate for Manual Review if critical information is unavailable.

---

# 10. Selective Reassessment Rules

Only the affected specialist agent should be reinvoked when new or corrected information becomes available.

Examples:

- Inventory changes → Reinvoke Inventory Impact Specialist.
- Supplier updates → Reinvoke Alternate Supplier Specialist.
- Customer order updates → Reinvoke Customer & Order Impact Specialist.
- Commercial changes → Reinvoke Commercial Impact Specialist.

Previously completed assessments remain valid and should not be repeated unnecessarily.

---

# 11. Reporting Rules

The Reporting & Communication Specialist may execute only after:

- The recovery strategy has been approved.
- The Supervisor authorizes report generation.
- Required approvals have been completed.

The agent must:

- Generate the recovery report.
- Prepare stakeholder notifications.
- Use only approved information.

---

# 12. Supervisor Governance Rules

The Supply Continuity Supervisor must always:

- Validate disruption requests before assessment.
- Use evidence from specialist agents.
- Follow the NovaSphere Supply Continuity Policy.
- Resolve conflicting recommendations.
- Make the final business decision.
- Maintain a complete audit trail.

The Supervisor must never:

- Fabricate business data.
- Skip validation.
- Ignore policy restrictions.
- Approve unapproved suppliers.
- Override required approvals.
- Perform specialist analysis directly.

---

# Summary

The decision rules ensure that every disruption assessment is:

- Evidence-based
- Policy-compliant
- Deterministic where applicable
- Consistent across executions
- Governed by the Supply Continuity Supervisor

These rules provide a structured framework for autonomous decision making while maintaining transparency, auditability, and alignment with organizational supply continuity policies.