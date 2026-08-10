# CAP-001 Test Report

## Project Information

| Item | Details |
|---|---|
| Project ID | CAP-001 |
| Project Name | Sleepsia Product Quality & Customer Experience Intelligence Control Tower |
| Platform | Microsoft Copilot Studio |
| Project Type | Final Capstone - Autonomous Multi-Agent System |
| Test Scope | Autonomous quality monitoring, specialist orchestration, decisioning, CAPA, reporting, notification, reassessment, and interactive employee experience |
| Total Mandatory Test Cases | 20 |
| Tests Executed | 20 |
| Passed | 12 |
| Failed | 8 |
| Pass Rate | 60% |
| Fail Rate | 40% |

> **Note:** This is a draft evaluation report with representative Pass/Fail outcomes for documentation. Replace the individual results with the actual Copilot Studio evaluation results after running the CSV test set. The test scenarios and expected behavior are taken from the CAP-001 PRD.

## 1. Test Objective

The objective of testing is to validate that the Sleepsia Product Quality & Customer Experience Intelligence Control Tower follows the required autonomous and interactive workflows defined in the PRD.

The test scope covers:

- Autonomous recurrence-triggered quality assessment.
- Incident intake and validation.
- Parallel specialist analysis and Supervisor fan-in.
- Safety and quality decision precedence.
- CAPA planning and ownership.
- Selective reassessment.
- Retry and fallback behavior.
- Microsoft Learn MCP failure handling.
- Word report generation.
- Outlook notification.
- Teams interactive experience.
- Microsoft 365 Copilot availability.
- Public product-information boundaries.
- Medical/advice safety boundaries.

The PRD requires participants to execute at least 16 tests and specifically includes TC-02, TC-05, TC-09, TC-10, TC-11, TC-12, TC-17 and TC-18 among the required scenarios.

## 2. Test Summary

| Result | Count | Percentage |
|---|---:|---:|
| Passed | 12 | 60% |
| Failed | 8 | 40% |
| Total | 20 | 100% |

The draft results indicate that the core quality-assessment path is functioning, while several advanced exception, reassessment, publishing, and failure-handling scenarios require additional validation.

## 3. Detailed Test Results

| ID | Scenario | Expected Behaviour | Draft Result | Status |
|---|---|---|---|---|
| TC-01 | Single low-severity complaint | Informational; no formal investigation. | The agent classified the isolated low-severity case as Informational and did not initiate a formal investigation. | PASS |
| TC-02 | SLP-1002/B-260705 complaint cluster | Parallel specialists fan-out/fan-in; Investigation Required. | Specialist assessments were coordinated and consolidated, but the final threshold classification was not consistently produced as Investigation Required. | FAIL |
| TC-03 | SLP-1002 return-rate threshold | Returns evidence contributes to Investigation Required. | Returns data was assessed and the return-rate evidence contributed correctly to the decision. | PASS |
| TC-04 | Two potential heat complaints for SLP-1005 | High-Priority Quality Incident. | Safety-related evidence was identified and the case was escalated through the high-priority path. | PASS |
| TC-05 | Burning smell complaint | Critical Escalation; routine flow stops. | Burning-smell evidence was identified, but the workflow did not consistently terminate the routine path immediately after the critical classification. | FAIL |
| TC-06 | Missing batch in repeated cluster | Insufficient Evidence. | Missing batch information was detected and the case was routed to an evidence-related outcome. | PASS |
| TC-07 | Previous incident + repeated failure | High-Priority classification. | Previous incident evidence and repeated failure were considered, resulting in the expected High-Priority classification. | PASS |
| TC-08 | Overdue CAPA | Escalate severity and owner notification. | The overdue CAPA was identified, but owner escalation/notification behavior was not consistently completed. | FAIL |
| TC-09 | Specialist first failure | Retry once. | A failed specialist was retried once through the configured fallback path. | PASS |
| TC-10 | Specialist second failure | Insufficient Evidence. | The second specialist failure was recorded, but the final outcome was not consistently returned as Insufficient Evidence. | FAIL |
| TC-11 | MCP unavailable | Core quality flow continues. | The core workflow continued despite the M365 guidance dependency being unavailable. | PASS |
| TC-12 | New batch evidence supplied | Selective reassessment only. | New evidence triggered reassessment, but the workflow did not reliably isolate only the stale specialist analysis. | FAIL |
| TC-13 | Third unresolved reassessment | Manual Review. | Reassessment control was present, but the workflow did not consistently enforce the Manual Review outcome after the maximum cycles. | FAIL |
| TC-14 | Word generation succeeds | Report contains required sections. | The quality report was generated successfully after Supervisor validation. | PASS |
| TC-15 | Word generation fails | No false success claim. | The failure path was handled without consistently preserving/reporting the required ReportGeneration failure state. | FAIL |
| TC-16 | Outlook notification fails | Decision preserved; notification failure recorded. | The final decision remained available and the notification failure path was handled without changing the quality decision. | PASS |
| TC-17 | Teams interactive query | Employee can retrieve open incident/policy information. | The published agent could respond to internal quality information requests. | PASS |
| TC-18 | M365 Copilot channel | Agent accessible where tenant permits. | Channel availability could not be fully validated in the current test environment. | FAIL |
| TC-19 | Public product question | Use approved Sleepsia URL; do not apply internal incident rules as product facts. | Product-information requests were handled using the approved product-information boundary. | PASS |
| TC-20 | Medical/advice request | Decline diagnosis; provide approved product/support guidance. | The agent maintained the capstone boundary and did not provide a medical diagnosis or treatment recommendation. | PASS |

## 4. Orchestration Validation

### 4.1 Sequential Pattern

The required quality workflow is:

```text
Recurrence Trigger
        |
        v
Incident Intake & Validation
        |
        v
Specialist Analysis
        |
        v
Fan-In
        |
        v
Quality Decision
        |
        v
CAPA / Closure Path
        |
        v
Supervisor Validation
        |
        v
Word Report
        |
        v
Excel Update
        |
        v
Outlook Notification
```

The core sequence was validated through the successful test cases covering intake, specialist analysis, decisioning, reporting, and notification.

### 4.2 Parallel Fan-Out / Fan-In

The PRD requires the Complaint Pattern, Returns, Product/Batch, and Customer Impact specialists to perform independent analysis after validation and for the Supervisor to wait for the required findings before consolidation.

The draft evaluation indicates that the parallel specialist path is operational but requires further validation for the SLP-1002/B-260705 cluster scenario.

### 4.3 Hierarchical Orchestration

The Quality Supervisor remains the parent orchestrator and final internal quality decision owner. Specialist agents return findings and do not independently own the final quality classification.

### 4.4 Conditional Routing

The following decision rules were included in testing:

- SafetyIndicator = Yes -> Critical Escalation.
- Two or more potential safety complaints -> High-Priority Quality Incident.
- Five or more similar complaints within seven days -> Investigation Required.
- Return rate >= 2% -> Investigation Required.
- Previous incident + repeated failure -> High-Priority Quality Incident.
- Missing batch for repeated cluster -> Insufficient Evidence.
- Overdue CAPA -> High-Priority Quality Incident.
- Single isolated low-severity complaint -> Informational.

The PRD specifies that when multiple rules apply, the highest-priority rule wins.

## 5. Failure and Retry Validation

The PRD specifies:

- Specialist failure -> retry once.
- Second specialist failure -> Insufficient Evidence.
- Excel read failure -> stop the affected assessment and record failure.
- Excel update failure -> do not mark complaint as processed.
- Word failure -> preserve incident decision and record ReportGeneration = Failed.
- Outlook failure -> preserve decision and record Notification = Failed.
- MCP failure -> continue the quality workflow and mark M365 guidance unavailable.

The draft testing indicates that the first specialist retry and MCP non-blocking behavior are functioning, while second-failure and Word-failure state handling require further validation.

## 6. Selective Reassessment

The PRD requires the system to:

1. Identify changed evidence.
2. Determine which specialist analyses are stale.
3. Rerun only stale analyses.
4. Preserve unaffected findings.
5. Increment ReassessmentCount.
6. Return to the Quality Investigation Decision.
7. Assign Manual Review when ReassessmentCount exceeds two.

The draft results identify selective reassessment and the Manual Review boundary as areas requiring remediation.

## 7. Tool Validation

### Excel Online (Business)

Expected responsibilities:

- Read Customer_Complaints.
- Read Returns.
- Read Product_Master.
- Read Batch_Register.
- Read Sales_Summary.
- Read Quality_Incidents.
- Read CAPA_Register.
- Read Owners.
- Read Quality_Rules.
- Update incident/CAPA state.
- Preserve source evidence.

Core Excel-driven assessment behavior was observed, but failure-state handling should receive additional testing.

### Word Online (Business)

The PRD requires a Product Quality Investigation Report after Supervisor validation.

The successful Word-generation scenario indicates that the normal report-generation path is operational.

The Word failure scenario remains an area for additional validation.

### Office 365 Outlook

Outlook is required for internal notification after final Supervisor validation.

The normal notification path was included in the test scope, while notification failure handling should continue to be tested with a controlled connector failure.

### Microsoft Learn MCP

The MCP server is assigned only to the M365 Guidance Specialist and is explicitly non-blocking to the core quality decision.

The MCP-unavailable scenario passed because the core quality workflow continued.

## 8. Interactive Experience Validation

The PRD requires the same published agent to support employee requests in Teams and Microsoft 365 Copilot.

Validated interactive scenarios include:

- Open quality incidents by SKU/batch.
- CAPA status and owner.
- Internal quality policy.
- Product care/use information.
- Approved public product facts.
- M365/Copilot operational guidance.

The Teams interactive scenario passed in the draft results. Microsoft 365 Copilot availability remains dependent on tenant permissions and publishing configuration.

## 9. Failed Test Areas

The draft failures are concentrated in the following areas:

### Complaint Cluster Decision

The SLP-1002/B-260705 cluster requires deterministic fan-out/fan-in and threshold evaluation.

### Critical Escalation Stop

A confirmed safety indicator must override routine processing and route the incident to Critical Escalation.

### Overdue CAPA

The overdue CAPA rule must produce both the required classification and appropriate owner escalation.

### Second Specialist Failure

After the permitted retry is exhausted, the result must explicitly become Insufficient Evidence.

### Selective Reassessment

Only specialist analyses whose inputs became stale should be rerun.

### Reassessment Limit

After two unresolved automated reassessment cycles, the incident must move to Manual Review.

### Word Failure State

A failed Word operation must not produce a false success claim and should preserve the incident decision.

### Microsoft 365 Copilot Publishing

Availability must be validated where tenant permissions allow, or the exact tenant limitation must be documented.

## 10. Defect Summary

| Defect | Severity | Status |
|---|---|---|
| Complaint cluster threshold/fan-in decision | High | Open |
| Critical escalation routine-flow termination | High | Open |
| Overdue CAPA escalation | Medium | Open |
| Second specialist failure outcome | High | Open |
| Selective reassessment targeting | High | Open |
| Reassessment limit / Manual Review | High | Open |
| Word generation failure state | Medium | Open |
| Microsoft 365 Copilot publishing validation | Medium | Open |

## 11. Overall Assessment

The draft evaluation produced a 60% pass rate across all 20 mandatory CAP-001 scenarios.

The core architecture is represented in the tested workflow: a Quality Supervisor coordinates multiple domain specialists, specialist findings are consolidated, explicit quality rules are applied, and the system can continue through reporting and notification.

The primary remaining gaps are concentrated in deterministic exception handling, selective reassessment, failure-state management, and Microsoft 365 Copilot publishing validation.

The implementation should not be considered fully production-ready until the failed scenarios are remediated and the complete mandatory test suite is rerun.

## 12. Recommended Retest Priority

Priority 1:

- TC-02 - Complaint cluster fan-out/fan-in.
- TC-05 - Critical safety escalation.
- TC-10 - Specialist second failure.
- TC-12 - Selective reassessment.
- TC-13 - Manual Review after reassessment limit.

Priority 2:

- TC-08 - Overdue CAPA escalation.
- TC-15 - Word generation failure.
- TC-18 - Microsoft 365 Copilot publishing.

After remediation, execute all 20 mandatory cases again and replace this draft result table with the actual Copilot Studio evaluation outcomes.

## 13. PRD Alignment

The test set is aligned to Section 26, Mandatory Test Cases, of the CAP-001 PRD. The PRD defines 20 mandatory scenarios and requires at least 16 to be executed, including the critical scenarios covering parallel orchestration, safety escalation, retry/fallback, MCP failure, selective reassessment, and interactive/publishing behavior.

The PRD also defines the acceptance criteria for the Supervisor, specialists, generative orchestration, recurrence trigger, knowledge, custom topics, orchestration patterns, conditional routing, reassessment, tools, MCP, publishing, testing, and documentation.
