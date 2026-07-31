# P2-003 Autonomous Sales Lead Qualification Agent

## Project Overview
The **Autonomous Sales Lead Qualification Agent** is an end-to-end autonomous business process agent developed in **Microsoft Copilot Studio**. The agent is designed for **NovaWorks Technologies** to automate their first-line inbound sales lead triage, validation, duplicate checking, scoring, classification, ownership routing, reporting, and communication.

Rather than running as a standard chat-based copilot, this agent operates asynchronously using event-driven execution. It reacts automatically to external email events, applies deterministic business rules combined with generative reasoning, writes records to database systems, creates document brief files, and sends outbound emails without manual human intervention, reserving only complex or sensitive exception cases for human review.

---

## Participant Information
- **Participant Name:** Poonam Bhatt
- **Project ID:** P2-003
- **Platform:** Microsoft Copilot Studio
- **Submission Date:** July 31, 2026

---

## Published Agent Information
- **Published URL:** [NovaWorks Sales Lead Agent](https://copilotstudio.microsoft.com/environments/Default-db0089db-6b8d-4e3e-86bc-1c5b771972d2/copilots/p2-003-autonomous-sales-lead-qualification-agent)
- **Authentication Method:** OAuth 2.0 / Microsoft Entra ID (configured for secure cross-tenant API integrations)
- **Access Limitations:** Restricted to NovaWorks internal tenant users; external email triggers require validation of sender domains and matching synthetic project headers.
- **Verification Date:** July 31, 2026

---

## Key Features & Capabilities
1. **Event-Driven Trigger:** Listens autonomously for incoming emails in a monitored shared M365 Outlook mailbox using the `When a new email arrives (V3)` event.
2. **Safety & Scope Filtering:** Processes only emails containing the subject prefix `[P2-003 LEAD]` to prevent processing unrelated inbox traffic.
3. **Structured Lead Extraction:** Employs generative extraction to pull Contact, Organization, Opportunity, and Assessment metadata from unstructured email bodies.
4. **Data Normalization:** Translates extracted inputs to match official lists (e.g., matching country names, mapping company size to standard tiers, normalizing decision roles).
5. **Exact & Probable Duplicate Detection:** Inspects `LeadsRegisterTable` in Excel. Checks first for exact `Source_Message_ID` match, and secondarily matches recent company, sender email, and product interest to update existing rows instead of creating duplicates.
6. **Multi-Factor Lead Scoring:** Automatically calculates scores up to 100 points across 8 dimensions (Product Fit, Budget, Timeline, Decision Role, Company Size, Territory, Lead Source, and Completeness).
7. **Rule-Based Classification & Overrides:** Categorizes leads into `Hot`, `Qualified`, `Nurture`, `Low Priority`, `Additional Information Required`, `Human Review Required`, `Duplicate`, or `Not a Sales Lead`, applying overrides like the Startup/Micro budget exception and Low-Confidence routes.
8. **Word Report Generation:** Dynamically creates a structured, detailed Word report for `Hot` and `Qualified` leads using the `Create a Microsoft Word document` tool, saving it securely in SharePoint/OneDrive.
9. **Targeted Outbound Communication:** Sends tailored external acknowledgements, missing information requests, and internal owner alerts via Office 365 Outlook.
10. **Human-in-the-Loop Safeguards:** Routes exceptions (e.g., competitor risk, unmapped territory, unknown product) directly to Sales Operations without sending external emails.

---

## Solution Configuration Status
- **Outlook Event Trigger:** Configured and filtered.
- **Generative Orchestration:** Enabled (using Copilot Studio generative orchestration capabilities for dynamic tool execution and extraction).
- **Excel Online (Business) Connector Tools:** Configured with read, write, and update permissions for:
  - `LeadsRegisterTable`
  - `QualificationRulesTable`
  - `TerritoryOwnersTable`
  - `ProductCatalogTable`
  - `SalesOwnersTable`
  - `ActionMatrixTable`
- **Word Online (Business) Connector Tool:** Configured to dynamically generate briefings for Hot/Qualified leads.
- **Office 365 Outlook Connector Actions:** Configured for internal notifications and external communications.
- **Publish & Share Status:** Published, shared with Ankur Saxena, and verified active.

---

## Directory Structure & Submission Files
All required markdown submission files are located in this folder:

| File Name | Purpose |
|---|---|
| [README.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/README.md) | Project summary, URL, configuration, and completion status. |
| [agent-url.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/agent-url.md) | Published URL, authentication setup, access limitations, and verification details. |
| [solution-summary.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/solution-summary.md) | Business problem, architecture, process flow, and business outcomes. |
| [agent-instructions-design.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/agent-instructions-design.md) | Detailed system instructions, roles, objectives, and boundaries without secrets. |
| [trigger-design.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/trigger-design.md) | Outlook trigger design, subject filters, input/output schemas, and safety boundaries. |
| [tool-design.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/tool-design.md) | Definitions, descriptions, inputs, outputs, and boundaries for Outlook, Excel, and Word tools. |
| [qualification-logic.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/qualification-logic.md) | Scoring calculations, normalization rules, duplicate prevention, and override logic. |
| [test-report.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/test-report.md) | Execution log, score verification, duplicate prevention evidence, and defect correction test reports. |
| [known-limitations.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/known-limitations.md) | Connector limits, tenant boundaries, and functional edge cases. |
| [ai-usage-declaration.md](file:///C:/Users/Poonam%20Bhatt/Desktop/p2-003_autonomous_sales_lead_qualification_agent/ai-usage-declaration.md) | AI tools used during development, validation procedures, and corrections. |

A companion `screenshots` folder is configured with images demonstrating the published agent, trigger filters, Excel tables, and successful execution runs.
