# P2-006 — Known Limitations

## Purpose

This document records known limitations and refinement areas identified during implementation and evaluation of the P2-006 solution.

## 1. Outlook Notification Failure Handling

The notification failure scenario requires additional refinement.

The system should ensure that:

- Notification failure is explicitly recorded.
- The final recovery decision is preserved.
- Notification status is tracked separately from recovery status.
- A communication failure does not invalidate the recovery decision.
- Retry or exception handling can be applied where configured.

## 2. No Pending Disruption Trigger

The no-pending-disruption scenario requires additional refinement.

The autonomous trigger should:

- Check for an eligible Pending disruption.
- Avoid unnecessary Supervisor execution.
- Avoid specialist fan-out when no eligible disruption exists.
- Avoid creating a recovery plan.
- Avoid sending unnecessary notifications.
- Record the trigger outcome clearly.

## 3. Human Approval Dependency

Certain actions cannot be completed autonomously.

Examples include:

- Supplier approval
- Supplier qualification
- Purchase-order placement
- Finance approval
- Commercial approval
- Customer agreement
- Management authorization

The system can recommend and route these actions but requires the appropriate human decision.

## 4. Specialist Failure Dependency

Specialist failures are handled through retry and fallback.

The current design allows one retry.

If the second attempt fails:

- The result must be treated as insufficient evidence.
- The system must not fabricate the missing analysis.
- Manual review may be required.

## 5. Reassessment Limit

Selective reassessment is intentionally bounded.

If the case remains unresolved after the configured reassessment limit:

- Automatic reassessment must stop.
- The case should move to Manual Review.
- Appropriate escalation should be generated.

## 6. Data Dependency

Recovery decisions depend on the availability and quality of the underlying disruption, inventory, supplier, customer, order, and commercial data.

Incomplete or inconsistent source data may result in:

- Insufficient evidence.
- Additional validation.
- Manual review.
- Escalation.

The system must not invent missing business data.

## 7. External System Dependency

The solution depends on connected systems for:

- Operational data retrieval.
- Excel updates.
- Word report generation.
- Outlook notifications.

A failure in an external connector may prevent completion of the corresponding downstream action.

## 8. Evaluation Evidence

The test report records 22 evaluated scenarios with 20 passing scenarios and 2 scenarios requiring refinement.

The two identified refinement areas are:

1. Outlook notification failure handling.
2. No-pending-disruption trigger handling.

Future evaluation should confirm these behaviours after refinement.

## 9. Autonomous Decision Boundary

The solution is designed for autonomous orchestration and recommendation, not unrestricted autonomous execution.

Business actions requiring authorization remain outside the autonomous decision boundary.

## 10. Limitation Principle

Known limitations must be handled transparently.

The system must:

- Preserve evidence.
- Clearly identify uncertainty.
- Avoid fabricated results.
- Avoid unauthorized actions.
- Escalate unresolved conditions.
- Preserve the final recovery state when downstream communication fails.
