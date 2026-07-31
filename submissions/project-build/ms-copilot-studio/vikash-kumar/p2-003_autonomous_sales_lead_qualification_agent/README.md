# NovaWorks Autonomous Sales Lead Qualification Agent

**Project ID:** P2-003 – Autonomous Sales Lead Qualification Agent

**Platform:** Microsoft Copilot Studio

**Agent Name:** NovaWorks Autonomous Sales Lead

**Status:** ✅ Completed

**Publishing Status:** Published

**Project Repository Folder**

```text
submissions/project-build/ms-copilot-studio/<firstname-lastname>/p2-003_autonomous_sales_lead_qualification_agent
```

---

## Agent URL

https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/d3af7856-a48c-f111-8077-000d3af21e08/overview

---

# Project Overview

The **NovaWorks Autonomous Sales Lead Qualification Agent** is an AI-powered autonomous sales intake solution built using **Microsoft Copilot Studio**.

The agent automatically processes incoming sales inquiry emails received through Microsoft Outlook, validates whether the inquiry is a genuine sales opportunity, extracts business information, evaluates the lead against operational qualification rules stored in Excel Online, updates the operational lead register, generates a qualification report, and sends an acknowledgement email to the customer.

The solution uses **Generative AI Orchestration** together with **Microsoft 365 connector actions** to autonomously decide which tools to invoke based on the incoming request. The implementation follows Microsoft Copilot Studio best practices for AI-driven tool orchestration and connector-based automation. :contentReference[oaicite:0]{index=0}

---

# Business Problem

Organizations receive large numbers of inbound sales enquiries through shared mailboxes.

Sales teams typically perform the following manual tasks:

- Read every incoming email
- Determine whether the email is a sales opportunity
- Extract customer information
- Identify duplicate enquiries
- Determine lead quality
- Assign the correct regional sales owner
- Update CRM or operational tracking spreadsheets
- Send acknowledgement emails
- Generate qualification reports
- Escalate uncertain opportunities

These repetitive activities consume valuable sales time and introduce inconsistencies.

This project automates the entire qualification workflow while ensuring human review is requested whenever confidence is insufficient.

---

# Objectives

The solution was designed to:

- Automatically process inbound sales enquiries
- Filter emails using a predefined trigger
- Extract structured business information
- Normalize extracted values
- Detect duplicate opportunities
- Apply qualification rules
- Classify lead priority
- Assign the appropriate sales owner
- Maintain an operational lead register
- Generate qualification documentation
- Send acknowledgement emails
- Escalate uncertain cases for human review

---

# Solution Architecture

```
Incoming Outlook Email
        │
        ▼
Outlook Trigger
        │
        ▼
Copilot Studio Agent
        │
        ▼
AI Reasoning & Orchestration
        │
 ┌──────┼──────────┐
 │      │          │
 ▼      ▼          ▼
Excel   Word    Outlook
Online  Online  Email
        │
        ▼
Lead Qualification
        │
        ▼
Operational Outputs
```

The agent autonomously selects connector actions based on the current processing stage instead of following a fixed workflow. This demonstrates AI orchestration, where the model reasons about when and how to invoke available tools. :contentReference[oaicite:1]{index=1}

---

# Key Features

## Automated Email Processing

- Outlook email trigger
- Subject validation
- Sales inquiry identification
- Commercial intent detection

---

## Lead Information Extraction

Automatically extracts:

### Contact Information

- Contact Name
- Email
- Job Title
- Decision Role

### Organization

- Company Name
- Country
- Territory
- Industry
- Company Size

### Opportunity Details

- Product Interest
- Budget
- Purchase Timeline
- Business Need
- Lead Source

---

## Data Normalization

Normalizes:

- Country names
- Product names
- Decision roles
- Company size
- Industry values

Missing values are retained as **Unknown** rather than replaced with default values.

---

## Duplicate Detection

Duplicate evaluation is performed using:

1. Message ID
2. Sender Email
3. Company Name
4. Product Interest

If a duplicate exists:

- Existing lead is updated
- No duplicate report is generated
- No duplicate acknowledgement email is sent

---

## Qualification

The agent evaluates:

- Product fit
- Completeness
- Business need
- Budget
- Timeline
- Confidence
- Operational rules

Possible outcomes:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

---

## Sales Owner Assignment

The assigned sales owner is determined using operational reference data stored in Excel.

---

## Report Generation

The solution generates a Microsoft Word qualification report containing:

- Lead information
- Qualification outcome
- Assigned owner
- Summary
- Processing timestamp

---

## Customer Communication

Successful enquiries automatically receive an acknowledgement email containing:

- Thank-you message
- Confirmation of receipt
- Next steps
- Assigned regional team notification

---

## Human Review

The agent requests manual review whenever:

- Product cannot be identified
- Territory is unknown
- Operational data cannot be accessed
- Tool execution fails
- Qualification confidence is low
- Conflicting information exists

---

# AI Orchestration

This solution uses **Generative AI Orchestration** in Microsoft Copilot Studio.

Rather than executing a predefined workflow, the language model determines:

- Which tool should execute
- When each connector should run
- Whether another tool is required
- Whether human review is necessary

The agent instructions define business policies while Copilot Studio determines the optimal connector execution sequence. :contentReference[oaicite:2]{index=2}

---

# 🖼️ Screenshot Index

The complete set of implementation screenshots is available in the `screenshots` directory.

| Screenshot | Description |
|------------|-------------|
| 01-agent-overview.png | Copilot Studio agent overview |
| 02-generative-orchestration.png | Generative AI orchestration configuration |
| 03-outlook-trigger.png | Outlook trigger configuration |
| 04-tools-overview.png | Configured Microsoft 365 tools |
| 05-excel-configuration.png | Excel Online configuration |
| 06-word-configuration.png | Word Online configuration |
| 07-outlook-configuration.png | Outlook email configuration |
| 08-successful-run.png | Successful execution |
| 09-duplicate-prevention.png | Duplicate prevention validation |
| 10-generated-word-report.png | Generated qualification report |
| 11-published-agent.png | Published agent |

---
# 📸 Implementation Screenshots

The following screenshots provide visual evidence of the implementation and validation of the **NovaWorks Autonomous Sales Lead Qualification Agent**.

---

## 🤖 1. Agent Overview

The agent overview displays the configured Microsoft Copilot Studio agent, including the agent details, configured tools, trigger, and publishing status.

![Agent Overview](screenshots/01-agent-overview.png)

---

## 🧠 2. Generative AI Orchestration

The following screenshot shows that the agent uses **Generative AI Orchestration**, allowing the Large Language Model (LLM) to dynamically determine when and how connector tools should be invoked.

![Generative AI Orchestration](screenshots/02-generative-orchestration.png)

---

## 📥 3. Outlook Trigger Configuration

The Outlook trigger is configured using **When a new email arrives (V3)**. The trigger activates only when the subject contains the required keyword.

Subject Filter:

```text
[P2-003 LEAD]
```

![Outlook Trigger](screenshots/03-outlook-trigger.png)

---

## 🛠️ 4. Configured Connector Tools

The following screenshot shows all Microsoft 365 connector tools configured within the agent.

![Tools Overview](screenshots/04-tools-overview.png)

---

## 📊 5. Excel Online Configuration

The Excel Online (Business) connector is configured to retrieve operational reference data, including qualification rules, territory mappings, sales owner mappings, and lead records.

![Excel Configuration](screenshots/05-excel-configuration.png)

---

## 📄 6. Word Online Configuration

The Word Online (Business) connector generates the Lead Qualification Report after successful lead processing.

![Word Configuration](screenshots/06-word-configuration.png)

---

## 📧 7. Outlook Email Configuration

The Outlook connector automatically sends acknowledgement emails after successful qualification.

![Outlook Configuration](screenshots/07-outlook-configuration.png)

---

## 🚀 8. Successful Agent Execution

The following screenshot shows a successful execution within Microsoft Copilot Studio after processing an incoming sales enquiry.

![Successful Run](screenshots/08-successful-run.png)

---

## 🔁 9. Duplicate Prevention

Duplicate detection prevents multiple records from being created for the same opportunity. Existing lead records are updated instead of creating new entries.

![Duplicate Prevention](screenshots/09-duplicate-prevention.png)

---

## 📄 10. Generated Lead Qualification Report

The generated Microsoft Word report summarizes the extracted lead information, qualification outcome, and recommended next steps.

![Generated Word Report](screenshots/10-generated-word-report.png)

---

## 🌐 11. Published Agent

The final screenshot confirms that the agent was successfully published and is ready for autonomous execution.

![Published Agent](screenshots/11-published-agent.png)

---

## 12. Evaluation

This is the screenshot of evaluation of the agent.

![Evaluation](screenshots/12-evaluation.png)

---
# Connector Tools

The implementation uses the following connector actions.

| Tool | Purpose |
|--------|----------|
| Read Operational Excel Tables | Read qualification rules, sales owners, territory mappings and operational reference data |
| Create New Lead Record | Insert newly qualified lead into operational register |
| Update Existing Lead Record | Update duplicate or existing lead |
| Generate Lead Qualification Report | Produce Word qualification document |
| Send Qualification Result Email | Send acknowledgement email |

---

# Trigger

**Type**

Microsoft Outlook – When a new email arrives (V3)

**Trigger Condition**

Subject contains:

```
[P2-003 LEAD]
```

Only matching emails are processed.

All other emails are ignored.

---

# Knowledge Sources

Operational workbook:

**P2-003_Sales_Lead_Operational_Data.xlsx**

Operational tables include:

- Leads Register
- Qualification Rules
- Territory Owners
- Product Catalog
- Sales Owners
- Action Matrix

---

# Technologies Used

- Microsoft Copilot Studio
- Microsoft Outlook Connector
- Excel Online (Business)
- Word Online (Business)
- Microsoft 365
- Generative AI Orchestration

---

# Testing

The solution has been validated using:

- Copilot Studio Test Panel
- Real Outlook Trigger
- Connector execution monitoring
- End-to-end orchestration
- Excel updates
- Word report generation
- Email acknowledgement
- Duplicate detection scenarios

---

# Deliverables

The repository includes:

- README.md
- agent-url.md
- solution-summary.md
- agent-instructions-design.md
- trigger-design.md
- tool-design.md
- qualification-logic.md
- test-report.md
- known-limitations.md
- ai-usage-declaration.md

---

# Configuration Status

| Component | Status |
|-----------|--------|
| Agent Created | ✅ |
| Agent Published | ✅ |
| Generative Orchestration Enabled | ✅ |
| Outlook Trigger Configured | ✅ |
| Excel Connector Configured | ✅ |
| Word Connector Configured | ✅ |
| Outlook Connector Configured | ✅ |
| AI Instructions Implemented | ✅ |
| Qualification Logic Implemented | ✅ |
| Duplicate Detection Implemented | ✅ |
| Human Review Logic Implemented | ✅ |
| End-to-End Testing Completed | ✅ |

---

# Completion Status

**Project:** ✅ Completed

**Agent Status:** Published

**Testing Status:** Successfully validated using both Copilot Studio test sessions and real Outlook-triggered email processing.

---
**Author:** Vikash Kumar
**Project:** P2-003 – Autonomous Sales Lead Qualification Agent
**Platform:** Microsoft Copilot Studio