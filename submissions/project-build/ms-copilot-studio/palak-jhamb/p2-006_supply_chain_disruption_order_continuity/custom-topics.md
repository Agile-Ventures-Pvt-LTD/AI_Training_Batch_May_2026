# Custom Topics

## Overview

The Supply Continuity Supervisor uses custom topics to organize the disruption assessment workflow into reusable, modular business processes. Each topic performs a specific responsibility and supports autonomous orchestration.

---

# Topic 1 – Disruption Intake & Validation

## Purpose

Validate the disruption request before any specialist assessment begins.

## Responsibilities

- Retrieve the disruption request
- Validate mandatory fields
- Validate business rules
- Verify disruption status
- Determine whether the assessment can begin

## Validation Rules

- Disruption ID exists
- Supplier ID exists
- SKU exists
- Purchase Order exists
- Affected Quantity > 0
- Status = Pending
- Expected Recovery Date exists
- Expected Recovery Date is not in the past

## Success Outcome

```json
{
  "validationStatus": "Passed"
}
```

## Failure Outcome

```json
{
  "validationStatus": "Failed",
  "validationErrors": [
    "Validation error details"
  ]
}
```

---

# Topic 2 – Recovery Strategy Resolution

## Purpose

Review the recovery recommendation and determine whether it satisfies organizational business rules.

## Responsibilities

- Review specialist assessments
- Validate the proposed recovery strategy
- Apply policy rules
- Resolve conflicting recommendations
- Determine approval requirements

## Inputs

- Inventory Assessment
- Alternate Supplier Assessment
- Customer Impact Assessment
- Commercial Assessment
- Recovery Strategy Recommendation

## Output

- Approved Strategy
- Approval Requirement
- Manual Review Recommendation (if applicable)

---

# Topic 3 – Approval, Exception & Selective Reassessment

## Purpose

Manage approval routing, retry logic, exception handling, and reassessment.

## Responsibilities

- Retry failed specialist assessments
- Route approval requests
- Trigger Manual Review
- Reinvoke only affected specialist agents
- Prevent unnecessary reassessment

## Business Rules

- Retry once on failure.
- Mark assessment as Insufficient Evidence if retry fails.
- Escalate to Manual Review when critical evidence is unavailable.
- Reinvoke only the affected specialist agent.
- Preserve successful specialist assessments.

---

# Topic Interaction

```
Disruption Intake & Validation

        │

        ▼

Specialist Assessments

        │

        ▼

Recovery Strategy Resolution

        │

        ▼

Approval & Exception Handling

        │

        ▼

Reporting & Communication
```

---

# Benefits

- Modular workflow
- Reusable conversation logic
- Easier maintenance
- Simplified orchestration
- Improved scalability
- Better governance