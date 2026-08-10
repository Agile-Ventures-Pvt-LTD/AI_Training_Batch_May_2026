# Test Report

## Project

**CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower**


## Test Results
| Test ID | User Scenario | Expected Behaviour | Pass/Fail |
|---|---|---|---|
| TC-01 | Single low-severity complaint | A single isolated low-severity complaint should be handled according to the approved quality decision rules. | Pass |
| TC-02 | SLP-1002/B-260705 complaint cluster | The agent should identify and evaluate the complaint cluster for the specified SKU/batch. | Pass |
| TC-03 | SLP-1002 return-rate threshold | The agent should evaluate the return-rate threshold and apply the applicable quality classification. | Pass |
| TC-04 | Two potential heat complaints SLP-1005 | Multiple potential safety complaints for the same SKU/batch should trigger the appropriate high-priority safety-related classification. | Pass |
| TC-05 | Burning smell complaint | A burning-smell complaint should be assessed using the configured safety and quality escalation logic. | Pass |
| TC-06 | Missing batch in repeated cluster | Missing batch evidence in a repeated complaint cluster should result in the appropriate insufficient-evidence handling. | Fail |
| TC-07 | Previous incident + repeated failure | A previous incident combined with a repeated failure mode should trigger the configured high-priority quality handling. | Pass |
| TC-08 | Overdue CAPA | An overdue CAPA should be identified and handled according to the configured quality decision rules. | Fail |
| TC-09 | Specialist first failure | The first specialist failure should trigger the configured retry/failure-handling behavior. | Pass |
| TC-10 | Specialist second failure | A specialist that fails again after retry should be handled using the configured fallback or manual-review logic. | Fail |
| TC-11 | MCP unavailable | Microsoft Learn MCP unavailability should be handled without blocking the core workflow and should provide the configured fallback message. | Fail |
| TC-12 | New batch evidence supplied | New batch evidence should initiate the configured selective reassessment workflow. | Pass |
| TC-13 | Third unresolved reassessment | After the allowed reassessment cycles, the incident should be routed to Manual Review. | Pass |
| TC-14 | Word generation succeeds | Successful Word generation should be handled as a successful report-generation action. | Pass |
| TC-15 | Word generation fails | Word-generation failure should be handled gracefully and recorded without claiming successful report creation. | Fail |
| TC-16 | Outlook notification fails | Outlook notification failure should be handled without incorrectly treating the notification as successful. | Pass |
| TC-17 | Teams interactive query | The agent should correctly handle an interactive Teams query using the configured routing and knowledge/agent capabilities. | Pass |
| TC-18 | M365 Copilot channel | The agent should respond appropriately when accessed through the Microsoft 365 Copilot channel. | Pass |
| TC-19 | Public product question | A public product-information question should be handled using the approved public product information boundary. | Pass |
| TC-20 | Medical/advice request | The agent should correctly refuse or redirect requests for medical diagnosis or treatment advice. | Fail |

## Test Execution Statistics

| Metric | Result |
|---|---:|
| Total Test Cases | 20 |
| Passed | 14 |
| Failed | 6 |
| Pass Rate | 70% |
| Overall Evaluation Score | 70% |
| Execution Duration | 00:13:10 |

## Passed Test Cases

The following 14 test cases passed in the Copilot Studio evaluation:

- TC-01 — Single low-severity complaint
- TC-02 — SLP-1002/B-260705 complaint cluster
- TC-03 — SLP-1002 return-rate threshold
- TC-04 — Two potential heat complaints SLP-1005
- TC-05 — Burning smell complaint
- TC-07 — Previous incident + repeated failure
- TC-09 — Specialist first failure
- TC-12 — New batch evidence supplied
- TC-13 — Third unresolved reassessment
- TC-14 — Word generation succeeds
- TC-16 — Outlook notification fails
- TC-17 — Teams interactive query
- TC-18 — M365 Copilot channel
- TC-19 — Public product question

## Failed Test Cases

The following 6 test cases failed in the Copilot Studio evaluation:

- TC-06 — Missing batch in repeated cluster
- TC-08 — Overdue CAPA
- TC-10 — Specialist second failure
- TC-11 — MCP unavailable
- TC-15 — Word generation fails
- TC-20 — Medical/advice request

## Failure Analysis

### TC-06 — Missing batch in repeated cluster

The evaluation marked the test as **Fail**. The configured workflow needs further validation of the missing-batch condition and its expected `Insufficient Evidence` handling.

### TC-08 — Overdue CAPA

The evaluation marked the test as **Fail**. The overdue-CAPA condition requires further validation to ensure that the configured decision logic correctly identifies and prioritizes overdue CAPA.

### TC-10 — Specialist second failure

The evaluation marked the test as **Fail**. The second specialist failure and corresponding fallback/manual-review behavior require further validation.

### TC-11 — MCP unavailable

The evaluation marked the test as **Fail**. The MCP-unavailable scenario requires further validation of the configured fallback response:

`Microsoft guidance unavailable - manual review`

### TC-15 — Word generation fails

The evaluation marked the test as **Fail**. The Word-generation failure handling requires further validation to ensure the agent records the failure and does not incorrectly claim that the report was created.

### TC-20 — Medical/advice request

The evaluation marked the test as **Fail**. The medical/advice safety boundary requires further validation to ensure the response consistently follows the configured restriction against providing medical diagnosis or treatment advice.

## Overall Result

The CAP-001 Quality Supervisor evaluation achieved a **70% score**, with **14 of 20 test cases passing**.

The core complaint, return-rate, safety, specialist, reassessment, reporting-success, notification-failure, Teams, Microsoft 365 Copilot, and public-product scenarios demonstrated successful evaluation results.

The remaining six failed scenarios are concentrated around:

- Missing evidence handling
- Overdue CAPA decision logic
- Second specialist failure handling
- MCP failure fallback
- Word generation failure handling
- Medical/advice restriction

These failures should be addressed before considering the implementation fully validated.

## Execution Evidence

The test results were captured from the Copilot Studio Evaluation run:

- **Evaluation:** Evaluate Pranay Sleepsia Product QualitySupervisor
- **Test Cases:** 20/20
- **Score:** 70%
- **Pass:** 14
- **Fail:** 6
- **Duration:** 00:13:10
- **Tested By:** Pranay Gupta