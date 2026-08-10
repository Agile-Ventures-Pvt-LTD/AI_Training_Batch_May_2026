# Qualification Logic

## Purpose

The Autonomous Sales Lead Qualification Agent evaluates incoming sales enquiries using predefined business rules and operational reference tables. The qualification process ensures consistent scoring, classification, duplicate prevention, and routing while maintaining controlled autonomy.

---

# Qualification Process

The agent performs the following sequence:

1. Validate that the email subject contains **[P2-003 LEAD]**.
2. Extract lead information from the email.
3. Check for duplicate opportunities.
4. Validate the requested product.
5. Retrieve qualification rules from the operational reference tables.
6. Determine the sales territory.
7. Assign the appropriate sales owner.
8. Calculate the qualification score.
9. Apply business override rules.
10. Determine the final classification.
11. Update or create the Lead Register record.
12. Generate a Microsoft Word qualification report when required.
13. Send the appropriate Outlook communication.

---

# Scoring Dimensions

The qualification score is calculated using the following dimensions:

| Dimension         | Maximum Points |
| ----------------- | -------------: |
| Product Fit       |             20 |
| Budget Viability  |             20 |
| Purchase Timeline |             15 |
| Decision Role     |             15 |
| Company Size      |             10 |
| Territory         |             10 |
| Lead Source       |              5 |
| Completeness      |              5 |

**Maximum Total Score:** **100**

The detailed point values are obtained from the **QualificationRulesTable**.

---

# Classification Thresholds

| Classification                  | Score / Rule                                                                                                                                                                                 |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hot                             | 85–100 and no exception condition                                                                                                                                                            |
| Qualified                       | 70–84 and no exception condition                                                                                                                                                             |
| Nurture                         | 50–69                                                                                                                                                                                        |
| Low Priority                    | Below 50 or commercial viability override                                                                                                                                                    |
| Additional Information Required | Three or more mandatory fields are missing                                                                                                                                                   |
| Human Review Required           | Low confidence, unknown product, unmapped territory, conflicting information, competitor enquiry, support request, recruitment request, academic research request, spam, or tool uncertainty |
| Duplicate                       | Existing matching message or opportunity                                                                                                                                                     |
| Not a Sales Lead                | Non-commercial enquiry or request outside the sales process                                                                                                                                  |

---

# Override Rules

The following business rules override the calculated qualification score:

* Startup/Micro leads with a budget below 50% of the product minimum are classified as **Low Priority**, regardless of score.
* Low-confidence assessments are routed to **Human Review Required**.
* Unknown products require **Human Review Required**.
* Unmapped territories require **Human Review Required**.
* Support, recruitment, academic research, competitor, or spam requests are not processed as standard sales opportunities.

---

# Duplicate Detection

The agent prevents duplicate processing by checking:

1. Exact **Message ID**.
2. Sender Email.
3. Company Name.
4. Product Interest.

When a duplicate is identified:

* The existing Lead Register record is updated.
* A new Lead Register record is not created.
* A duplicate Word report is not generated.
* A duplicate acknowledgement email is not sent.
* The processing outcome is recorded as **Duplicate**.

---

# Normalization Rules

Before qualification, extracted values are normalized using operational reference tables.

The agent normalizes:

* Country names using **TerritoryOwnersTable**.
* Product names using **ProductCatalogTable**.
* Company Size to one of:

  * Enterprise
  * Mid-Market
  * SMB
  * Startup/Micro
* Decision Role to one of:

  * Decision Maker
  * Strong Influencer
  * Researcher/User
  * Unknown

Missing budget and purchase timeline remain **Unknown** rather than being treated as zero.

---

# Qualification Outcomes

Based on the final classification, the agent performs the following actions:

| Classification                  | Autonomous Action                                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Hot                             | Create Lead Register record, generate Word report, assign owner, notify Sales Operations, send acknowledgement |
| Qualified                       | Create Lead Register record, generate Word report, assign owner, send acknowledgement                          |
| Nurture                         | Create Lead Register record and send limited acknowledgement or request missing information                    |
| Low Priority                    | Create Lead Register record without qualification report or sales acknowledgement                              |
| Additional Information Required | Create incomplete record and request required information                                                      |
| Human Review Required           | Create or update record, notify Sales Operations, withhold external qualification decision                     |
| Duplicate                       | Update existing record without creating duplicate reports or communications                                    |
| Not a Sales Lead                | Record the processing outcome and prevent sales qualification actions                                          |

---

# Error Handling

The qualification process supports controlled error handling for:

* Excel lookup failures
* Excel update failures
* Word document creation failures
* Outlook communication failures
* Missing connector connections
* Invalid tables
* Ambiguous products
* Ambiguous territories
* Malformed emails
* Repeated trigger deliveries

One controlled retry is permitted for transient failures. If the retry is unsuccessful, the failure is recorded where possible, Sales Operations is notified when appropriate, and unsuccessful actions are not reported as completed.
