# test-report.md

# CAP-001 — Test Report

## 1. Overview

This document records the validation approach and test scenarios for the Sleepsia Product Quality & Customer Experience Intelligence Control Tower.

Testing focuses on the autonomous multi-agent quality workflow, specialist orchestration, deterministic decision precedence, CAPA and evidence handling, reassessment, tool failures, reporting, notification, and interactive employee access.

The test suite is designed to validate the mandatory scenarios defined for CAP-001.

---

## 2. Test Objectives

The testing objectives are to verify that:

- The recurrence trigger starts the autonomous workflow.
- Complaint intake validation works correctly.
- Specialist agents perform their assigned domain analysis.
- Parallel fan-out/fan-in behavior is preserved.
- The Quality Supervisor remains the final decision owner.
- Safety findings receive the required precedence.
- Return-rate and complaint-pattern thresholds are applied correctly.
- Previous incidents and repeated failures are considered.
- Missing evidence results in the appropriate evidence path.
- CAPA requirements and overdue CAPA are handled correctly.
- Selective reassessment reruns only affected analyses.
- Reassessment is limited to two automated cycles.
- Specialist failures trigger retry and fallback.
- MCP failure does not block the core quality workflow.
- Word report generation is controlled by the Supervisor.
- Outlook notification is conditional on the validated outcome.
- Tool failures are never represented as successful actions.
- Interactive Teams/Microsoft 365 scenarios follow the configured governance.

---

## 3. Test Environment

| Component | Environment |
|---|---|
| Platform | Microsoft Copilot Studio |
| Supervisor | Quality Supervisor |
| Data Source | Excel Online (Business) |
| Report Connector | Word Online (Business) |
| Notification Connector | Office 365 Outlook |
| MCP | Microsoft Learn MCP |
| Autonomous Trigger | Recurrence Trigger |
| Intended Interactive Channel | Microsoft Teams |
| Secondary Intended Channel | Microsoft 365 Copilot |

---

## 4. Test Case Summary

| Test ID | Scenario | Expected Outcome |
|---|---|---|
| TC-001 | Parallel specialist fan-out/fan-in | Required specialist findings are consolidated by Supervisor |
| TC-002 | Return-rate threshold | Return rate ≥ 2% routes to Investigation Required |
| TC-003 | Safety Critical escalation | Safety indicator routes to Critical |
| TC-004 | Missing evidence | Incident routes to Evidence Request / Insufficient Evidence |
| TC-005 | Previous incident / repeat failure | Repeat incident results in High-Priority handling |
| TC-006 | Overdue CAPA | Overdue CAPA triggers escalation |
| TC-007 | Specialist first failure | Specialist is retried once |
| TC-008 | Specialist second failure | Result becomes Insufficient Evidence / Manual Review path |
| TC-009 | MCP unavailable | Core quality workflow continues |
| TC-010 | Selective reassessment | Only affected specialist analysis is rerun |
| TC-011 | Reassessment limit | Third automated cycle is prevented |
| TC-012 | Word report generation | Validated result produces quality report |
| TC-013 | Word generation failure | Decision is preserved and report failure is recorded |
| TC-014 | Outlook notification failure | Decision is preserved and notification failure is recorded |
| TC-015 | Teams interactive query | Published agent returns appropriate quality information |
| TC-016 | Microsoft 365 Copilot validation | Agent is accessible where tenant permissions allow |

---

## 5. Detailed Test Cases

### TC-001 — Parallel Specialist Fan-Out/Fan-In

**Objective:**  
Verify that independent specialist analyses are coordinated and consolidated by the Quality Supervisor.

**Input:**  
A valid complaint record requiring specialist analysis.

**Expected Result:**

```text
Quality Supervisor
       |
       +--> Complaint Pattern Specialist
       +--> Returns Specialist
       +--> Product-Batch Specialist
       +--> Customer Impact Specialist
       |
       ▼
Supervisor Fan-In
       |
       ▼
Unified Decision Context
```

**Pass Criteria:**

* Required specialists are invoked.
* Specialist outputs are returned.
* Supervisor consolidates the findings.
* No specialist independently issues the final decision.

---

### TC-002 — Return-Rate Threshold

**Objective:**  
Verify the return-rate governance threshold.

**Input:**  
Return rate greater than or equal to 2%.

**Expected Result:**  
Classification routes to **Investigation Required** unless a higher-precedence condition applies.

**Pass Criteria:**

* Returns Specialist calculates the applicable return rate.
* Supervisor receives the result.
* The ≥2% rule is applied.
* Final classification reflects the required precedence.

---

### TC-003 — Safety Critical Escalation

**Objective:**  
Verify safety override behavior.

**Input:**  
A complaint containing a safety indicator of `Yes` or applicable potential safety evidence.

**Expected Result:**  
Incident follows the **Critical** path.

**Pass Criteria:**

* Safety Specialist identifies the safety concern.
* Supervisor applies safety precedence.
* Lower-priority findings do not override the Critical path.
* Critical incident is not independently closed by the CAPA Specialist.

---

### TC-004 — Missing Evidence

**Objective:**  
Verify handling of incomplete evidence.

**Input:**  
Complaint record with required evidence missing.

**Expected Result:**  
Incident routes to **Evidence Request / Insufficient Evidence**.

**Pass Criteria:**

* Missing evidence is explicitly identified.
* System does not invent the missing information.
* Unsupported classification is prevented.
* Appropriate evidence follow-up is initiated.

---

### TC-005 — Previous Incident / Repeat Failure

**Objective:**  
Verify repeat-incident handling.

**Input:**  
Product or batch with a previous applicable quality incident.

**Expected Result:**  
Incident follows the **High-Priority** path unless a higher-precedence condition applies.

**Pass Criteria:**

* Product-Batch Specialist identifies the previous incident.
* Supervisor receives the finding.
* Repeat-incident rule is applied.
* Final classification follows precedence.

---

### TC-006 — Overdue CAPA

**Objective:**  
Verify escalation for overdue CAPA.

**Input:**  
Existing CAPA with a target date that has passed.

**Expected Result:**  
Overdue CAPA is escalated.

**Pass Criteria:**

* CAPA status is retrieved.
* Overdue condition is identified.
* Escalation is recorded.
* Supervisor retains final control.

---

### TC-007 — Specialist First Failure

**Objective:**  
Verify specialist retry behavior.

**Input:**  
Simulated first execution failure from a specialist.

**Expected Result:**  
The failed specialist is retried once.

**Pass Criteria:**

* First failure is recorded.
* One retry is initiated.
* Successful retry allows the workflow to continue.
* No fabricated successful result is produced before retry completion.

---

### TC-008 — Specialist Second Failure

**Objective:**  
Verify fallback after a second specialist failure.

**Input:**  
Specialist fails during the first execution and again during retry.

**Expected Result:**  
The affected finding is treated as **Insufficient Evidence** and the incident follows the appropriate manual-review/evidence path.

**Pass Criteria:**

* Both failures are recorded.
* No unsupported specialist result is created.
* Incident cannot be incorrectly classified as Ready/clear based on the failed specialist.
* Appropriate escalation or manual review occurs.

---

### TC-009 — Microsoft Learn MCP Unavailable

**Objective:**  
Verify that MCP failure does not block the core quality workflow.

**Input:**  
Microsoft Learn MCP unavailable.

**Expected Result:**  
Core quality assessment continues.

**Pass Criteria:**

* MCP failure is recorded.
* No fabricated Microsoft guidance is returned.
* Quality specialists continue their core work.
* Product-quality classification is not blocked solely by MCP unavailability.

---

### TC-010 — Selective Reassessment

**Objective:**  
Verify that only stale specialist results are rerun after evidence changes.

**Input:**  
New evidence affecting one specialist domain.

**Expected Result:**

```text
New Evidence
     |
     ▼
Identify Affected Domain
     |
     ▼
Mark Related Result Stale
     |
     ▼
Re-run Affected Specialist
     |
     ▼
Supervisor Fan-In
     |
     ▼
Recalculate Decision
```

**Pass Criteria:**

* Changed evidence is identified.
* Unaffected specialist results are retained.
* Affected specialist is rerun.
* Supervisor recalculates the final decision.

---

### TC-011 — Reassessment Limit

**Objective:**  
Verify the maximum automated reassessment limit.

**Input:**  
An incident requiring repeated reassessment.

**Expected Result:**  
After two automated reassessment cycles, further automated reassessment is prevented and the incident routes to **Manual Review**.

**Pass Criteria:**

* Cycle 1 is allowed.
* Cycle 2 is allowed.
* Cycle 3 is not automatically executed.
* Manual Review is assigned.

---

### TC-012 — Word Report Generation

**Objective:**  
Verify generation of the Product Quality Investigation Report.

**Input:**  
Validated final quality decision.

**Expected Result:**  
Word report is generated using the approved incident findings.

**Pass Criteria:**

* Report generation occurs only after Supervisor validation.
* Incident information is correctly represented.
* Final classification matches the validated decision.
* Report generation success is recorded.

---

### TC-013 — Word Generation Failure

**Objective:**  
Verify safe handling of report-generation failure.

**Input:**  
Simulated Word generation failure.

**Expected Result:**

* Final quality decision is preserved.
* Report failure is recorded.
* System does not claim that the report was generated.

**Pass Criteria:**

```text
Decision
   |
   ▼
Word Generation Failure
   |
   ├── Preserve Decision
   └── Record Report Failure
```

---

### TC-014 — Outlook Notification Failure

**Objective:**  
Verify safe handling of notification failure.

**Input:**  
Simulated Outlook send failure.

**Expected Result:**

* Final quality decision is preserved.
* Notification failure is recorded.
* System does not claim that the email was sent.

**Pass Criteria:**

```text
Validated Decision
       |
       ▼
Outlook Send Failure
       |
       ├── Preserve Decision
       └── Record Notification Failure
```

---

### TC-015 — Microsoft Teams Interactive Query

**Objective:**  
Verify interactive employee access.

**Input Example:**

```text
Show open quality incidents for SKU SK-1001.
```

**Expected Result:**  
The Quality Supervisor retrieves applicable operational data and returns the appropriate result.

**Pass Criteria:**

* Request is understood.
* Appropriate data source/tool is used.
* Response is based on available evidence.
* No unsupported quality decision is fabricated.

**Status:**  
Pending successful agent publication because the current Copilot Studio publishing process is blocked by a publishing error.

---

### TC-016 — Microsoft 365 Copilot Validation

**Objective:**  
Verify Microsoft 365 Copilot access where supported by tenant permissions.

**Input Example:**

```text
What is the current CAPA status for the affected batch?
```

**Expected Result:**  
The published Quality Supervisor returns the applicable CAPA information.

**Pass Criteria:**

* Agent is available in the supported Microsoft 365 environment.
* Appropriate operational data is retrieved.
* Response follows Supervisor governance.

**Status:**  
Pending successful agent publication and tenant availability.

---

## 6. Test Result Recording

| Field | Description |
|--------|-------------|
| Test ID | Unique test identifier |
| Scenario | Scenario being tested |
| Input | Test data or condition |
| Expected Result | Required behavior |
| Actual Result | Observed behavior |
| Final Classification | Result assigned by the system |
| Pass / Fail | Test outcome |
| Failure Reason | Reason when failed |
| Remediation | Corrective action taken |
| Retest Result | Result after correction |
| Evidence | Screenshot or execution evidence |

---

## 7. Defect Handling

When a test fails:

1. Record the failure.
2. Identify the affected component.
3. Correct the configuration or logic.
4. Re-run the affected test.
5. Record the retest result.
6. Preserve the original failure for traceability.

No test should be marked Passed without corresponding execution evidence.

---

## 8. Publishing Constraint

The Quality Supervisor agent is currently configured but cannot be successfully published because of a Microsoft Copilot Studio publishing error.

As a result:

* Live Teams validation is blocked.
* Live Microsoft 365 Copilot validation is blocked.
* The implementation has been shared with **Ankur Sir via Outlook email** for review.

This limitation is recorded as an environment/publishing constraint rather than an unimplemented workflow requirement.

---

## 9. Overall Test Status

| Area | Status |
|--------|--------|
| Core workflow validation | Completed |
| Specialist orchestration validation | Completed |
| Decision-precedence validation | Completed |
| Reassessment validation | Completed |
| Retry/fallback validation | Completed |
| Tool failure handling | Completed |
| Word report validation | Completed |
| Outlook validation | Completed |
| Teams live validation | Blocked by publishing error |
| Microsoft 365 Copilot live validation | Blocked by publishing error |

---

## 10. Test Conclusion

The test suite validates the required autonomous quality-governance behavior, including specialist orchestration, deterministic decision-making, CAPA/evidence handling, bounded reassessment, failure handling, reporting, and notification.

The remaining channel-level validation is dependent on successful Microsoft Copilot Studio publication and tenant availability.

The configured implementation has been shared with **Ankur Sir via Outlook email** for review.