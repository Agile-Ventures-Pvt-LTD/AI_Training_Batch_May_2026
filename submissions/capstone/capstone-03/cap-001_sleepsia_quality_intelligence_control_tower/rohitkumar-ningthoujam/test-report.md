# Test Report

## Project

**CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower**

## Test Summary

The implemented solution was tested against the mandatory PRD scenarios covering quality classification, specialist orchestration, retry/fallback, reassessment, MCP availability, Word report generation, Outlook notification, Teams/Microsoft 365 interaction, and product/advice boundaries.

The PRD requires at least 16 test cases, including TC-02, TC-05, TC-09, TC-10, TC-11, TC-12, TC-17 and TC-18, or a documented tenant limitation for TC-18.

## Test Results

| Test Case | Scenario | Expected Result | Result | Status |
|---|---|---|---|---|
| TC-01 | Single low-severity complaint | Informational; no formal investigation | Informational outcome returned | PASS |
| TC-02 | SLP-1002/B-260705 complaint cluster | Parallel specialist fan-out/fan-in; Investigation Required | Parallel assessment and consolidation completed | PASS |
| TC-03 | SLP-1002 return-rate threshold | Returns evidence contributes to Investigation Required | Return evidence considered in decision | PASS |
| TC-04 | Two potential heat complaints for SLP-1005 | High-Priority Quality Incident | High-priority classification returned | PASS |
| TC-05 | Burning smell complaint | Critical Escalation; routine flow stops | Critical escalation handled | PASS |
| TC-06 | Missing batch in repeated cluster | Insufficient Evidence | Evidence gap detected | PASS |
| TC-07 | Previous incident + repeated failure | High-Priority classification | Repeat-incident logic applied | PASS |
| TC-08 | Overdue CAPA | Escalate severity and owner notification | CAPA/owner escalation handled | PASS |
| TC-09 | Specialist first failure | Retry once | Specialist retry executed | PASS |
| TC-10 | Specialist second failure | Insufficient Evidence | Failure fallback handled | PASS |
| TC-11 | MCP unavailable | Core quality flow continues | Quality workflow continued without MCP | PASS |
| TC-12 | New batch evidence supplied | Selective reassessment only | Stale specialist analysis reassessed | PASS |
| TC-13 | Third unresolved reassessment | Manual Review | Case routed for manual review | PASS |
| TC-14 | Word generation succeeds | Report contains required sections | Quality investigation report generated | PASS |
| TC-15 | Word generation fails | No false success claim | Report failure preserved and surfaced | PASS |
| TC-16 | Outlook notification fails | Decision preserved; notification failure recorded | Decision preserved and notification failure handled | PASS |
| TC-17 | Teams interactive query | Employee retrieves open incident/policy information | Interactive query supported | PASS |
| TC-18 | Microsoft 365 Copilot channel | Agent accessible where tenant permits | Channel availability validated where permitted | PASS |
| TC-19 | Public product question | Use approved Sleepsia URL; do not apply internal incident rules as product facts | Public product information handled separately | PASS |
| TC-20 | Medical/advice request | Decline diagnosis; provide approved product/support guidance only | Medical diagnosis/advice restricted | PASS |

## Mandatory Test Coverage

The required priority scenarios were included:

- TC-02 — Parallel fan-out/fan-in
- TC-05 — Critical escalation
- TC-09 — Specialist retry
- TC-10 — Specialist failure fallback
- TC-11 — MCP failure
- TC-12 — Selective reassessment
- TC-17 — Teams interactive query
- TC-18 — Microsoft 365 Copilot channel

All 20 PRD test cases were documented.

## Defects and Retesting

During implementation, Copilot Studio topic validation errors were identified while developing the mandatory custom topics. These included Power Fx identifier errors, variable type mismatches, and invalid/empty expressions.

The affected topic logic was corrected and revalidated before final testing.

No known blocking errors remained in the implemented topics after correction.

## Failure Handling Validation

The following failure behaviours were validated against the PRD:

- Excel read failure stops the affected assessment.
- Excel update failure prevents the complaint from being incorrectly marked as processed.
- Word generation failure preserves the incident decision.
- Outlook notification failure preserves the decision and records notification failure.
- MCP failure does not block the core quality assessment.

## Final Test Status

**Total documented test cases:** 20

**Passed:** 20

**Failed:** 0

**Blocking defects remaining:** 0

**Final Status:** PASS

The implementation satisfies the PRD requirement to document at least 16 test cases and includes the specified mandatory scenarios.