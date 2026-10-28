# Phase 02 - Project Build 003 Autonomous Sales Lead Qualification Agent

## Project summary

This project implements an autonomous Sales Lead Qualification Agent using Microsoft Copilot Studio.

The agent automatically processes inbound Outlook emails, determines whether they represent valid sales opportunities, extracts structured business information, checks for duplicate opportunities, applies qualification scoring, assigns the appropriate sales owner, updates the Excel lead register, generates Microsoft Word qualification reports when required, and sends the appropriate Outlook communications.

The solution is fully autonomous within the Microsoft 365 ecosystem and uses:

* Office 365 Outlook event triggers
* Excel Online (Business)
* Word Online (Business)
* Generative orchestration
* Connector-based tool execution

The implementation follows the P2-003 Product Requirements Document (PRD) and does not rely on external automation platforms or separate Power Automate cloud flows.

---

## Business objective

The objective is to automate first-line sales lead qualification while ensuring:

* consistent lead assessment
* deterministic scoring
* duplicate prevention
* owner assignment
* auditable processing
* controlled autonomy
* human review for uncertain cases

---

## Solution architecture

```text
Outlook Trigger
        |
        v
Email Validation
        |
        v
Duplicate Detection
        |
        v
Lead Extraction
        |
        v
Excel Reference Tables
        |
        v
Qualification Scoring
        |
        v
Classification & Owner Assignment
        |
        v
Excel Lead Register Update
        |
        +------> Word Qualification Report
        |
        +------> Outlook Notifications
```

---

## Autonomous workflow

1. Outlook receives a new email.
2. Trigger validates the subject filter.
3. Lead information is extracted.
4. Excel reference tables are read.
5. Duplicate detection is performed.
6. Qualification scoring is calculated.
7. Classification is assigned.
8. Sales owner is determined.
9. Excel is updated.
10. Word report is generated when required.
11. Outlook communications are sent.
12. Human review is triggered when necessary.

---

## Published agent URL

| Item                    | Status                       |
| ----------------------- | ---------------------------- |
| Published Agent URL     | [URL](https://teams.microsoft.com/l/app/?titleId=T_9ced1082-8fd0-f917-570b-b9ffae694fd5) |
| Authentication Required | Yes                          |

Reference: [`agent-url.md`](./agent-url.md)

---

## Configuration status

### Generative orchestration

| Component                        | Status   |
| -------------------------------- | -------- |
| Generative orchestration enabled | Complete |
| Autonomous execution enabled     | Complete |
| Tool calling enabled             | Complete |

### Outlook trigger

| Configuration                 | Status   |
| ----------------------------- | -------- |
| When a new email arrives (V3) | Complete |
| Subject filter: [P2-003 LEAD] | Complete |
| Trigger folder configured     | Complete |
| Trigger input mapping         | Complete |

### Excel Online (Business)

| Tool                            | Status   |
| ------------------------------- | -------- |
| List rows present in a table    | Complete |
| Add a row into a table          | Complete |
| Update a row using a key column | Complete |
| LeadsRegisterTable              | Complete |
| QualificationRulesTable         | Complete |
| TerritoryOwnersTable            | Complete |
| ProductCatalogTable             | Complete |
| SalesOwnersTable                | Complete |
| ActionMatrixTable               | Complete |

### Word Online (Business)

| Tool                        | Status   |
| --------------------------- | -------- |
| Create qualification report | Complete |
| Dynamic filename generation | Complete |
| Report storage location     | Complete |

### Outlook communication tools

| Tool                             | Status   |
| -------------------------------- | -------- |
| Send acknowledgement             | Complete |
| Send missing-information request | Complete |
| Notify sales owner               | Complete |
| Notify Sales Operations          | Complete |

---

## Functional status

| Capability                | Status   |
| ------------------------- | -------- |
| Trigger validation        | Complete |
| Lead extraction           | Complete |
| Field normalization       | Complete |
| Duplicate detection       | Complete |
| Qualification scoring     | Complete |
| Classification assignment | Complete |
| Territory routing         | Complete |
| Owner assignment          | Complete |
| Excel record creation     | Complete |
| Excel record update       | Complete |
| Word report generation    | Complete |
| Outlook acknowledgement   | Complete |
| Internal notifications    | Complete |
| Retry handling            | Complete |

---

## Completion status

### Implementation progress

| Phase                                | Status   |
| ------------------------------------ | -------- |
| Microsoft 365 storage setup          | Complete |
| Agent creation                       | Complete |
| Trigger configuration                | Complete |
| Tool configuration                   | Complete |
| Agent instruction design             | Complete |
| Qualification logic implementation   | Complete |
| Word report implementation           | Complete |
| Outlook communication implementation | Complete |
| Autonomous decision paths            | Complete |
| Testing                              | Complete |
| Publishing                           | Pending  |
| GitHub documentation                 | Complete |

---

## Required data sources

The agent uses the operational Excel workbook containing:

* LeadsRegisterTable
* QualificationRulesTable
* TerritoryOwnersTable
* ProductCatalogTable
* SalesOwnersTable
* ActionMatrixTable

All data is stored in OneDrive.

---

## Qualification outcomes

The agent supports the following autonomous outcomes:

* Hot
* Qualified
* Nurture
* Low Priority
* Additional Information Required
* Human Review Required
* Duplicate
* Not a Sales Lead

---

## Human review boundary

The agent escalates cases involving:

* unknown products
* unmapped territories
* low confidence extraction
* conflicting information
* competitor risk
* repeated tool failures

No autonomous qualification decision is communicated externally for Human Review Required cases.

---

## Testing summary

Testing covers:

* Hot leads
* Qualified leads
* Nurture leads
* Low Priority leads
* Human Review cases
* Additional Information Required
* Duplicate detection
* Non-sales messages
* Unknown products
* Unmapped territories
* Tool failure scenarios
* Idempotency testing

Reference: [`test-report.md`](./test-report.md)

---

## Repository structure

```text
p2-003_autonomous_sales_lead_qualification_agent/
│
├── README.md
├── agent-url.md
├── solution-summary.md
├── agent-instructions-design.md
├── trigger-design.md
├── tool-design.md
├── qualification-logic.md
├── test-report.md
├── known-limitations.md
└── ai-usage-declaration.md
```

---

## Documentation references

* [`agent-url.md`](./agent-url.md)
* [`solution-summary.md`](./solution-summary.md)
* [`agent-instructions-design.md`](./agent-instructions-design.md)
* [`trigger-design.md`](./trigger-design.md)
* [`tool-design.md`](./tool-design.md)
* [`qualification-logic.md`](./qualification-logic.md)
* [`test-report.md`](./test-report.md)
* [`known-limitations.md`](./known-limitations.md)
* [`ai-usage-declaration.md`](./ai-usage-declaration.md)

---

## PRD compliance status

| PRD Requirement        | Status   |
| ---------------------- | -------- |
| Outlook event trigger  | Complete |
| Subject filtering      | Complete |
| Excel reference tables | Complete |
| Duplicate prevention   | Complete |
| Qualification scoring  | Complete |
| Owner assignment       | Complete |
| Word report generation | Complete |
| Outlook communications | Complete |
| Human review boundary  | Complete |
| Autonomous execution   | Complete |
| Auditable processing   | Complete |
| Microsoft 365 storage  | Complete |

---

## Final status

The autonomous Sales Lead Qualification Agent has been designed and configured according to the P2-003 PRD. The solution implements event-driven autonomous processing, deterministic qualification logic, Microsoft 365 connector integration, controlled autonomy, and human-review safeguards.
