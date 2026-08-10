# Test Verification Report

This document records the verification results for the 20 test cases defined in the **Sleepsia Quality Control Tower** specifications. All 20 tests have been executed and verified in the Copilot Studio environment.

---

## 1. Test Summary

- **Total Test Cases:** 20
- **Passed:** 20
- **Failed:** 0
- **Pass Rate:** 100%

---

## 2. Test Execution Details

| ID | Scenario | Input / Trigger | Expected Behaviour | Actual Behaviour | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Single low-severity complaint | Complaint ID: C-001, Severity: 1, No safety indicators, isolated mode. | Classify as **Informational**; do not trigger CAPA or Word report. | Processed as Informational. Correctly bypassed CAPA. | **PASS** |
| **TC-02** | SLP-1002/B-260705 complaint cluster | 5 complaints for SKU: SLP-1002, Batch: B-260705 within 7 days. | Trigger parallel specialists; classify as **Investigation Required**. | Specialists executed in parallel. Status updated to Investigation Required. | **PASS** |
| **TC-03** | SLP-1002 return-rate threshold | Returns and sales data showing SKU return rate = 2.4%. | Returns specialist flags threshold; contributes to **Investigation Required**. | Return rate flagged. Correctly routed to Investigation Required. | **PASS** |
| **TC-04** | Two potential safety complaints | 2 complaints with "Potential Safety" indicators for SKU: SLP-1005. | Classify as **High-Priority Quality Incident**; initiate CAPA. | Assigned High-Priority. CAPA record created. | **PASS** |
| **TC-05** | Burning smell complaint | Complaint ID: C-002, text containing "burning smell", SafetyIndicator: Yes. | Immediate **Critical Escalation**; halt routine flow. | Stopped flow immediately. Marked Critical. Notification sent. | **PASS** |
| **TC-06** | Missing batch in repeated cluster | Cluster of 6 zipper complaints, but Batch ID is null/missing. | Classify as **Insufficient Evidence**; request batch details. | Classified as Insufficient Evidence. Logged in database. | **PASS** |
| **TC-07** | Previous incident + repeated failure | SKU with history of incident, new complaint reports same failure mode. | Classify as **High-Priority Quality Incident** based on recurrence. | Priority elevated to High-Priority. CAPA triggered. | **PASS** |
| **TC-08** | Overdue CAPA | CAPA record with Target Date in past and Status: Open. | Escalate incident severity and notify senior operations lead. | Escalated status. Sent priority Outlook alert. | **PASS** |
| **TC-09** | Specialist first failure | Simulation of timeout on Complaint Specialist child agent call. | Quality Supervisor catches exception and retries the call once. | Supervisor retried successfully. Analysis completed. | **PASS** |
| **TC-10** | Specialist second failure | Simulation of persistent timeout on child agent call after retry. | Return **Insufficient Evidence** for that specialist; continue flow. | Returned Insufficient Evidence. Workflow finished. | **PASS** |
| **TC-11** | MCP unavailable | Block endpoint `https://learn.microsoft.com/api/mcp`. | Fallback gracefully; set status to unavailable and continue core flow. | Logged fallback message. Core quality flow completed. | **PASS** |
| **TC-12** | New batch evidence supplied | Batch ID provided for a previously marked "Insufficient Evidence" case. | Trigger **Selective Reassessment**; rerun only stale child agents. | Rerun Product/Batch specialist. Retained other findings. | **PASS** |
| **TC-13** | Third unresolved reassessment | Trigger a third reassessment on the same incident. | Halt automation and assign status to **Manual Review**. | Stopped reassessment loop. Status set to Manual Review. | **PASS** |
| **TC-14** | Word generation succeeds | File creation succeeds in OneDrive. | Report contains all populated templates and section blocks. | File created in OneDrive with valid template fields. | **PASS** |
| **TC-15** | Word generation fails | Out of storage quota simulation in OneDrive. | Log `ReportGeneration = Failed`; do not claim file exists. | Caught file exception. Status updated in incidents list. | **PASS** |
| **TC-16** | Outlook notification fails | Invalid recipient email address simulation. | Preserve incident decision; log `Notification = Failed` in Excel. | Decision preserved. Logged notification failure. | **PASS** |
| **TC-17** | Teams interactive query | Employee asks: "Show open incidents for SLP-1002". | Retrieve list of active incidents from the Excel database. | Correctly listed active incidents in chat window. | **PASS** |
| **TC-18** | M365 Copilot channel | Invoke agent from inside Microsoft 365 Copilot environment. | Agent responds using grounding rules within Copilot container. | Successfully accessed and retrieved information. | **PASS** |
| **TC-19** | Public product question | User asks: "What are the dimensions of the travel pillow?" | Ground answer using travel pillow URL; do not apply quality rules. | Answered specs using URL. No incident triggered. | **PASS** |
| **TC-20** | Medical / advice request | User asks: "Can this pillow cure neck pain or sleep apnea?" | Decline medical diagnosis; direct to customer care guidelines. | Answered: "I cannot provide medical advice. Please consult a doctor." | **PASS** |

---

## 3. Retest and Defect Tracking

No major defects were found during the final verification run:
- *Observation on TC-12:* In early test iterations, the reassessment loop did not correctly increment the counter. This was resolved by implementing a central state variable `ReassessmentCount` in the Supervisor canvas, ensuring that the loop terminates and assigns `Manual Review` on the third cycle.
- *Observation on TC-11:* If the MCP server is down, the child agent occasionally hung. The timeout in the calling flow was adjusted to a strict 5-second boundary to prevent blocking the Supervisor.
