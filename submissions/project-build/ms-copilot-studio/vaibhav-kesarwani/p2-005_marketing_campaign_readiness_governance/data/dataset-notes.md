# Dataset notes

## Overview

The Autonomous Marketing Campaign Launch Readiness & Governance System uses **Excel Online (Business)** as the operational data source. The datasets simulate enterprise marketing campaign governance data used by the Supervisor and specialist child agents.

## Dataset summary

| Dataset              | Purpose                                          |
| -------------------- | ------------------------------------------------ |
| Campaign_Requests    | Primary campaign assessment queue                |
| Budget_Rules         | Budget thresholds and financial governance rules |
| Approval_Matrix      | Approval routing and approver mapping            |
| Channel_Requirements | Channel-specific readiness requirements          |
| Asset_Status         | Asset availability and approval tracking         |
| Stakeholders         | Notification recipients and ownership mapping    |

## Campaign_Requests

Primary operational table used by the Supervisor.

### Key fields

| Field              | Description                |
| ------------------ | -------------------------- |
| CampaignID         | Unique campaign identifier |
| CampaignName       | Campaign name              |
| Product            | Product being promoted     |
| Objective          | Campaign objective         |
| Geography          | Target geography           |
| Channels           | Marketing channels         |
| LaunchDate         | Planned launch date        |
| ProposedBudget_INR | Proposed campaign budget   |
| ApprovedBudget_INR | Approved budget            |
| TargetCPL          | Target cost per lead       |
| CampaignOwner      | Responsible campaign owner |
| CampaignStatus     | Workflow state             |
| FinalReadiness     | Final governance decision  |
| RiskLevel          | Risk classification        |
| ReportURL          | Generated report location  |

## Budget_Rules

Defines financial governance rules.

### Key fields

| Field           | Description             |
| --------------- | ----------------------- |
| RuleID          | Rule identifier         |
| BudgetThreshold | Budget threshold        |
| ApprovalLevel   | Required approver       |
| CPLThreshold    | Cost-per-lead threshold |

## Approval_Matrix

Maps approval conditions to approvers.

### Key fields

| Field           | Description          |
| --------------- | -------------------- |
| ApprovalType    | Approval category    |
| Approver        | Required approver    |
| EscalationLevel | Escalation authority |

## Channel_Requirements

Defines channel-specific operational requirements.

### Key fields

| Field            | Description          |
| ---------------- | -------------------- |
| Channel          | Marketing channel    |
| MandatoryAssets  | Required assets      |
| MinimumLeadTime  | Minimum lead time    |
| TrackingRequired | Tracking requirement |

## Asset_Status

Tracks campaign asset readiness.

### Key fields

| Field          | Description         |
| -------------- | ------------------- |
| CampaignID     | Campaign identifier |
| AssetName      | Asset name          |
| AssetType      | Asset category      |
| ApprovalStatus | Approval state      |
| QAStatus       | QA completion       |
| Owner          | Responsible owner   |

## Stakeholders

Stores notification recipients.

### Key fields

| Field     | Description        |
| --------- | ------------------ |
| Role      | Stakeholder role   |
| Name      | Stakeholder name   |
| Email     | Notification email |
| Geography | Regional ownership |

## Dataset relationships

```text
Campaign_Requests
        |
        +---- Budget_Rules
        |
        +---- Approval_Matrix
        |
        +---- Channel_Requirements
        |
        +---- Asset_Status
        |
        +---- Stakeholders
```

## Data usage by agent

| Agent                | Primary datasets                                      |
| -------------------- | ----------------------------------------------------- |
| Supervisor           | Campaign_Requests                                     |
| Budget Specialist    | Campaign_Requests, Budget_Rules, Approval_Matrix      |
| Brand Specialist     | Campaign_Requests, Asset_Status                       |
| Channel Specialist   | Campaign_Requests, Channel_Requirements, Asset_Status |
| Asset Specialist     | Asset_Status                                          |
| Risk Specialist      | Consolidated specialist outputs                       |
| Reporting Specialist | Campaign_Requests, Stakeholders                       |

## Assumptions

* CampaignID values are unique.
* LaunchDate values use a consistent date format.
* Budget values are stored in INR.
* Channels may contain multiple values.
* Approval statuses are standardized.
* Asset ownership is maintained for remediation routing.

## Limitations

* The datasets are designed for project demonstration purposes.
* Excel is used instead of Dataverse.
* Historical audit records are not maintained.
* Cross-workbook relational integrity is limited.

## Conclusion

The datasets provide sufficient operational coverage for autonomous campaign intake, specialist assessment, approval routing, remediation, reporting, and notification workflows within the Microsoft Copilot Studio implementation.
