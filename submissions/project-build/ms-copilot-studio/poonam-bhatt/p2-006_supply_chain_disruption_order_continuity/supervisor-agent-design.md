# Supervisor Agent Design

## Role & Responsibilities
The **Supply Continuity Supervisor** is the central brain of the system. It is responsible for:
- Detecting new disruptions.
- Enforcing intake validations and locking requests.
- Coordinating specialist child agents.
- Enforcing policy precedence in conflict scenarios.
- Executing final validation of recovery recommendations.
- Managing state transitions.

## Disruption State Transition Model
Only the following states are permitted. The Supervisor prevents invalid state transitions (e.g. going from `Pending` directly to `Completed` without assessment).

| From State | Trigger/Action | To State | Purpose |
| :--- | :--- | :--- | :--- |
| **Pending** | Autonomous recurrence trigger | **In Assessment** | Lock record and start analysis. |
| **In Assessment** | Validation fails (missing PO/SKU/date) | **Insufficient Evidence** | Terminate and flag missing data. |
| **In Assessment** | Duplicate request detected | **Manual Review** | Prevent duplicate analysis. |
| **In Assessment** | Strategy resolved; no approval needed | **Recovery Plan Proposed** | Proceed to execution. |
| **In Assessment** | Strategy resolved; approval required | **Awaiting Approval** | Halt and await human decision. |
| **In Assessment** | No approved route exists | **Management Escalation** | Route to director level. |
| **In Assessment** | Customer date negotiation required | **Customer Action Required** | Halt for customer alignment. |
| **Awaiting Approval** | Human approver approves strategy | **Recovery Plan Proposed** | Transition to execution stage. |
| **Awaiting Approval** | Human approver rejects strategy | **Manual Review** | Halt for planner manual review. |
| **In Assessment** | Automated reassessment count > 2 | **Manual Review** | Halt loop runaway. |
| **Recovery Plan Proposed** | Report created, status updated, email sent | **Completed** | Disruption resolved and logged. |

## Instructions for Supervisor Agent
```text
Role: Supply Continuity Supervisor Agent
Goal: Manage the end-to-end orchestration, validation, and resolution of supply chain disruptions.

Constraints:
1. NEVER allow a direct transition from Pending to Completed without running validations, assessments, and planning.
2. Ensure that any unapproved alternate supplier (SUP-04 for SKU-1003 or SUP-02 for SKU-1008) is NEVER recommended for autonomous sourcing.
3. If validation fails, route immediately to Insufficient Evidence or Manual Review and record the exact failure reason in the Notes column.
4. Stop and route to Awaiting Approval if alternate cost premium exceeds 15% or expedite premium exceeds 10%.
```
