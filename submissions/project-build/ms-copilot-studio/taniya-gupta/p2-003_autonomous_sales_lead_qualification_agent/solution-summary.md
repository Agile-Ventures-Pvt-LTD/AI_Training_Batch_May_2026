# solution-summary.md — Solution Summary
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Business Problem

NovaWorks receives inbound sales lead emails from prospects across multiple countries and product lines. Without automation, a human sales operations analyst must manually read each email, extract contact and opportunity information, score the lead, assign it to the correct regional owner, create a qualification report, and send acknowledgement and notification emails. This process is slow, inconsistent and error-prone — especially at volume.

The P2-003 project automates the entire intake-to-notification workflow using an autonomous AI agent.

---

## Solution Architecture

```
[Prospect sends email with subject [P2-003 LEAD]]
        |
        v
[Outlook Inbox — monitored mailbox]
        |
        v
[Copilot Studio Agent — triggered automatically]
        |
        +---> Step 1: Parse email → extract 11 fields
        |
        +---> Step 2: Classify inquiry type
        |           (Sales / Support / Academic / Competitor / Spam)
        |
        +---> Step 3: Check for duplicate
        |           (Excel Get Rows → LeadsRegisterTable)
        |
        +---> Step 4: Normalise values
        |           (Country → Territory, Company Size, Decision Role)
        |
        +---> Step 5: Score lead (8 dimensions, max 100 points)
        |
        +---> Step 6: Apply override rules
        |           (Startup override, territory exception, confidence check)
        |
        +---> Step 7: Classify
        |           (Hot / Qualified / Nurture / Low Priority /
        |            Human Review / Additional Info / Duplicate / Non-Sales)
        |
        +---> Step 8: Assign owner
        |           (Territory → Owner lookup from TerritoryOwnersTable)
        |
        +---> Step 9: Take autonomous actions
                    |
                    +---> Excel: Add or update row in LeadsRegisterTable
                    +---> Word: Create qualification report (Hot and Qualified only)
                    +---> Outlook: Send acknowledgement to sender
                    +---> Outlook: Send internal alert to assigned owner
                    +---> Outlook: Notify Sales Operations (Hot and Human Review)
```

---

## Components

### Microsoft Copilot Studio
The agent is built entirely in Copilot Studio with generative orchestration enabled. All logic runs inside the agent instruction prompt, supported by connected tools.

### Knowledge Source
`NovaWorks_Sales_Lead_Qualification_and_Autonomy_Policy.docx` is uploaded as the agent knowledge source. It contains the qualification rules, scoring bands, classification thresholds, override conditions, communication boundaries and autonomy constraints.

### Excel Workbook (OneDrive)
`P2-003_Sales_Lead_Operational_Data.xlsx` contains six named tables:
- LeadsRegisterTable — all lead records
- QualificationRulesTable — scoring rules reference
- TerritoryOwnersTable — country-to-owner mapping
- ProductCatalogTable — product list with minimum budgets
- SalesOwnersTable — owner capacity and email data
- ActionMatrixTable — required actions per classification

### Word Online Tool
Used to generate structured qualification reports for Hot and Qualified leads. Reports are saved to the root folder in OneDrive.

### Office 365 Outlook Tool
Used to send external acknowledgements to senders and internal notifications to owners and Sales Operations.

---

## Supported Products

| Product | Minimum Budget | Category |
|---|---|---|
| AI Agent Enablement Workshop | $15,000 | Training |
| Enterprise RAG Knowledge Assistant | $60,000 | Solution |
| Autonomous Sales Operations Agent | $90,000 | Solution |
| Multi-Agent Service Operations System | $140,000 | Solution |
| AI Governance and Evaluation Accelerator | $75,000 | Advisory |
| Custom Agentic AI Platform Implementation | $250,000 | Implementation |

---

## Supported Territories

| Country | Territory | Assigned Owner |
|---|---|---|
| India | South Asia | Priya Nair |
| United States | North America | Sophia Carter |
| Canada | North America | Sophia Carter |
| United Kingdom | UK and Ireland | Emma Clarke |
| Ireland | UK and Ireland | Emma Clarke |
| United Arab Emirates | Middle East | Omar Rahman |
| Singapore | Southeast Asia | Daniel Tan |
| Australia | ANZ | Olivia Bennett |
| Germany | Western Europe | Lucas Martin |
| France | Western Europe | Lucas Martin |
| South Africa | Africa | Amina Mensah |
| Other / Unmapped | Unassigned | Sales Operations (Human Review) |

---

## Outcomes

### Agent Capabilities Delivered
- Autonomous end-to-end processing from email receipt to owner notification
- 8-dimension scoring model producing scores from 0 to 100
- Five classification paths plus three special-case paths
- Override rules enforced for Startup/Micro budget exceptions and unmapped territories
- Duplicate detection using Excel lookup before any new record is created
- Tool failure handling with one-retry logic and internal escalation
- Idempotency — repeated email triggers produce only one record

### Evaluation Results
- 23 test cases executed covering all PRD mandatory scenario categories
- 23 of 23 passed (100% pass rate)
- Test method: Compare Meaning in Copilot Studio Evaluate panel

---

## Constraints
- The agent operates within one Microsoft 365 tenant
- All external email addresses in test data use `.example` domains and are non-routable
