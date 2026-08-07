# Test Report

## Project

**P2-006 — Autonomous Supply Chain Disruption & Order Continuity System**

## Test Summary

The project defines **24 mandatory test cases**. For this draft execution record, **21 test cases are marked as executed** and the remaining 3 are marked as not executed.


| ID | Category | Test Case | Expected Result | Sample Execution Result | Status |
|---|---|---|---|---|---|
| TC-01 | Trigger / Intake | Valid Pending disruption | Validate and continue | Disruption `DR-1007` was selected from Pending status and validation completed successfully. | Pass |
| TC-02 | Conditional | Duplicate In Assessment case | Prevent duplicate processing | Disruption `DR-1012` was already In Assessment and a duplicate run was prevented. | Not Executed |
| TC-03 | Parallel / Fan-In | Four independent impact analyses | Fan-out and fan-in | Inventory, Supplier, Customer, and Commercial assessments completed and were consolidated. | Pass |
| TC-04 | Hierarchical | Strategic SLA order at risk | Customer priority overrides lower concerns | Order `CO-2048` was identified as Strategic/SLA protected and received highest fulfilment priority. | Pass |
| TC-05 | Conditional | ATP protects demand | Prefer existing stock | SKU `SKU-104` had sufficient usable ATP of 420 units against affected demand of 360 units. | Pass |
| TC-06 | Parallel + Hierarchical | ATP partially protects demand | Rank orders and assess alternate supply | SKU `SKU-221` had ATP of 180 units against demand of 320 units; priority orders were protected and alternate supply was assessed. | Not Executed |
| TC-07 | Conditional | Approved alternate meets date | Recommend alternate subject to approval rules | Approved supplier `SUP-ALT-04` showed 5-day lead time against the 7-day recovery requirement. | Pass |
| TC-08 | Conditional | Alternate premium >15% | Finance approval required | Alternate cost premium was calculated at 18.5%; Finance Business Partner approval was required. | Pass |
| TC-09 | Guardrail | Unapproved alternate only | Do not select autonomously | Supplier `SUP-ALT-09` was marked unapproved and was not selected for autonomous recovery. | Pass |
| TC-10 | Sequential | Quality-held inbound | Exclude held quantity | 120 units under Quality Hold were excluded from usable ATP calculation. | Pass |
| TC-11 | Hierarchical | Supplier cancellation on Critical SKU | High/Critical escalation | Critical SKU `SKU-305` was affected by supplier cancellation and the case was escalated as Critical. | Pass |
| TC-12 | Fan-In | Conflicting specialist outputs | Apply decision precedence | Customer and Inventory findings conflicted with cost optimisation; Strategic/SLA priority took precedence. | Pass |
| TC-13 | Conditional | Partial fulfilment allowed | May recommend partial fulfilment | 140 of 250 units were available and partial fulfilment was permitted by the applicable recovery rule. | Pass |
| TC-14 | Conditional | Partial fulfilment prohibited | Prevent split order | Split fulfilment was prohibited for order `CO-2087`; the workflow prevented partial fulfilment. | Pass |
| TC-15 | Fallback | Specialist fails | Retry once | Inventory specialist returned no result on first attempt and was retried successfully. | Pass |
| TC-16 | Fallback | Specialist fails twice | Insufficient Evidence | Alternate Supplier specialist failed twice and the workflow classified the result as Insufficient Evidence. | Pass |
| TC-17 | Selective Loop | Alternate capacity changes | Rerun affected specialists | Alternate supplier capacity changed from 600 to 250 units; affected supplier and recovery assessments were rerun. | Pass |
| TC-18 | Loop Limit | Second reassessment unresolved | Manual Review | Second reassessment did not produce a viable approved route and the case moved to Manual Review. | Pass |
| TC-19 | Hierarchical | No viable approved recovery route | Management Escalation | No approved recovery route protected the critical demand; Management Escalation was triggered. | Pass |
| TC-20 | Sequential | Final recovery plan validated | Generate Word report | Recovery plan for `DR-1018` was validated and the Word recovery report generation step completed. | Pass |
| TC-21 | Sequential | Report created | Update Excel | After report creation, the disruption record was updated with the recovery-plan status. | Pass |
| TC-22 | Hierarchical | Supervisor authorises email | Send Outlook notification | Supervisor authorised communication and the stakeholder notification was sent successfully. | Not Executed |
| TC-23 | Failure | Outlook fails | Record notification failure | Outlook action failed during the test and the notification failure was recorded without reporting success. | Pass |
| TC-24 | Trigger | No Pending disruption | Exit safely | No Pending disruption was available during the trigger run and the workflow exited without invoking assessment agents. | Pass |

## Execution Summary

| Metric | Result |
|---|---:|
| Total mandatory test cases | 24 |
| Executed | 21 |
| Passed | 21 |
| Failed | 0 |
| Not Executed | 3 |
| Blocked | 0 |
| Pass rate among executed tests | 88% |


## Orchestration Validation

| Pattern | Result |
|---|---|
| Sequential execution | Pass |
| Parallel fan-out | Pass |
| Fan-in consolidation | Pass |
| Hierarchical supervision | Pass |
| Conditional routing | Pass |
| Selective reassessment | Pass |
| Failure / fallback handling | Pass |
| Guardrail handling | Pass |
| Autonomous trigger | Pass |

## Coverage by Pattern

| Pattern Tested | Mandatory Scenarios | Executed | Result |
|---|---:|---:|---|
| Sequential | 3+ | 4 | Pass |
| Parallel / Fan-In | 3+ | 3 | Pass |
| Hierarchical | 3+ | 4 | Pass |
| Conditional | 3+ | 6 | Pass |
| Selective reassessment | 2 | 2 | Pass |
| Failure / Fallback | 2+ | 3 | Pass |
| Guardrail | 1 | 1 | Pass |
| Autonomous Trigger | 1 | 2 | Pass |

## Test Evidence

The following evidence should be attached to the final submission after actual execution:

- Supervisor agent configuration
- Child-agent configuration
- Recurrence trigger
- Disruption Intake & Validation topic
- Parallel specialist execution
- Fan-in consolidation
- Recovery Planning
- Recovery Strategy Resolution
- Approval and exception handling
- Selective reassessment
- Excel tool execution
- Word report generation
- Outlook notification
- Final Supervisor decision

## Conclusion

The draft execution record covers the **24 mandatory P2-006 test scenarios** and demonstrates the required trigger, orchestration, decision, recovery, failure-handling, reporting, and communication behaviours.

For the final submission, replace all sample execution values and statuses with actual Copilot Studio test evidence. The final report should reflect the real number of executed, passed, failed, and not-executed test cases.

**Final submission status: Pending verification against actual execution evidence.**
