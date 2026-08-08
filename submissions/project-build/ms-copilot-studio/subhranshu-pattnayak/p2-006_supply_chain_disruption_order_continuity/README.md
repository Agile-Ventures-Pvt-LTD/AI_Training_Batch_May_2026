# Supply Chain Disruption Order Continuity System

## Agent Access

Agent URL:

[<SUPPLY CONTINUITY SUPERVISOR>](https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/74662ff6-aa92-f111-b8dc-000d3af21e08/overview)


## Overview

The Supply Chain Disruption Order Continuity System is an autonomous multi-agent solution built using Microsoft Copilot Studio to manage supply disruption events and support business continuity decisions.

The solution continuously monitors disruption requests, validates incoming incidents, coordinates specialist assessments, determines recovery strategies, routes approval requirements, generates stakeholder reports, and communicates outcomes through automated workflows.

The system follows a governed decision-making process where specialist agents perform domain-specific assessments while a central Supervisor Agent orchestrates execution, enforces policy rules, and determines the final recommendation.

---

## Business Problem

Supply chain disruptions can impact inventory availability, customer commitments, supplier operations, service-level agreements (SLAs), and commercial performance.

Traditionally, disruption assessment requires multiple teams to manually gather information, evaluate risks, identify recovery options, obtain approvals, and communicate decisions. This process is often time-consuming, inconsistent, and difficult to audit.

The objective of this solution is to automate disruption assessment and recovery planning while ensuring that business policies, approval requirements, and operational constraints are consistently enforced.

---

## Solution Summary

The solution uses a Supervisor Agent that orchestrates a network of specialist agents and deterministic governance topics.

The workflow:

1. Detects pending disruption requests.
2. Validates disruption data.
3. Launches specialist assessments in parallel.
4. Consolidates specialist findings.
5. Generates recovery recommendations.
6. Applies policy-driven recovery selection.
7. Determines approval and escalation requirements.
8. Produces stakeholder reports.
9. Sends business notifications.
10. Updates disruption status records.

---

## Solution Components

### Supervisor Agent

The Supply Continuity Supervisor is responsible for:

- Workflow orchestration
- Specialist coordination
- Fan-out and fan-in processing
- Conflict resolution
- Policy enforcement
- Approval determination
- Escalation handling
- Final recommendation generation

The Supervisor does not perform specialist analysis directly and relies on specialist findings before making decisions.

---

### Specialist Agents

#### Inventory Impact Specialist

Assesses:

- Inventory availability
- Available-To-Promise (ATP)
- Inventory sufficiency
- Inventory shortages
- Safety stock impact
- Inventory risk

---

#### Alternate Supplier Specialist

Assesses:

- Alternate supplier availability
- Supplier approval status
- Supplier capacity
- Lead times
- Supplier risks
- Alternate sourcing feasibility

---

#### Customer & Order Impact Specialist

Assesses:

- Affected customer orders
- Customer priorities
- SLA exposure
- Revenue exposure
- Fulfillment risks
- Customer impact classification

---

#### Commercial Impact Specialist

Assesses:

- Revenue exposure
- Alternate sourcing costs
- Cost premiums
- Expedite premiums
- Commercial risk
- Approval requirements

---

#### Recovery Planning Specialist

Assesses:

- Recovery options
- Recovery feasibility
- Order protection capability
- Residual risk
- Required actions
- Recommended recovery strategy

---

#### Reporting & Communication Specialist

Generates:

- Final disruption report
- Stakeholder communications
- Outlook notifications
- Execution summaries

---

## Custom Topics

The solution contains three mandatory deterministic governance topics.

### Topic 1 – Disruption Intake & Validation

Purpose:

Validate disruption requests before specialist assessments begin.

Outputs:

    - ValidationStatus
    - DuplicateDetected

---

### Topic 2 – Recovery Strategy Resolution

Purpose:

Select the appropriate recovery branch based on specialist outputs and policy rules.

Outputs:

    - SelectedRecoveryBranch
    - SelectedRecoveryStrategy
    - EscalationRequired

---

### Topic 3 – Approval, Exception & Selective Reassessment

Purpose:

Manage approval routing, reassessment limits, and manual review escalation.

Outputs:

    - CaseStatus
    - ManualReviewRequired
    - UpdatedReassessmentCycleCount

---

## Workflow Architecture

```text
                Autonomous Trigger
                        |
                        V
                Supply Continuity Supervisor
                        |
                        V
                Disruption Intake & Validation
                        |
        +----------------------------------+
        |          |          |            |
        V          V          V            V
Inventory   Alternate   Customer    Commercial
Specialist  Supplier    Impact      Impact
                        Specialist  Specialist
        |
        +----------------------------------+
                       |
                       V
              Fan-In Consolidation
                       |
                       V
          Recovery Planning Specialist
                       |
                       V
         Recovery Strategy Resolution
                       |
                       V
 Approval, Exception & Reassessment
                       |
                       V
      Reporting & Communication Agent
                       |
                       V
               Status Update
```

---

## Technologies Used

- Microsoft Copilot Studio
- Microsoft Power Automate
- Microsoft Excel Online
- Microsoft Word Online
- Microsoft Outlook
- Autonomous Agents
- Custom Topics
- Knowledge Base Driven Policy Enforcement

---

## Key Design Principles

The solution was designed around the following principles:

- Deterministic governance decisions
- Policy-driven execution
- Separation of responsibilities
- Evidence-based recommendations
- Human approval for governed actions
- Explainable recovery decisions
- Auditable workflow execution

---

## Testing

The solution was tested across:

- Validation scenarios
- Recovery branch selection scenarios
- Approval routing scenarios
- Escalation scenarios
- Reassessment scenarios
- End-to-end workflow execution

Detailed test results are available in:

`test-report.md`

---

## Limitations

The solution:

- Depends on workbook data accuracy.
- Cannot assess unavailable data.
- Cannot approve expenditures.
- Cannot approve supplier qualification.
- Cannot commit inventory.
- Cannot create purchase orders.
- Cannot make customer delivery commitments.
- Requires human approval where policy mandates approval.

Additional limitations are documented in:

`known-limitations.md`

---

## Repository Structure

```text
p2-006_supply_chain_disruption_order_continuity/

├── README.md
├── solution-summary.md
├── architecture.md
├── orchestration-patterns.md
├── supervisor-agent-design.md
├── specialist-agent-design.md
├── custom-topics.md
├── autonomous-trigger.md
├── decision-rules.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md

├── data/
│   └── dataset-notes.md

└── screenshots/
    ├── supervisor-agent.png
    ├── child-agents.png
    ├── recurrence-trigger.png
    ├── intake-validation-topic.png
    ├── fan-out-specialists.png
    ├── fan-in-consolidation.png
    ├── recovery-strategy-topic.png
    ├── approval-reassessment-topic.png
    ├── excel-tools.png
    ├── word-tool.png
    ├── outlook-tool.png
    └── final-response.png
```

---

## Author

Project: P2-006 Supply Chain Disruption Order Continuity

Platform: Microsoft Copilot Studio

Implementation Type: Autonomous Multi-Agent Workflow with Deterministic Governance Topics

---