# P2-003 Autonomous Sales Lead Qualification Agent

## Project Information

**Project ID:** P2-003
**Project Name:** Autonomous Sales Lead Qualification Agent
**Platform:** Microsoft Copilot Studio
**Project Type:** Individual Autonomous Agent Build

---

# Project Overview

This project implements an autonomous Sales Lead Qualification Agent using Microsoft Copilot Studio. The agent automatically processes incoming sales inquiry emails received through Outlook, extracts business information, checks for duplicate opportunities, evaluates lead qualification using operational reference data, assigns a sales owner, updates the lead register, generates qualification reports when required, and sends appropriate Outlook communications.

The solution uses Microsoft Copilot Studio generative orchestration together with Outlook, Excel Online (Business), and Word Online (Business) connector tools to automate the complete first-level lead qualification process while routing uncertain or exceptional cases for human review.

---

# Business Problem

NovaWorks Technologies receives sales inquiries through a monitored Microsoft 365 mailbox. The manual qualification process is time-consuming and may lead to inconsistent lead evaluation, duplicate entries, delayed responses, and additional operational effort.

This autonomous agent standardizes the qualification process by applying predefined business rules, reducing manual work, improving consistency, and maintaining an auditable qualification workflow.

---

# Solution Features

* Autonomous Outlook email processing
* Outlook event trigger using **When a new email arrives (V3)**
* Subject filtering for **[P2-003 LEAD]**
* Lead information extraction from email content
* Data normalization
* Duplicate detection
* Qualification scoring
* Lead classification
* Sales owner assignment
* Excel Lead Register updates
* Word qualification report generation
* Outlook acknowledgements and internal notifications
* Human review routing for uncertain or non-sales requests
* Activity monitoring and auditing

---

# Microsoft 365 Components Used

* Microsoft Copilot Studio
* Office 365 Outlook
* Excel Online (Business)
* Word Online (Business)
* OneDrive for Business

---

# Agent Workflow

1. Outlook receives a new email.
2. The trigger validates that the subject contains **[P2-003 LEAD]**.
3. The agent extracts lead information from the email.
4. Duplicate records are identified.
5. Operational reference tables are read from Excel.
6. Qualification scores are calculated.
7. The lead is classified according to business rules.
8. A sales owner is assigned.
9. The Lead Register is created or updated.
10. A Word qualification report is generated when applicable.
11. Outlook communications are sent according to the qualification outcome.
12. Exceptional cases are routed for human review.

---

# Configuration Status

| Component                     | Status       |
| ----------------------------- | ------------ |
| Agent Created                 | ✅ Completed  |
| Generative Orchestration      | ✅ Enabled    |
| Outlook Trigger               | ✅ Configured |
| Outlook Tools                 | ✅ Configured |
| Excel Online (Business) Tools | ✅ Configured |
| Word Online (Business) Tool   | ✅ Configured |
| Knowledge Sources             | ✅ Added      |
| Agent Published               | ✅ Published  |
| Testing                       | ✅ Completed  |

---

# Repository Structure

```text
submissions/
└── project-build/
    └── ms-copilot-studio/
        └── firstname-lastname/
            └── p2-003_autonomous_sales_lead_qualification_agent/
```

---

# Published Agent

**Agent Name:** Autonomous Sales Lead Qualification Agent

**Published URL:** *(Add your published Copilot Studio agent URL here.)*

**Authentication:** Microsoft 365 Account Required

---

# AI Usage

AI was used to assist with:

* Requirement analysis
* Agent instruction design
* Documentation preparation
* Test scenario preparation
* Technical clarification

All configuration, validation, testing, and final verification were completed manually.

---

# Project Completion Status

The autonomous agent was implemented in Microsoft Copilot Studio according to the project requirements. The solution includes autonomous event triggering, lead extraction, qualification logic, duplicate detection, Excel integration, Word report generation, Outlook communication, and human review handling using Microsoft 365 services.
