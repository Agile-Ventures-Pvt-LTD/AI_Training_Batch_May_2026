# Orchestration Patterns

## 1. Sequential Orchestration
The workflow uses sequential gates where later stages depend on validated outputs:

`Trigger → Validation → Analysis → Decision → CAPA/Closure → Validation → Reporting → Notification`

This prevents reporting or notification before the quality decision has been finalized.

## 2. Parallel Fan-Out / Fan-In
Independent specialists are invoked in parallel after a valid incident is established. The Supervisor performs fan-in only after the required specialist results are available.

Benefits:
- Independent evidence collection.
- Reduced unnecessary sequential waiting.
- Clear specialist ownership.
- Easier failure isolation.

## 3. Hierarchical Delegation
The Supervisor delegates evidence gathering and action planning but retains final authority.

No child agent should independently change the final quality classification.

## 4. Conditional Routing
Examples:
- Safety indicator → Critical Escalation.
- Complaint cluster threshold exceeded → Investigation Required.
- Return rate at/above the defined threshold → Investigation Required.
- Previous incident plus repeated failure → High-Priority path.
- Missing required evidence → Insufficient Evidence.
- Overdue CAPA → Escalation.
- Microsoft guidance unavailable → manual-review guidance while core quality processing continues.

## 5. Retry and Fallback
A failed specialist is retried once where the workflow permits. A second failure results in an explicit insufficient-evidence outcome rather than invented findings.

## 6. Selective Reassessment
When new evidence changes an existing incident:
1. Identify what evidence changed.
2. Identify specialists whose findings are stale.
3. Rerun only affected specialists.
4. Preserve unaffected findings.
5. Increment the reassessment count.
6. Re-enter the decision stage.

After the permitted automated reassessment limit is reached without resolution, route the incident to Manual Review.

## 7. Controlled Finalization
Word generation, final Excel state update and Outlook notification occur only after Supervisor validation. A failure at one stage does not create a false-success state at another stage.
