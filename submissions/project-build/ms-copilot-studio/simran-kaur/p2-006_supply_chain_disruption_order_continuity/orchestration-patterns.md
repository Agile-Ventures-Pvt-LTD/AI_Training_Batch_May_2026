# Multi-Agent Orchestration Patterns

This document details how the P2-006 system implements the seven mandatory orchestration patterns in Microsoft Copilot Studio.

---

## 1. Sequential Pattern
The system executes in a strict, linear progression. Stages depend entirely on prior inputs, preventing subsequent steps from executing on invalid data.

```
[Trigger] ➔ [Validation] ➔ [Scope Identification] ➔ [Specialist Assessments] ➔ [Fan-In] ➔ [Recovery Planning] ➔ [Supervisor Decision] ➔ [Approval/Exception Handling] ➔ [Report] ➔ [Excel Update] ➔ [Notification]
```

* **Guardrail**: Specialist analysis is blocked if validation fails (status is set to `Insufficient Evidence` or `Manual Review`).
* **Guardrail**: Recovery planning does not run unless all specialist outputs are successfully consolidated during the Fan-In step.
* **Guardrail**: Reporting and external communication are blocked until the Supervisor makes the final decision.

---

## 2. Parallel Fan-Out/Fan-In Pattern
Once the affected SKU and PO are identified, the Supervisor runs four independent specialist assessments in parallel.

```
                    ┌──> Inventory Impact Specialist ───────┐
                    │                                       │
                    ├──> Alternate Supplier Specialist ─────┼──> [Supervisor Fan-In]
[Scope Identified] ─┤                                       │
                    ├──> Customer & Order Specialist ───────┤
                    │                                       │
                    └──> Commercial Impact Specialist ──────┘
```

* **Independent Sourcing**: Sourcing, Inventory, Customer, and Commercial impact assessments do not depend on each other's outputs.
* **Logical Fan-In**: The Supervisor acts as a barrier, waiting until all four specialist outputs are returned before transferring variables to the Recovery Planning Specialist.

---

## 3. Hierarchical Pattern (Supervisor-to-Specialists)
The Supply Continuity Supervisor acts as the orchestrator. The specialists act as specialized workers.
* **Orchestration Control**: The Supervisor executes child agents, inspects outputs, resolves conflicts, and manages approval routing.
* **No Specialist Autonomy**: Specialists cannot finalize recovery actions or update the disruption status directly. They write recommendations, metrics, and confidence scores back to the Supervisor.

---

## 4. Conditional Routing Pattern
The system dynamically reroutes execution based on operational data and policies:
* **Quality Hold**: Inbound stock marked with a quality hold is excluded from Available to Promise (ATP) calculations.
* **Alternate Supplier Approval**: If an alternate supplier is approved, the system routes to autonomous sourcing. If unapproved, the system routes to a manual supplier qualification workflow.
* **Strategic SLA Protection**: If a customer order is marked as Strategic + SLA and stock is short, the system routes to the highest-priority stock allocation path.
* **Commercial Thresholds**: If an alternate unit cost premium exceeds 15% or an expediting premium exceeds 10%, the system routes to the human approval loop.

---

## 5. Selective Reassessment Pattern
If underlying data changes while a case is being assessed (e.g., alternate supplier capacity drops), the system performs a targeted reassessment instead of rerunning the entire sequence.

```
[Capacity Change] ──> [Detect Stale Alternate Sourcing] ──> [Rerun Sourcing Specialist & Commercial Specialist] ──> [Fan-In Updates]
```

* **Optimization**: The system preserves the unaffected findings from the Inventory and Customer Specialists. Only the Alternate Supplier Specialist and the Commercial Specialist (for cost updates) are reinvoked.
* **Boundary**: A loop counter tracks reassessments, limiting automated loops to **2 cycles** before escalating to `Manual Review`.

---

## 6. Retry/Fallback Pattern
To handle specialist or connector failures:
1. **First Invocation**: If a specialist returns a blank, null, or error output, the Supervisor triggers a retry.
2. **Retry (Attempt 2)**: The Supervisor reinvokes the specialist.
3. **Fallback**: If the retry fails, the Supervisor marks the specialist output status as `Insufficient Evidence` and escalates the case to `Management Escalation` or `Manual Review`.
4. **Invocation Limit**: Max attempts = 2.

---

## 7. Conflict Resolution Pattern
When specialists make contradictory recommendations, the Supervisor resolves them using a deterministic priority list rather than averaging scores:

1. **Safety/Quality Restrictions** (Exclude held stock, unapproved suppliers)
2. **Strategic/SLA-Protected Customer Commitments** (Prioritize these orders)
3. **Supplier Approval Restrictions** (Enforce qualification check)
4. **Inventory Availability and Timing** (Select existing supply over alternate if feasible)
5. **Commercial Approval Requirements** (Check cost/expediting premiums)
6. **Cost Optimization** (Select lowest-cost feasible route)
7. **Lower-Priority Customer Convenience**
