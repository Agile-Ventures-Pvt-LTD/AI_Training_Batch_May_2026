# Test Report

## Test status
This document is a **test-report template** until execution evidence is captured from the completed Copilot Studio solution. Do not mark unexecuted cases as Passed.

The PRD requires at least 16 documented tests and coverage across sequential, parallel fan-out/fan-in, hierarchical, conditional, reassessment-loop, failure/fallback, and end-to-end autonomous behavior.

## Mandatory test matrix

| ID | Scenario | Pattern | Expected |
|---|---|---|---|
| TC-01 | Valid Pending campaign | Sequential | Validate and proceed |
| TC-02 | Campaign already Completed | Conditional | Prevent duplicate assessment |
| TC-03 | Four independent specialist assessments | Parallel | Fan-out then wait for all |
| TC-04 | Budget exceeds approved budget | Conditional | Route to approval |
| TC-05 | Budget exceeds INR 1M | Conditional | VP Marketing approval |
| TC-06 | High-sensitivity content | Hierarchical | Additional review |
| TC-07 | Multiple channels | Parallel | Evaluate all channels |
| TC-08 | Missing mandatory asset | Sequential/Conditional | Remediation |
| TC-09 | Launch <5 days with missing asset | Decision | Not Ready |
| TC-10 | Only landing page corrected | Reassessment loop | Rerun affected assessment only |
| TC-11 | Second remediation fails | Loop limit | Manual Review |
| TC-12 | Specialist produces no result | Fallback | Retry once |
| TC-13 | Specialist retry fails | Fallback | Insufficient evidence/manual review |
| TC-14 | Brand Block + Budget Pass | Fan-in | Blocking result prevails |
| TC-15 | APAC/multi-market review missing | Conditional | Regional approval required |
| TC-16 | All controls pass | Sequential | Ready |
| TC-17 | Only permitted QA remains | Decision | Ready with Conditions |
| TC-18 | Final readiness validated | Sequential | Generate Word report |
| TC-19 | Word succeeds | Sequential | Update Excel then prepare notification |
| TC-20 | Supervisor approves communication | Hierarchical | Send Outlook notification |
| TC-21 | Outlook fails | Failure | Record notification failure |
| TC-22 | No Pending campaign | Trigger | Exit safely |

## Evidence fields
For each executed test record:
- Test Case ID
- Campaign ID
- Trigger execution
- Topic invoked
- Child agents invoked
- Pattern demonstrated
- Specialist outputs
- Expected result
- Actual result
- Final status
- Pass/Fail
- Failure reason
- Remediation
- Retest result
- Screenshot reference



