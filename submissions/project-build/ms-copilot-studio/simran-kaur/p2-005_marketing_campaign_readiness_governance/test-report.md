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



