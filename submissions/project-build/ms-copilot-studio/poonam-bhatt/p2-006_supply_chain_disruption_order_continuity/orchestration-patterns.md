# Orchestration Patterns

## 1. Purpose

This document describes the orchestration patterns used in the P2-006 Supply Chain Disruption & Order Continuity solution.

The solution uses the Supervisor Agent as the central orchestration component and delegates domain-specific assessment activities to specialist agents.

The orchestration is designed around the workflow defined for the solution:

1. Retrieve the disruption.
2. Validate the disruption.
3. Update the disruption status.
4. Run specialist assessments.
5. Consolidate specialist results.
6. Determine the recovery strategy.
7. Evaluate approval and reassessment conditions.
8. Generate the final response.
9. Send the authorized stakeholder notification.

---

## 2. Supervisor-Orchestrated Architecture

The primary orchestration pattern is a **Supervisor / Specialist** model.

The Supervisor Agent controls the overall workflow.

Specialist agents are responsible for specific business assessment areas.

```text
                         SUPERVISOR
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
     Inventory          Alternate Supplier   Customer & Order
      Impact                 Impact              Impact
    Specialist             Specialist           Specialist
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                     Commercial Impact
                        Specialist
                              |
                              v
                         Supervisor
                              |
                              v
                     Strategy Resolution
                              |
                              v
                    Approval/Reassessment
                              |
                              v
                    Final Response Flow
````

The Supervisor therefore provides centralized control while the specialists provide domain-specific reasoning.

---

## 3. Orchestration Stages

The orchestration can be divided into the following stages:

```text
Stage 1  - Intake
Stage 2  - Validation
Stage 3  - Status Transition
Stage 4  - Specialist Fan-Out
Stage 5  - Specialist Assessments
Stage 6  - Fan-In / Consolidation
Stage 7  - Strategy Resolution
Stage 8  - Approval / Reassessment
Stage 9  - Reporting
Stage 10 - Notification
```

Each stage has a specific purpose.

---

# 4. Stage 1 — Disruption Intake

The workflow begins when the Supervisor receives a disruption assessment request or is invoked through the configured autonomous trigger.

The first responsibility is to identify the disruption that needs to be assessed.

The Supervisor retrieves the appropriate disruption record from the configured business data source.

The record contains the information required by the intake validation process.

Typical information includes:

* Disruption ID
* Supplier ID
* SKU
* Disruption Type
* Reported Date
* Expected Recovery Date
* Affected PO
* Affected Quantity
* Reported Severity
* Status

The Supervisor should use the retrieved record as the source for the downstream workflow.

---

# 5. Stage 2 — Intake Validation

After retrieving the disruption, the Supervisor invokes the Disruption Intake topic.

The topic validates the required information.

The configured validation includes:

* Disruption ID must exist.
* Status must be Pending.
* Supplier ID must exist.
* SKU must exist.
* Disruption Type must exist.
* Reported Date must exist.
* Affected PO must exist.
* Affected Quantity must be positive.

The topic also performs duplicate/existing-disruption checks.

The validation process has two primary outcomes.

### Validation Passed

```text
ValidationStatus = Passed
Status = In Assessment
```

The disruption can proceed to specialist assessment.

### Validation Failed

```text
Status = Insufficient Evidence
```

The workflow should not proceed as if the disruption had passed validation.

---

# 6. Duplicate Detection Pattern

The intake topic also contains duplicate detection.

A disruption is considered already active or resolved when its current status is one of the configured workflow states.

The configured duplicate-status checks include:

```text
In Assessment
Awaiting Approval
Recovery Plan Proposed
Customer Action Required
Management Escalation
Completed
```

If the disruption is already in one of these states, the topic sets:

```text
DuplicateDetected = true
```

and stops normal intake processing.

The purpose of this pattern is to prevent an already processed disruption from being unnecessarily re-assessed.

---

# 7. Stage 3 — Status Transition

A valid Pending disruption is transitioned into the assessment stage.

The configured transition is:

```text
Pending
   |
   v
In Assessment
```

This status transition is important because it indicates that the disruption has successfully passed the initial validation gate.

It also provides a workflow control point for later duplicate detection.

---

# 8. Stage 4 — Specialist Fan-Out

After the disruption enters assessment, the Supervisor launches the required specialist assessments.

The implemented specialist areas are:

```text
Inventory Impact Specialist
Alternate Supplier Specialist
Customer & Order Impact Specialist
Commercial Impact Specialist
```

The orchestration uses a fan-out pattern.

Conceptually:

```text
                         Supervisor
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
        Inventory        Alternate        Customer &
         Impact           Supplier         Order Impact
             |                |                |
             +----------------+----------------+
                              |
                              v
                     Commercial Impact
```

The purpose of fan-out is to separate the assessment responsibilities.

Each specialist focuses on the business information relevant to its domain.

---

# 9. Inventory Impact Assessment

The Inventory Impact Specialist evaluates the inventory consequences of the disruption.

The specialist retrieves the relevant authorized business data and evaluates whether the evidence is sufficient to determine inventory impact.

The configured assessment can involve:

```text
On Hand
Reserved
Quality Hold
Inbound
Daily Consumption
Safety Stock
Available to Promise
Demand Until Recovery
Shortage
```

The specialist should identify missing or conflicting evidence.

For example, if the SKU cannot be found in the required source data, the specialist should report that the inventory assessment cannot be reliably completed.

The specialist should not invent missing inventory values.

---

# 10. Alternate Supplier Assessment

The Alternate Supplier Specialist evaluates whether an alternative supplier can support recovery.

The assessment distinguishes between:

```text
No alternate supplier
        |
        v
No viable supplier recovery route
```

and:

```text
Alternate supplier exists
        |
        +---- Approved
        |
        +---- Unapproved
```

The result is consumed by the recovery-strategy topic.

An approved alternate can support an autonomous recovery strategy.

An unapproved alternate results in a controlled/manual qualification path.

---

# 11. Customer & Order Impact Assessment

The Customer & Order Impact Specialist evaluates the impact of the disruption on customer orders.

The output helps determine whether customer commitments can be fulfilled from the available recovery options.

When inventory is insufficient, the assessment can support prioritization of important customer commitments and determine whether customer action is required.

This output contributes to the final recovery strategy.

---

# 12. Commercial Impact Assessment

The Commercial Impact Specialist evaluates the commercial aspects of the disruption and potential recovery action.

Commercial information can be used by the downstream approval logic.

Examples of configured approval-related information include:

```text
Cost Premium Percentage
Expedite Premium Percentage
```

The specialist does not independently approve the recovery action.

Instead, it provides the information required by the Supervisor's approval/reassessment workflow.

---

# 13. Stage 5 — Specialist Completion

Each specialist returns an assessment result.

The result should communicate whether the specialist completed its assessment and whether the available evidence is sufficient.

For example:

```text
SpecialistName
AssessmentStatus
Confidence
Completed
```

Specialists can return an **Insufficient Evidence** outcome when required source information is unavailable.

This is different from an execution failure.

For example:

```text
Completed = True
AssessmentStatus = Insufficient Evidence
```

can mean that the specialist completed its evaluation but could not produce a reliable business conclusion because the required evidence was unavailable.

---

# 14. Stage 6 — Fan-In / Consolidation

Once the required specialist assessments have been performed, the Supervisor consolidates their outputs.

This is the fan-in stage.

```text
Inventory Impact
       |
Alternate Supplier
       |
Customer & Order Impact
       |
Commercial Impact
       |
       v
+-------------------------+
| Supervisor Consolidation|
+------------+------------+
             |
             v
      Strategy Resolution
```

The Supervisor uses the consolidated information to determine the next workflow stage.

The Supervisor should preserve important evidence limitations when consolidating the specialist results.

---

# 15. Evidence-Based Consolidation

The consolidation stage should not replace missing evidence with assumptions.

For example, if the Inventory Impact Specialist reports:

```text
AvailableToPromise = unavailable
```

the Supervisor should not automatically convert that into:

```text
AvailableToPromise = 0
```

unless the configured business rule explicitly defines that behavior.

Instead, the Supervisor should preserve the evidence limitation and allow the appropriate workflow status or escalation path to be selected.

This ensures that downstream recovery decisions remain evidence-based.

---

# 16. Stage 7 — Recovery Strategy Resolution

After consolidation, the Supervisor invokes the Strategy Resolution topic.

The topic evaluates the recovery conditions using the configured decision precedence.

The implemented branches are:

### Branch 1 — No Viable Recovery Route

```text
AvailableToPromise <= 0
AND
AlternateAvailable = false
```

Result:

```text
ProposedStrategy =
Management escalation - no viable recovery route

FinalStrategyStatus =
Management Escalation

FinalRisk =
Critical
```

---

### Branch 2 — Unapproved Alternate Supplier

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = Unapproved
```

Result:

```text
ProposedStrategy =
Manual supplier qualification option

FinalStrategyStatus =
Manual Review

FinalRisk =
High
```

---

### Branch 3 — Existing Inventory Sufficient

```text
AvailableToPromise >= DemandUntilRecovery
```

Result:

```text
ProposedStrategy =
Use existing stock

FinalStrategyStatus =
Recovery Plan Proposed

FinalRisk =
Low
```

---

### Branch 4 — Approved Alternate Supplier

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = Approved
```

Result:

```text
ProposedStrategy =
Use approved alternate supplier

FinalStrategyStatus =
Recovery Plan Proposed

FinalRisk =
Medium
```

---

### Branch 5 — Partial Inventory

```text
AvailableToPromise < DemandUntilRecovery
AND
AvailableToPromise > 0
```

Result:

```text
ProposedStrategy =
Reallocate inventory & negotiate customer dates

FinalStrategyStatus =
Customer Action Required

FinalRisk =
Medium
```

---

# 17. Decision Precedence

The Strategy Resolution topic uses ordered condition evaluation.

This is important because more than one condition can potentially appear applicable to the same disruption.

The configured topic evaluates the branches in the order defined by the implementation.

The intended precedence is:

```text
No viable route
       ↓
Unapproved alternate
       ↓
Existing inventory sufficient
       ↓
Approved alternate
       ↓
Partial inventory
```

The Supervisor should rely on the configured topic rather than independently inventing a different precedence model.

---

# 18. Stage 8 — Approval Evaluation

After strategy resolution, the Supervisor invokes the Approval/Reassessment topic.

The topic evaluates the configured approval conditions.

Approval is required when one or more configured conditions are true.

The conditions include:

```text
CostPremiumPct > 15
```

```text
ExpeditePremiumPct > 10
```

```text
AlternateAvailable = true
AND
AlternateApprovedStatus = Unapproved
```

```text
StrategicSLAAtRisk = true
AND
SafetyStockConsumed = true
```

When approval is required:

```text
ApprovalRequired = true
Status = Awaiting Approval
```

The topic also identifies the required approver.

---

# 19. Approval Routing

The configured approval routing includes:

| Condition                                     | Required Approver        |
| --------------------------------------------- | ------------------------ |
| Cost premium > 15%                            | Finance Business Partner |
| Expedite premium > 10%                        | Supply Chain Director    |
| Unapproved alternate supplier                 | Sourcing Manager         |
| Strategic SLA risk + safety stock consumption | Operations Director      |

The AI does not fabricate approval.

The configured topic explicitly communicates that human approval cannot be automatically invented or approved by the AI.

---

# 20. Reassessment Pattern

If approval is not required, the workflow evaluates whether reassessment is required.

The topic checks the reassessment cycle count.

The configured maximum automated reassessment count is:

```text
2
```

When the limit has already been reached:

```text
Status = Manual Review
```

This prevents uncontrolled reassessment loops.

---

# 21. Selective Reassessment

The reassessment logic does not require every specialist to be rerun for every data change.

It checks which relevant information has become stale.

The configured indicators include:

```text
InventoryStale
SupplierStale
```

When inventory information changes:

```text
InventoryStale = true
```

the workflow identifies the Inventory Specialist for reassessment.

When supplier information changes:

```text
SupplierStale = true
```

the workflow identifies the Alternate Supplier Specialist for reassessment.

After the relevant stale indicator is handled, it is reset.

---

# 22. Reassessment Cycle Control

Each reassessment increments the cycle count.

Conceptually:

```text
ReassessmentCycleCount
        |
        +---- < 2 ----> Continue automated reassessment
        |
        +---- >= 2 ---> Manual Review
```

The purpose is to prevent the agent from repeatedly reassessing the same disruption without reaching a controlled outcome.

---

# 23. Stage 9 — Final Response

After the recovery strategy and approval/reassessment stages are complete, the Supervisor coordinates the final response.

The final response should reflect the actual workflow outcome.

It should not claim that an assessment, report, or notification was completed unless the corresponding operation actually succeeded.

The final response can communicate:

* Disruption ID.
* Validation status.
* Specialist assessment outcome.
* Recovery strategy.
* Risk.
* Rationale.
* Approval requirement.
* Required approver.
* Final status.
* Evidence limitations.

---

# 24. Word Report Generation

The final response report is generated through the configured Microsoft Word capability.

The Word operation belongs near the end of the orchestration.

The expected pattern is:

```text
Specialist Assessments
        ↓
Consolidation
        ↓
Strategy
        ↓
Approval/Reassessment
        ↓
Final Outcome
        ↓
Populate/Create Word Report
```

The report should therefore not be generated before the assessment result is finalized.

---

# 25. Stakeholder Notification

The authorized stakeholder notification is also a downstream activity.

The intended orchestration is:

```text
Final Outcome
      ↓
Report Created
      ↓
Authorized Stakeholder Notification
```

This prevents a notification from being sent before the assessment result has been finalized.

If report creation fails, the Supervisor should not claim that the report was successfully created.

Likewise, if the notification operation fails, the final response should identify the notification failure rather than reporting successful delivery.

---

# 26. Autonomous Trigger Pattern

The autonomous trigger provides an automated entry point into the workflow.

The trigger can periodically initiate processing of eligible disruption records.

The trigger should hand control to the Supervisor Agent.

The Supervisor remains responsible for validation.

```text
Recurrence Trigger
        |
        v
Supervisor
        |
        v
Retrieve Eligible Record
        |
        v
Validate
        |
        v
Continue Workflow
```

The trigger therefore initiates the workflow but does not bypass the intake validation logic.

---

# 27. Error Handling Pattern

The solution must distinguish between:

1. Business validation failure.
2. Insufficient evidence.
3. Connector/tool failure.
4. Specialist assessment failure.
5. Report-generation failure.
6. Notification failure.

These conditions should not be treated as the same outcome.

For example:

```text
Missing business data
        ↓
Insufficient Evidence
```

is different from:

```text
Excel connector HTTP 500
        ↓
Tool/connector failure
```

A connector failure should not be represented as a successful specialist assessment.

---

# 28. Connector Failure Handling

The specialist workflow depends on configured data connectors.

If a connector returns an error, the Supervisor should recognize that the required evidence may not have been retrieved.

The workflow should avoid producing a confident business conclusion from unavailable data.

For example:

```text
Excel retrieval fails
        ↓
Required evidence unavailable
        ↓
Do not fabricate values
        ↓
Report the evidence/tool limitation
```

This is particularly important for inventory and commercial assessments.

---

# 29. Long-Running Workflow Considerations

The end-to-end workflow involves multiple agent calls and tool operations.

Therefore, the conversation can produce multiple intermediate messages while the workflow is running.

These intermediate messages may include:

* Retrieval progress.
* Validation progress.
* Specialist invocation.
* Specialist assessment output.
* Consolidation.
* Strategy evaluation.
* Approval evaluation.

The final result should be based on the completed workflow state rather than on an individual intermediate message.

---

# 30. Orchestration Responsibility Matrix

| Component                          | Primary Responsibility                   |
| ---------------------------------- | ---------------------------------------- |
| Supervisor Agent                   | End-to-end orchestration                 |
| Disruption Intake Topic            | Input validation and duplicate detection |
| Inventory Impact Specialist        | Inventory assessment                     |
| Alternate Supplier Specialist      | Alternate supplier assessment            |
| Customer & Order Impact Specialist | Customer/order impact                    |
| Commercial Impact Specialist       | Commercial impact                        |
| Strategy Resolution Topic          | Recovery strategy                        |
| Approval/Reassessment Topic        | Approval and reassessment                |
| Excel Data Source                  | Business data retrieval/update           |
| Word Capability                    | Final response report                    |
| Outlook Capability                 | Authorized stakeholder notification      |
| Recurrence Trigger                 | Automated workflow initiation            |

---

# 31. Complete Orchestration Sequence

The complete pattern is:

```text
1. Trigger or request received
            |
            v
2. Supervisor identifies disruption
            |
            v
3. Retrieve disruption record
            |
            v
4. Run Disruption Intake Topic
            |
       +----+----+
       |         |
     FAIL      PASS
       |         |
       v         v
Insufficient  In Assessment
Evidence          |
                  v
5. Specialist Fan-Out
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Inventory  Supplier   Customer/Order
       |          |          |
       +----------+----------+
                  |
                  v
            Commercial
                  |
                  v
6. Fan-In / Consolidation
                  |
                  v
7. Strategy Resolution
                  |
                  v
8. Approval / Reassessment
                  |
          +-------+-------+
          |               |
       Approval        Continue
          |               |
          v               v
Awaiting Approval   Final Outcome
                          |
                          v
9. Create Final Report
                          |
                          v
10. Send Authorized Notification
```

---

# 32. Key Design Principle

The most important orchestration principle is:

**The Supervisor coordinates the workflow; specialist agents provide domain-specific evidence; configured topics make deterministic business-rule decisions; and final reporting/notification occurs only after the workflow reaches the appropriate final stage.**

This separation makes the solution easier to test, understand, and maintain while keeping the implementation aligned with the defined supply continuity workflow.

```
```
