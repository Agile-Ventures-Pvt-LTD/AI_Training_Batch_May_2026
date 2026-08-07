# Dataset Notes

## Overview

The Campaign Readiness Assessment solution uses a set of Microsoft Excel tables as its primary data source. These tables simulate enterprise marketing operations and provide the information required by the Supervisor Agent and Specialist Agents during campaign readiness assessment.

The datasets are stored in **Excel Online (Business)** and are accessed through Microsoft Copilot Studio connector tools.

---

# Data Source

**Platform:** Microsoft Excel Online (Business)

**Storage:** OneDrive for Business

**Access Method:** Excel Online (Business) Connector

---

# Dataset Purpose

The dataset represents marketing campaign information required to evaluate whether a campaign is ready for launch.

It contains campaign metadata, financial information, brand compliance data, channel requirements, asset readiness information, approval status, and reporting information.

---

# Tables

## 1. Campaign Requests

### Purpose

Stores the primary campaign information submitted for readiness assessment.

### Used By

- Campaign Intake & Validation Topic
- Supervisor Agent
- Budget Specialist
- Launch Risk Specialist

### Key Fields

| Field | Description |
|--------|-------------|
| CampaignID | Unique campaign identifier |
| CampaignName | Campaign title |
| Product | Product being promoted |
| CampaignOwner | Campaign owner |
| CampaignStatus | Current workflow status |
| LaunchDate | Planned launch date |
| Geography | Campaign region |
| Channels | Marketing channels |
| ProposedBudget_INR | Requested budget |
| ApprovedBudget_INR | Approved budget |
| ExpectedLeads | Expected lead count |
| TargetAudience | Target audience |
| TargetCPL_INR | Target cost per lead |
| RegulatorySensitivity | Campaign sensitivity |
| ExternalAgency | External agency involved |
| SubmissionDate | Campaign submission date |
| Notes | Additional comments |

---

## 2. Budget Allocation

### Purpose

Stores campaign budget allocation and approval information.

### Planned Usage

Budget & Commercial Specialist

### Example Fields

- CampaignID
- Budget Category
- Allocated Budget
- Approved Budget
- Remaining Budget
- Budget Owner

---

## 3. Brand Guidelines

### Purpose

Contains mandatory branding and compliance rules.

### Planned Usage

Brand & Content Compliance Specialist

### Example Fields

- Brand Rule
- Requirement
- Mandatory
- Compliance Status
- Supporting Evidence

---

## 4. Channel Requirements

### Purpose

Defines launch prerequisites for each marketing channel.

### Planned Usage

Channel Readiness Specialist

### Example Fields

- Channel
- Lead Time
- Mandatory Assets
- Tracking Requirement
- Channel Owner
- Brand Approval Required

---

## 5. Asset Status

### Purpose

Tracks readiness and approval status of campaign assets.

### Planned Usage

Asset Readiness Specialist

### Example Fields

- Asset Name
- Asset Type
- Approval Status
- QA Status
- Owner
- Readiness Status

---

## Dataset Relationships

The CampaignID field acts as the primary key used to associate campaign information across all datasets.

```
Campaign Requests
        │
        ├──────────── Budget Allocation
        │
        ├──────────── Brand Guidelines
        │
        ├──────────── Channel Requirements
        │
        └──────────── Asset Status
```

---

# Current Dataset Usage

At the current stage of implementation, only the **Campaign Requests** table is actively used.

The Campaign Intake & Validation topic retrieves campaign records from this table and validates mandatory campaign information before the readiness assessment begins.

---

# Data Validation

The Campaign Intake & Validation topic validates the following fields:

- Campaign ID
- Campaign Name
- Product
- Campaign Status
- Launch Date
- Proposed Budget
- Geography
- Marketing Channels
- Campaign Owner

Only campaigns with a **Pending** status are eligible for assessment.

---

# Data Access

The dataset is accessed through Microsoft Copilot Studio tools using the **Excel Online (Business)** connector.

Current implementation uses:

- List Rows
- Get Row (evaluated during development)
- AI Builder Prompt for campaign validation

---

# Assumptions

The dataset is intended for academic demonstration purposes.

The following assumptions were made:

- Every campaign has a unique CampaignID.
- Campaign data is maintained in Excel Online.
- Required fields follow a consistent schema.
- Campaign statuses follow the predefined workflow.
- Launch dates use a valid date format.

---

# Future Dataset Enhancements

Future versions of the solution may include:

- Dataverse as the primary data source
- Multiple campaign versions
- Historical assessment records
- Audit logs
- User and department tables
- Approval history
- Risk history
- Notification logs

---

# Dataset Summary

| Dataset | Current Status |
|----------|----------------|
| Campaign Requests |  Implemented |
| Budget Allocation | Planned |
| Brand Guidelines | Planned |
| Channel Requirements | Planned |
| Asset Status | Planned |

The current implementation focuses on validating campaign records from the **Campaign Requests** dataset, providing the foundation for subsequent specialist evaluations.