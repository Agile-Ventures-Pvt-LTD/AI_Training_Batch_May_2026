# P2-003 Autonomous Sales Lead Qualification Agent

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |
| Environment | Microsoft Copilot Studio |
| AI Usage | Permitted (Validated by Participant) |
| Project Type | Individual Project Build |

---

# Project Overview

The Autonomous Sales Lead Qualification Agent is an event-driven Microsoft Copilot Studio solution designed to automatically process incoming sales enquiries received through Microsoft Outlook.

The agent evaluates each incoming email, extracts structured business information, checks for duplicate opportunities, determines lead quality, updates operational records, generates qualification documentation, and sends the appropriate communication while following NovaWorks business policies.

The solution was implemented entirely within Microsoft Copilot Studio using Generative Orchestration and Microsoft 365 connector tools.

---

# Business Problem

Sales Operations currently perform several repetitive manual activities including:

- Reading every inbound sales email
- Extracting customer information
- Checking duplicate opportunities
- Reviewing qualification criteria
- Updating Excel lead registers
- Creating qualification reports
- Sending acknowledgement emails

These activities increase response time and reduce consistency.

This solution automates the initial qualification process while ensuring uncertain or exceptional cases are routed for human review.

---

# Solution Objectives

The implemented solution performs the following high-level activities:

- Monitor Outlook for new project lead emails
- Validate email scope
- Extract structured lead information
- Read qualification reference tables
- Detect duplicate opportunities
- Calculate qualification score
- Classify each lead
- Assign sales owner
- Update operational Excel workbook
- Generate Microsoft Word qualification reports
- Send Outlook communications
- Route exception cases for human review

---

# Solution Architecture

```
Outlook Trigger
        │
        ▼
Validate Subject
        │
        ▼
Extract Lead Information
        │
        ▼
Duplicate Detection
        │
        ▼
Read Excel Reference Tables
        │
        ▼
Qualification Scoring
        │
        ▼
Classification
        │
 ┌──────┴────────┐
 │               │
 ▼               ▼
Excel Update   Human Review
 │
 ▼
Word Report
 │
 ▼
Outlook Communication
```

---

# Microsoft 365 Connector Tools

The solution uses the following connector actions.

| Connector | Purpose |
|-----------|----------|
| Office 365 Outlook | Event trigger and email communication |
| Excel Online (Business) | Read and update operational data |
| Word Online (Business) | Generate qualification reports |

---

# Major Functionalities

- Event-driven processing
- Lead extraction
- Data normalization
- Duplicate detection
- Qualification scoring
- Classification
- Sales owner assignment
- Excel updates
- Word report generation
- Outlook communication
- Human review routing
- Exception handling

---

# Qualification Outcomes

The solution supports the following business classifications.

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

---

# Required Excel Tables

The operational workbook contains:

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

---

# Required Outputs

The solution may generate:

### Excel

Lead Register updates

### Microsoft Word

Qualification Report

### Outlook

- Lead acknowledgement
- Missing information request
- Internal notification
- Human review alert

---

# Configuration Status

| Component | Status |
|-----------|---------|
| Generative Orchestration | Configured |
| Outlook Trigger | Configured |
| Excel Connectors | Configured |
| Word Connector | Configured |
| Outlook Connector | Configured |
| Agent Instructions | Configured |
| Knowledge Sources | Configured |

---

# Repository Structure

```
submissions/
└── project-build/
    └── ms-copilot-studio/
        └── mohammad-anas/
            └── p2-003_autonomous_sales_lead_qualification_agent/
                ├── README.md
                ├── agent-url.md
                ├── solution-summary.md
                ├── agent-instructions-design.md
                ├── trigger-design.md
                ├── tool-design.md
                ├── qualification-logic.md
                ├── test-report.md
                ├── known-limitations.md
                ├── ai-usage-declaration.md
                └── screenshots/
```

---

# Security Considerations

The solution follows the project policy by:

- Using synthetic training data only.
- Avoiding pricing commitments.
- Avoiding contractual commitments.
- Preventing duplicate processing.
- Restricting qualification decisions during human review.
- Preventing disclosure of internal operational information.

---

# Known Constraints

Current implementation depends on:

- Microsoft 365 connectors
- Outlook availability
- Excel Online availability
- Word Online availability
- Microsoft tenant permissions
- Connector authentication

---

# Completion Status

| Feature | Status |
|----------|---------|
| Event Trigger | Implemented |
| Lead Extraction | Implemented |
| Duplicate Detection | Implemented |
| Qualification Logic | Implemented |
| Excel Operations | Implemented |
| Word Generation | Implemented |
| Outlook Communication | Implemented |
| Human Review Routing | Implemented |
| Documentation | Completed |

---

# References

- Microsoft Copilot Studio
- Microsoft 365 Outlook Connector
- Excel Online (Business)
- Word Online (Business)
- P2-003 Product Requirements Document

---

# Author

**Mohammad Anas**

Microsoft Copilot Studio Project Build

P2-003 Autonomous Sales Lead Qualification Agent