# P2-005 — Autonomous marketing campaign launch readiness & governance system

## Project overview

This project implements an **Autonomous Marketing Campaign Launch Readiness & Governance System** using **Microsoft Copilot Studio**. The solution autonomously evaluates whether a marketing campaign is ready for launch by orchestrating multiple specialist child agents under the control of a central **Campaign Readiness Supervisor**.

The system uses **event-driven execution**, **hierarchical multi-agent orchestration**, **parallel specialist assessments**, **conditional routing**, **selective reassessment**, and **governance-based decision making** to determine campaign launch readiness.

The implementation follows the architecture and orchestration requirements defined in the P2-005 Product Requirements Document (PRD).

## Business objective

NovaSphere Technologies Pvt. Ltd. executes campaigns across email, LinkedIn, webinars, web, paid search, and events.

Before launch, every campaign must be validated for:

* Budget approval
* Brand compliance
* Content governance
* Channel readiness
* Asset readiness
* Geographic approvals
* Timing risk
* Executive approvals
* Tracking readiness
* Governance compliance

The autonomous system replaces manual cross-functional review by coordinating specialist AI assessments and producing a final governance decision.

## Solution architecture

The solution uses a **Supervisor-Agent architecture**.

```
Recurrence Trigger
        |
        v
Campaign Readiness Supervisor
        |
        v
Campaign Intake & Validation
        |
        v
-----------------------------------------
|        |         |          |
v        v         v          v
Budget  Brand    Channel    Asset
Specialist Specialist Specialist Specialist
-----------------------------------------
        |
        v
Launch Risk & Decision Specialist
        |
        v
Supervisor Validation
        |
        v
Remediation / Approval
        |
        v
Reporting & Communication
        |
        v
Excel + Word + Outlook
```

## Orchestration patterns implemented

The solution demonstrates all mandatory orchestration patterns.

### Sequential orchestration

Execution order:

1. Trigger
2. Intake validation
3. Specialist assessments
4. Fan-in consolidation
5. Risk evaluation
6. Supervisor validation
7. Reporting
8. Excel update
9. Outlook notification

### Parallel fan-out / fan-in

The Supervisor invokes four independent specialist child agents:

* Budget & Commercial Specialist
* Brand & Content Compliance Specialist
* Channel Readiness Specialist
* Asset Readiness Specialist

The Supervisor waits for all mandatory specialist results before consolidation.

### Hierarchical orchestration

The Supervisor controls:

* Child-agent invocation
* Campaign state
* Final readiness classification
* Conflict resolution
* Reassessment
* Reporting authorization
* Notification authorization

Child agents return findings only.

### Conditional routing

Conditional execution includes:

* Approval routing
* Remediation routing
* High-sensitivity review
* Multi-market review
* Manual review
* Failure handling

### Selective reassessment

Only specialist domains whose underlying data changes are reassessed.

Examples:

* Asset correction → Asset/Channel reassessment
* Budget approval → Budget reassessment
* Brand correction → Brand reassessment

## Supervisor responsibilities

The Campaign Readiness Supervisor is the only component authorized to:

* Assign final readiness
* Update campaign state
* Invoke child agents
* Authorize reporting
* Authorize stakeholder communication
* Trigger reassessment
* Resolve specialist conflicts

## Specialist agents

### Budget & Commercial Specialist

Evaluates:

* Budget variance
* CPL thresholds
* Approval requirements
* Financial blockers

### Brand & Content Compliance Specialist

Evaluates:

* Product naming
* Claims
* Disclaimers
* Brand approval
* Content compliance

### Channel Readiness Specialist

Evaluates:

* Mandatory channel assets
* Lead times
* Tracking readiness
* Channel blockers

### Asset Readiness Specialist

Evaluates:

* Asset availability
* Approval status
* QA status
* Missing assets

### Launch Risk & Decision Specialist

Evaluates:

* Risk level
* Timing risk
* Approval exposure
* Governance impact

### Reporting & Communication Specialist

Generates:

* Word readiness report
* Outlook stakeholder notification

## Data sources

The solution uses Excel Online (Business) tables:

* Campaign_Requests
* Budget_Rules
* Approval_Matrix
* Channel_Requirements
* Asset_Status
* Stakeholders

## Knowledge sources

The following governance documents are used:

* NovaSphere Marketing Governance Policy
* NovaSphere Brand & Content Guidelines

## Campaign state model

Supported states:

* Pending
* In Assessment
* Awaiting Remediation
* Awaiting Approval
* Ready with Conditions
* Ready
* Not Ready
* Manual Review
* Completed

## Final readiness outcomes

The Supervisor applies the mandatory precedence:

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

## Failure handling

The implementation safely handles:

* Specialist failures
* Missing evidence
* Word generation failure
* Outlook delivery failure
* Reassessment limits
* Duplicate processing
* Missing campaign data

The system never fabricates:

* Specialist success
* Human approvals
* Reports
* Notifications

## Technologies used

* Microsoft Copilot Studio
* Generative Orchestration
* Child Agents
* Custom Topics
* Excel Online (Business)
* Word Online (Business)
* Outlook
* OneDrive for Business

## Repository structure

```
p2-005_marketing_campaign_readiness_governance/
│
├── README.md
├── solution-summary.md
├── architecture.md
├── orchestration-patterns.md
├── supervisor-agent-design.md
├── specialist-agent-design.md
├── custom-topics.md
├── autonomous-trigger.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
│
├── data/
│   └── dataset-notes.md
│
└── screenshots/
    ├── supervisor-agent.png
    ├── child-agents.png
    ├── recurrence-trigger.png
    ├── intake-topic.png
    ├── parallel-specialists.png
    ├── fan-in-consolidation.png
    ├── remediation-topic.png
    ├── approval-topic.png
    ├── excel-tools.png
    ├── word-tool.png
    ├── outlook-tool.png
    └── final-assessment.png
```