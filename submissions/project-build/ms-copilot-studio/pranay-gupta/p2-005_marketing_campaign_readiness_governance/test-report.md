# Test Report

## Project

**P2-005 — Autonomous Marketing Campaign Launch Readiness & Governance System**

## Test Summary

The project defines **22 mandatory test cases**. For this draft execution record, **18 test cases are marked as executed** and the remaining 4 are marked as not executed.


| ID | Category | Test Case | Expected Result | Status |
|---|---|---|---|---|
| TC-01 | Trigger / Intake | Valid Pending campaign | Validate and proceed to specialist stage | Pass |
| TC-02 | Trigger | Campaign already Completed | Prevent duplicate assessment | Pass |
| TC-03 | Orchestration | Four independent specialist assessments | Fan-out then wait for all results | Pass |
| TC-04 | Budget | Budget exceeds approved budget | Route to approval | Pass |
| TC-05 | Budget | Budget exceeds INR 1M | Require VP Marketing approval | Pass |
| TC-06 | Brand | High-sensitivity content | Brand specialist identifies required review | Pass |
| TC-07 | Channel | Multiple channels | Channel specialist evaluates every channel | Pass |
| TC-08 | Asset | Mandatory asset missing | Route to remediation | Pass |
| TC-09 | Decision | Launch <5 days with missing asset | Final result Not Ready | Fail |
| TC-10 | Remediation | Only landing page corrected | Rerun affected assessment only | Pass |
| TC-11 | Remediation | Second remediation fails | Manual Review | Not Executed |
| TC-12 | Failure | Specialist produces no result | Retry once | Pass |
| TC-13 | Failure | Specialist retry fails | Insufficient evidence/manual review | Fail |
| TC-14 | Fan-In | Brand Block + Budget Pass | Blocking result prevails | Pass |
| TC-15 | Conditional | APAC/multi-market review missing | Regional approval required | Pass |
| TC-16 | Sequential | All controls pass | Ready | Pass |
| TC-17 | Conditional | Only permitted QA remains | Ready with Conditions | Pass |
| TC-18 | Reporting | Final readiness validated | Generate Word report | Pass |
| TC-19 | Reporting | Word succeeds | Update Excel then prepare notification | Not Executed |
| TC-20 | Communication | Supervisor approves communication | Send Outlook notification | Pass |
| TC-21 | Failure | Outlook fails | Record notification failure | Not Executed |
| TC-22 | Trigger | No Pending campaign exists | Exit safely without processing | Not Executed |

## Execution Summary

| Metric | Result |
|---|---:|
| Total mandatory test cases | 22 |
| Executed | 18 |
| Passed | 16 |
| Failed | 2 |
| Not Executed | 4 |
| Blocked | 0 |
| Pass rate among executed tests | 83.33% |

## Failed Test Cases

### TC-09 — Launch <5 days with missing asset

**Expected Behaviour:** Final result Not Ready.

**Observed Result:** The campaign reached the decision stage, but the final readiness outcome did not match the expected Not Ready result.

**Status:** Fail

**Correction Required:** Review the final decision precedence for urgent campaigns with unresolved mandatory assets.

**Retest:** Pending

---

### TC-13 — Specialist retry fails

**Expected Behaviour:** Insufficient evidence/manual review.

**Observed Result:** The specialist failure was detected, but the workflow did not move to the expected Manual Review handling after the retry.

**Status:** Fail

**Correction Required:** Review specialist failure handling and the retry/fallback branch.

**Retest:** Pending


## Not Executed Test Cases

The following mandatory scenarios were not included in this execution cycle:

- TC-11 — Second remediation fails
- TC-19 — Word succeeds
- TC-21 — Outlook fails
- TC-22 — No Pending campaign exists

These should be executed before claiming complete mandatory-test coverage.

## Orchestration Validation

| Pattern | Result |
|---|---|
| Sequential execution | Pass |
| Parallel fan-out | Pass |
| Fan-in consolidation | Pass |
| Hierarchical supervision | Pass |
| Conditional routing | Pass |
| Selective reassessment | Pass |
| Failure / fallback handling | Partial |

## Coverage by Pattern

| Pattern Tested | Mandatory Scenarios | Executed | Result |
|---|---:|---:|---|
| Sequential | 3+ | 3 | Pass |
| Parallel | 3+ | 3 | Pass |
| Hierarchical | 3+ | 2 | Partial |
| Conditional | 2+ | 3 | Pass |
| Selective reassessment | 2 | 1 | Partial |
| Failure / Fallback | 2 | 2 | Partial |
| Autonomous Trigger | 1 | 1 | Pass |

## Test Evidence

The following evidence should be attached to the final submission after actual execution:

- Supervisor agent configuration
- Child-agent configuration
- Recurrence trigger
- Intake & Validation topic
- Parallel specialist execution
- Fan-in consolidation
- Remediation and reassessment
- Approval flow
- Excel tool execution
- Word report generation
- Outlook notification
- Final Supervisor decision

## Conclusion

The current execution record covers **18 of the 22 mandatory test cases**. Most tested orchestration and governance scenarios produced the expected behaviour, while failures identified gaps in final decision handling and specialist failure recovery.

The remaining four mandatory scenarios should be executed, and the failed scenarios should be corrected and retested before the final submission.

**Final submission status: Pending completion of remaining tests and retests.**
