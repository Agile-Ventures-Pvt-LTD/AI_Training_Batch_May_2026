# Custom Topics

## 1. Purpose

The P2-006 Supply Chain Disruption & Order Continuity solution uses custom topics to implement defined workflow and decision logic that should execute consistently for every disruption assessment.

The custom topics are coordinated by the Supervisor Agent.

The three implemented custom topics are:

1. Disruption Intake
2. Strategy Resolution
3. Approval/Reassessment

These topics provide deterministic workflow logic for validation, recovery strategy selection, approval handling, and reassessment.

---

# 2. Disruption Intake Topic

## 2.1 Purpose

The Disruption Intake topic is the first decision stage of the disruption assessment workflow.

Its purpose is to validate the retrieved disruption record before the Supervisor allows specialist assessments to proceed.

The topic checks required information and determines whether the disruption can enter the assessment workflow.

---

## 2.2 Trigger

The topic is configured as an event-based topic.

The topic receives the disruption information through its defined input schema.

The main input fields include:

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- ReportedSeverity
- Status

---

## 2.3 Validation Initialization

The topic initializes:

```text
ValidationStatus = Pending
DuplicateDetected = false
````

These variables are used within the topic to track the validation result.

---

## 2.4 Duplicate Disruption Check

The topic first checks whether the disruption is already associated with an active or completed workflow state.

The configured statuses include:

```text
In Assessment
Awaiting Approval
Recovery Plan Proposed
Customer Action Required
Management Escalation
Completed
```

If the disruption is already in one of these states:

```text
DuplicateDetected = true
```

and the validation status is changed to indicate that the disruption is already undergoing assessment or has already been processed.

The intake process is stopped for that record.

---

## 2.5 Required Field Validation

For a non-duplicate disruption, the topic validates the required fields.

The implemented checks include:

### Disruption ID

The topic checks whether `DisruptionID` is blank.

If missing:

```text
ValidationStatus = Failed: Disruption ID is missing
```

### Status

The topic checks that the disruption is still:

```text
Pending
```

If the status is not Pending, validation fails.

### Supplier ID

The topic checks whether `SupplierID` is available.

### SKU

The topic checks whether `SKU` is available.

### Disruption Type

The topic checks whether `DisruptionType` is available.

### Reported Date

The topic checks whether `ReportedDate` is available.

### Affected PO

The topic checks whether `AffectedPO` is available.

### Affected Quantity

The topic checks that:

```text
AffectedQty > 0
```

If the quantity is zero or negative, validation fails.

---

## 2.6 Successful Validation

If all required validation checks pass:

```text
ValidationStatus = Passed
```

and the disruption status is changed to:

```text
In Assessment
```

The topic then communicates that the disruption has successfully passed intake validation.

This status transition allows the Supervisor to proceed with specialist assessment.

---

## 2.7 Failed Validation

If validation fails and the disruption is not a duplicate, the topic changes the status to:

```text
Insufficient Evidence
```

This prevents an invalid disruption from being treated as a fully validated assessment.

The validation result is also returned to the Supervisor.

---

## 2.8 Topic Outputs

The Disruption Intake topic returns:

```text
DuplicateDetected
Status
ValidationStatus
```

These outputs allow the Supervisor to determine whether downstream processing should continue.

---

# 3. Strategy Resolution Topic

## 3.1 Purpose

The Strategy Resolution topic determines the proposed recovery strategy after the relevant assessment information has been collected.

It uses defined decision precedence so that competing recovery conditions are handled consistently.

---

## 3.2 Inputs

The topic receives information including:

* AvailableToPromise
* SafetyStock
* DemandUntilRecovery
* AlternateAvailable
* AlternateApprovedStatus
* StrategicOrdersAtRisk
* SLAOrdersAtRisk
* CostPremiumPct
* ExpeditePremiumPct

These values are used to evaluate the available recovery options.

---

# 4. Decision Precedence

The configured strategy logic evaluates the recovery conditions in a defined order.

The main branches are:

1. No viable recovery route
2. Unapproved alternate supplier
3. Existing inventory sufficient
4. Approved alternate supplier
5. Partial inventory

This allows the topic to select a consistent outcome when multiple conditions may be present.

---

# 5. No Viable Recovery Route

The first strategy condition is:

```text
AvailableToPromise <= 0
AND
AlternateAvailable = false
```

This indicates that:

* sufficient inventory is not available; and
* no alternate supplier is available.

The topic sets:

```text
ProposedStrategy =
Management escalation - no viable recovery route
```

The resulting status is:

```text
Management Escalation
```

The risk is:

```text
Critical
```

The rationale explains that there is no inventory and no alternate recovery route.

---

# 6. Unapproved Alternate Supplier

The topic checks:

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Unapproved"
```

When this condition is met, autonomous sourcing is blocked.

The topic sets:

```text
ProposedStrategy =
Manual supplier qualification option
```

The status becomes:

```text
Manual Review
```

The risk is:

```text
High
```

The rationale indicates that an alternate supplier exists but does not have the required approval status.

---

# 7. Existing Inventory Sufficient

The topic checks:

```text
AvailableToPromise >= DemandUntilRecovery
```

When sufficient inventory is available to cover demand during the recovery period, the topic recommends:

```text
Use existing stock
```

The resulting status is:

```text
Recovery Plan Proposed
```

The risk is:

```text
Low
```

The rationale indicates that available-to-promise inventory is sufficient for the recovery period.

---

# 8. Approved Alternate Supplier

The topic checks:

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Approved"
```

When the condition is met, the topic proposes:

```text
Use approved alternate supplier
```

The resulting status is:

```text
Recovery Plan Proposed
```

The risk is:

```text
Medium
```

The rationale indicates that an approved alternate supplier is available.

---

# 9. Partial Inventory

The topic evaluates the partial inventory condition:

```text
AvailableToPromise < DemandUntilRecovery
AND
AvailableToPromise > 0
```

When inventory is available but insufficient to cover total demand, the topic proposes:

```text
Reallocate inventory & negotiate customer dates
```

The resulting status is:

```text
Customer Action Required
```

The risk is:

```text
Medium
```

The rationale identifies the need to prioritize strategic and SLA customer commitments.

---

# 10. Strategy Outputs

The Strategy Resolution topic returns:

```text
ProposedStrategy
FinalStrategyStatus
RequiredApprover
FinalRisk
Rationale
```

These outputs are consumed by the Supervisor and the downstream approval/reassessment process.

---

# 11. Approval/Reassessment Topic

## 11.1 Purpose

The Approval/Reassessment topic determines whether a proposed recovery action requires human approval and whether reassessment is required when relevant information changes.

The topic supports controlled automation while maintaining human approval boundaries.

---

## 11.2 Approval Initialization

The topic initializes:

```text
ApprovalRequired = false
ApprovalReason = ""
```

The default required approver is:

```text
None
```

---

# 12. Cost Premium Approval

The topic checks:

```text
CostPremiumPct > 15
```

If true:

```text
ApprovalRequired = true
```

The required approver is:

```text
Finance Business Partner
```

The approval reason is:

```text
Cost premium exceeds 15% threshold.
```

---

# 13. Expedite Premium Approval

The topic checks:

```text
ExpeditePremiumPct > 10
```

If true:

```text
ApprovalRequired = true
```

The required approver becomes:

```text
Supply Chain Director
```

The approval reason is:

```text
Expedite premium exceeds 10% threshold.
```

---

# 14. Alternate Supplier Approval

The topic also checks whether an alternate supplier exists but is unapproved.

The configured condition is:

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = "Unapproved"
```

If true:

```text
ApprovalRequired = true
```

The required approver is:

```text
Sourcing Manager
```

The approval reason is:

```text
Alternate supplier lacks qualification status.
```

---

# 15. Safety Stock Approval

The topic checks the condition:

```text
StrategicSLAAtRisk = true
AND
SafetyStockConsumed = true
```

If true:

```text
ApprovalRequired = true
```

The required approver is:

```text
Operations Director
```

The approval reason is:

```text
Strategic SLA orders require safety stock consumption.
```

---

# 16. Awaiting Approval State

When any configured approval condition is met, the topic changes the disruption status to:

```text
Awaiting Approval
```

The workflow also communicates:

* that approval is required;
* who the required approver is;
* why approval is required.

The solution explicitly prevents the AI from fabricating or automatically approving a human approval decision.

---

# 17. Reassessment Logic

If approval is not required, the topic evaluates whether reassessment is necessary.

Reassessment is controlled through:

```text
ReassessmentCycleCount
```

The implemented maximum automated reassessment count is:

```text
2
```

If the maximum is reached, the topic changes the status to:

```text
Manual Review
```

This prevents unlimited automated reassessment.

---

# 18. Inventory Reassessment

The topic checks:

```text
InventoryStale = true
```

When inventory information is stale, the topic identifies that inventory assessment needs to be rerun.

After detecting the condition, the stale indicator is reset.

The workflow can then return to the assessment state.

---

# 19. Supplier Reassessment

The topic checks:

```text
SupplierStale = true
```

When supplier information is stale, the topic identifies that the Alternate Supplier Specialist needs to be rerun.

The stale indicator is then reset.

---

# 20. Reassessment State

When reassessment is performed, the topic increments:

```text
ReassessmentCycleCount
```

and sets the disruption status back to:

```text
In Assessment
```

This allows the updated information to be incorporated into the workflow.

---

# 21. Topic Outputs

The Approval/Reassessment topic returns:

```text
ApprovalReason
ApprovalRequired
Status
RequiredApprover
ReassessmentCycleCount
```

These outputs allow the Supervisor to determine the next workflow action.

---

# 22. Relationship Between the Three Topics

The three topics work together as follows:

```text
Disruption Intake
       |
       v
Validation
       |
       v
In Assessment
       |
       v
Specialist Assessments
       |
       v
Strategy Resolution
       |
       v
Approval/Reassessment
       |
       +------------------+
       |                  |
       v                  v
Awaiting Approval     Reassessment
       |                  |
       |                  v
       |             In Assessment
       |                  |
       +---------> Final Workflow
```

The topics therefore represent distinct workflow responsibilities rather than independent conversations.

---

# 23. Topic Design Principle

The custom topics are designed to implement deterministic business rules defined by the solution.

The principle is:

> Use custom topics for explicit workflow validation and decision rules, while using specialist agents for domain-specific assessment and the Supervisor for overall orchestration.

This keeps the implementation aligned with the defined supply continuity workflow and avoids placing all business logic inside a single agent.

```
```
