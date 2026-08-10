# CAP-001 — Test Report

## 1. Test Evidence Source

The evaluation contains **20 test cases (TC-01 to TC-20)** with expected responses, actual responses, and evaluator results where available.

## 2. Overall Evaluation Summary

| Metric | Result |
|---|---:|
| Total test cases | 20 |
| Passed | 17 |
| Failed | 1 |
| Not evaluated / no result recorded | 2 |
| Pass rate among evaluated tests | 94.44% |
| Overall completion | Partial |

**Calculation:** 17 passed out of 18 tests that received an evaluator result = **94.44%**.

> TC-03 and TC-05 have no recorded evaluator result or actual response in the supplied CSV. They are therefore reported as **Not Evaluated**, not as Passed or Failed.

---

## 3. Test Results

| ID | Scenario | Expected Result | Evaluation | Status |
|---|---|---|---|---|
| TC-01 | Single low-severity complaint for SLP-1001 with no safety indicator and no repeated history | Informational; no formal investigation | Pass | PASS |
| TC-02 | Valid SLP-1002 complaint for batch B-260705 with repeated complaints | Run required specialists in parallel using fan-out/fan-in and classify as Investigation Required | Pass | PASS |
| TC-03 | Valid SLP-1002 complaint with return rate above configured threshold | Return-rate evidence contributes to Investigation Required | No result recorded | NOT EVALUATED |
| TC-04 | Two potential heat complaints for SLP-1005 with no confirmed safety indicator | High-Priority Quality Incident | Pass | PASS |
| TC-05 | SLP-1005 complaint with SafetyIndicator = Yes and burning smell | Critical Escalation; stop routine troubleshooting | No result recorded | NOT EVALUATED |
| TC-06 | Repeated complaint cluster with missing/unverifiable BatchID | Insufficient Evidence | Pass | PASS* |
| TC-07 | SKU with repeated failure evidence and previous quality incident | High-Priority Quality Incident | Pass | PASS |
| TC-08 | Active incident with overdue CAPA target date | Escalate severity and notify assigned owner | Pass | PASS |
| TC-09 | Complaint Pattern Specialist fails first attempt | Retry specialist once | Pass | PASS |
| TC-10 | Same specialist fails after retry | Insufficient Evidence | Pass | PASS |
| TC-11 | M365 Guidance Specialist MCP unavailable | Continue core quality flow without MCP guidance | Pass | PASS |
| TC-12 | New batch evidence added to existing incident | Run only stale/affected specialists and preserve unaffected findings | Pass | PASS |
| TC-13 | Third unresolved reassessment cycle | Set status to Manual Review | Pass | PASS |
| TC-14 | Valid incident completes analysis and Word generation succeeds | Report contains required sections and final decision | Fail | FAIL |
| TC-15 | Word report generation fails after decision | Report generation failure recorded; no false success | Pass | PASS |
| TC-16 | Outlook notification fails after decision | Preserve decision and record notification failure | Pass | PASS |
| TC-17 | Employee asks for open incident status in Teams | Provide approved open incident information and relevant policy guidance | Pass | PASS |
| TC-18 | Agent opened from M365 Copilot where tenant permits access | Agent is accessible and responds | Pass | PASS |
| TC-19 | User asks for public Sleepsia product information | Use approved Sleepsia public source; do not apply internal incident rules as product facts | Pass | PASS |
| TC-20 | Customer asks for medical diagnosis related to product use | Decline diagnosis and provide approved product/support guidance | Pass | PASS |

\* **TC-06 evaluator result is Pass, but the actual response contains a governance inconsistency:** the expected response says `Insufficient Evidence`, while the actual response ultimately states `Investigation Required` because the complaint-cluster threshold is independently met. The actual response does correctly preserve the missing BatchID as Missing/Unverified. This should be reviewed against the authoritative project policy before final submission.

---

## 4. Detailed Passed Tests

### TC-01 — Low-Severity Isolated Complaint

**Expected:** Informational; no formal investigation.

**Result:** Pass.

The evaluation confirms that the response was on topic, useful, and supported by the available documents.

---

### TC-02 — Complaint Cluster / Parallel Investigation

**Expected:** Run required specialists in parallel using fan-out/fan-in and classify as Investigation Required.

**Result:** Pass.

This validates the required parallel specialist orchestration and consolidated decision flow.

---

### TC-04 — Repeated Heat Complaints Without Confirmed Safety

**Expected:** High-Priority Quality Incident.

**Result:** Pass.

The response correctly distinguished repeated failure evidence from a confirmed safety indicator.

---

### TC-06 — Missing BatchID

**Expected:** Insufficient Evidence.

**Evaluation:** Pass.

The actual response explicitly preserved the missing BatchID as **Missing/Unverified** and correctly stated that missing evidence must not be treated as Passed.

However, the actual response classified the case as **Investigation Required** because the complaint cluster threshold was independently met. This creates a policy interpretation point that should be resolved before final implementation.

---

### TC-07 — Previous Incident + Repeated Failure

**Expected:** High-Priority Quality Incident.

**Result:** Pass.

The response correctly applied the rule only when both a previous incident and repeated failure mode are present.

---

### TC-08 — Overdue CAPA

**Expected:** Escalate severity and notify the assigned owner.

**Result:** Pass.

The response included incident update, escalation, CAPA reassessment, notification, and report-generation actions.

---

### TC-09 — First Specialist Failure

**Expected:** Retry once.

**Result:** Pass.

The response correctly preserved the failed state and instructed the Supervisor to retry the Complaint Pattern Specialist once.

---

### TC-10 — Specialist Failure After Retry

**Expected:** Insufficient Evidence.

**Result:** Pass.

The response correctly required the failed evidence domain to remain Missing/Unverified and recommended manual review/selective reassessment.

---

### TC-11 — MCP Unavailable

**Expected:** Continue core quality flow without MCP guidance.

**Result:** Pass.

The response correctly applied the fallback:

`Microsoft guidance unavailable - manual review.`

It also correctly stated that MCP availability must not block or alter the core quality decision.

---

### TC-12 — New Batch Evidence

**Expected:** Run only stale/affected specialists and preserve unaffected findings.

**Result:** Pass.

The response correctly identified Product/Batch as the affected evidence domain and preserved unaffected specialist findings.

---

### TC-13 — Third Unresolved Reassessment

**Expected:** Set status to Manual Review.

**Result:** Pass.

The response correctly stopped further autonomous reassessment and required human review.

---

### TC-15 — Word Generation Failure

**Expected:** Report generation failed; do not claim false success.

**Result:** Pass.

The response correctly preserved the quality decision while recording report-generation failure.

---

### TC-16 — Outlook Notification Failure

**Expected:** Preserve decision and record notification failure.

**Result:** Pass.

The response correctly stated that notification failure does not invalidate the quality decision and must not be reported as success.

---

### TC-17 — Open Incident Status

**Expected:** Provide approved open incident information and relevant policy guidance.

**Result:** Pass.

---

### TC-18 — M365 Copilot Access

**Expected:** Agent is accessible and responds when tenant access is permitted.

**Result:** Pass.

---

### TC-19 — Public Sleepsia Product Information

**Expected:** Use the approved Sleepsia public source and keep internal incident rules separate from public product facts.

**Result:** Pass.

---

### TC-20 — Medical Diagnosis Request

**Expected:** Decline diagnosis and provide only approved product/support guidance.

**Result:** Pass.

The response correctly maintained the agent's scope boundary.

---

## 5. Failed Test

### TC-14 — Word Quality Incident Report Contents

**Expected:**

The generated report should contain the required incident identification, final classification/status, complete specialist evidence, decision rationale, missing evidence, CAPA information, reporting/notification status, recommended next action, and relevant human decision boundaries.

**Result:** FAIL.

### Evaluator Finding

The evaluator stated that the response was relevant and based on the knowledge sources, but it was incomplete.

Specifically, the response omitted some details including:

- Full previous incident history evidence.
- Open/overdue CAPA evidence.
- Human decision boundaries contained in the knowledge.

### Required Fix

Update the **Generate Quality Incident Report** design and/or the Supervisor reporting instructions so the final Word report explicitly includes:

1. Incident identification.
2. Final classification.
3. Incident status.
4. Complaint Pattern finding.
5. Returns finding.
6. Product/Batch finding.
7. Customer Impact finding.
8. Safety finding.
9. Previous incident/history evidence where applicable.
10. Open/overdue CAPA information where applicable.
11. Decision rationale.
12. Missing evidence.
13. CAPA details.
14. Report generation status.
15. Notification status.
16. Recommended next action.
17. Applicable human decision boundaries/escalation limitations.

After the change, **retest TC-14**.

---

## 6. Not Evaluated Tests

### TC-03 — Return Rate Threshold

**Expected:** Return-rate evidence contributes to Investigation Required.

No actual response or evaluator result is recorded in the supplied CSV.

**Required retest:** Submit a valid SLP-1002 complaint with return rate above the configured threshold and verify that Returns Specialist evidence contributes to `Investigation Required`.

---

### TC-05 — Confirmed Safety Indicator

**Expected:** Critical Escalation; stop routine troubleshooting.

No actual response or evaluator result is recorded in the supplied CSV.

**Required retest:** Submit a valid SLP-1005 complaint with `SafetyIndicator = Yes` and a burning-smell description. Verify:

- Safety Specialist evidence is identified.
- Final classification is `Critical Escalation`.
- Safety takes precedence over other rules.
- Routine troubleshooting is not continued.
- Required escalation/CAPA behavior is triggered.

---

## 7. Orchestration Validation

The supplied evaluation provides evidence for the following behaviors:

| Capability | Evidence |
|---|---|
| Fan-out / parallel specialist analysis | TC-02 |
| Fan-in / consolidated evidence | TC-02 |
| Specialist retry | TC-09 |
| Failed specialist handling | TC-10 |
| MCP fallback | TC-11 |
| Selective reassessment | TC-12 |
| Reassessment limit / Manual Review | TC-13 |
| CAPA escalation | TC-07, TC-08 |
| Word failure handling | TC-15 |
| Outlook failure handling | TC-16 |

---

## 8. Failure Handling

The evaluation validates the following important failure-handling rules:

### Specialist Failure
- Retry an unavailable/failed specialist once.
- Do not treat failure as Passed.
- Preserve Failed/Missing/Unverified state.
- After repeated failure, record the affected domain as missing/insufficient evidence.

### MCP Failure
- Continue the core quality flow.
- Provide the MCP fallback message.
- Do not allow MCP availability to alter the quality decision.

### Word Failure
- Record `ReportGenerated = Failed`.
- Do not claim successful document generation.
- Preserve the quality decision.

### Outlook Failure
- Record notification failure.
- Do not claim notification success.
- Preserve the quality decision.

---

## 9. Defects and Required Retests

| Defect | Source | Required Action | Retest |
|---|---|---|---|
| TC-14 report content incomplete | Evaluation CSV | Expand report requirements to include previous incident history, open/overdue CAPA, and human decision boundaries | TC-14 |
| TC-03 has no evaluation result | Evaluation CSV | Execute test | TC-03 |
| TC-05 has no evaluation result | Evaluation CSV | Execute test | TC-05 |
| TC-06 expected outcome conflicts with actual classification | Evaluation CSV | Resolve policy precedence between missing BatchID and independently satisfied complaint-cluster threshold | TC-06 |

---

## 10. Final Test Status

**Current status: PARTIALLY PASSED**

The evaluation demonstrates strong coverage of the Supervisor's orchestration, decision governance, failure handling, reassessment, CAPA, MCP fallback, and M365 behavior.

However, the project should not be marked fully passed until:

1. **TC-14 is fixed and retested.**
2. **TC-03 is executed and evaluated.**
3. **TC-05 is executed and evaluated.**
4. **TC-06's policy precedence is explicitly resolved and retested if required.**

## 11. Submission Evidence

Source evaluation file:

`Evaluate Sleepsia Quality Supervisor 260810_1806.csv`

Additional evidence to attach where available:

- Copilot Studio test screenshots.
- Topic execution screenshots.
- Parallel specialist execution evidence.
- Tool execution evidence.
- Word report-generation evidence.
- Outlook notification evidence.
- MCP retrieval/fallback evidence.
- Publishing/billing restriction screenshot.
