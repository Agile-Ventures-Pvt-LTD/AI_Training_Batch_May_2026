# Test Report

## Project

**Project ID:** P2-003 – Autonomous Sales Lead Qualification Agent

---

## Test Environment

| Item | Value |
|------|-------|
| Platform | Microsoft Copilot Studio |
| Trigger | Office 365 Outlook – When a new email arrives (V3) |
| Data Source | Microsoft Excel |
| Report Generation | Microsoft Word Online |
| Notification | Outlook |

---

## Test Summary

| Total Test Cases | Passed | Failed |
|------------------|--------|--------|
| 20 | 20 | 0 |

---

## Test Execution Details

| Case ID | Execution Date | Actual Classification | Excel Result | Word Result | Outlook Result | Duplicate Prevention | Pass/Fail | Issue | Correction | Retest | Screenshot Path |
|---------|----------------|-----------------------|--------------|-------------|----------------|----------------------|-----------|-------|------------|--------|-----------------|
| TC-001 | Completed | Hot | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Test-Evidence/TC-001/ |
| TC-002 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Test-Evidence/TC-002/ |
| TC-003 | Completed | Not Qualified | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Test-Evidence/TC-003/ |
| TC-004 | Completed | Duplicate Lead | Existing Record Updated | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Test-Evidence/TC-004/ |
| TC-005 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Test-Evidence/TC-005/ |
| TC-006 | Completed | Cold | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-007 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-008 | Completed | Missing Information | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-009 | Completed | Support Request | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-010 | Completed | Cold | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-011 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-012 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-013 | Completed | Cold | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-014 | Completed | Cold | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-015 | Completed | Missing Information | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-016 | Completed | Not Qualified | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-017 | Completed | Warm | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-018 | Completed | Cold | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-019 | Completed | Hot | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |
| TC-020 | Completed | Missing Information | Updated Successfully | Generated | Email Sent | Passed | PASS | None | N/A | Not Required | Not Available |

---

## Test Evidence

Screenshots have been provided **only for TC-001 to TC-005** in the **`Test-Evidence`** folder. These include the Outlook email, Copilot Studio execution, Excel update, Word report generation, and Outlook response.

The remaining test cases (**TC-006 to TC-020**) were executed successfully and are documented in this report; however, screenshots were not captured.

---

## Overall Result

- All 20 test cases were executed successfully.
- Email trigger functioned as expected.
- Excel records were created or updated correctly.
- Word qualification reports were generated successfully.
- Outlook acknowledgement and notification emails were sent successfully.
- Duplicate detection worked correctly.
- The agent correctly classified Hot, Warm, Cold, Duplicate, Missing Information, Not Qualified, and Support Request scenarios.

---

## Conclusion

The **P2-003 Autonomous Sales Lead Qualification Agent** successfully passed all planned test cases and met the expected functional requirements. The solution demonstrated reliable lead qualification, duplicate detection, report generation, Excel updates, and Outlook notifications across all tested scenarios.