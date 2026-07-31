# Solution Summary

## Project Information

* **Project ID:** P2-003
* **Project Name:** Autonomous Sales Lead Qualification Agent
* **Platform:** Microsoft Copilot Studio
* **Technology:** Microsoft Copilot Studio with Generative Orchestration

---

# Business Problem

NovaWorks Technologies receives sales inquiries through a monitored Microsoft 365 mailbox. The existing qualification process requires Sales Operations to manually review every email, extract customer information, check for duplicate opportunities, determine lead quality, assign a sales owner, update operational records, prepare qualification documents, and send follow-up communications.

This manual approach is time-consuming, inconsistent, and susceptible to duplicate records, delayed responses, and human error. As the volume of inquiries increases, manual processing becomes difficult to scale while maintaining consistent qualification standards.

The objective of this project is to automate first-line sales lead qualification using Microsoft Copilot Studio while ensuring that uncertain, exceptional, or policy-restricted cases are routed to Sales Operations for human review.

---

# Solution Architecture

The solution is implemented as an autonomous Microsoft Copilot Studio agent that integrates Outlook, Excel Online (Business), and Word Online (Business) using Microsoft 365 connector tools.

The processing workflow is as follows:

1. An Outlook **When a new email arrives (V3)** event trigger starts the agent automatically.
2. The trigger validates that the email subject contains **[P2-003 LEAD]**.
3. The agent extracts and normalizes lead information from the email.
4. Existing records are checked to identify exact or probable duplicate opportunities.
5. The agent retrieves operational reference data from Excel Online (Business), including qualification rules, territory ownership, product catalog, sales owner information, and action rules.
6. Qualification scores are calculated using predefined business rules.
7. Override rules and confidence checks are applied to determine the final classification.
8. The appropriate sales owner is assigned based on territory and routing information.
9. The Leads Register is updated by creating a new record or updating an existing duplicate.
10. A Microsoft Word qualification report is generated for eligible leads.
11. Outlook sends acknowledgements or internal notifications according to the qualification outcome.
12. Human Review cases are recorded and routed to Sales Operations without sending an external qualification decision.

---

# Solution Logic

The agent processes only emails whose subject contains **[P2-003 LEAD]**, ensuring unrelated mailbox messages are ignored.

Lead information is extracted from unstructured email content, including contact details, organization information, product interest, business requirements, budget, purchase timeline, company size, country, and decision role. Extracted values are normalized using the operational reference tables before qualification.

Duplicate detection first compares the Outlook Message ID. If no exact match exists, the agent compares company name, sender email address, and product interest to identify probable duplicates. Existing records are updated instead of creating duplicate entries, and duplicate acknowledgement emails or Word reports are prevented.

Qualification scoring evaluates the lead across Product Fit, Budget Viability, Purchase Timeline, Decision Role, Company Size, Territory, Lead Source, and Information Completeness. The calculated score is combined with business override rules to determine the final classification.

The agent assigns one of the following classifications:

* Hot
* Qualified
* Nurture
* Low Priority
* Additional Information Required
* Human Review Required
* Duplicate
* Not a Sales Lead

Depending on the classification, the agent automatically updates the Excel Lead Register, generates a Word qualification report when required, sends Outlook communications, assigns the appropriate sales owner, or routes exceptional cases for human review. Tool failures are retried once for transient errors, and unsuccessful actions are not reported as completed.

---

# Solution Outcomes

The implemented solution provides an autonomous and auditable lead qualification process that reduces manual effort while maintaining consistent business rules.

Key outcomes include:

* Automatic processing of qualifying Outlook emails.
* Consistent extraction and normalization of lead information.
* Prevention of duplicate lead records and duplicate communications.
* Rule-based lead qualification and classification.
* Automatic assignment of sales owners using operational reference data.
* Automated updates to the Excel Lead Register.
* Automatic generation of Microsoft Word qualification reports for eligible leads.
* Controlled Outlook communications based on qualification outcomes.
* Human review routing for uncertain, exceptional, or non-sales inquiries.
* Improved auditability, transparency, and operational consistency through Microsoft Copilot Studio and Microsoft 365 integration.
