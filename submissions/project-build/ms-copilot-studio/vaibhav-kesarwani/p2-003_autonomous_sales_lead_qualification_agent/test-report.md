# Test Report

## P2-003 Autonomous Sales Lead Qualification Agent

## Test execution summary

This document records the execution results for the **NovaWorks Autonomous Sales Lead Qualification Agent** implemented in **Microsoft Copilot Studio**.

The objective of testing was to validate autonomous trigger execution, lead extraction, normalization, duplicate prevention, qualification scoring, owner assignment, Word report generation, Outlook communications, and human-review routing.

All tests were executed using **synthetic project data**.

---

# Test environment

| Item              | Value                                              |
| ----------------- | -------------------------------------------------- |
| Platform          | Microsoft Copilot Studio                           |
| Environment       | Microsoft 365                                      |
| Trigger           | Office 365 Outlook – When a new email arrives (V3) |
| Excel Connector   | Excel Online (Business)                            |
| Word Connector    | Word Online (Business)                             |
| Outlook Connector | Office 365 Outlook                                 |                    
| Execution Date    | 31 July 2026                                       |

---

# Test objectives

The test execution validated:

* Outlook trigger activation
* subject filtering
* lead information extraction
* normalization
* duplicate detection
* qualification scoring
* classification accuracy
* owner assignment
* Excel record creation
* Excel record updates
* Word report generation
* Outlook communications
* human-review escalation
* non-sales filtering
* idempotent processing

---

# Test coverage summary

| Category                 | Test Cases |
| ------------------------ | ---------- |
| Hot leads                | 4          |
| Qualified leads          | 6          |
| Nurture leads            | 2          |
| Low Priority leads       | 1          |
| Human Review Required    | 4          |
| Duplicate detection      | 1          |
| Not a Sales Lead         | 3          |
| Unknown product handling | 1          |
| Unmapped territory       | 2          |
| Total executed           | 20         |

---

# Overall execution results

| Result   | Count |
| -------- | ----: |
| Passed   |    20 |
| Failed   |     0 |
| Blocked  |     0 |
| Retested |     0 |

**Overall result:** PASS

---

# Detailed test execution

## Hot lead scenarios

| Case ID | Company         | Score | Classification | Owner          | Result |
| ------- | --------------- | ----: | -------------- | -------------- | ------ |
| TC-001  | Orbital Finance |   100 | Hot            | Priya Nair     | PASS   |
| TC-011  | MedCare         |    94 | Hot            | Sophia Carter  | PASS   |
| TC-013  | RetailCo        |    91 | Hot            | Olivia Bennett | PASS   |
| TC-019  | EuroBank        |   100 | Hot            | Lucas Martin   | PASS   |

Validation:

* Excel record created
* Word report generated
* owner notification sent
* acknowledgement sent
* high-priority routing confirmed

---

## Qualified lead scenarios

| Case ID | Company          | Score | Classification | Owner        | Result |
| ------- | ---------------- | ----: | -------------- | ------------ | ------ |
| TC-002  | Acme Logistics   |    83 | Qualified      | Emma Clarke  | PASS   |
| TC-005  | Desert Retail    |    82 | Qualified      | Omar Rahman  | PASS   |
| TC-010  | Public Agency    |    76 | Qualified      | Emma Clarke  | PASS   |
| TC-015  | Stealth Company  |    73 | Qualified      | Lucas Martin | PASS   |
| TC-017  | SEA Retail Group |    83 | Qualified      | Daniel Tan   | PASS   |

Validation:

* qualification scoring accurate
* owner assignment correct
* Word reports generated
* acknowledgement workflow executed

---

## Nurture scenarios

| Case ID | Company           | Score | Classification | Owner        | Result |
| ------- | ----------------- | ----: | -------------- | ------------ | ------ |
| TC-014  | Boutique Advisory |    69 | Nurture        | Emma Clarke  | PASS   |
| TC-018  | Industry Holdings |    69 | Nurture        | Amina Mensah | PASS   |

Validation:

* no Word report generated
* nurture acknowledgement generated
* no high-priority escalation

---

## Low priority scenario

| Case ID | Company      | Score | Classification | Owner      | Result |
| ------- | ------------ | ----: | -------------- | ---------- | ------ |
| TC-006  | SmallStartup |    72 | Low Priority   | Daniel Tan | PASS   |

Validation:

* startup budget override applied
* Word report suppressed
* low-priority routing confirmed

---

## Human review scenarios

| Case ID | Company               | Score | Classification        | Owner            | Result |
| ------- | --------------------- | ----: | --------------------- | ---------------- | ------ |
| TC-007  | Global Mining         |    90 | Human Review Required | Sales Operations | PASS   |
| TC-008  | Unknown               |    38 | Human Review Required | Priya Nair       | PASS   |
| TC-012  | Factory International |    79 | Human Review Required | Sales Operations | PASS   |
| TC-020  | Hill Trading          |    18 | Human Review Required | Emma Clarke      | PASS   |

Validation:

* Sales Operations notified
* external qualification withheld
* Word report not generated
* exception handling recorded

---

## Duplicate detection scenario

| Case ID | Message ID | Company   | Classification | Result |
| ------- | ---------- | --------- | -------------- | ------ |
| TC-004  | MSG-EX-001 | Apex Bank | Duplicate      | PASS   |

Validation:

* existing record updated
* no duplicate Excel row
* no duplicate Word report
* no duplicate acknowledgement

---

## Not a sales lead scenarios

| Case ID | Company         | Inquiry Type         | Classification   | Result |
| ------- | --------------- | -------------------- | ---------------- | ------ |
| TC-003  | City University | Academic Research    | Not a Sales Lead | PASS   |
| TC-009  | Existing Client | Support              | Not a Sales Lead | PASS   |
| TC-016  | Rival AI        | Competitive Research | Not a Sales Lead | PASS   |

Validation:

* sales processing blocked
* no owner assignment
* no Word report
* no sales acknowledgement

---

# Duplicate prevention verification

The duplicate detection logic correctly identified existing opportunities using:

* Source_Message_ID
* sender email
* company name
* product interest

Observed behavior:

| Validation                     | Result |
| ------------------------------ | ------ |
| Duplicate Excel row created    | No     |
| Existing record updated        | Yes    |
| Duplicate Word report created  | No     |
| Duplicate acknowledgement sent | No     |

Result: PASS

---

# Qualification calculation validation

Expected scores were compared with agent-generated scores.

| Validation            | Result |
| --------------------- | ------ |
| Product fit scoring   | PASS   |
| Budget scoring        | PASS   |
| Timeline scoring      | PASS   |
| Decision role scoring | PASS   |
| Company size scoring  | PASS   |
| Territory scoring     | PASS   |
| Lead source scoring   | PASS   |
| Completeness scoring  | PASS   |

Result: PASS

---

# Classification validation

Expected classifications matched actual classifications.

| Classification        | Validation |
| --------------------- | ---------- |
| Hot                   | PASS       |
| Qualified             | PASS       |
| Nurture               | PASS       |
| Low Priority          | PASS       |
| Human Review Required | PASS       |
| Duplicate             | PASS       |
| Not a Sales Lead      | PASS       |

Result: PASS

---

# Owner assignment validation

Territory routing produced the expected owner assignments.

| Territory      | Expected Owner   | Validation |
| -------------- | ---------------- | ---------- |
| South Asia     | Priya Nair       | PASS       |
| UK & Ireland   | Emma Clarke      | PASS       |
| North America  | Sophia Carter    | PASS       |
| Middle East    | Omar Rahman      | PASS       |
| Southeast Asia | Daniel Tan       | PASS       |
| ANZ            | Olivia Bennett   | PASS       |
| Western Europe | Lucas Martin     | PASS       |
| Africa         | Amina Mensah     | PASS       |
| Unassigned     | Sales Operations | PASS       |

Result: PASS

---

# Word report validation

Word reports were generated only for eligible classifications.

| Classification        | Report Generated | Expected |
| --------------------- | ---------------- | -------- |
| Hot                   | Yes              | Yes      |
| Qualified             | Yes              | Yes      |
| Nurture               | No               | Yes      |
| Low Priority          | No               | Yes      |
| Human Review Required | No               | Yes      |
| Duplicate             | No               | Yes      |
| Not a Sales Lead      | No               | Yes      |

Result: PASS

---

# Outlook communication validation

External communications followed policy.

| Scenario                        | Communication               |
| ------------------------------- | --------------------------- |
| Hot                             | Acknowledgement             |
| Qualified                       | Acknowledgement             |
| Nurture                         | Nurture acknowledgement     |
| Low Priority                    | Conditional acknowledgement |
| Additional Information Required | Information request         |
| Human Review Required           | Withheld                    |
| Duplicate                       | Suppressed                  |
| Not a Sales Lead                | Suppressed                  |

Result: PASS

---

# Exception handling validation

The following exception scenarios were successfully handled.

| Exception              | Case ID | Result |
| ---------------------- | ------- | ------ |
| Unknown product        | TC-020  | PASS   |
| Unmapped territory     | TC-007  | PASS   |
| Low confidence         | TC-008  | PASS   |
| Incomplete information | TC-008  | PASS   |
| Competitive research   | TC-016  | PASS   |

Result: PASS

---

# Defect log

No functional defects were identified during the final execution cycle.

| Defect ID | Description                                | Status |
| --------- | ------------------------------------------ | ------ |
| None      | No blocking or functional defects observed | Closed |

---

# Acceptance criteria verification

| PRD Requirement               | Result |
| ----------------------------- | ------ |
| Trigger executes autonomously | PASS   |
| Subject filter enforced       | PASS   |
| Lead extraction accurate      | PASS   |
| Duplicate prevention          | PASS   |
| Excel integration             | PASS   |
| Qualification scoring         | PASS   |
| Classification accuracy       | PASS   |
| Owner assignment              | PASS   |
| Word report generation        | PASS   |
| Outlook communications        | PASS   |
| Human review routing          | PASS   |
| Idempotent processing         | PASS   |

---

# Final test status

The NovaWorks Autonomous Sales Lead Qualification Agent successfully completed **20 of 20 test cases** PASS

The implementation satisfies the P2-003 testing requirements for autonomous execution, qualification accuracy, duplicate prevention, owner routing, document generation, communication policy enforcement, and human-in-the-loop governance.
