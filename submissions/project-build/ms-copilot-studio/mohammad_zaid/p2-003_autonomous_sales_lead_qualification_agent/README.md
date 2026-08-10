
# NovaWorks Sales Lead Qualification Agent

## Project Overview

The **NovaWorks Sales Lead Qualification Agent** is an autonomous AI solution developed using **Microsoft Copilot Studio** to automate the processing, qualification, and management of incoming sales leads. The agent monitors Outlook for new lead inquiries, extracts relevant business information, validates lead completeness, checks for duplicates, evaluates qualification using predefined business rules, updates operational records, generates a professional Lead Qualification Report, and sends appropriate business communications.

The solution was developed as part of **Project P2-003** and follows the functional, operational, and governance requirements specified in the project documentation.

---

# Business Objective

The primary objective of this solution is to reduce manual effort in processing inbound sales leads while ensuring:

- Consistent lead qualification
- Standardized business decisions
- Automated operational record management
- Professional report generation
- Controlled customer communication
- Human escalation for uncertain cases

---

# Technology Stack

| Component           | Technology                                       |
| ------------------- | ------------------------------------------------ |
| AI Platform         | Microsoft Copilot Studio                         |
| AI Model            | GPT-4.1                                          |
| Trigger             | Office 365 Outlook (When a new email arrives V3) |
| Data Source         | Excel Online (Business)                          |
| Report Generation   | Word Online (Business)                           |
| Email Communication | Office 365 Outlook                               |
| Storage             | OneDrive for Business                            |

---

# Solution Architecture

The agent performs the following workflow:

1. Monitor Outlook for new sales lead emails.
2. Trigger automatically when the configured subject filter is matched.
3. Read operational reference data from the Excel workbook.
4. Extract lead information from the incoming email.
5. Validate mandatory business information.
6. Detect duplicate leads.
7. Apply qualification rules.
8. Determine lead classification.
9. Assign the appropriate sales owner.
10. Generate the Lead Qualification Report.
11. Create or update the operational lead register.
12. Send the appropriate business communication.
13. Escalate exceptional cases for manual review when required.

---

# Implemented Features

- Autonomous Outlook event trigger
- AI-driven lead information extraction
- Operational data lookup
- Duplicate lead detection
- Qualification scoring
- Lead classification
- Sales owner assignment
- Excel operational record management
- Word report generation
- Automated Outlook communication
- Human escalation support

---

# Configured Tools

The following tools are configured within the agent:

| Tool                               | Purpose                                                                           |
| ---------------------------------- | --------------------------------------------------------------------------------- |
| Read Lead Reference Data           | Reads operational Excel reference tables                                          |
| Create Lead Record                 | Creates a new lead record in the operational workbook                             |
| Update Lead Record                 | Updates an existing lead record                                                   |
| Generate Lead Qualification Report | Generates the Lead Qualification Report in Microsoft Word                         |
| Send Email                         | Sends customer acknowledgements, information requests, and internal notifications |

---

# Trigger Configuration

Platform:

- Office 365 Outlook

Trigger:

- When a new email arrives (V3)

Configuration:

- Inbox monitored
- Attachment support enabled
- Subject filter configured for project testing
- Automatic execution enabled

---

# Configuration Status

| Component                | Status        |
| ------------------------ | ------------- |
| Agent Created            | ✅ Completed  |
| Instructions Configured  | ✅ Completed  |
| Outlook Trigger          | ✅ Configured |
| Excel Tools              | ✅ Configured |
| Word Tool                | ✅ Configured |
| Outlook Tool             | ✅ Configured |
| Generative Orchestration | ✅ Enabled    |
| Test Execution           | ✅ Completed  |
| Documentation            | ✅ Completed  |

---

# Project Files

The implementation uses the following project resources:

- P2-003_Sales_Lead_Operational_Data.xlsx
- P2-003_Test_Cases_and_Execution_Log.xlsx
- NovaWorks_Sales_Lead_Qualification_and_Autonomy_Policy.docx
- Lead_Qualification_Report_Required_Structure.docx
- Sample_Incoming_Lead_Emails.txt
- Autonomous_Email_Content_Requirements.txt

---

# Repository Contents

This repository contains:

- Agent documentation
- Design documentation
- Trigger documentation
- Tool documentation
- Qualification logic
- Testing evidence
- Known limitations
- AI usage declaration

---

# Completion Status

| Deliverable           | Status       |
| --------------------- | ------------ |
| Copilot Studio Agent  | ✅ Completed |
| Tool Configuration    | ✅ Completed |
| Trigger Configuration | ✅ Completed |
| Documentation         | ✅ Completed |
| Testing               | ✅ Completed |
| Final Submission      | ✅ Ready     |

---

# Notes

- All business data used within this project is synthetic.
- No production customer information, credentials, API keys, or confidential organizational data are included.
- The implementation follows the governance and operational requirements defined in Project P2-003.
