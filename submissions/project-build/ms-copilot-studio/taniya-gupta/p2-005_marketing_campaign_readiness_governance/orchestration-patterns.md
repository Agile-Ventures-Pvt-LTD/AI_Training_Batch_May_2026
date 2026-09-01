# Mandatory Orchestration Patterns Documentation - P2-005

This document details how the six mandatory multi-agent orchestration patterns are implemented in Microsoft Copilot Studio.

---

## 1. Sequential Pattern
The solution enforces a mandatory execution sequence:
`Recurrence Trigger` -> `Topic 1: Intake & Validation` -> `Parallel Specialist Assessments` -> `Fan-In Consolidation` -> `Child Agent 5: Launch Risk & Decision` -> `Remediation/Approval Topics` -> `Supervisor Validation` -> `Child Agent 6: Reporting & Communication`.

* **Dependency Guard:** Reporting cannot run before decision validation. Specialist assessment cannot start before intake validation passes.

---

## 2. Parallel Fan-Out/Fan-In Pattern
After campaign intake validation locks the record to `In Assessment`, the Supervisor fan-out invokes four independent domain specialists simultaneously:
1. **Budget & Commercial Specialist**
2. **Brand & Content Compliance Specialist**
3. **Channel Readiness Specialist**
4. **Asset Readiness Specialist**

* **Fan-In Consolidation:** The Supervisor waits until all 4 structured outputs are returned before passing consolidated data to Child Agent 5 (Launch Risk & Decision).

---

## 3. Hierarchical Pattern
* **Supervisor Agent:** Controls workflow execution, resolves specialist output conflicts, enforces mandatory policy precedence, authorises remediation, and validates final communication.
* **Specialist Child Agents:** Execute domain-focused analysis with narrow tool access and return structured findings (`SpecialistName`, `AssessmentStatus`, `BlockingIssues`, `Conditions`). Child agents are forbidden from independently issuing final readiness status.

---

## 4. Conditional Routing Pattern
Dynamic branching paths are evaluated automatically based on campaign parameters:
* **High Regulatory Sensitivity:** Triggers additional brand/governance review.
* **Proposed Budget > Approved Budget / > INR 1,000,000:** Routes to Topic 3 (Approval & Finalisation) assigning Marketing Director or VP Marketing approver.
* **Geography = "APAC":** Routes to Regional Marketing Lead approval.
* **Missing Mandatory Assets:** Routes to Topic 2 (Remediation & Selective Reassessment).

---

## 5. Reassessment Loop Pattern
When a campaign fails due to correctable issues:
* Topic 2 increments `ReassessmentCount`.
* Preserves already-passed specialist domain results.
* Re-runs **only** affected failed specialists upon data correction.
* **Bounded Loop:** Maximum 2 automated cycles. If `ReassessmentCount > 2`, escalates status to `Manual Review`.

---

## 6. Fallback and Escalation Pattern
If a child agent or connector tool fails or returns unusable data:
* Supervisor retries the specialist once.
* If retry fails, the domain status is set to `Insufficient Evidence`.
* Unsupported `Ready` classification is strictly blocked, routing the campaign to `Manual Review`.
