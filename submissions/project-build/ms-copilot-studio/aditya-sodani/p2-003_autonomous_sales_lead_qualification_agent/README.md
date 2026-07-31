# P2-003 – Autonomous Sales Lead Qualification Agent

## Project Summary

This project implements an autonomous AI-powered Sales Lead Qualification Agent using Microsoft Copilot Studio. The agent automatically processes inbound sales enquiries received through Outlook, extracts lead information, evaluates qualification criteria, determines lead priority, generates qualification reports, updates the lead register, and notifies internal stakeholders.

The solution minimizes manual effort, standardizes lead qualification, and improves sales response time through autonomous orchestration.

---

## Project Information

| Item | Value |
|------|-------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Trigger | Office 365 Outlook |
| AI Model | Microsoft Copilot Studio Generative Orchestration |
| Storage | Microsoft Excel |
| Report Generation | Microsoft Word Online |
| Notifications | Outlook |

---

## Submission Details

| Item | Value |
|------|-------|
| **Project ID** | P2-003 |
| **Participant Name** | Aditya Sodani |
| **GitHub Username** | adityasodani03 |
| **Agent Name** | Autonomous Sales Lead Agent |
| **Published Agent URL** | *https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/70dec960-a38c-f111-8077-000d3af21e08/overview* |
| **Authentication Requirement** | Microsoft 365 Authentication |
| **Trigger Configured** | Outlook – When a new email arrives (V3) |
| **Excel Tools Configured** | 8 |
| **Word Tool Configured** | 1 |
| **Outlook Tools Configured** | 3 |
| **Test Totals** | 20 Executed (20 Passed, 0 Failed) |
| **Known Limitations** | Documented in `known-limitations.md` |
| **AI Tools Used** | Microsoft Copilot Studio, ChatGPT (OpenAI) |
| **Submission Date** | *(31/07/2026)* |

---

## Implemented Components

### Trigger

- Outlook Email Trigger
- Subject Filter
- Inbox Monitoring

### Knowledge Sources

- Lead Register
- Qualification Rules
- Territory Owners
- Product Catalog
- Sales Owners
- Action Matrix

### Tools

- Read Lead Register
- Read Qualification Rules
- Read Territory Owners
- Read Product Catalog
- Read Sales Owners
- Read Action Matrix
- Create Lead Record
- Update Existing Lead
- Generate Qualification Report
- Send External Acknowledgement
- Request Missing Information
- Notify Sales Operations

---

## Agent Workflow

1. Receive email
2. Validate subject
3. Extract lead details
4. Check duplicate leads
5. Read qualification rules
6. Calculate qualification score
7. Determine lead classification
8. Update Excel records
9. Generate qualification report
10. Send customer acknowledgement
11. Notify Sales Operations
12. Complete processing

---

## Configuration Status

| Component | Status |
|-----------|--------|
| Agent | Completed |
| Trigger | Configured |
| Excel Connections | Configured |
| Word Connection | Configured |
| Outlook Connection | Configured |
| Agent Instructions | Completed |
| Generative Orchestration | Enabled |

---

## Completion Status

| Activity | Status |
|----------|--------|
| Agent Design | Completed |
| Tool Configuration | Completed |
| Trigger Configuration | Completed |
| Agent Instructions | Completed |
| Testing | Pending |
| Documentation | In Progress |

---

## Repository Contents

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

---
