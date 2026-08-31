# Test Report

## Project Information

| Field                | Value                                     |
| -------------------- | ----------------------------------------- |
| **Project ID**       | P2-003                                    |
| **Project Title**    | Autonomous Sales Lead Qualification Agent |
| **Participant Name** | Pranay Gupta                      |
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent                           |
| **Platform**         | Microsoft Copilot Studio                  |
| **Execution Date**   | 31/07/2026                        |

---

# Test Environment

| Component                | Status     |
| ------------------------ | ---------- |
| Microsoft Copilot Studio | Configured |
| Office 365 Outlook       | Connected  |
| Excel Online (Business)  | Connected  |
| Word Online (Business)   | Connected  |
| Generative Orchestration | Enabled    |

---

# Test Summary

| Metric           | Result   |
| ---------------- | -------- |
| Total Test Cases | 20       |
| Executed         | 20       |
| Passed           | 20       |
| Failed           | 0        |
| Overall Result   | **PASS** |

---

# Test Execution Results

| Test ID    | Test Scenario                                | Expected Behaviour                                                         | Actual Result                                                                                                            | Status |
| ---------- | -------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------ |
| **TC-001** | Enterprise multi-agent platform enquiry      | Lead qualified, owner assigned, report generated and acknowledgement sent. | Lead extracted successfully, classified as **Hot**, Excel updated, Word report generated and acknowledgement email sent. | ✅ Pass |
| **TC-002** | Sales automation enquiry                     | Commercial opportunity processed successfully.                             | Lead processed successfully, classified as **Qualified**, owner assigned and report generated.                           | ✅ Pass |
| **TC-003** | Academic research request                    | Should not be treated as a sales lead.                                     | Identified as **Not a Sales Lead**. No report or sales acknowledgement generated.                                        | ✅ Pass |
| **TC-004** | Existing enquiry follow-up                   | Detect duplicate and avoid duplicate processing.                           | Existing enquiry detected and processed as **Duplicate**. Existing record updated without creating a new lead.           | ✅ Pass |
| **TC-005** | Service operations automation                | Commercial lead should be qualified.                                       | Lead processed successfully, classified as **Qualified**, operational records updated and acknowledgement sent.          | ✅ Pass |
| **TC-006** | Startup with limited budget                  | Apply budget override rules.                                               | Business override applied. Classified as **Low Priority** due to insufficient budget.                                    | ✅ Pass |
| **TC-007** | Governance engagement                        | Valid commercial opportunity.                                              | Lead qualified successfully, assigned to sales owner and qualification report generated.                                 | ✅ Pass |
| **TC-008** | Minimal information provided                 | Request additional information.                                            | Classified as **Additional Information Required** and follow-up email generated requesting missing details.              | ✅ Pass |
| **TC-009** | Product support request                      | Should not enter sales workflow.                                           | Identified as **Support Request / Not a Sales Lead**. Sales qualification workflow skipped.                              | ✅ Pass |
| **TC-010** | Long-term governance enquiry                 | Apply qualification considering long timeline.                             | Lead evaluated successfully and classified appropriately based on qualification rules.                                   | ✅ Pass |
| **TC-011** | Clinical knowledge search                    | Process valid enterprise enquiry.                                          | Lead qualified successfully, report generated and acknowledgement email sent.                                            | ✅ Pass |
| **TC-012** | Pricing enquiry with missing sponsor         | Request missing mandatory information.                                     | Classified as **Additional Information Required** and information request email generated.                               | ✅ Pass |
| **TC-013** | AI workshop request                          | Process commercial workshop enquiry.                                       | Lead qualified successfully, owner assigned and acknowledgement email sent.                                              | ✅ Pass |
| **TC-014** | Boutique workshop enquiry                    | Process workshop opportunity.                                              | Workshop enquiry qualified and operational records updated successfully.                                                 | ✅ Pass |
| **TC-015** | Limited company information                  | Request additional information.                                            | Missing mandatory details detected and additional information requested before qualification.                            | ✅ Pass |
| **TC-016** | Competitor research request                  | Protect confidential information.                                          | Routed to **Human Review Required**. No confidential business information disclosed.                                     | ✅ Pass |
| **TC-017** | Multi-country sales automation               | Assign territory owner correctly.                                          | Territory mapped successfully, sales owner assigned and lead processed successfully.                                     | ✅ Pass |
| **TC-018** | Manufacturing assessment enquiry             | Qualify according to business rules.                                       | Lead processed successfully, classified appropriately and operational records updated.                                   | ✅ Pass |
| **TC-019** | Urgent governance programme                  | High-priority commercial opportunity.                                      | Classified as **Hot**, report generated, sales owner assigned and acknowledgement email sent.                            | ✅ Pass |
| **TC-020** | General AI enquiry without product selection | Request missing product information.                                       | Classified as **Additional Information Required** and follow-up email sent requesting product/use-case details.          | ✅ Pass |

---

# Functional Coverage

The executed test cases validated the following functionalities:

* Outlook email trigger
* Subject-based filtering
* Lead information extraction
* Data normalization
* Duplicate detection
* Qualification scoring
* Lead classification
* Sales owner assignment
* Excel record creation and update
* Microsoft Word report generation
* Outlook email notifications
* Human review routing
* Privacy and security controls
* End-to-end autonomous workflow

---

# Conclusion

All planned test cases were executed successfully. The Autonomous Sales Lead Qualification Agent correctly processed valid commercial enquiries, rejected non-sales requests, handled duplicate scenarios, generated qualification reports for eligible leads, updated operational records, and sent the appropriate Outlook communications in accordance with the project requirements.
