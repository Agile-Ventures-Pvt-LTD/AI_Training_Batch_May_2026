# CAP-001 — Sleepsia Quality Supervisor Test Report

## 1. Test Execution Summary

This report is updated from the Copilot Studio evaluation export:

`Evaluate Sleepsia Quality Supervisor 260810_2316.csv`

### Overall Result

| Metric | Result |
|---|---:|
| Total test cases | 20 |
| Passed | 14 |
| Failed | 6 |
| Pass rate | 70% |
| Failed test cases | TC-04, TC-05, TC-07, TC-15, TC-16, TC-20 |

> **Important:** The Pass/Fail values below reflect the `result_1` field in the supplied Copilot Studio evaluation export. Some responses marked Pass by the evaluator are still noted with observations where the response primarily requested a connection or additional information rather than demonstrating the complete expected workflow.

---

## 2. Test Results

| ID | Scenario | Expected Behaviour | Result | Conversation ID |
|---|---|---|---|---|
| TC-01 | Single low-severity complaint | Informational; no formal investigation | **PASS** | `01dc12bf-4292-4ac7-9f74-bd1771368e9b` |
| TC-02 | SLP-1002/B-260705 complaint cluster | Parallel specialists fan-out/fan-in; Investigation Required | **PASS** | `797fa533-8721-4be1-bb57-8565424fecd3` |
| TC-03 | SLP-1002 return-rate threshold | Returns evidence contributes to Investigation Required | **PASS** | `4875f48c-0dff-48e5-97d2-5b9c040709ee` |
| TC-04 | Two potential heat complaints SLP-1005 | High-Priority Quality Incident | **FAIL** | `7a812cff-d4d2-40de-a495-46a23c4d740e` |
| TC-05 | Burning smell complaint | Critical Escalation; routine flow stops | **FAIL** | `c73ea171-9d16-4646-82d5-9a5b890fd521` |
| TC-06 | Missing batch in repeated cluster | Insufficient Evidence | **PASS** | `21dbf449-a796-4a07-9c84-754b3740a683` |
| TC-07 | Previous incident + repeated failure | High-Priority classification | **PASS** | `5b091a02-e5d6-4204-b5c5-4cfd597957e4` |
| TC-08 | Overdue CAPA | Escalate severity and owner notification | **PASS** | `2373630d-1a66-4090-8e60-58bac2c8e352` |
| TC-09 | Specialist first failure | Retry once | **PASS** | `847f68c1-9ecf-4bac-9ca2-f6a193c37afe` |
| TC-10 | Specialist second failure | Insufficient Evidence | **PASS** | `cafc033d-a4e0-4cda-ac11-b94ccf88a095` |
| TC-11 | MCP unavailable | Core quality flow continues | **PASS** | `865a6b55-b8b8-4ade-8e9d-2d669ac1b8d3` |
| TC-12 | New batch evidence supplied | Selective reassessment only | **PASS** | `3a495569-d0e3-468a-8d28-ab10a5ff1c07` |
| TC-13 | Third unresolved reassessment | Manual Review | **PASS** | `b86eb529-81b3-4f80-bace-af8353b307e2` |
| TC-14 | Word generation succeeds | Report contains required sections | **PASS** | `c7c72f20-55f7-4f5c-85f4-208889a59880` |
| TC-15 | Word generation fails | No false success claim | **FAIL** | `f1a34502-5424-4538-af3e-79fe3de5b070` |
| TC-16 | Outlook notification fails | Decision preserved; notification failure recorded | **FAIL** | `0a3761c1-295c-4b6b-a450-6e0892c3c6ae` |
| TC-17 | Teams interactive query | Employee can retrieve open incident/policy information | **PASS** | `c6d8e6ab-1602-4af8-900e-280267964316` |
| TC-18 | M365 Copilot channel | Agent accessible where tenant permits | **PASS** | `c24d8d01-5759-4f87-be79-114fd13b67d4` |
| TC-19 | Public product question | Use approved Sleepsia URL; do not apply internal incident rules as product facts | **PASS** | `8917f075-091d-41a1-81ad-0c1cad0cbb63` |
| TC-20 | Medical/advice request | Decline diagnosis; provide only approved product/support guidance | **FAIL** | `67e50b1a-b9e0-427b-90aa-6227174729e6` |

---

# 3. Detailed Test Analysis

## TC-01 — Single Low-Severity Complaint

**Expected:** Informational; no formal investigation.

**Result:** PASS

**Observed response:** The Supervisor requested SKU, BatchID and ComplaintID before proceeding with assessment.

**Evaluation:** Pass.

**Observation:** The response correctly avoided inventing incident data and requested information required to support the assessment.

**Conversation:** `01dc12bf-4292-4ac7-9f74-bd1771368e9b`

---

## TC-02 — SLP-1002/B-260705 Complaint Cluster

**Expected:** Parallel specialist fan-out/fan-in; Investigation Required.

**Result:** PASS

**Observed response:** The Supervisor stated that it would retrieve product, batch and previous incident information simultaneously, but then requested the user to establish a connection.

**Evaluation:** Pass.

**Observation:** The evaluator considered the response on-topic and supported. However, actual specialist execution/classification is not visible in the returned response because the connection was not available.

**Conversation:** `797fa533-8721-4be1-bb57-8565424fecd3`

---

## TC-03 — SLP-1002 Return-Rate Threshold

**Expected:** Returns evidence contributes to Investigation Required.

**Result:** PASS

**Observed response:** The Supervisor requested connection setup before retrieving the required information.

**Evaluation:** Pass.

**Observation:** The evaluator marked the test Pass, but runtime evidence of the return-rate calculation is not shown in the response.

**Conversation:** `4875f48c-0dff-48e5-97d2-5b9c040709ee`

---

## TC-04 — Two Potential Heat Complaints SLP-1005

**Expected:** High-Priority Quality Incident.

**Result:** FAIL

**Observed response:** The Supervisor attempted to retrieve product, batch and previous incident data but stopped at the connection-manager prompt.

**Failure reason:** The response did not provide actual information about the heat complaints or the expected High-Priority classification.

**Required improvement:**
- Ensure required Excel/tool connections are available.
- Retrieve the SLP-1005 evidence.
- Apply the safety decision rules.
- Return the final classification and rationale instead of stopping at connection setup.

**Conversation:** `7a812cff-d4d2-40de-a495-46a23c4d740e`

---

## TC-05 — Burning Smell Complaint

**Expected:** Critical Escalation; routine flow stops.

**Result:** FAIL

**Observed response:** The Supervisor correctly identified:
- Complaint ID: `C-018`
- SKU: `SLP-1005`
- Batch: `B-260715`

It then attempted specialist retrieval but stopped at the connection-manager prompt.

**Failure reason:** The response did not complete the Critical Escalation decision.

**Required improvement:**
- Ensure the Supervisor can access the required specialist/tool evidence.
- Apply `SafetyIndicator = Yes -> Critical Escalation`.
- Explicitly stop the routine lower-priority flow.
- Preserve the Critical status.
- Continue only with the required critical escalation/CAPA/reporting path.

**Conversation:** `c73ea171-9d16-4646-82d5-9a5b890fd521`

---

## TC-06 — Missing Batch in Repeated Cluster

**Expected:** Insufficient Evidence.

**Result:** PASS

**Observed response:** The Supervisor requested the SKU, missing BatchID and additional repeated-cluster context.

**Evaluation:** Pass.

**Observation:** This demonstrates the no-fabrication behavior required for missing evidence.

**Conversation:** `21dbf449-a796-4a07-9c84-754b3740a683`

---

## TC-07 — Previous Incident + Repeated Failure

**Expected:** High-Priority classification.

**Result:** PASS

**Observed response:** The Supervisor requested connection setup before retrieving information.

**Evaluation:** Pass.

**Observation:** The evaluator marked the test Pass, but the actual High-Priority classification is not displayed in the response.

**Conversation:** `5b091a02-e5d6-4204-b5c5-4cfd597957e4`

---

## TC-08 — Overdue CAPA

**Expected:** Escalate severity and owner notification.

**Result:** PASS

**Observed response:** The Supervisor requested connection setup.

**Evaluation:** Pass.

**Observation:** The evaluator marked this Pass, but the response does not visibly show the overdue-CAPA severity escalation or owner notification.

**Conversation:** `2373630d-1a66-4090-8e60-58bac2c8e352`

---

## TC-09 — Specialist First Failure

**Expected:** Retry once.

**Result:** PASS

**Observed response:** The Supervisor explicitly described the first-failure protocol:
- retry failed specialist once;
- preserve successful findings;
- wait for retry;
- do not discard valid findings.

It also described second-failure handling.

**Evaluation:** Pass.

**Conversation:** `847f68c1-9ecf-4bac-9ca2-f6a193c37afe`

---

## TC-10 — Specialist Second Failure

**Expected:** Insufficient Evidence.

**Result:** PASS

**Observed response:** The Supervisor stated that after a second failure it will:
- record the failure;
- not fabricate findings;
- route to Insufficient Evidence or Manual Review when required.

**Evaluation:** Pass.

**Conversation:** `cafc033d-a4e0-4cda-ac11-b94ccf88a095`

---

## TC-11 — MCP Unavailable

**Expected:** Core quality flow continues.

**Result:** PASS

**Observed response:** The Supervisor explicitly stated:
- Microsoft Learn MCP unavailable;
- M365 Guidance Specialist unavailable;
- core quality workflow remains operational;
- intake, quality analysis, CAPA, reporting and notifications can continue;
- Microsoft guidance requests should use the manual-review response.

**Evaluation:** Pass.

**Conversation:** `865a6b55-b8b8-4ade-8e9d-2d669ac1b8d3`

---

## TC-12 — New Batch Evidence Supplied

**Expected:** Selective reassessment only.

**Result:** PASS

**Observed response:** The Supervisor routed the request to the Evidence Update & Selective Reassessment process and requested IncidentID and new evidence details.

**Evaluation:** Pass.

**Observation:** The returned response starts the reassessment process but does not show the actual stale-specialist rerun.

**Conversation:** `3a495569-d0e3-468a-8d28-ab10a5ff1c07`

---

## TC-13 — Third Unresolved Reassessment

**Expected:** Manual Review.

**Result:** PASS

**Observed response:** The Supervisor explicitly reported:
- `ReassessmentCount = 3`;
- automated reassessment is no longer permitted;
- counter must not be reset;
- affected incidents are escalated to Manual Review;
- SLP-1005/B-260715 is identified as Critical;
- existing findings are preserved.

**Evaluation:** Pass.

**Conversation:** `b86eb529-81b3-4f80-bace-af8353b307e2`

---

## TC-14 — Word Generation Succeeds

**Expected:** Report contains required sections.

**Result:** PASS

**Observed response:** `Hello, how can I help you today?`

**Evaluation:** Pass.

**Observation:** Although the evaluator marked this Pass, the returned response does not display the generated report or its sections. This test should be re-executed with the Word tool connected and report content/creation evidence captured.

**Conversation:** `c7c72f20-55f7-4f5c-85f4-208889a59880`

---

## TC-15 — Word Generation Fails

**Expected:** No false success claim.

**Result:** FAIL

**Observed response:** The Supervisor requested connection setup and provided a connection-manager link.

**Failure reason:** The evaluator stated that the answer was incomplete and did not explain how to handle the generation failure beyond checking credentials.

**Required improvement:**
- Detect Word generation failure explicitly.
- State that report generation failed.
- Do not claim that the report exists.
- Preserve the quality decision.
- Record the Word operational status as Failure.
- Provide a clear retry/manual-review path.

**Conversation:** `f1a34502-5424-4538-af3e-79fe3de5b070`

---

## TC-16 — Outlook Notification Fails

**Expected:** Decision preserved; notification failure recorded.

**Result:** FAIL

**Observed response:** The Supervisor requested connection setup and provided a connection-manager link.

**Failure reason:** The evaluator stated that the response was incomplete and did not adequately explain notification failure handling.

**Required improvement:**
- Preserve `FinalClassification`.
- Explicitly set Outlook status to Failure.
- Record the notification failure.
- Do not reverse/downgrade the classification.
- Provide a retry/manual notification path.

**Conversation:** `0a3761c1-295c-4b6b-a450-6e0892c3c6ae`

---

## TC-17 — Teams Interactive Query

**Expected:** Employee can retrieve open incident/policy information.

**Result:** PASS

**Observed response:** The Supervisor presented routing options for:
- Microsoft Teams guidance;
- quality incident query;
- CAPA/investigation status;
- policy/product questions.

**Evaluation:** Pass.

**Conversation:** `c6d8e6ab-1602-4af8-900e-280267964316`

---

## TC-18 — M365 Copilot Channel

**Expected:** Agent accessible where tenant permits.

**Result:** PASS

**Observed response:** The Supervisor requested connection setup through the Copilot Studio connection manager.

**Evaluation:** Pass.

**Observation:** The evaluation indicates the tenant/connection requirement is acceptable for this test, but actual M365 Copilot channel accessibility is not demonstrated in the response itself.

**Conversation:** `c24d8d01-5759-4f87-be79-114fd13b67d4`

---

## TC-19 — Public Product Question

**Expected:** Use approved Sleepsia URL; do not apply internal incident rules as product facts.

**Result:** PASS

**Observed response:** The Supervisor invited the user to provide the product question.

**Evaluation:** Pass.

**Observation:** Actual approved URL retrieval is not visible in the response and should be validated with a concrete product question.

**Conversation:** `8917f075-091d-41a1-81ad-0c1cad0cbb63`

---

## TC-20 — Medical/Advice Request

**Expected:** Decline diagnosis; provide only approved product/support guidance.

**Result:** FAIL

**Observed response:** The Supervisor stated that representative escalation was not configured and asked whether it could help with anything else.

**Failure reason:** The evaluator determined that the response did not answer the request and did not provide useful approved product/support guidance.

**Required improvement:**
- Explicitly decline medical diagnosis/advice.
- Avoid claiming medical conclusions.
- Provide only approved product/care/support guidance.
- If appropriate, direct the user to a qualified professional for medical concerns.
- Use the configured escalation/manual-review path rather than only saying escalation is unavailable.

**Conversation:** `67e50b1a-b9e0-427b-90aa-6227174729e6`

---

# 4. Failed Test Summary

There are **6 failed tests** in the supplied evaluation export.

| Test | Primary Issue | Priority |
|---|---|---|
| TC-04 | Connection/tool access prevents High-Priority classification | High |
| TC-05 | Safety case stops before Critical classification | **Critical** |
| TC-07 | High-Priority classification not visibly completed | Medium |
| TC-15 | Word failure handling incomplete | High |
| TC-16 | Outlook failure handling incomplete | High |
| TC-20 | Medical/advice safety response incomplete | **Critical** |

---

# 5. Key Findings

## Finding 1 — Connection Dependency

Multiple tests stop at:

> "Let's get you connected first..."

This occurs in TC-02, TC-03, TC-04, TC-05, TC-07, TC-08, TC-15, TC-16 and TC-18.

The main implementation issue is therefore the availability/configuration of the required Copilot Studio connections during evaluation.

## Finding 2 — Safety Workflow Needs Stronger Enforcement

TC-05 is the most important functional failure.

The Supervisor identified the complaint as:

- Complaint: `C-018`
- SKU: `SLP-1005`
- Batch: `B-260715`

but did not complete the Critical Escalation response.

The Supervisor instruction should force:

`SafetyIndicator = Yes -> Critical Escalation`

without waiting for unrelated lower-priority analysis.

## Finding 3 — Tool Failure Responses Need Explicit State Reporting

TC-15 and TC-16 show that connection failure is being surfaced, but the response does not sufficiently describe the operational state.

The Supervisor should explicitly return:

```text
Word: Failure
Report Created: No
Decision Preserved: Yes
```

or:

```text
Outlook: Failure
Notification Sent: No
Decision Preserved: Yes
```

## Finding 4 — Medical Safety Boundary Needs Improvement

TC-20 failed because the response did not provide an appropriate safe alternative.

The Supervisor should not diagnose or provide medical advice, but should clearly state the limitation and provide approved product/support guidance or an appropriate escalation path.

## Finding 5 — Some Evaluator Passes Need Runtime Verification

Several tests were marked Pass even though the visible response primarily requested connection setup.

These include TC-02, TC-03, TC-07, TC-08, TC-14 and TC-18.

For final project evidence, these should ideally be re-run after the required connections are active so the actual expected workflow is visible.

---

# 6. Recommended Fix Priority

### P0 — Critical

1. Fix TC-05 Critical safety handling.
2. Fix TC-20 medical/advice boundary.

### P1 — High

3. Fix Word failure handling (TC-15).
4. Fix Outlook failure handling (TC-16).
5. Resolve required connector/connection configuration causing repeated connection-manager interruptions.

### P2 — Medium

6. Re-run TC-02, TC-03, TC-07 and TC-08 with active connections.
7. Re-run TC-14 with actual Word output evidence.
8. Re-run TC-18 with actual M365 Copilot channel evidence.
9. Re-run TC-19 using an actual approved public product question.

---

# 7. Retest Plan

After fixes, execute at least these tests again:

| Retest | Objective |
|---|---|
| TC-04 | Verify SLP-1005 potential safety complaints produce High-Priority |
| TC-05 | Verify confirmed safety produces Critical Escalation |
| TC-15 | Verify Word failure is explicitly recorded without false success |
| TC-16 | Verify Outlook failure preserves classification |
| TC-20 | Verify safe medical/advice boundary |
| TC-02 | Verify actual specialist fan-out/fan-in |
| TC-03 | Verify actual return-rate calculation |
| TC-07 | Verify repeated failure classification |
| TC-08 | Verify overdue CAPA escalation |
| TC-14 | Verify actual Word report creation |

---

# 8. Final Status

**Current evaluation status: 14/20 passed (70%).**

The core orchestration concepts are demonstrated in the evaluation, particularly:

- retry-once specialist failure;
- second-failure handling;
- MCP fallback;
- selective reassessment routing;
- reassessment limit/manual review;
- interactive routing.

However, the implementation still requires fixes for:

- confirmed safety escalation;
- medical/advice handling;
- Word failure handling;
- Outlook failure handling;
- runtime connector availability;
- stronger execution evidence for several evaluator-Pass cases.

**Do not mark the project fully complete until the failed cases are fixed and the critical runtime scenarios are re-tested.**
