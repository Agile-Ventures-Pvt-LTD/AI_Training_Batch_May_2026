# Tool Implementation

## Overview

The Sleepsia Quality & Customer Experience Intelligence Control Tower integrates Microsoft 365 tools to manage investigation data, generate reports, and notify stakeholders. These tools are orchestrated by the **Quality Supervisor** during the investigation lifecycle.

---

# Excel Online Tools

## Purpose

Excel Online serves as the project's operational data store, maintaining investigation, complaint, and CAPA records.

## Configuration

| Item | Configuration |
|------|---------------|
| Platform | Excel Online (Business) |
| Authentication | Microsoft 365 Connection |
| Data Source | Excel Tables |
| Invoked By | Quality Supervisor |

## Excel Actions Used

| Tool | Purpose |
|------|---------|
| List Rows | Retrieve investigation, complaint, batch, CAPA, and owner records |
| Update a Row | Update investigation status, classification, and CAPA information |
| Add a Row | Create new investigation, CAPA, evidence, and audit records |

## Usage

- Retrieve investigation records
- Retrieve complaint history
- Retrieve product and batch details
- Store investigation outcomes
- Store CAPA plans
- Record reassessment history
- Maintain audit trail

---

# Word Online Tool

## Purpose

Automatically generates the final investigation report after the workflow is completed.

## Configuration

| Item | Configuration |
|------|---------------|
| Platform | Word Online (Business) |
| Invoked By | Quality Supervisor |

## Usage

The generated report includes:

- Investigation Summary
- Incident Details
- Specialist Findings
- Quality Classification
- Decision Rationale
- CAPA Recommendations
- Record Update Summary
- Investigation Status

---

# Outlook Tool

## Purpose

Automatically notifies stakeholders after investigation completion.

## Configuration

| Item | Configuration |
|------|---------------|
| Platform | Outlook (Microsoft 365) |
| Invoked By | Quality Supervisor |

## Notification Recipients

- Quality Manager
- Product Team
- Customer Support
- Operations Team
- Assigned CAPA Owner

## Notification Content

- Investigation ID
- Final Classification
- CAPA Status
- Report Availability
- Investigation Completion Status

---

# Tool Integration Workflow

```text
Investigation Request
        │
        ▼
Excel Online
(List Rows)
        │
        ▼
Quality Supervisor
        │
        ▼
Specialist Agents & Topics
        │
        ▼
Excel Online
(Update Row / Add a Row)
        │
        ▼
Word Online
(Generate Investigation Report)
        │
        ▼
Outlook
(Send Stakeholder Notification)
```

---

# Error Handling

| Tool | Failure Behavior |
|------|------------------|
| Excel Online | Report retrieval/update failure and continue where possible without fabricating data |
| Word Online | Notify that report generation failed and allow manual generation |
| Outlook | Record notification failure and continue investigation completion |

---

# Summary

The project uses Microsoft 365 tools to support the complete investigation lifecycle:

- **Excel Online** manages investigation, complaint, CAPA, and audit records using **List Rows**, **Update a Row**, and **Add a Row**.
- **Word Online** automatically generates the final investigation report.
- **Outlook** sends investigation completion notifications to relevant stakeholders.

These tools are orchestrated by the **Quality Supervisor**, providing a structured, traceable, and auditable workflow.