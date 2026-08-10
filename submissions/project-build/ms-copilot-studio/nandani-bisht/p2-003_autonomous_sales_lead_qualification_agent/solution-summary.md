# Solution Summary

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |
| Version | 1.0 |

---

# Business Problem

NovaWorks Technologies receives numerous sales inquiries through a monitored Microsoft 365 mailbox. Manually reviewing each email, extracting lead information, checking for duplicate opportunities, assigning sales representatives, updating operational records, creating qualification reports, and responding to customers is time-consuming and inconsistent.

The objective of this project is to automate the complete first-stage sales qualification process using Microsoft Copilot Studio while ensuring consistent business decisions, reducing manual effort, and maintaining auditability.

---

# Proposed Solution

An autonomous Microsoft Copilot Studio agent was developed to process qualifying Outlook emails automatically.

The solution uses Microsoft 365 connector tools together with Generative Orchestration to perform lead qualification without requiring manual intervention for standard business scenarios.

The agent:

- Monitors Outlook for incoming sales inquiries.
- Extracts structured lead information from unstructured email content.
- Reads operational reference data from Excel Online (Business).
- Detects duplicate opportunities.
- Calculates qualification scores.
- Assigns lead classifications.
- Assigns the appropriate sales owner.
- Creates qualification reports in Microsoft Word when required.
- Sends internal and external Outlook communications.
- Records all completed actions in the operational Excel workbook.

---

# Solution Architecture

```
Incoming Outlook Email
          │
          ▼
Outlook Event Trigger
          │
          ▼
Lead Information Extraction
          │
          ▼
Duplicate Detection
          │
          ▼
Excel Reference Lookup
          │
          ▼
Qualification Score Calculation
          │
          ▼
Lead Classification
          │
          ▼
Sales Owner Assignment
          │
          ▼
Excel Record Creation / Update
          │
          ▼
Word Qualification Report
          │
          ▼
Outlook Notifications
```

---

# Microsoft Components Used

## Microsoft Copilot Studio

- Autonomous Agent
- Generative Orchestration
- Event Trigger
- Knowledge Sources

## Office 365 Outlook

- When a New Email Arrives (V3)
- Lead Acknowledgement
- Missing Information Request
- Sales Owner Notification
- Sales Operations Notification

## Excel Online (Business)

- Read operational reference tables
- Create lead records
- Update duplicate records

## Word Online (Business)

- Generate qualification reports

## OneDrive for Business

- Operational workbook storage
- Qualification report storage

---

# Business Logic

The agent performs the following business operations:

1. Validate trigger conditions.
2. Extract lead information.
3. Verify mandatory information.
4. Detect duplicate opportunities.
5. Read qualification rules.
6. Calculate qualification score.
7. Apply business overrides.
8. Determine lead classification.
9. Assign sales owner.
10. Update operational workbook.
11. Generate qualification report when required.
12. Send appropriate Outlook communication.

---

# Business Outcomes

The implemented solution provides:

- Faster lead qualification.
- Reduced manual effort.
- Consistent scoring.
- Automated owner assignment.
- Standardized communications.
- Duplicate prevention.
- Improved auditability.
- Better operational efficiency.

---

# Testing Summary

The solution was validated using the supplied synthetic lead scenarios.

Testing included:

- Hot Leads
- Qualified Leads
- Nurture Leads
- Low Priority Leads
- Duplicate Detection
- Missing Information
- Human Review
- Competitor Risk
- Support Requests
- Unknown Product
- Outlook Trigger Validation
- Excel Updates
- Word Report Generation
- Outlook Notifications

---

# Final Outcome

The autonomous agent successfully performs end-to-end sales lead qualification within Microsoft Copilot Studio using Outlook, Excel Online (Business), and Word Online (Business) connectors.

The solution satisfies the functional objectives of the P2-003 project and demonstrates autonomous event-driven business process automation using Microsoft technologies.