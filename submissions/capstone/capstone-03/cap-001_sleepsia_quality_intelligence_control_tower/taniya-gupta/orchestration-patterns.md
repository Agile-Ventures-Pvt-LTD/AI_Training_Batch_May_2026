# Required Orchestration Patterns Implementation

## 1. Sequential Pattern
- **Flow:** Recurrence Trigger → Topic 1 (Intake Validation) → Specialist Fan-Out → Fan-In → Topic 2 (Quality Investigation Decision) → CAPA Specialist & Topic 3 → Supervisor Authorization → Word Report → Excel Update → Outlook Email.
- **Evidence:** Demonstrated in Test TC-05 and TC-02 trajectories.

---

## 2. Parallel Fan-Out / Fan-In Pattern
- **Fan-Out:** After Topic 1 validates intake, Quality Supervisor simultaneously invokes 5 specialist child agents (Complaint Pattern, Returns, Product/Batch, Customer Impact, Safety).
- **Fan-In:** Quality Supervisor pauses execution until all 5 specialists return findings before evaluating Topic 2.
- **Evidence:** Verified in Test TC-02.

---

## 3. Hierarchical Pattern
- **Parent Agent:** Quality Supervisor holds sole authority for severity assignment and external tool execution.
- **Child Agents:** 7 specialist child agents operate under Quality Supervisor supervision, returning domain findings without modifying records or deciding final severity.

---

## 4. Conditional Routing Pattern
- **Safety Indicator = Yes:** Immediately routes to Critical Escalation path.
- **Potential Safety Count ≥ 2:** Routes to High-Priority path.
- **Missing Mandatory Identifier / Missing Batch:** Routes to Invalid / Insufficient Evidence path (Topic 1 gate).
- **Return Rate ≥ 2%:** Routes to Investigation Required path.
- **MCP Unavailable:** Routes to non-blocking fallback while preserving quality workflow.

---

## 5. Selective Reassessment Loop Pattern
- **Trigger:** Topic 4 receives new evidence (e.g., confirmed Batch ID).
- **Selective Execution:** Evaluates which specialists are stale; reruns ONLY stale specialists while preserving unaffected findings.
- **Max Iteration Boundary:** Enforces `ReassessmentCount <= 2`. On the 3rd unresolved cycle (`ReassessmentCount > 2`), sets status to **Manual Review**.
