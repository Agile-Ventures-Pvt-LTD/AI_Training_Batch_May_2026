# 📊 Dataset Notes

> **Project:** P2-005 – Marketing Campaign Readiness Governance  
> **Platform:** Microsoft Copilot Studio

---

# 📖 Overview

The Campaign Readiness Governance solution uses a Microsoft Excel workbook as the primary data source for campaign assessment and governance activities.

The dataset contains campaign information, business rules, approval mappings, channel requirements, and campaign asset details used by the specialist agents during the readiness assessment.

The dataset was provided as part of the project resources and serves as the central repository for all campaign-related information.

---

# 🎯 Purpose

The dataset supports the following business capabilities:

- Campaign intake
- Campaign validation
- Budget evaluation
- Commercial assessment
- Brand compliance
- Channel readiness
- Asset readiness
- Approval routing
- Reporting
- Campaign status tracking

---

# 🗂 Workbook Structure

The workbook contains multiple Excel tables used throughout the assessment workflow.

---

## 📄 CampaignRequestsTable

### Purpose

Stores campaign requests awaiting readiness assessment.

### Used By

- Campaign Readiness Supervisor
- Budget & Commercial Specialist
- Brand & Content Compliance Specialist
- Channel Readiness Specialist

### Example Fields

| Column | Description |
|----------|-------------|
| CampaignID | Unique campaign identifier |
| CampaignName | Campaign title |
| Product | Product or service being promoted |
| CampaignOwner | Campaign owner |
| LaunchDate | Planned launch date |
| Geography | Target market |
| Channels | Marketing channels |
| ProposedBudget | Requested campaign budget |
| ApprovedBudget | Approved budget |
| TargetCPL | Target Cost Per Lead |
| CampaignStatus | Current campaign lifecycle status |

---

## 💰 BudgetRulesTable

### Purpose

Contains commercial rules and financial thresholds used during budget validation.

### Used By

- Budget & Commercial Specialist

### Example Fields

| Column | Description |
|----------|-------------|
| BudgetThreshold | Maximum permitted budget |
| TargetCPLLimit | Acceptable CPL threshold |
| BudgetVariance | Allowed budget variance |
| CommercialRule | Business rule description |

---

## 🖼 AssetStatusTable

### Purpose

Tracks campaign assets and their readiness.

### Used By

- Asset Readiness Specialist
- Brand & Content Compliance Specialist
- Channel Readiness Specialist

### Example Fields

| Column | Description |
|----------|-------------|
| AssetID | Asset identifier |
| AssetName | Asset description |
| AssetType | Image, Video, Landing Page, etc. |
| ApprovalStatus | Current approval state |
| QAStatus | Quality review status |
| AssetOwner | Responsible owner |

---

## 📣 ChannelRequirementsTable

### Purpose

Stores requirements for each supported marketing channel.

### Used By

- Channel Readiness Specialist

### Example Fields

| Column | Description |
|----------|-------------|
| ChannelName | Marketing channel |
| MandatoryAssets | Required assets |
| TrackingRequired | Tracking requirement |
| ApprovalRequired | Approval requirement |
| MinimumLeadTime | Required preparation time |

---

## ✅ ApprovalMatrixTable

### Purpose

Defines campaign approval responsibilities.

### Used By

- Budget & Commercial Specialist
- Launch Risk & Decision Specialist

### Example Fields

| Column | Description |
|----------|-------------|
| CampaignType | Campaign category |
| Approver | Responsible approver |
| ApprovalLevel | Required approval level |
| EscalationRequired | Escalation indicator |

---

# 🤖 Dataset Usage by Specialist Agents

| Specialist Agent | Dataset |
|------------------|---------|
| 💰 Budget & Commercial Specialist | CampaignRequestsTable, BudgetRulesTable, ApprovalMatrixTable |
| 🛡 Brand & Content Compliance Specialist | CampaignRequestsTable, AssetStatusTable |
| 📣 Channel Readiness Specialist | CampaignRequestsTable, ChannelRequirementsTable, AssetStatusTable |
| 🖼 Asset Readiness Specialist | AssetStatusTable |
| 🚀 Launch Risk & Decision Specialist | Specialist assessment results |
| 📄 Reporting & Communication Specialist | Final assessment results, CampaignRequestsTable |

---

# 🔄 Data Flow

The following illustrates how campaign data moves through the solution.

```text
CampaignRequestsTable

↓

Campaign Readiness Supervisor

↓

Campaign Intake & Validation

↓

Specialist Agents

↓

Launch Risk Assessment

↓

Reporting & Communication

↓

CampaignRequestsTable (Updated)

↓

Final Report

↓

Outlook Notification
```

---

# 🔗 Dataset Relationships

```text
CampaignRequestsTable
        │
        ├──────────────┐
        ▼              ▼
BudgetRulesTable   ChannelRequirementsTable
        │              │
        └──────┐  ┌────┘
               ▼  ▼
        AssetStatusTable
               │
               ▼
      ApprovalMatrixTable
```

Each table contributes information required by one or more specialist agents during campaign assessment.

---

# 📋 Data Assumptions

The implementation assumes:

- Each campaign has a unique **CampaignID**.
- Campaign information is complete before assessment begins.
- Budget values are stored using a consistent currency.
- Launch dates are maintained in a valid date format.
- Marketing channels follow predefined naming conventions.
- Asset records accurately reflect their current approval status.
- Approval rules are maintained within the Approval Matrix.

---

# 🔒 Data Governance

The dataset is treated as the authoritative source of campaign information.

Key governance principles include:

- Read-only access during assessment (except final status updates).
- Consistent naming conventions.
- Controlled Microsoft 365 access.
- No modification of business rules during execution.
- Centralized campaign tracking.

---

# 📊 Data Quality Considerations

To ensure reliable assessments, the following practices are recommended:

- Regular validation of campaign records.
- Removal of duplicate campaign entries.
- Periodic review of budget rules.
- Verification of approval assignments.
- Maintenance of asset approval status.
- Consistent channel configuration.

---

# 📈 Future Enhancements

The dataset can be extended to support:

- Dataverse integration
- SharePoint lists
- SQL databases
- Campaign history
- Audit logs
- Regional compliance rules
- Multi-language campaigns
- Marketing performance metrics

These enhancements can be introduced without changing the existing Supervisor–Specialist architecture.

---

# 📌 Dataset Summary

| Dataset | Purpose |
|----------|---------|
| CampaignRequestsTable | Campaign information |
| BudgetRulesTable | Financial validation |
| AssetStatusTable | Asset readiness |
| ChannelRequirementsTable | Channel validation |
| ApprovalMatrixTable | Approval governance |

---

# 📸 Supporting Evidence

Relevant screenshots include:

- 📷 excel-tools.png
- 📷 supervisor-agent.png
- 📷 final-assessment.png

---

# ✅ Conclusion

The Microsoft Excel dataset provides the foundational data required by the Campaign Readiness Governance solution.

By organizing campaign information into dedicated business tables, the solution enables the Supervisor Agent and specialist agents to perform structured assessments while maintaining clear separation of responsibilities and supporting scalable campaign governance within Microsoft Copilot Studio.