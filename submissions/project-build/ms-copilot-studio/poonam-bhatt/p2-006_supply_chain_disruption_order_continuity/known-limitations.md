# Known Limitations

## 1. Purpose

This document records the known limitations of the P2-006 Supply Chain Disruption / Order Continuity solution.

The limitations described here are based on the implemented architecture, configured agents, topics, tools, data sources, and testing performed during development.

These limitations should be considered when evaluating the current solution and its readiness for production use.

---

## 2. Data Quality Dependency

The solution depends on the quality and completeness of the configured source data.

The agents can only perform reliable assessments when the required disruption, inventory, supplier, purchase-order, customer, and commercial information is available.

If source data is missing or inconsistent, the resulting assessment may be classified as insufficient evidence.

### Example

If a disruption references a SKU that does not exist in the configured SKU Master or Inventory data, the Inventory Impact Specialist cannot reliably calculate:

- Available to Promise
- Safety stock
- Demand until recovery
- Shortage quantity

The system should report the evidence limitation instead of inventing values.

---

## 3. Source Data Mismatch

The solution may identify inconsistencies between different source records.

Examples include:

- SKU mismatch between disruption and purchase order.
- Supplier mismatch between disruption and purchase order.
- Affected quantity not matching purchase-order quantity.
- Recovery dates not matching purchase-order dates.

These conflicts can prevent a reliable assessment.

The current solution identifies such conflicts but does not automatically correct the underlying source records.

Source-data correction remains an operational responsibility.

---

## 4. Excel Connector Dependency

Several assessment steps depend on the configured Excel Online (Business) connector.

If the connector is unavailable, authentication fails, the workbook is inaccessible, or the connector returns an error, the affected specialist may not be able to retrieve the required evidence.

For example:

```text
Excel Online (Business) HTTP 500
ConnectorRequestFailure
````

is a technical failure and should not be interpreted as a business result such as zero inventory.

The workflow therefore remains dependent on connector availability.

---

## 5. Workbook Availability

The configured Excel workbook and required tables must remain available to the connected tools.

Changes to:

* Workbook location
* Workbook name
* Table name
* Column name
* Table structure
* Access permissions

may cause existing tools to fail.

Any changes to the underlying workbook structure may require corresponding updates to the configured tools and agent instructions.

---

## 6. Tool Configuration Dependency

The specialist agents depend on correctly configured tools.

A tool must have:

* The correct connection.
* The correct workbook or data source.
* The correct table.
* The correct key column.
* Correct input mappings.
* Correct output mappings.

Incorrect mappings may cause a specialist to return incomplete or incorrect results.

---

## 7. Connector Errors Can Interrupt the Workflow

A failure in one of the connected tools may interrupt or reduce the completeness of the overall assessment.

For example, if a Commercial Impact Specialist cannot retrieve its required Excel data, the Supervisor may not receive the expected commercial assessment.

The current solution does not provide a fully independent fallback data platform for failed connectors.

---

## 8. Specialist Agent Dependency

The Supervisor relies on the configured specialist agents to complete their respective assessments.

The current architecture includes:

* Inventory Impact Specialist
* Alternate Supplier Specialist
* Customer & Order Impact Specialist
* Commercial Impact Specialist

If a specialist fails to execute, returns incomplete information, or encounters a connector failure, the Supervisor may not have a complete evidence set.

The Supervisor should identify the missing assessment rather than assuming that the specialist completed successfully.

---

## 9. AI Response Variability

AI-generated responses can vary in wording and presentation even when the underlying assessment is similar.

For this reason, validation should focus on:

* Correct status.
* Correct decision.
* Correct rationale.
* Correct evidence.
* Correct required action.

rather than requiring every natural-language response to be textually identical.

---

## 10. Long Responses and Execution Messages

During testing, the agents may generate extensive intermediate messages describing their reasoning, source retrieval, validation, or assessment activities.

This can make the conversation appear longer than the final business result.

The final submission should focus on the consolidated outcome rather than relying on every intermediate conversational message as the final assessment.

---

## 11. Conversation Runtime

A multi-agent workflow can take longer than a simple conversational response because the Supervisor may:

1. Retrieve the disruption.
2. Validate the record.
3. Update the status.
4. Call multiple specialists.
5. Retrieve additional source data.
6. Consolidate specialist results.
7. Evaluate recovery strategy.
8. Evaluate approval conditions.
9. Perform reassessment checks.
10. Generate the final response.

Execution time therefore depends on the number of agents, tools, connector calls, and data operations involved.

---

## 12. Recurrence Trigger Dependency

The autonomous workflow depends on the configured recurrence trigger.

The trigger must be correctly connected to the Supervisor workflow and must have valid access to the required resources.

If the recurrence trigger does not execute, the autonomous assessment will not begin automatically.

Trigger configuration and connection health therefore remain important operational dependencies.

---

## 13. Manual Testing Limitation

The conversational test can validate the Supervisor's orchestration behavior, but it does not completely reproduce every production trigger scenario.

For complete validation, both of the following should be tested:

* Direct conversational execution.
* Autonomous/recurrence-trigger execution.

This helps distinguish agent-logic issues from trigger or connection issues.

---

## 14. Status Management Dependency

The solution uses disruption status values to control workflow progression.

Important statuses include:

* Pending
* In Assessment
* Insufficient Evidence
* Recovery Plan Proposed
* Customer Action Required
* Awaiting Approval
* Management Escalation
* Manual Review
* Completed

Incorrect source status values can prevent a disruption from entering the expected workflow.

For example, a disruption that is not in `Pending` may fail the initial intake validation.

---

## 15. Duplicate Detection Limitation

Duplicate detection is based on the configured disruption status logic.

A disruption may be treated as already processed when its status indicates that it is already undergoing or has completed assessment.

This means status accuracy is important for duplicate detection.

The current logic does not provide a separate enterprise-wide duplicate-resolution mechanism beyond the configured disruption identifier and status checks.

---

## 16. Approval Dependency

Some recovery decisions require human approval.

The AI can determine that approval is required and identify the configured approver.

However, the AI cannot independently create a genuine human approval.

The workflow therefore depends on the appropriate human approval process where approval is required.

---

## 17. Approval State Does Not Equal Approval Completion

The status:

```text
Awaiting Approval
```

means that approval is required.

It does not mean that the requested action has been approved.

The solution must not treat an approval requirement as an approval confirmation.

---

## 18. Reassessment Limit

The current Approval and Reassessment topic limits automated reassessment cycles.

The configured maximum is:

```text
2
```

When the reassessment limit is reached, the workflow moves the disruption to:

```text
Manual Review
```

This prevents uncontrolled automated reassessment loops.

---

## 19. No Automatic Source Correction

The system can identify data conflicts but does not automatically modify the underlying business data to resolve them.

For example, if:

```text
Disruption SKU = SKU-1009
Purchase Order SKU = SKU-1008
```

the system can report the mismatch.

It should not automatically change either source record.

---

## 20. Date Representation

Dates retrieved from Excel may sometimes appear as Excel serial numbers rather than formatted dates.

For example:

```text
46241
```

may represent a calendar date.

This can make intermediate agent responses less readable.

The underlying date interpretation should be verified against the source data when date accuracy is important.

---

## 21. Recovery Strategy Depends on Available Evidence

The Strategy Resolution topic uses values such as:

* AvailableToPromise
* DemandUntilRecovery
* AlternateAvailable
* AlternateApprovedStatus

If these values are missing or unreliable because of source-data problems, the recovery strategy may not be reliably determined.

The system should not force a strategy simply to complete the workflow.

---

## 22. No Autonomous Approval Override

The solution intentionally does not bypass approval requirements.

If a configured approval condition is triggered, the workflow moves into the applicable approval state.

The system cannot autonomously override the approval requirement.

This is a design limitation as well as a control.

---

## 23. Document Generation Dependency

The final response report depends on the configured Microsoft Word document-generation capability and its connection.

If the Word tool fails, the document may not be created even when the assessment itself is completed.

The Supervisor must verify successful tool execution before reporting that the document has been created.

---

## 24. OneDrive/Document Storage Dependency

The final document is dependent on the configured document storage location and permissions.

If the destination cannot be accessed, the document may fail to save even if the document-generation action itself is configured correctly.

The solution does not independently guarantee document persistence if the storage connection is unavailable.

---

## 25. Email/Notification Dependency

Stakeholder notification depends on the configured Outlook/notification tool and its connection.

If the communication tool fails, the assessment can still exist even though the stakeholder notification was not successfully sent.

The system should distinguish between:

```text
Assessment completed
```

and:

```text
Notification successfully sent
```

These are separate execution outcomes.

---

## 26. No Guarantee of External System Availability

The solution relies on external services and connectors.

Availability of services such as:

* Microsoft Copilot Studio
* Excel Online
* Microsoft Word/OneDrive capabilities
* Outlook/notification capabilities

can affect workflow execution.

A technically correct agent configuration cannot eliminate external service outages or connector failures.

---

## 27. Scope of Current Solution

The solution is designed specifically for the supply chain disruption and order continuity workflow defined for P2-006.

It should not automatically be interpreted as a generalized supply chain management platform.

The implemented workflow focuses on:

* Disruption intake
* Specialist assessment
* Recovery strategy
* Approval/reassessment
* Final response/reporting
* Stakeholder notification

Additional business processes would require additional requirements, data sources, tools, agents, topics, and testing.

---

## 28. Production Readiness Considerations

Before production deployment, the following areas should be validated:

* Connector reliability.
* Workbook availability.
* Data quality.
* Table and column stability.
* Agent permissions.
* Trigger configuration.
* Word document generation.
* Document storage.
* Notification delivery.
* Human approval process.
* Error handling.
* Monitoring and logging.
* Security and access controls.

---

## 29. Summary

The P2-006 solution demonstrates an autonomous multi-agent approach for supply chain disruption and order continuity assessment.

Its primary limitations are related to:

* Source-data quality.
* Connector availability.
* Tool configuration.
* Specialist-agent execution.
* AI response variability.
* Human approval dependencies.
* Document-generation dependencies.
* Notification dependencies.
* Controlled reassessment.

These limitations do not invalidate the implemented workflow. They define the operational conditions under which the workflow can produce reliable results.

The solution should therefore be evaluated as an orchestrated AI-assisted assessment workflow that depends on configured data, tools, connections, deterministic rules, and human oversight.

```
```
