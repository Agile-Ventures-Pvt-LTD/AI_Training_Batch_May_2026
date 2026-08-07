# P2-006 Supply Chain Disruption & Order Continuity

## 1. Project Overview

The P2-006 Supply Chain Disruption & Order Continuity solution is an autonomous multi-agent workflow designed to assess supply chain disruptions and determine appropriate order-continuity recovery actions.

The solution uses a Supervisor Agent to coordinate the assessment and multiple specialist agents to perform focused analysis.

The objective is to provide a structured, evidence-based assessment of a supply disruption while maintaining appropriate workflow status, recovery strategy, approval requirements, and reassessment controls.

The solution is implemented using Microsoft Copilot Studio and configured data, agent, and productivity tools.

---

## 2. Business Objective

A supply disruption can affect inventory availability, alternate sourcing options, customer commitments, commercial exposure, and recovery timelines.

The solution automates the assessment process by coordinating multiple specialized assessments through a central Supervisor Agent.

The workflow is intended to:

- Retrieve a pending disruption.
- Validate the disruption information.
- Prevent duplicate processing.
- Move a valid disruption into assessment.
- Run the required specialist assessments.
- Consolidate specialist findings.
- Determine a recovery strategy.
- Identify whether human approval is required.
- Support controlled reassessment when relevant data changes.
- Produce a final assessment response.
- Support authorized stakeholder notification and final output generation.

The solution is designed to make decisions from available evidence rather than relying on assumptions.

---

## 3. Solution Scope

The implemented solution focuses on supply continuity assessment for disruption records.

The main workflow includes:

1. Disruption intake.
2. Disruption validation.
3. Duplicate detection.
4. Specialist assessment.
5. Recovery strategy resolution.
6. Approval and reassessment evaluation.
7. Final workflow outcome.
8. Final response/report and notification activities where configured.

The solution does not attempt to replace human approval decisions.

Where a condition requires human approval, the workflow identifies the required approver and moves the disruption to the appropriate approval state.

---

## 4. Multi-Agent Architecture

The solution follows a Supervisor and Specialist Agent model.

The Supervisor Agent is responsible for orchestration and workflow control.

The specialist agents are responsible for focused assessments.

The implemented specialist areas are:

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

The Supervisor coordinates these specialists and consolidates their results.

The high-level architecture is:

    Trigger / User Request
             |
             v
        Supervisor
             |
             v
      Disruption Intake
             |
             v
         Validation
             |
             v
       In Assessment
             |
       +-----+-----+-----+
       |     |     |     |
       v     v     v     v
    Inventory  Alternate  Customer  Commercial
      Impact    Supplier   & Order    Impact
       |          |          |          |
       +----------+----------+----------+
                         |
                         v
                 Strategy Resolution
                         |
                         v
                Approval/Reassessment
                         |
                         v
                   Final Outcome

---

## 5. Supervisor Agent

The Supervisor Agent acts as the central coordinator.

Its responsibilities include:

- Retrieving the disruption requiring assessment.
- Starting the disruption intake process.
- Validating required fields.
- Checking for duplicate or already-processed disruptions.
- Updating valid pending disruptions to `In Assessment`.
- Calling the required specialist agents.
- Consolidating specialist results.
- Determining whether sufficient evidence exists.
- Running recovery strategy logic.
- Running approval and reassessment logic.
- Maintaining the appropriate disruption status.
- Producing the final response.

The Supervisor does not independently replace specialist analysis.

Instead, it coordinates the specialist agents and uses their results to determine the next workflow stage.

---

## 6. Disruption Intake

The Disruption Intake topic is responsible for validating the disruption before specialist processing begins.

The validation checks include:

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- AffectedPO
- AffectedQty
- Status

The expected starting status for a disruption entering the normal workflow is:

`Pending`

When the required information is valid, the disruption is moved to:

`In Assessment`

When validation fails, the disruption is routed to:

`Insufficient Evidence`

---

## 7. Duplicate Detection

The Disruption Intake topic also checks whether the disruption is already undergoing assessment or has reached a later workflow state.

The implemented duplicate status checks include:

- `In Assessment`
- `Awaiting Approval`
- `Recovery Plan Proposed`
- `Customer Action Required`
- `Management Escalation`
- `Completed`

If a disruption is detected in one of these states, the workflow identifies it as a duplicate/existing disruption and stops normal intake processing.

This prevents an existing disruption from being unnecessarily restarted.

---

## 8. Specialist Assessments

After successful intake validation, the Supervisor launches the required specialist assessments.

The specialist responsibilities are separated by assessment area.

### Inventory Impact Specialist

The Inventory Impact Specialist evaluates inventory-related evidence and determines whether sufficient information is available to assess inventory availability and recovery impact.

The assessment can involve information such as:

- Available inventory.
- Reserved inventory.
- Quality-hold inventory.
- Inbound inventory.
- Safety stock.
- Demand during the recovery period.
- Available-to-Promise.
- Potential shortage.

If required records are missing or inconsistent, the specialist reports insufficient evidence.

---

### Alternate Supplier Specialist

The Alternate Supplier Specialist evaluates available alternate supplier information and determines whether an alternate supplier can be considered as a recovery option.

The assessment distinguishes between approved and unapproved alternate suppliers.

An unapproved supplier must not automatically become an authorized recovery route.

---

### Customer & Order Impact Specialist

The Customer & Order Impact Specialist evaluates the effect of the disruption on affected customer orders and associated commitments.

The result contributes to the overall continuity assessment and recovery decision.

---

### Commercial Impact Specialist

The Commercial Impact Specialist evaluates relevant commercial considerations associated with the disruption and potential recovery options.

Commercial information can contribute to approval requirements and recovery strategy decisions.

---

## 9. Recovery Strategy

The Strategy Resolution topic evaluates the specialist results and determines the applicable recovery strategy.

The implemented strategy conditions include:

### Existing Inventory

When available inventory is sufficient to cover demand until recovery:

`Use existing stock`

Status:

`Recovery Plan Proposed`

Risk:

`Low`

---

### Approved Alternate Supplier

When an approved alternate supplier is available:

`Use approved alternate supplier`

Status:

`Recovery Plan Proposed`

Risk:

`Medium`

---

### Partial Inventory

When available inventory is greater than zero but insufficient to cover the required demand:

`Reallocate inventory & negotiate customer dates`

Status:

`Customer Action Required`

Risk:

`Medium`

---

### Unapproved Alternate Supplier

When an alternate supplier exists but is unapproved:

`Manual supplier qualification option`

Status:

`Manual Review`

Risk:

`High`

---

### No Viable Recovery Route

When no inventory is available and no alternate supplier exists:

`Management escalation - no viable recovery route`

Status:

`Management Escalation`

Risk:

`Critical`

---

## 10. Approval and Reassessment

The Approval/Reassessment topic determines whether additional human approval is required.

The implemented approval conditions include:

- Cost premium greater than 15%.
- Expedite premium greater than 10%.
- Alternate supplier exists but is unapproved.
- Strategic/SLA exposure requires safety-stock consumption.

When approval is required, the disruption moves to:

`Awaiting Approval`

The workflow identifies the required approver.

The implemented approver roles include:

- Finance Business Partner
- Supply Chain Director
- Sourcing Manager
- Operations Director

The solution does not fabricate or automatically approve a human approval decision.

---

## 11. Reassessment Controls

The solution supports selective reassessment when relevant information changes.

The implemented stale indicators include:

- `InventoryStale`
- `SupplierStale`

When inventory information changes, the workflow can identify the need to reassess the Inventory Specialist.

When supplier information changes, the workflow can identify the need to reassess the Alternate Supplier Specialist.

The solution also limits automated reassessment cycles.

When:

`ReassessmentCycleCount >= 2`

the workflow moves to:

`Manual Review`

This prevents uncontrolled automated reassessment loops.

---

## 12. Evidence-Based Processing

A key design principle is that the workflow should use available source evidence.

The agents should not invent missing values.

For example, if a disruption references a SKU that cannot be found in the configured SKU or inventory data, the specialist should report insufficient evidence.

Similarly, if a purchase order does not match the SKU or supplier referenced by the disruption, the mismatch should be reported as an evidence issue.

This ensures that the final assessment reflects the actual available evidence.

---

## 13. Workflow Statuses

The implemented workflow uses status values to represent the current state of a disruption.

The main statuses include:

- `Pending`
- `In Assessment`
- `Insufficient Evidence`
- `Recovery Plan Proposed`
- `Customer Action Required`
- `Awaiting Approval`
- `Management Escalation`
- `Manual Review`
- `Completed`

The Supervisor and custom topics use these statuses to control workflow progression.

---

## 14. Data and Tools

The solution uses configured data sources and tools to retrieve and process disruption information.

The tools are used according to the workflow stage.

Examples include:

- Retrieving disruption records.
- Updating disruption records.
- Retrieving inventory-related information.
- Retrieving supplier-related information.
- Retrieving customer/order information.
- Retrieving commercial information.
- Creating the final response/report.
- Sending the authorized stakeholder notification.

Tools should only be called when required for the current workflow stage.

---

## 15. Final Outcome

The final outcome depends on the evidence and decisions generated during the assessment.

Possible outcomes include:

- Recovery Plan Proposed.
- Customer Action Required.
- Awaiting Approval.
- Management Escalation.
- Manual Review.
- Insufficient Evidence.
- Completed.

The final response should summarize the assessment outcome and relevant evidence.

Where configured and authorized, the workflow also creates the final response/report and sends the stakeholder notification.

---

## 16. Error and Evidence Handling

The solution distinguishes business evidence problems from technical failures.

Examples of business evidence problems include:

- Missing SKU.
- Missing inventory record.
- Missing supplier evidence.
- Mismatched purchase order.
- Missing customer/order evidence.

These conditions should be represented as insufficient evidence rather than replaced with assumed values.

Technical failures, such as a connector failure, should also not be represented as a successful assessment.

The workflow should preserve the distinction between:

- Successful assessment.
- Insufficient evidence.
- Connector/tool failure.

---

## 17. Expected End-to-End Flow

The intended end-to-end workflow is:

    1. Trigger or user request
             |
             v
    2. Supervisor receives request
             |
             v
    3. Retrieve pending disruption
             |
             v
    4. Validate disruption
             |
             v
    5. Update status to In Assessment
             |
             v
    6. Call specialist agents
             |
             v
    7. Consolidate specialist results
             |
             v
    8. Determine recovery strategy
             |
             v
    9. Evaluate approval/reassessment
             |
             v
    10. Determine final status
             |
             v
    11. Create final response/report
             |
             v
    12. Send authorized stakeholder notification

---

## 18. Project Deliverables

The project repository contains documentation covering:

- Solution summary.
- Architecture.
- Orchestration patterns.
- Supervisor agent design.
- Specialist agent design.
- Custom topics.
- Autonomous trigger.
- Decision rules.
- Test results.
- Known limitations.
- AI usage declaration.
- Dataset notes.
- Implementation screenshots.

The documentation is intended to provide a complete explanation of the implemented P2-006 solution and its assessment workflow.

---

## 19. Design Principles

The solution follows these primary principles:

1. Supervisor-led orchestration.
2. Specialist responsibility separation.
3. Evidence-based assessment.
4. Controlled workflow status transitions.
5. Human approval for configured approval conditions.
6. No fabricated evidence.
7. Duplicate disruption protection.
8. Controlled reassessment.
9. Explicit handling of insufficient evidence.
10. Traceable progression from intake to final outcome.

---

## 20. Conclusion

The P2-006 Supply Chain Disruption & Order Continuity solution demonstrates a multi-agent approach to supply disruption assessment.

The Supervisor coordinates the workflow while specialist agents perform focused assessments.

The custom topics provide validation, strategy resolution, approval handling, and reassessment controls.

The resulting workflow is designed to provide a structured and evidence-based approach to supply continuity assessment while preserving human control where approval is required.