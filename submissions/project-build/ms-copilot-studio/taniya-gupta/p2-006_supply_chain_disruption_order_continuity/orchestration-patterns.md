# Mandatory Orchestration Patterns — P2-006

### 1. Sequential Pattern
The system strictly enforces logical execution order:
`Trigger → Intake Validation → Scope Identification → Parallel Assessments → Fan-In → Recovery Planning → Supervisor Validation → Approval Routing → Word Report → Excel Update → Outlook Email`.

- **Dependency Guard:** Specialist assessment cannot begin before validation succeeds.
- **Dependency Guard:** Recovery planning cannot execute until all four specialist outputs are available.
- **Dependency Guard:** Word reports and Outlook emails are strictly blocked until the Supervisor validates the final decision.

---

### 2. Parallel Fan-Out Pattern
Once scope is identified (affected SKU, PO, and open orders), the Supervisor triggers four specialist agents independently:
1. `Inventory Impact Specialist`
2. `Alternate Supplier Specialist`
3. `Customer & Order Impact Specialist`
4. `Commercial Impact Specialist`

These sub-agents operate on non-overlapping domains and run in parallel logical fan-out.

---

### 3. Fan-In Consolidation Pattern
The Supervisor acts as the consolidation node, gathering all structured outputs (`AssessmentStatus`, `Confidence`, quantitative findings, blocking issues, and recommendations) from the four parallel specialists into a single unified context before invoking the sequential `Recovery Planning Specialist`.

---

### 4. Hierarchical Pattern
- **Supervisor Agent:** Controls lifecycle, state updates, topic execution, retry loops, and stakeholder communication authorization.
- **Specialist Child Agents:** Perform domain calculations and return standard output contracts. Specialist agents cannot independently declare the final recovery strategy or update Excel state.

---

### 5. Conditional Routing Pattern
Execution branches dynamically based on domain findings:
- `Quality Hold = Yes` → Stock strictly excluded from ATP.
- `Approved = Yes` on alternate supplier → Viable for autonomous recovery option.
- `Approved = No` on alternate supplier → Autonomous selection blocked; routed to manual qualification.
- `Cost Premium > 15%` → Finance Business Partner approval branch.
- `Expedite Premium > 10%` → Supply Chain Director approval branch.
- `No Viable Recovery Route` → Management Escalation branch.

---

### 6. Policy Precedence Pattern (Conflict Resolution)
1. Safety / Quality Hold restrictions (Highest Priority)
2. Strategic + SLA-Protected customer commitments
3. Supplier approval guardrails
4. Inventory availability & ATP timing
5. Commercial approval requirements
6. Cost optimization
7. Lower-priority customer convenience (Lowest Priority)

---

### 7. Selective Reassessment Pattern
When underlying operational data changes (e.g. alternate supplier capacity changes), the Supervisor recalculates stale findings by reinvoking *only* the affected specialist agents (e.g. Alternate Supplier & Commercial Impact), preserving valid results from unaffected specialists (Inventory & Customer Impact).

---

### 8. Retry & Fallback Pattern
If a specialist fails to return a valid result:
- The Supervisor retries the specialist **once**.
- If the retry succeeds, execution proceeds normally.
- If the retry fails a second time, the domain is marked `Insufficient Evidence`.
- Execution-ready recommendations are blocked, and the case escalates to `Manual Review`.
- **Loop Limit:** Automated reassessment is bounded to a maximum of **2 cycles** before forcing `Manual Review`.
