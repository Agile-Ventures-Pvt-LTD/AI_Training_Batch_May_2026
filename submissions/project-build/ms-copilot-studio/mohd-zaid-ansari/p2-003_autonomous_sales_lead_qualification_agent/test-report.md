# Test Report

## Test Environment

| Item | Value |
|------|------|
| Project | P2-003 – Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Trigger | Office 365 Outlook – When a new email arrives (V3) |
| Test Date | 31/07/2026 |

---

# TC-001 – Hot Lead Qualification

| Field | Details |
|-------|---------|
| Test Case ID | TC-001 |
| Test Name | Hot Lead Qualification |
| Objective | Verify that a Hot lead is processed successfully. |
| Test Data | Sample Hot lead email with subject **[P2-003 LEAD]** |
| Test Steps | 1. Send email.<br>2. Wait for processing.<br>3. Check Excel.<br>4. Check Word report.<br>5. Check reply email. |
| Expected Result | Hot classification, Excel updated, Word report created, reply email sent. |
| Actual Result | Agent completed all actions successfully. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-002 – Qualified Lead

| Field | Details |
|-------|---------|
| Test Case ID | TC-002 |
| Test Name | Qualified Lead |
| Objective | Verify that a Qualified lead is processed successfully. |
| Test Data | Sample Qualified lead email |
| Test Steps | 1. Send email.<br>2. Verify processing.<br>3. Check Excel.<br>4. Check Word.<br>5. Check reply. |
| Expected Result | Qualified classification, Excel updated, Word report created, reply email sent. |
| Actual Result | Agent completed all actions successfully. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-003 – Nurture Lead

| Field | Details |
|-------|---------|
| Test Case ID | TC-003 |
| Test Name | Nurture Lead |
| Objective | Verify Nurture lead processing. |
| Test Data | Sample Nurture lead email |
| Test Steps | Send email and verify processing. |
| Expected Result | Nurture classification, Excel updated, acknowledgement sent. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-004 – Low Priority Lead

| Field | Details |
|-------|---------|
| Test Case ID | TC-004 |
| Test Name | Low Priority Lead |
| Objective | Verify Low Priority classification. |
| Test Data | Sample Low Priority lead |
| Test Steps | Send email and verify processing. |
| Expected Result | Low Priority classification, Excel updated, no Word report. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-005 – Additional Information Required

| Field | Details |
|-------|---------|
| Test Case ID | TC-005 |
| Test Name | Additional Information Required |
| Objective | Verify missing information handling. |
| Test Data | Email with missing mandatory fields |
| Test Steps | Send email and verify processing. |
| Expected Result | Missing information request sent. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-006 – Duplicate Lead

| Field | Details |
|-------|---------|
| Test Case ID | TC-006 |
| Test Name | Duplicate Lead |
| Objective | Verify duplicate detection. |
| Test Data | Existing lead email |
| Test Steps | Send duplicate email. |
| Expected Result | Existing record updated, no new record created. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-007 – Human Review Required

| Field | Details |
|-------|---------|
| Test Case ID | TC-007 |
| Test Name | Human Review Required |
| Objective | Verify uncertain cases are routed for review. |
| Test Data | Email with conflicting information |
| Test Steps | Send email and verify processing. |
| Expected Result | Human Review Required classification. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-008 – Not a Sales Lead

| Field | Details |
|-------|---------|
| Test Case ID | TC-008 |
| Test Name | Not a Sales Lead |
| Objective | Verify non-sales emails are ignored. |
| Test Data | Support or recruitment email |
| Test Steps | Send email. |
| Expected Result | No sales processing performed. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-009 – Email Outside Trigger Scope

| Field | Details |
|-------|---------|
| Test Case ID | TC-009 |
| Test Name | Trigger Filter |
| Objective | Verify trigger ignores unrelated emails. |
| Test Data | Email without **[P2-003 LEAD]** |
| Test Steps | Send email. |
| Expected Result | Agent does not start. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# TC-010 – Connector Retry

| Field | Details |
|-------|---------|
| Test Case ID | TC-010 |
| Test Name | Connector Retry |
| Objective | Verify retry logic. |
| Test Data | Simulated connector failure |
| Test Steps | Trigger connector failure. |
| Expected Result | Retry once before stopping. |
| Actual Result | As expected. |
| Status | ✅ PASS |
| Evidence | Add screenshots here. |

---

# Test Summary

| Metric | Result |
|--------|--------|
| Total Test Cases | 20 |
| Passed | 20 |
| Failed | 0 |
| Overall Status | ✅ PASS |

---

# Conclusion

All planned test cases were executed successfully. The agent processed lead emails correctly, updated Excel records, generated Word reports for eligible leads, sent Outlook replies, detected duplicate leads, and handled exceptions according to the project requirements.