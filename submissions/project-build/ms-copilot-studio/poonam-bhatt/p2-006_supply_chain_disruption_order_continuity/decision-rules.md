# Decision Rules

## 1. Purpose

This document defines the decision rules used by the Autonomous Multi-Agent Supply Chain Disruption Order Continuity solution.

The rules provide a consistent basis for:

- Disruption validation
- Evidence sufficiency
- Recovery strategy selection
- Risk classification
- Approval determination
- Reassessment control
- Final status determination

The Supervisor Agent orchestrates these rules through the configured custom topics and specialist agents.

The system must use evidence from the configured data sources and specialist assessments. It must not invent missing values or approvals.

---

## 2. Decision Processing Sequence

The decision process follows this sequence:

1. Retrieve disruption record.
2. Validate disruption input.
3. Confirm the disruption is eligible for assessment.
4. Set status to `In Assessment` when validation succeeds.
5. Run the required specialist assessments.
6. Evaluate specialist results.
7. Determine the recovery strategy.
8. Determine whether approval is required.
9. Perform reassessment checks when applicable.
10. Determine the final status.
11. Generate the final response report.
12. Send the authorized stakeholder notification.

A later decision must not override a blocking validation or evidence issue without sufficient supporting evidence.

---

# 3. Disruption Intake Rules

## Rule DI-01 — Disruption ID Required

A disruption must have a valid `DisruptionID`.

### Condition

```text
IsBlank(DisruptionID)
````

### Result

```text
ValidationStatus = Failed: Disruption ID is missing
```

The disruption should not proceed to specialist assessment.

---

## Rule DI-02 — Status Must Be Pending

A new assessment must start from:

```text
Status = Pending
```

If the status is not `Pending`, the record should not be treated as a new intake.

### Condition

```text
Status <> "Pending"
```

### Result

```text
ValidationStatus = Failed: Disruption status is not Pending
```

This prevents already-processed disruptions from being assessed as new cases.

---

## Rule DI-03 — Supplier ID Required

The disruption must contain a `SupplierID`.

### Condition

```text
IsBlank(SupplierID)
```

### Result

```text
ValidationStatus = Failed: Supplier ID is missing
```

---

## Rule DI-04 — SKU Required

The disruption must contain a `SKU`.

### Condition

```text
IsBlank(SKU)
```

### Result

```text
ValidationStatus = Failed: SKU is missing
```

---

## Rule DI-05 — Disruption Type Required

The disruption must contain a `DisruptionType`.

### Condition

```text
IsBlank(DisruptionType)
```

### Result

```text
ValidationStatus = Failed: Disruption Type is missing
```

---

## Rule DI-06 — Reported Date Required

The disruption must contain a `ReportedDate`.

### Condition

```text
IsBlank(ReportedDate)
```

### Result

```text
ValidationStatus = Failed: Reported Date is missing
```

---

## Rule DI-07 — Affected PO Required

The disruption must contain the affected purchase order reference.

### Condition

```text
IsBlank(AffectedPO)
```

### Result

```text
ValidationStatus = Failed: Affected PO is missing
```

---

## Rule DI-08 — Affected Quantity Must Be Positive

The affected quantity must be greater than zero.

### Condition

```text
AffectedQty <= 0
```

### Result

```text
ValidationStatus = Failed: Affected quantity must be positive
```

---

# 4. Duplicate Disruption Rules

The system must prevent a disruption from being processed repeatedly when it is already under assessment or has reached a completed workflow state.

## Rule DUP-01 — Duplicate Active Assessment

A disruption is considered already processed when its status is one of:

```text
In Assessment
Awaiting Approval
Recovery Plan Proposed
Customer Action Required
Management Escalation
Completed
```

### Result

```text
DuplicateDetected = true
ValidationStatus = Failed: Duplicate disruption detected for active status
```

The intake workflow stops.

The system should communicate that the disruption is already undergoing assessment or has already been resolved.

---

# 5. Successful Intake Rule

## Rule DI-09 — Validation Passed

When all required validation conditions are satisfied:

```text
ValidationStatus = Passed
```

The disruption status is changed to:

```text
In Assessment
```

This status transition indicates that the disruption has successfully entered the assessment workflow.

Only after this transition should the Supervisor initiate the specialist assessment stage.

---

# 6. Failed Intake Rule

## Rule DI-10 — Validation Failure

When validation fails and the failure is not a duplicate that has already been identified:

```text
ValidationStatus <> Passed
```

and:

```text
DuplicateDetected = false
```

the disruption status becomes:

```text
Insufficient Evidence
```

The specialist fan-out should not be treated as a successful assessment.

---

# 7. Evidence Sufficiency Rules

Specialist assessments must be based on actual source evidence.

The system must distinguish between:

* Valid evidence
* Missing evidence
* Conflicting evidence
* Connector/tool failure

Missing evidence must not be replaced with assumptions.

---

## Rule EVD-01 — Missing Source Record

If a required source record does not exist, the specialist should report insufficient evidence for the affected assessment.

Example:

If the disruption references a SKU that is not present in the configured SKU Master or Inventory source, inventory calculations cannot be reliably completed.

The system must not assume:

```text
ATP = 0
```

unless the source data explicitly supports that value.

---

## Rule EVD-02 — Conflicting Source Data

If two authorized sources contain conflicting values, the conflict must be preserved as an evidence issue.

Examples include:

* Disruption SKU does not match PO SKU.
* Disruption SupplierID does not match PO SupplierID.
* Affected quantity does not match the corresponding order quantity.

The Supervisor should not silently select one value without a defined basis.

---

## Rule EVD-03 — Connector Failure

A connector failure is not equivalent to a business value of zero.

For example:

```text
Excel Online (Business) HTTP 500
```

must be treated as a technical/data retrieval failure.

The system must not convert the failure into:

```text
No inventory
```

or another assumed business conclusion.

The affected specialist result should indicate that the required evidence could not be retrieved.

---

# 8. Recovery Strategy Decision Rules

The Strategy Resolution topic evaluates recovery options according to defined decision precedence.

The rules below represent the configured strategy logic.

---

## Rule STR-01 — No Viable Recovery Route

### Condition

```text
AvailableToPromise <= 0
AND
AlternateAvailable = false
```

### Decision

```text
ProposedStrategy =
Management escalation - no viable recovery route
```

### Status

```text
Management Escalation
```

### Risk

```text
Critical
```

### Rationale

```text
No inventory available and no alternate supplier exists.
```

This is the highest-severity recovery condition in the configured strategy logic.

---

# 9. Unapproved Alternate Supplier Rule

## Rule STR-02 — Alternate Supplier Exists but Is Unapproved

### Condition

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Unapproved"
```

### Decision

```text
ProposedStrategy =
Manual supplier qualification option
```

### Status

```text
Manual Review
```

### Risk

```text
High
```

### Rationale

```text
Alternate supplier exists but lacks approval status.
Autonomous sourcing is blocked.
```

The system must not treat an unapproved supplier as an approved recovery route.

---

# 10. Existing Inventory Rule

## Rule STR-03 — Existing Inventory Covers Recovery Demand

### Condition

```text
AvailableToPromise >= DemandUntilRecovery
```

### Decision

```text
ProposedStrategy = Use existing stock
```

### Status

```text
Recovery Plan Proposed
```

### Risk

```text
Low
```

### Rationale

```text
Available-to-promise inventory is sufficient to cover demand
during the recovery period.
```

This rule applies when reliable inventory and demand evidence is available.

---

# 11. Approved Alternate Supplier Rule

## Rule STR-04 — Approved Alternate Supplier Available

### Condition

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Approved"
```

### Decision

```text
ProposedStrategy =
Use approved alternate supplier
```

### Status

```text
Recovery Plan Proposed
```

### Risk

```text
Medium
```

### Rationale

```text
Approved alternate supplier exists and has capacity to meet timing.
```

---

# 12. Partial Inventory Rule

## Rule STR-05 — Inventory Covers Only Part of Demand

### Condition

```text
AvailableToPromise < DemandUntilRecovery
AND
AvailableToPromise > 0
```

### Decision

```text
ProposedStrategy =
Reallocate inventory & negotiate customer dates
```

### Status

```text
Customer Action Required
```

### Risk

```text
Medium
```

### Rationale

```text
ATP covers partial demand. Prioritize Strategic and SLA orders.
```

The strategy indicates that inventory allocation and customer-date management may be required.

---

# 13. Strategy Decision Precedence

The configured Strategy Resolution topic evaluates the recovery branches in the following order:

1. No viable recovery route.
2. Unapproved alternate supplier.
3. Existing inventory sufficient.
4. Approved alternate supplier.
5. Partial inventory.

The Supervisor must preserve the decision returned by the configured Strategy Resolution topic.

A strategy should not be selected using assumptions outside the configured decision rules.

---

# 14. Approval Decision Rules

Approval is determined by the Approval and Reassessment topic.

The system evaluates the configured approval conditions independently.

---

## Rule APR-01 — Cost Premium Approval

### Condition

```text
CostPremiumPct > 15
```

### Required Approver

```text
Finance Business Partner
```

### Approval Reason

```text
Cost premium exceeds 15% threshold.
```

### Result

```text
ApprovalRequired = true
```

---

## Rule APR-02 — Expedite Premium Approval

### Condition

```text
ExpeditePremiumPct > 10
```

### Required Approver

```text
Supply Chain Director
```

### Approval Reason

```text
Expedite premium exceeds 10% threshold.
```

### Result

```text
ApprovalRequired = true
```

---

## Rule APR-03 — Unapproved Alternate Supplier Approval

### Condition

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Unapproved"
```

### Required Approver

```text
Sourcing Manager
```

### Approval Reason

```text
Alternate supplier lacks qualification status.
```

### Result

```text
ApprovalRequired = true
```

---

## Rule APR-04 — Strategic SLA and Safety Stock Approval

### Condition

```text
StrategicSLAAtRisk = true
AND
SafetyStockConsumed = true
```

### Required Approver

```text
Operations Director
```

### Approval Reason

```text
Strategic SLA orders require safety stock consumption.
```

### Result

```text
ApprovalRequired = true
```

---

# 15. Awaiting Approval Rule

## Rule APR-05 — Approval Required

When any configured approval condition results in:

```text
ApprovalRequired = true
```

the disruption status becomes:

```text
Awaiting Approval
```

The system should communicate:

* Approval is required.
* The required approver.
* The reason for approval.

The system must not automatically approve the request.

---

# 16. Human Approval Integrity

## Rule APR-06 — No Fabricated Approval

The AI system must not claim that a human approval occurred unless an actual approval action or authorized approval record confirms it.

The system may state:

```text
Approval Required
```

but must not state:

```text
Approved
```

without evidence of an actual approval.

---

# 17. Reassessment Rules

The Approval and Reassessment topic supports selective reassessment.

---

## Rule REA-01 — Inventory Data Changed

When:

```text
InventoryStale = true
```

the workflow should identify that inventory information has changed and rerun the Inventory Specialist assessment where the orchestration configuration supports that reassessment.

After the reassessment condition is handled:

```text
InventoryStale = false
```

---

## Rule REA-02 — Supplier Data Changed

When:

```text
SupplierStale = true
```

the workflow should identify that supplier information has changed and rerun the Alternate Supplier Specialist assessment where supported by the orchestration.

After the reassessment condition is handled:

```text
SupplierStale = false
```

---

# 18. Reassessment Loop Limit

## Rule REA-03 — Maximum Reassessment Cycles

The configured maximum reassessment cycle count is:

```text
2
```

When:

```text
ReassessmentCycleCount >= 2
```

the status becomes:

```text
Manual Review
```

The system should stop automated reassessment rather than continuing indefinitely.

---

# 19. Reassessment Counter

When reassessment is performed, the configured cycle counter is incremented:

```text
ReassessmentCycleCount =
ReassessmentCycleCount + 1
```

The Supervisor should use the counter to prevent uncontrolled reassessment loops.

---

# 20. Final Status Rules

The final status should reflect the outcome of the configured assessment workflow.

Possible final outcomes include:

| Condition                                         | Final Status                               |
| ------------------------------------------------- | ------------------------------------------ |
| Validation fails                                  | Insufficient Evidence                      |
| Duplicate detected                                | Existing status preserved / intake stopped |
| Validated and recovery strategy available         | Recovery Plan Proposed                     |
| Partial inventory requires customer coordination  | Customer Action Required                   |
| Human approval required                           | Awaiting Approval                          |
| No viable recovery route                          | Management Escalation                      |
| Unapproved recovery option requires manual action | Manual Review                              |
| Reassessment limit exceeded                       | Manual Review                              |
| Required evidence unavailable                     | Insufficient Evidence                      |

The Supervisor should not select a final status that contradicts the actual specialist or topic results.

---

# 21. Risk Rules

The configured Strategy Resolution topic assigns risk according to the recovery strategy.

| Strategy                                         | Risk     |
| ------------------------------------------------ | -------- |
| Use existing stock                               | Low      |
| Use approved alternate supplier                  | Medium   |
| Reallocate inventory & negotiate customer dates  | Medium   |
| Manual supplier qualification option             | High     |
| Management escalation - no viable recovery route | Critical |

Risk should be based on the configured decision rules and available evidence.

---

# 22. Insufficient Evidence Rule

An assessment should be treated as insufficient when required evidence cannot be established.

Examples include:

* Missing SKU Master record.
* Missing inventory record.
* Missing required purchase-order information.
* Conflicting SKU or supplier references.
* Required connector failure.
* Required specialist output unavailable.

The system should clearly identify the blocking issue.

It must not manufacture a recovery decision to make the workflow appear complete.

---

# 23. Report Creation Rule

The final report should only be created after the Supervisor has consolidated the required assessment results.

The report should contain the final evidence-based outcome.

The Supervisor must verify that the document creation action succeeds before stating that the report was created.

If document creation fails, the final response should clearly state that the report could not be created.

---

# 24. Notification Rule

The authorized stakeholder notification should be sent only after the assessment reaches the appropriate workflow stage.

The notification should contain the relevant final result and required action.

The Supervisor must not claim that the notification was sent unless the configured Outlook action successfully completes.

---

# 25. Rule Precedence

When multiple conditions are true, the configured topic logic determines which decision is applied.

The Supervisor must not invent a new precedence order during execution.

For recovery strategy selection, the configured Strategy Resolution topic provides the decision precedence.

For approval, all configured approval conditions should be evaluated so that the resulting approval requirement reflects the applicable conditions.

---

# 26. Decision Integrity Principles

The following principles apply to every decision:

### Principle 1 — Evidence over assumption

Only supported values should be used for business decisions.

### Principle 2 — Missing evidence remains missing

The system must not replace missing data with invented values.

### Principle 3 — Errors are not business values

A connector failure must not be interpreted as zero inventory, zero demand, or another business value.

### Principle 4 — Approval cannot be fabricated

AI can identify an approval requirement but cannot invent human approval.

### Principle 5 — Status must reflect reality

The disruption status must represent the actual workflow state.

### Principle 6 — Reassessment must be controlled

Automated reassessment must respect the configured maximum cycle count.

### Principle 7 — Reporting must reflect execution

The system must not claim that a Word report was created unless the document action succeeded.

### Principle 8 — Notification must reflect execution

The system must not claim that an email was sent unless the Outlook action succeeded.

---

# 27. Decision Flow Summary

The overall decision model can be summarized as:

```text
Pending Disruption
        |
        v
Disruption Validation
        |
   +----+----+
   |         |
Failed     Passed
   |         |
   v         v
Insufficient  In Assessment
Evidence          |
                  v
          Specialist Assessments
                  |
                  v
           Strategy Resolution
                  |
                  v
        Approval/Reassessment
                  |
        +---------+---------+
        |                   |
 Approval Required      No Approval
        |                   |
        v                   v
Awaiting Approval    Final Strategy/Status
        |                   |
        +---------+---------+
                  |
                  v
          Final Consolidation
                  |
                  v
          Final Response Report
                  |
                  v
        Authorized Notification
```

---

# 28. Expected Decision Outcome

The decision engine is designed to provide a controlled, evidence-based response to supply disruptions.

The expected outcome is not simply a recommendation.

The workflow should establish:

* Whether the disruption is valid.
* Whether sufficient evidence exists.
* What recovery options are available.
* Which recovery strategy is proposed.
* What risk is associated with the strategy.
* Whether human approval is required.
* Whether reassessment is necessary.
* What final status should be assigned.
* What action should be communicated to stakeholders.

This ensures that the final decision remains traceable to the configured workflow, specialist assessments, source evidence, and defined business rules.

```
```
