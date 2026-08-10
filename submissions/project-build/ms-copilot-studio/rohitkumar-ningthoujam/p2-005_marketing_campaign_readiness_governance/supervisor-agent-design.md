# Supervisor Agent Design

## Agent Overview

The **Campaign Readiness Supervisor** is the primary autonomous agent responsible for coordinating the complete marketing campaign readiness assessment workflow. It orchestrates specialist child agents, applies governance policies, consolidates assessment results, manages remediation, and determines the final campaign readiness status.

---

# Agent Details

| Property | Value |
|----------|-------|
| Agent Name | Campaign Readiness Supervisor |
| Type | Autonomous Supervisor Agent |
| Platform | Microsoft Copilot Studio |
| Architecture | Hierarchical Multi-Agent |

---

# Purpose

The supervisor autonomously manages the end-to-end campaign assessment lifecycle by:

- Retrieving pending campaigns
- Validating campaign intake
- Coordinating specialist assessments
- Executing orchestration workflows
- Applying governance policies
- Managing remediation cycles
- Determining Final Readiness
- Generating reports
- Updating campaign records
- Triggering stakeholder notifications

---

# Responsibilities

## Campaign Intake

- Retrieve pending campaigns from Excel
- Validate mandatory campaign information
- Prevent duplicate assessments

## Workflow Orchestration

- Launch specialist agents
- Coordinate sequential and parallel execution
- Wait for specialist completion
- Aggregate assessment results

## Governance

- Apply business rules
- Evaluate approval requirements
- Escalate when governance thresholds are exceeded

## Remediation

- Identify failed assessments
- Trigger selective reassessment
- Consolidate updated specialist outputs

## Finalisation

- Determine Final Readiness
- Generate Word report
- Update campaign status
- Trigger Outlook notification

---

# Child Agents

The supervisor coordinates the following specialist agents:

1. Campaign Intake & Validation
2. Budget & Commercial Specialist
3. Brand & Content Compliance Specialist
4. Channel Readiness Specialist
5. Asset Readiness Specialist
6. Launch Risk & Decision Specialist
7. Reporting & Communication Specialist

---

# Connected Tools

| Tool | Purpose |
|------|---------|
| Get Pending Campaigns | Retrieve pending campaigns from Excel |
| Get Budget Rules | Retrieve governance thresholds |
| Update Row | Update campaign status |
| Create Word Document | Generate readiness report |
| Send Email | Notify stakeholders |

---

# Knowledge Sources

The supervisor references project knowledge including:

- Business Requirements Document (BRD)
- Governance rules
- Workflow orchestration guidance
- Approval rules
- Decision logic
- Remediation process

---

# Custom Topics

The supervisor implements three orchestration topics:

### Topic 1

Campaign Intake & Validation

### Topic 2

Remediation & Selective Reassessment

### Topic 3

Approval & Finalisation

---

# Decision Outputs

The supervisor determines one of the following outcomes:

- Ready
- Ready with Conditions
- Remediation Required
- Not Ready

These outputs drive the approval and reporting workflow.

---

# Design Principles

The supervisor is designed to support:

- Autonomous execution
- Hierarchical orchestration
- Parallel specialist coordination
- Governance-driven decision making
- Modular architecture
- Fault tolerance
- Selective reassessment
- Human approval where required

---

# Outcome

The Campaign Readiness Supervisor serves as the central orchestration layer of the solution, ensuring that every campaign is consistently evaluated against organisational governance requirements before launch.