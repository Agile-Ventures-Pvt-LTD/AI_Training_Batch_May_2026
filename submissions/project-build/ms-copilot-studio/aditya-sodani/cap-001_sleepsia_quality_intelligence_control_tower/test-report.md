# Test Report — Sleepsia Quality Intelligence Control Tower

## Test Summary

| Metric | Result |
|---|---:|
| Total Tests Executed | 21 |
| Passed | 20 |
| Failed | 1 |
| Retests | 0 |
| Overall Result | Pass with 1 minor defect |

## Executed Tests

| Test | Expected Result | Status |
|---|---|---|
| Valid complaint C-001 | Validation passes | PASS |
| Invalid complaint C-9999 | Validation fails | PASS |
| Safety override | Critical Escalation | PASS |
| Potential safety cluster | High-Priority Quality Incident | PASS |
| Complaint cluster ≥5 | Investigation Required | PASS |
| Return rate ≥2% | Investigation Required | PASS |
| Previous incident | High-Priority Quality Incident | PASS |
| Missing evidence | Insufficient Evidence | PASS |
| Overdue CAPA | High-Priority Quality Incident | PASS |
| No trigger | Informational | PASS |
| High-Priority CAPA | CAPA created | PASS |
| Critical CAPA | CAPA created | PASS |
| Investigation Required CAPA | CAPA created | PASS |
| Informational CAPA | No active CAPA required | FAIL |
| Return evidence reassessment | Only Returns Specialist reruns | PASS |
| Complaint + Safety reassessment | Only affected specialists rerun | PASS |
| ReassessmentCount >2 | Manual Review | PASS |
| No evidence changed | Findings preserved | PASS |
| Complaint evidence changed | Only Complaint Specialist reruns | PASS |
| Selective reassessment | Unaffected findings preserved | PASS |
| Full quality decision | Exactly one classification + rationale | PASS |

## Test Areas

### Topic 1 — Intake & Validation

Valid and invalid complaint scenarios were tested.

**Result:** PASS

### Topic 2 — Quality Investigation Decision

Safety override, potential safety, complaint cluster, return-rate, previous incident, missing evidence, overdue CAPA and informational scenarios were tested.

**Result:** PASS

### Topic 3 — CAPA Planning & Ownership

Critical, High-Priority and Investigation Required cases were tested for CAPA planning, actions and ownership.

**Result:** PASS

### Topic 4 — Evidence Update & Selective Reassessment

Changed evidence scenarios were tested to verify that only stale specialist analyses are rerun and unaffected findings are preserved.

**Result:** PASS

## Defect

### DEF-001 — Informational CAPA Handling

**Status:** OPEN  
**Severity:** Minor

**Expected:**  
For an Informational classification, the agent should explicitly return:

`CAPA Required = No`

and explain that active CAPA planning is not required unless another configured policy condition applies.

**Actual:**  
The agent correctly declined to authorize CAPA planning but did not provide the expected explicit alternative handling/confirmation.


## Final Status

**20/21 tests passed.**

The core quality decision, policy precedence, CAPA workflows and selective reassessment passed the executed tests. One minor defect remains in the Informational CAPA response and should be fixed and retested before final submission.