# Autonomous Sales Lead Qualification Agent

## Project Overview

The **Sales Lead Qualification Agent (Palak)** is an AI-powered autonomous agent developed using **Microsoft Copilot Studio** to automate the end-to-end qualification of inbound sales enquiries. The agent continuously monitors Outlook for new lead emails, extracts structured business information, validates the extracted data using operational reference tables stored in Excel Online, applies qualification rules, determines lead priority, assigns the appropriate sales owner, generates Microsoft Word qualification reports, sends the required email communications, and routes exceptional cases for human review.

The solution minimizes manual effort, improves consistency in lead qualification, reduces response time, and ensures every lead is processed according to NovaWorks Technologies' business policies.

---

# Business Problem

Sales teams often receive a large number of enquiries through email. Manually reviewing every enquiry introduces several challenges:

- Delayed response times
- Inconsistent lead qualification
- Duplicate lead creation
- Incorrect owner assignment
- Missed sales opportunities
- Manual report generation
- Human errors during qualification

The Autonomous Sales Lead Qualification Agent addresses these challenges by automating the complete lead qualification workflow while allowing human intervention only when required.

---

# Solution Objectives

The solution is designed to:

- Automatically monitor incoming sales enquiry emails
- Extract structured lead information
- Validate extracted information
- Detect duplicate opportunities
- Calculate lead qualification scores
- Classify leads
- Assign sales owners
- Generate qualification reports
- Send customer and internal communications
- Escalate uncertain cases for manual review

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Microsoft Copilot Studio | Autonomous AI Agent |
| Microsoft 365 Outlook | Email trigger and communication |
| Excel Online (Business) | Operational reference data |
| Microsoft Word Online | Qualification report generation |
| Microsoft OneDrive | Document storage |
| Microsoft Power Platform Connectors | Business integrations |
| Generative Orchestration | Autonomous tool selection and execution |

---

# Knowledge Sources

The agent uses three knowledge sources.

| Knowledge Source | Purpose |
|-----------------|---------|
| **Sales Lead Qualification Policy** | Qualification policies, duplicate handling, escalation rules, processing guidance |
| **Sales Communication Guidelines** | Email templates, communication standards, customer interactions |
| **Lead Qualification Report Structure** | Required report sections and formatting |

Knowledge sources are used only for policy and documentation guidance.

Operational business decisions always come from Excel reference tables.

---

# Connector Tools

## Outlook

- Get emails (V3)
- Send External Acknowledgement
- Send Missing Information Request
- Send Internal Owner Notification
- Send Sales Operations Review Alert

---

## Excel Online

- Read Leads Register
- Read Qualification Rules
- Read Product Catalog
- Read Territory Owners
- Read Sales Owners
- Read Action Matrix
- Add Lead to Register
- Update Lead Register

---

## Microsoft Word

- Generate Lead Qualification Report

---

# Solution Architecture

```
Incoming Email
        │
        ▼
Get Emails (V3)
        │
        ▼
Extract Lead Information
        │
        ▼
Normalize Data
        │
        ▼
Read Excel Reference Tables
        │
        ▼
Duplicate Detection
        │
        ▼
Lead Qualification
        │
        ▼
Lead Classification
        │
        ▼
Sales Owner Assignment
        │
        ▼
Update Lead Register
        │
        ▼
Generate Word Report
        │
        ▼
Send Outlook Communications
        │
        ▼
Human Review (if required)
```

---

# Operational Workflow

The autonomous agent performs the following workflow:

1. Monitor Outlook for new sales enquiry emails.
2. Validate trigger conditions.
3. Extract structured lead information.
4. Normalize extracted values.
5. Read operational reference data.
6. Detect duplicate opportunities.
7. Calculate qualification score.
8. Apply business rules.
9. Determine lead classification.
10. Assign sales owner.
11. Create or update Lead Register.
12. Generate Lead Qualification Report.
13. Send customer and internal communications.
14. Escalate uncertain cases for Human Review.
15. Complete autonomous processing.

---

# Lead Classifications

The agent supports the following classifications:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

---

# Human Review Conditions

The agent routes leads for manual review when:

- Qualification confidence is low.
- Territory cannot be determined.
- Product cannot be validated.
- Business rules cannot be applied.
- Information conflicts exist.
- Tool execution fails.
- Action Matrix requires manual approval.

---

# Testing Summary

The solution was evaluated using **23 test cases** covering all mandatory scenarios.

Test categories include:

- Hot Leads
- Qualified Leads
- Nurture Leads
- Low Priority Leads
- Human Review
- Duplicate Detection
- Additional Information Required
- Non-Sales Requests
- Academic Requests
- Competitor Risk
- Unknown Product
- Unmapped Territory
- Invalid Data Correction
- Excel Failure
- Word Failure
- Outlook Failure
- Repeated Trigger (Idempotency)
- Failed Test with Successful Retest

All mandatory scenarios specified in the project requirements were executed.

---

# Configuration Status

| Component | Status |
|----------|--------|
| Autonomous Agent |  Completed |
| Generative Orchestration |  Enabled |
| Outlook Trigger |  Configured |
| Outlook Connectors |  Configured |
| Excel Connectors |  Configured |
| Word Connector |  Configured |
| Knowledge Sources |  Added |
| Agent Instructions |  Completed |
| Qualification Logic |  Implemented |
| Human Review Logic |  Implemented |
| Testing |  Completed |
| Publishing |  Completed |

---

# Completion Status

| Deliverable | Status |
|------------|--------|
| Agent Design |  Completed |
| Tool Configuration |  Completed |
| Knowledge Configuration |  Completed |
| Qualification Workflow |  Completed |
| Duplicate Detection |  Completed |
| Report Generation |  Completed |
| Email Automation |  Completed |
| Human Review Workflow |  Completed |
| Testing |  Completed |
| Documentation |  Completed |

---

# Project Deliverables

- Autonomous Copilot Studio Agent
- Configured Outlook Connectors
- Configured Excel Online Connectors
- Configured Microsoft Word Connector
- Knowledge Sources
- Agent Instructions
- Qualification Logic
- Test Cases
- Documentation

---

# Repository Contents

```
README.md
agent-url.md
solution-summary.md
agent-instructions-design.md
trigger-design.md
tool-design.md
qualification-logic.md
test-report.md
known-limitations.md
ai-usage-declaration.md
Autonomous_Sales_Lead_Qualification_Agent_Test_Cases.csv
```

---

# Future Improvements

Potential enhancements include:

- Integration with Dynamics 365 CRM
- Support for multilingual email processing
- AI-powered sentiment analysis
- Lead enrichment using external business data
- Power BI dashboards for qualification analytics
- Automatic follow-up reminders
- Teams notifications for sales owners
- Adaptive qualification rules using AI models

---

# Author

**Project:** Autonomous Sales Lead Qualification Agent

**Platform:** Microsoft Copilot Studio

**Organization:** NovaWorks Technologies

**Status:** Completed