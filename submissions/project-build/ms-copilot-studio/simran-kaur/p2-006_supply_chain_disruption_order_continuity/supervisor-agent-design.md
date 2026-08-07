# Supervisor Agent Design — Supply Continuity Supervisor

The **Supply Continuity Supervisor** is the central orchestrator of the multi-agent system. It manages the disruption lifecycle, controls execution flow, validates incoming data, delegates to specialists, resolves conflicts, and manages approval handoffs.

---

## 1. State Transition Model
The Supervisor enforces a state machine model. The system must prevent invalid transitions (e.g., transition from `Pending` directly to `Completed` without assessment is blocked).

```
   [Pending] 
       │ (Trigger selects record)
       ▼
 [In Assessment] <─────── (Selective Reassessment - max 2 loops)
       │
       ├─────────────────────────┼─────────────────────────┐
       │ (Validation Fails)      │ (Assessments Complete)  │ (No Viable Recovery Route)
       ▼                         ▼                         ▼
 [Insufficient Evidence]   [Recovery Plan Proposed]  [Management Escalation]
       │                         │
       │                         ▼ (Approval Needed)
       │                   [Awaiting Approval]
       │                         │
       │                         ▼ (Approved or Rejected)
       └─────────────────────────┼─────────────────────────┘
                                 │
                                 ▼
                            [Completed]
```

### Table of Disruption States & Transitions

| Current State | Permitted Next States | Business Criteria |
|---|---|---|
| **Pending** | `In Assessment` | Selected by autonomous recurrence trigger; begins validation. |
| **In Assessment** | `Insufficient Evidence`, `Recovery Plan Proposed`, `Management Escalation`, `Manual Review` | Active multi-agent analysis is running. |
| **Awaiting Approval**| `Recovery Plan Proposed`, `Management Escalation`, `Completed` | Human decision required due to commercial or policy thresholds. |
| **Recovery Plan Proposed**| `Awaiting Approval`, `Customer Action Required`, `Completed` | Feasible strategy found, routing for final approval/reporting. |
| **Customer Action Required**| `Completed`, `Management Escalation` | Customer needs to approve split shipment or delivery date change. |
| **Management Escalation**| `Completed`, `Manual Review` | No approved recovery option exists; requires supply chain director intervention. |
| **Insufficient Evidence**| `Manual Review` | Disruption data is missing, corrupted, or specialist fails twice. |
| **Manual Review** | `Completed` | Reassessment loops exhausted (exceeds 2) or validation requires human fix. |
| **Completed** | None | Execution finished; report generated, database updated, notification sent. |

---

## 2. Orchestration Sequence Lifecycle
The Supervisor executes the following logical orchestration loop:

1. **Trigger Ingestion**: Checks `DisruptionRequestsTable` for records where `Status = 'Pending'`. Selects the oldest record and updates the status to `In Assessment`.
2. **Deterministic Validation**: Invokes the **Disruption Intake & Validation** topic. If validation fails, sets status to `Insufficient Evidence` or `Manual Review` and terminates the sequence.
3. **Information Scope**: Extracts the affected SKU, affected Purchase Order (PO), and open customer orders.
4. **Parallel Fan-Out**: Simultaneously executes:
   * Inventory Impact Specialist
   * Alternate Supplier Specialist
   * Customer & Order Impact Specialist
   * Commercial Impact Specialist
5. **Fan-In & Retry Logic**: Consolidates results. If any specialist returns no data, retries once. If retry fails, flags the specialist status as `Insufficient Evidence` and escalates.
6. **Recovery Planning**: Runs the **Recovery Planning Specialist** with consolidated outputs and the Supply Continuity Policy.
7. **Deterministic Resolution**: Invokes the **Recovery Strategy Resolution** topic to apply the precedence rules and resolve any conflicting specialist suggestions.
8. **Approval Routing Check**: Invokes the **Approval, Exception & Reassessment** topic. If approval rules are triggered, transition status to `Awaiting Approval`.
9. **Selective Reassessment Check**: Checks for data changes. Reruns only stale specialists up to 2 cycles.
10. **Downstream Reporting**: Runs the **Reporting Specialist** to generate a Word response report.
11. **Stakeholder Notification**: Sends an Outlook email notification to the designated stakeholder (e.g. Finance, Director, Customer Operations) based on the final decision.
12. **Status Update**: Writes the final state and resolution details to `DisruptionRequestsTable` in Excel.
