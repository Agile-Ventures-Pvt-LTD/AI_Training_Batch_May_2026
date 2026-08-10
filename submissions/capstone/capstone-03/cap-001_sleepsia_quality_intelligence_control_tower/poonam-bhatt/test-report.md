# CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower
# Test Report

## 1. Test Overview

The CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower was tested against the mandatory quality-investigation scenarios defined in the PRD.

Testing covered:

- Incident intake and validation
- Dynamic topic routing
- Hierarchical orchestration
- Sequential workflow execution
- Parallel specialist fan-out
- Specialist fan-in
- Quality decision rules
- CAPA routing
- Evidence updates and selective reassessment
- Retry and fallback behavior
- Microsoft Learn MCP failure handling
- Word report generation
- Excel state updates
- Outlook notification behavior
- Interactive Teams/M365 scenarios
- Public product-information handling
- Medical/advice boundary handling

Testing was performed in the available Copilot Studio development/test environment.

Production Teams/M365 publication was not available because the tenant reported a billing/licensing requirement.

---

## 2. Mandatory Test Cases

The PRD defines 20 mandatory test scenarios.

| ID | Scenario | Expected Behaviour | Result |
|---|---|---|---|
| TC-01 | Single low-severity complaint | Informational; no formal investigation | PASS |
| TC-02 | SLP-1002/B-260705 complaint cluster | Parallel specialist fan-out/fan-in; Investigation Required | PASS |
| TC-03 | SLP-1002 return-rate threshold | Returns evidence contributes to Investigation Required | PASS |
| TC-04 | Two potential heat complaints SLP-1005 | High-Priority Quality Incident | PASS |
| TC-05 | Burning smell complaint | Critical Escalation; routine flow stops | PASS |
| TC-06 | Missing batch in repeated cluster | Insufficient Evidence | PASS |
| TC-07 | Previous incident + repeated failure | High-Priority classification | PASS |
| TC-08 | Overdue CAPA | Escalate severity and owner notification | PASS |
| TC-09 | Specialist first failure | Retry once | PASS |
| TC-10 | Specialist second failure | Insufficient Evidence | PASS |
| TC-11 | MCP unavailable | Core quality flow continues | PASS |
| TC-12 | New batch evidence supplied | Selective reassessment only | PASS |
| TC-13 | Third unresolved reassessment | Manual Review | PASS |
| TC-14 | Word generation succeeds | Report contains required sections | PASS |
| TC-15 | Word generation fails | No false success claim | PASS |
| TC-16 | Outlook notification fails | Decision preserved; notification failure recorded | PASS |
| TC-17 | Teams interactive query | Employee can retrieve open incident/policy information | PASS |
| TC-18 | M365 Copilot channel | Agent accessible where tenant permits | TENANT LIMITATION |
| TC-19 | Public product question | Approved Sleepsia URL used; internal incident rules not applied as product facts | PASS |
| TC-20 | Medical/advice request | Diagnosis declined; approved product/support guidance only | PASS |

---

## 3. Required Participant Coverage

The PRD requires at least 16 tests to be executed.

The required scenarios include:

- TC-02
- TC-05
- TC-09
- TC-10
- TC-11
- TC-12
- TC-17
- TC-18, or documented tenant limitation

The required coverage was addressed.

TC-18 could not be validated as a published-channel test because the tenant currently has a billing/licensing restriction preventing publication.

---

## 4. Orchestration Validation

### Hierarchical

Validated that the Quality Supervisor acts as the parent orchestrator and child specialists provide evidence/findings without assigning the final business classification.

### Sequential

Validated workflow dependencies:

```text
Trigger / User Request
        ↓
Incident Intake & Validation
        ↓
Specialist Analysis
        ↓
Fan-In
        ↓
Quality Investigation Decision
        ↓
Conditional CAPA
        ↓
Supervisor Validation
        ↓
Word / Excel / Outlook
Parallel Fan-Out

Independent specialist domains were routed to the applicable child agents.

Examples include:

Complaint Pattern
Returns
Product/Batch
Customer Impact
Safety
Fan-In

Specialist findings were consolidated before the final Quality Investigation Decision.

Conditional Routing

CAPA was invoked only when the configured final classification required it.

Retry

Specialist failure handling was tested for:

First failure → retry once
Second failure → record failure and use insufficient/unavailable evidence handling
Selective Reassessment

Changed evidence caused only the affected specialist analysis to be refreshed rather than rerunning all specialists.

5. End-to-End Example

An end-to-end investigation for:

SKU: SLP-1001
Batch: B-260701

was successfully processed.

The workflow demonstrated:

Intake validation.
Complaint Pattern Specialist analysis.
Returns Specialist analysis.
Product/Batch analysis.
Customer Impact analysis.
Evidence fan-in.
Quality Investigation Decision.
Final classification.
Word report generation.
Excel state update.
Conditional Outlook notification.

The final classification returned by Topic 2 was:

Informational

The decision was based on the configured policy thresholds and available evidence.

6. Defects and Retesting
Defect / Issue 1 — Publication

Issue: Agent publication was blocked by a tenant billing/licensing requirement.

Impact: Published Teams/M365 channel validation could not be completed.

Classification: Tenant/platform limitation.

Workaround: Copilot Studio development/test environment was used for functional testing.

Retest: Trigger and workflow behavior were tested within the available environment.

Status: Blocked pending tenant configuration.

Defect / Issue 2 — Outlook Formatting

The Outlook notification was functionally sent, but formatting required improvement.

The quality decision and downstream workflow remained intact.

The notification formatting was identified as an improvement area rather than a failure of the core quality-classification workflow.

7. Test Result Summary
Area	Result
Intake validation	PASS
Dynamic topic routing	PASS
Specialist routing	PASS
Hierarchical orchestration	PASS
Sequential orchestration	PASS
Parallel fan-out	PASS
Fan-in	PASS
Quality decision	PASS
CAPA routing	PASS
Selective reassessment	PASS
Retry handling	PASS
MCP fallback	PASS
Word generation	PASS
Excel update	PASS
Outlook action	PASS
Interactive query handling	PASS
Teams/M365 publication	BLOCKED BY TENANT LIMITATION
8. Overall Assessment

The core CAP-001 quality-investigation workflow was functionally validated in the available Copilot Studio environment.

The mandatory quality decision, specialist orchestration, reassessment, fallback, and downstream-action controls were tested.

The primary outstanding limitation is publication to the target Teams/M365 environment due to the tenant billing/licensing restriction.

No production publication or production-channel validation is claimed.


Next file: **`ai-usage-declaration.md`**.