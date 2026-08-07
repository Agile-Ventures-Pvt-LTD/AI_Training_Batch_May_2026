# Dataset Notes

## Overview

The Campaign Readiness Governance System uses structured Microsoft Excel tables as its primary operational data source.

Each table represents a specific business domain and is accessed through Microsoft Excel Online (Business) connectors in Microsoft Copilot Studio.

The data supports campaign retrieval, specialist assessments, governance validation, reporting, and campaign lifecycle management.

---

# Dataset Summary

| Table Name | Purpose | Primary Consumer |
|------------|---------|------------------|
| CampaignRequestsTable | Campaign information and lifecycle | Supervisor |
| BudgetRulesTable | Budget governance policies | Budget & Commercial Specialist |
| ApprovalMatrixTable | Approval hierarchy | Budget & Commercial Specialist |
| AssetStatusTable | Campaign asset readiness | Asset Readiness Specialist, Channel Readiness Specialist, Brand & Content Compliance Specialist |
| ChannelRequirementsTable | Channel operational requirements | Channel Readiness Specialist |

---

# CampaignRequestsTable

## Purpose

Stores the master record for every marketing campaign submitted for readiness assessment.

This table is the primary entry point for the workflow.

---

## Key Information

The table contains campaign information including:

- Campaign ID
- Campaign Name
- Product
- Business Objective
- Target Audience
- Geography
- Launch Date
- Proposed Budget
- Approved Budget
- Marketing Channels
- Campaign Owner
- Campaign Status
- Submission Date
- Expected Leads
- Target CPL
- Regulatory Sensitivity
- External Agency Indicator
- Campaign Notes

---

## Used By

Campaign Readiness Supervisor

Purpose:

- Retrieve pending campaigns
- Select oldest pending campaign
- Retrieve campaign details
- Update campaign lifecycle status

---

# BudgetRulesTable

## Purpose

Defines financial governance rules for campaign approval.

The table stores the policies used to evaluate commercial readiness.

---

## Typical Information

- Budget thresholds
- Maximum approved variance
- Target CPL thresholds
- Financial approval rules
- Commercial governance policies

---

## Used By

Budget & Commercial Specialist

Purpose:

- Budget validation
- Budget variance assessment
- CPL validation
- Financial governance

---

# ApprovalMatrixTable

## Purpose

Stores the organizational approval hierarchy used during campaign governance.

---

## Typical Information

- Approval level
- Required approver
- Budget approval thresholds
- Executive approval requirements
- Regional approval rules

---

## Used By

Budget & Commercial Specialist

Purpose:

- Determine required approver
- Validate approval requirements
- Apply governance policies

---

# AssetStatusTable

## Purpose

Stores the readiness status of campaign assets.

---

## Typical Information

- Asset Name
- Asset Type
- Availability
- Approval Status
- QA Status
- Production Readiness
- Review Status

---

## Used By

Asset Readiness Specialist

Purpose:

- Asset readiness assessment
- Missing asset identification
- QA validation

---

Brand & Content Compliance Specialist

Purpose:

- Brand approval validation
- Campaign content validation

---

Channel Readiness Specialist

Purpose:

- Validate required channel assets
- Confirm operational dependencies

---

# ChannelRequirementsTable

## Purpose

Stores operational requirements for each marketing channel.

---

## Typical Information

- Channel Name
- Required Assets
- Minimum Lead Time
- Tracking Requirements
- Channel Owner
- Operational Dependencies
- Launch Prerequisites

---

## Used By

Channel Readiness Specialist

Purpose:

- Channel readiness assessment
- Dependency validation
- Operational readiness

---

# Data Relationships

```
CampaignRequestsTable
        │
        ├──────────────┐
        │              │
        ▼              ▼
BudgetRulesTable   ApprovalMatrixTable
        │
        ▼
Budget Specialist

CampaignRequestsTable
        │
        ▼
AssetStatusTable
        │
        ├──────────────┬──────────────┐
        │              │              │
        ▼              ▼              ▼
Asset        Brand & Content      Channel
Specialist     Specialist        Specialist

CampaignRequestsTable
        │
        ▼
ChannelRequirementsTable
        │
        ▼
Channel Readiness Specialist
```

---

# Data Management

The solution follows the following data management principles:

- Campaign data is retrieved from structured Excel tables.
- Each specialist accesses only the data required for its assigned responsibility.
- The Supervisor coordinates all workflow execution.
- Campaign lifecycle updates are written back to the CampaignRequestsTable.
- Knowledge sources are used only for governance and policy decisions.

---

# Notes

The datasets supplied with this project are intended to simulate enterprise marketing governance data.

The structured tables enable autonomous campaign readiness assessment while maintaining consistency, traceability, and separation of responsibilities across the Supervisor and Specialist Agents.