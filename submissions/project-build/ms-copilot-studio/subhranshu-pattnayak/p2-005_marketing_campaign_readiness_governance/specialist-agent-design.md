# Specialist Agent Design

## Overview

The solution uses six specialist agents.

Each specialist focuses on a specific assessment domain and returns findings using a standardized output contract.

The Supervisor consolidates specialist outputs and determines final readiness.

---

# Standard Output Contract

All specialists return:

- SpecialistName
- AssessmentStatus
- EvidenceSummary
- BlockingIssues
- Conditions
- RequiredActions
- RequiredApprover
- Confidence
- Completed

AssessmentStatus values:

- Pass
- Condition
- Block
- Insufficient Evidence

---

# Budget & Commercial Specialist

## Purpose

Evaluate financial readiness.

## Data Sources

- Campaign Requests
- Budget Rules
- Approval Matrix

## Responsibilities

Evaluate:

- Proposed Budget
- Approved Budget
- Budget Variance
- Target CPL
- Expected Leads
- Approval Requirements

## Outputs

- Budget Assessment
- Approval Requirements
- Budget Findings
- Recommended Actions

---

# Brand & Content Compliance Specialist

## Purpose

Evaluate campaign content compliance.

## Knowledge Source

- NovaSphere Brand & Content Guidelines

## Data Sources

- Campaign Requests
- Asset Status

## Responsibilities

Evaluate:

- Product Naming
- Claims
- Disclaimers
- Regulatory Sensitivity
- Brand Approval Requirements
- CTA Consistency

## Outputs

- Brand Assessment
- Compliance Findings
- Required Approvals
- Recommended Actions

---

# Channel Readiness Specialist

## Purpose

Evaluate operational channel readiness.

## Data Sources

- Campaign Requests
- Channel Requirements
- Asset Status

## Responsibilities

Evaluate:

- Channel Assets
- Lead Times
- Tracking Requirements
- Channel Ownership
- Launch Prerequisites

## Outputs

- Channel Assessment
- Launch Blockers
- Missing Requirements

---

# Asset Readiness Specialist

## Purpose

Evaluate campaign asset readiness.

## Data Sources

- Asset Status
- Campaign Requests

## Responsibilities

Evaluate:

- Asset Availability
- Approval Status
- QA Status
- Missing Assets

## Asset Classification

- Ready
- Conditional
- Blocking
- Missing

## Outputs

- Asset Assessment
- Aggregate Counts
- Missing Asset Findings

---

# Launch Risk & Decision Specialist

## Purpose

Assess overall campaign launch risk.

## Inputs

- Budget Findings
- Brand Findings
- Channel Findings
- Asset Findings
- Days To Launch
- Geography
- Sensitivity
- Pending Approvals

## Responsibilities

Identify:

- Blocking Issues
- Timing Risks
- Approval Risks
- Campaign Risk Level

## Risk Levels

- Low
- Medium
- High
- Critical

## Outputs

- Risk Classification
- Proposed Outcome
- Additional Findings

---

# Reporting & Communication Specialist

## Purpose

Generate reports and stakeholder communications.

## Responsibilities

Generate:

- Campaign Readiness Report
- Stakeholder Notifications

## Outputs

- Word Report
- Notification Content
- Readiness Summary