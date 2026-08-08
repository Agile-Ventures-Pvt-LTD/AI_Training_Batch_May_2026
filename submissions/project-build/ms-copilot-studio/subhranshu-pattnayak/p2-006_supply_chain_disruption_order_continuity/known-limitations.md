# Known Limitations

## Purpose

This document identifies the current limitations, assumptions, and operational constraints of the Supply Continuity Disruption Response Agent implementation.

These limitations are known at the time of delivery and should be considered during future enhancements and production deployment planning.

---

# 1. Knowledge-Based Specialist Assessments

## Limitation

Specialist agents rely on retrieved workbook data and knowledge-base instructions.

The quality of assessments depends on the completeness and accuracy of the source data.

## Impact

Missing, incomplete, or outdated workbook records may result in:

- Insufficient Evidence findings
- Reduced confidence scores
- Escalation recommendations
- Manual review recommendations

---

# 2. No Autonomous Business Approval

## Limitation

The solution cannot grant business approvals.

## Impact

The system cannot:

- Approve alternate suppliers
- Approve expenditures
- Approve expedited sourcing costs
- Approve contract changes
- Approve inventory consumption exceptions

Human approval remains mandatory where policy requires.

---

# 3. No Transaction Execution

## Limitation

The solution is advisory and orchestration-focused.

## Impact

The system does not:

- Create purchase orders
- Allocate inventory
- Update ERP systems
- Modify supplier records
- Change customer commitments
- Execute procurement transactions

Recommendations must be executed by authorized personnel or downstream systems.

---

# 4. Deterministic Recovery Strategy Resolution

## Limitation

Recovery Strategy Resolution is implemented through rule-based topic logic.

## Impact

The topic selects recovery branches using predefined conditions rather than dynamic optimization.

This improves predictability but may not identify every theoretically optimal recovery path.

---

# 5. Limited Reassessment Cycles

## Limitation

The reassessment workflow is intentionally restricted.

Current limit:

Maximum Reassessment Cycles = 2

## Impact

Cases exceeding the reassessment threshold automatically route to:

- Manual Review

This prevents infinite reassessment loops but may increase human intervention requirements.

---

# 6. Supervisor Does Not Perform Specialist Analysis

## Limitation

The Supervisor acts strictly as an orchestrator.

## Impact

The Supervisor cannot independently:

- Calculate ATP
- Assess supplier capacity
- Evaluate customer impact
- Calculate commercial impact
- Perform recovery planning

If specialist findings are unavailable, the Supervisor cannot continue analysis independently.

---

# 7. Dependency on Structured Data Quality

## Limitation

Several workflow decisions depend on structured workbook fields.

Examples:

- Inventory quantities
- Supplier approval status
- Customer order data
- Recovery dates
- Cost information

## Impact

Incorrect source data may lead to:

- Incorrect recommendations
- Escalations
- Approval routing errors
- Insufficient evidence outcomes

---

# 8. Validation Depends on Required Fields

## Limitation

Workflow execution requires valid disruption records.

Required fields include:

- Disruption ID
- Supplier ID
- SKU
- Reported Date
- Expected Recovery Date
- Affected Quantity
- Severity
- Status

## Impact

Missing values will prevent workflow execution and result in validation failure.

---

# 9. Reporting Depends on Final Decision Availability

## Limitation

The Reporting & Communication Specialist requires a completed Supervisor decision.

## Impact

Reports and notifications cannot be generated when:

- Recovery planning is incomplete
- Approval routing is unresolved
- Specialist findings are missing
- Manual review is pending

---

# 10. Limited Duplicate Detection Logic

## Limitation

The Validation Topic currently initializes duplicate detection but does not perform advanced duplicate analysis.

Current behavior:

DuplicateDetected = False

unless enhanced logic is added.

## Impact

Potential duplicate disruption requests may require manual review.

---

# 11. Power Automate Dependency

## Limitation

Autonomous execution depends on Power Automate orchestration.

## Impact

If Power Automate is unavailable:

- Scheduled execution stops
- Autonomous monitoring stops
- Workflow initiation must be performed manually

---

# 12. Email Delivery Dependency

## Limitation

Stakeholder communication relies on Outlook integration.

## Impact

Notification delivery may fail if:

- Mailbox permissions change
- Outlook connector becomes unavailable
- Recipient information is incomplete

---

# 13. No Historical Learning

## Limitation

The solution does not learn from previous disruption cases.

## Impact

Each disruption is evaluated independently.

Past outcomes do not automatically influence future recommendations.

---

# 14. Policy Changes Require Manual Updates

## Limitation

Business rules are defined within:

- Knowledge Base
- Supervisor Instructions
- Topic Logic

## Impact

Changes to approval policies, escalation rules, or recovery policies require manual maintenance and redeployment.

---

# 15. Evaluation Dataset Limitations

## Limitation

Copilot Studio Evaluation results depend on the quality of test records.

## Impact

Scenarios lacking complete disruption information may produce:

- Requests for additional information
- Incomplete workflow execution
- Tool invocation failures

These results do not necessarily indicate workflow defects.

---

# 16. Agent Not Published Because of Billing Issue

Copilot Studio's publishing feature is currently unavailable due to a billing issue.

## Impact

- All specialist agents are made as lightweight agents and are not published to the Copilot Studio Agent Catalog.
- Supervisor agent is also not published to the Copilot Studio Agent Catalog.
- Link to the Supervisor agent is provided in the README file.
- Not published state of Supervisor agent does not affect the functionality of the solution.
- Not published state of Supervisor agent makes it unavailable for other users to use it in their own environment without Editor Access.

# Future Enhancement Opportunities

Potential future improvements include:

- Dynamic duplicate detection
- Automated approval workflows
- ERP integration
- Multi-level approval chains
- Historical disruption analytics
- Recovery strategy optimization
- Automated reassessment routing
- Real-time inventory synchronization
- Dashboard and monitoring integration

---

# Conclusion

The current implementation satisfies the PRD requirements for workflow orchestration, specialist coordination, recovery governance, approval routing, and reporting.

The identified limitations primarily relate to governance boundaries, data availability, external system dependencies, and intentional controls designed to maintain compliance and human oversight.

---