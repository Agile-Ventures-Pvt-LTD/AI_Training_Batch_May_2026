# Tool Design

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |

---

# Overview

The Autonomous Sales Lead Qualification Agent uses Microsoft Copilot Studio connector tools to retrieve reference data, maintain operational records, generate qualification reports, and send automated communications.

The solution consists of Excel Online (Business), Word Online (Business), Outlook, and Knowledge tools working together through Generative Orchestration.

---

# Tool Summary

| Tool Category | Number of Tools |
|--------------|-----------------|
| Excel Online (Business) | 8 |
| Word Online (Business) | 1 |
| Outlook | 4 |
| Knowledge Sources | 3 |
| **Total** | **16** |

---

# Excel Online (Business) Tools

## 1. Read Leads Register

**Purpose**

Reads the operational Leads Register to identify existing opportunities and support duplicate detection.

**Input**

- Workbook
- Leads Register Table

**Output**

- Existing lead records

**Action Boundary**

Read-only operation.

---

## 2. Read Qualification Rules

**Purpose**

Retrieves business qualification rules used during lead scoring.

**Input**

- Qualification Rules Table

**Output**

- Qualification criteria
- Scoring values

**Action Boundary**

Read-only operation.

---

## 3. Read Territory Owners

**Purpose**

Maps territories to the appropriate sales owner.

**Input**

- Territory name

**Output**

- Assigned territory owner

**Action Boundary**

Read-only operation.

---

## 4. Read Product Catalog

**Purpose**

Validates the requested product against the approved product catalogue.

**Input**

- Product name

**Output**

- Product validation details

**Action Boundary**

Read-only operation.

---

## 5. Read Sales Owners

**Purpose**

Retrieves sales owner details for notifications.

**Input**

- Sales owner identifier

**Output**

- Sales owner information

**Action Boundary**

Read-only operation.

---

## 6. Create Lead Record

**Purpose**

Creates a new lead entry after successful qualification.

**Input**

- Lead details
- Qualification score
- Classification
- Assigned owner

**Output**

- New row added to the Leads Register

**Action Boundary**

Creates new records only.

---

## 7. Update Lead Record

**Purpose**

Updates an existing lead when a duplicate opportunity is detected or additional information is received.

**Input**

- Lead ID
- Updated lead information

**Output**

- Existing record updated

**Action Boundary**

Updates existing records only.

---

# Word Online (Business)

## 8. Create Qualification Report

**Purpose**

Generates a Microsoft Word qualification report for applicable sales opportunities.

**Input**

- Lead details
- Qualification results
- Assigned owner
- Classification

**Output**

- Qualification Report (.docx)

**Action Boundary**

Creates a new document without modifying existing reports.

---

# Outlook Tools

## 9. Send Lead Acknowledgement

**Purpose**

Sends an acknowledgement email to qualified leads confirming receipt of the inquiry.

**Input**

- Customer email
- Customer name

**Output**

- Acknowledgement email

**Action Boundary**

External communication only.

---

## 10. Send Missing Information Request

**Purpose**

Requests additional information when mandatory business details are unavailable.

**Input**

- Customer email
- Missing information list

**Output**

- Information request email

**Action Boundary**

External communication only.

---

## 11. Notify Sales Owner

**Purpose**

Notifies the assigned sales representative regarding a qualified opportunity.

**Input**

- Sales owner email
- Lead summary

**Output**

- Internal notification email

**Action Boundary**

Internal communication only.

---

## 12. Notify Sales Operations

**Purpose**

Notifies the Sales Operations team regarding lead processing outcomes requiring operational awareness.

**Input**

- Lead summary
- Processing status

**Output**

- Internal operational notification

**Action Boundary**

Internal communication only.

---

# Knowledge Sources

## 13. NovaWorks Policy

**Purpose**

Provides company business policies and qualification guidance used during autonomous decision making.

**Usage**

Reference only.

---

## 14. Qualification Report Structure

**Purpose**

Provides the standard structure and formatting for Microsoft Word qualification reports.

**Usage**

Reference only.

---

# Tool Execution Sequence

```
Outlook Trigger
        │
        ▼
Read Leads Register
        │
        ▼
Read Qualification Rules
        │
        ▼
Read Territory Owners
        │
        ▼
Read Product Catalog
        │
        ▼
Read Sales Owners
        │
        ▼
Create / Update Lead Record
        │
        ▼
Create Qualification Report
        │
        ▼
Send Outlook Notifications
```

---

# Design Principles

The tools were designed according to the following principles:

- Single responsibility per tool.
- Read and write operations are separated.
- Reference data remains read-only.
- External communications are isolated from internal notifications.
- Operational records remain auditable.
- Connector actions are executed only when required.

---

# Limitations

- All tools require authenticated Microsoft 365 connections.
- Excel operations depend on workbook availability.
- Word generation depends on template accessibility.
- Outlook actions require valid mailbox permissions.
- Knowledge sources are read-only and do not modify business data.

---

# Summary

The tool architecture separates data retrieval, record management, document generation, and communication into dedicated connector actions. This modular design improves maintainability, auditability, and reliable execution while supporting autonomous lead qualification within Microsoft Copilot Studio.