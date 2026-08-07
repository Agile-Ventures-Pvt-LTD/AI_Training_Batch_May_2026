
# Dataset Notes

# 1. Overview

The Autonomous Marketing Campaign Launch Readiness & Governance System uses Microsoft Excel Online (Business) as its operational data source. The workbook serves as the central repository for campaign information, governance rules, operational metadata, and supporting reference data used throughout the campaign readiness assessment process.

The dataset is accessed through Microsoft Copilot Studio using native Microsoft Excel Online (Business) connector actions.

---

# 2. Operational Data Source

| Property         | Value                                              |
| ---------------- | -------------------------------------------------- |
| Storage Platform | Microsoft OneDrive for Business                    |
| Data Source      | Microsoft Excel Online (Business)                  |
| Primary Workbook | Campaign Readiness Dataset                         |
| Access Method    | Native Microsoft Excel Online (Business) Connector |
| Primary Key      | CampaignID                                         |

The workbook provides all operational information required to evaluate marketing campaigns.

---

# 3. Dataset Structure

The workbook contains the following logical datasets.

| Dataset              | Purpose                                           |
| -------------------- | ------------------------------------------------- |
| Campaign Requests    | Primary operational campaign records              |
| Budget Rules         | Budget validation thresholds and commercial rules |
| Channel Requirements | Channel-specific readiness requirements           |
| Asset Status         | Asset availability and approval status            |
| Approval Matrix      | Approval rules and required approvers             |
| Stakeholders         | Notification recipients and campaign owners       |
| Test Scenarios       | Validation scenarios used during testing          |
| README               | Dataset documentation and metadata                |

---

# 4. Primary Operational Table

The primary operational table is:

**CampaignRequestsTable**

This table contains the campaign records processed by the Campaign Readiness Supervisor.

Each campaign is uniquely identified using:

**CampaignID**

CampaignID serves as the logical primary key throughout the entire solution.

---

# 5. Campaign Requests Table

The Campaign Requests dataset contains the information required for campaign intake validation and specialist assessment.

Typical campaign attributes include:

- CampaignID
- CampaignName
- CampaignObjective
- CampaignStatus
- CampaignOwner
- Product
- Geography
- LaunchDate
- ProposedBudget_INR
- ApprovedBudget_INR
- TargetCPL_INR
- RegulatorySensitivity
- Channels
- Notes

These attributes are consumed by different specialist agents according to their business responsibilities.

---

# 6. Dataset Usage by Agent

## Campaign Readiness Supervisor

Uses:

- Campaign Requests

Purpose:

- Identify Pending campaigns.
- Retrieve campaign information.
- Update campaign lifecycle status.
- Coordinate campaign processing.

---

## Budget & Commercial Specialist

Uses:

- Campaign Requests
- Budget Rules

Purpose:

- Validate commercial readiness.
- Compare approved and proposed budgets.
- Identify financial approval requirements.

---

## Brand & Content Compliance Specialist

Uses:

- Campaign Requests
- Brand-related campaign information

Purpose:

- Validate campaign branding.
- Review content compliance.
- Verify governance requirements.

---

## Channel Readiness Specialist

Uses:

- Campaign Requests
- Channel Requirements

Purpose:

- Validate channel prerequisites.
- Verify campaign delivery readiness.

---

## Asset Readiness Specialist

Uses:

- Campaign Requests
- Asset Status

Purpose:

- Verify required campaign assets.
- Detect missing or unapproved assets.

---

## Launch Risk & Decision Specialist

Uses:

- Campaign information
- Specialist assessment results
- Governance policy

Purpose:

- Evaluate overall campaign risk.
- Recommend campaign readiness.

---

## Reporting & Communication Specialist

Uses:

- Final validated campaign information.
- Final readiness outcome.
- Specialist findings.

Purpose:

- Generate campaign reports.
- Prepare stakeholder notifications.

---

# 7. Campaign Lifecycle Values

The CampaignStatus field is used to manage campaign progression throughout the assessment workflow.

Typical lifecycle values include:

- Pending
- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Ready
- Ready with Conditions
- Not Ready
- Manual Review
- Completed

The Campaign Readiness Supervisor manages all lifecycle transitions.

---

# 8. Dataset Relationships

The operational datasets are logically related through campaign information.

```text
Campaign Requests
        │
        ├────────► Budget Rules
        │
        ├────────► Channel Requirements
        │
        ├────────► Asset Status
        │
        ├────────► Approval Matrix
        │
        └────────► Stakeholders
```

Campaign Requests serves as the central dataset for all assessments.

---

# 9. Knowledge vs Operational Data

The solution distinguishes between operational data and enterprise knowledge.

## Operational Data

Stored in Microsoft Excel:

- Campaign Requests
- Budget Rules
- Channel Requirements
- Asset Status
- Approval Matrix
- Stakeholders

Operational data changes over time and is retrieved dynamically during workflow execution.

---

## Enterprise Knowledge

Knowledge documents include:

- NovaSphere Marketing Governance Policy
- NovaSphere Brand & Content Guidelines

These documents are used to ground AI reasoning but are not modified during execution.

---

# 10. Evaluator Reference

The evaluator expected outcomes provided with the project are used exclusively for validation and testing.

They are **not** added to any agent as knowledge and are **not** used during campaign assessment.

This ensures that campaign readiness decisions are based solely on operational data and governance policies.

---

# 11. Data Integrity Assumptions

The solution assumes:

- CampaignID values are unique.
- Required operational tables exist.
- Workbook schema remains unchanged.
- Microsoft Excel Online (Business) is accessible.
- Campaign records accurately represent the current campaign state.

Changes to the workbook structure may require connector reconfiguration.

---

# 12. Summary

The Microsoft Excel workbook provides the operational foundation for the Autonomous Marketing Campaign Launch Readiness & Governance System. By separating operational data from enterprise knowledge, the solution enables deterministic workflow execution, governance-based AI reasoning, structured campaign lifecycle management, and scalable multi-agent orchestration while maintaining data integrity and traceability.
