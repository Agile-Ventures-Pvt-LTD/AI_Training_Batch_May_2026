# Architecture

## System architecture

The Autonomous Marketing Campaign Launch Readiness & Governance System is implemented using **Microsoft Copilot Studio** with a **hierarchical Supervisor-Agent architecture**. The architecture is designed around a central **Campaign Readiness Supervisor** that orchestrates multiple specialist child agents, custom topics, and Microsoft 365 integrations.

The implementation follows the mandatory architectural patterns defined in the project requirements:

* Sequential orchestration
* Parallel fan-out / fan-in
* Hierarchical supervision
* Conditional routing
* Selective reassessment
* Failure handling

## High-level architecture

```text
Recurrence Event Trigger
           |
           v
Campaign Readiness Supervisor
           |
           v
Campaign Intake & Validation
           |
           v
-------------------------------------------------
|          |            |             |
v          v            v             v
Budget   Brand       Channel       Asset
Agent    Agent        Agent         Agent
-------------------------------------------------
           |
           v
Launch Risk & Decision Specialist
           |
           v
Supervisor Validation
           |
     ---------------------
     |                   |
     v                   v
Approval Topic      Remediation Topic
     |                   |
     -----------+---------
                |
                v
Reporting & Communication Specialist
                |
         ------------------
         |                |
         v                v
Word Report          Outlook Email
                |
                v
Excel Update
```

## Architectural principles

### Supervisor-controlled orchestration

The Campaign Readiness Supervisor acts as the parent orchestration agent and controls the complete execution lifecycle.

Supervisor responsibilities:

* campaign selection,
* intake validation,
* specialist invocation,
* fan-in consolidation,
* conflict resolution,
* readiness classification,
* remediation coordination,
* approval routing,
* reporting authorization,
* notification authorization.

Child agents are intentionally restricted to domain-specific analysis.

### Event-driven autonomous execution

The system begins execution through a **Copilot Studio Recurrence Trigger**.

On each trigger:

1. Read pending campaigns from Excel.
2. Select the oldest pending campaign.
3. Mark it In Assessment.
4. Begin autonomous orchestration.

This design prevents duplicate concurrent processing.

## Core components

### Campaign Readiness Supervisor

The Supervisor is the central decision-making component.

Inputs:

* campaign data,
* specialist outputs,
* approval status,
* remediation status,
* governance policy.

Outputs:

* final readiness,
* campaign state,
* reporting authorization,
* notification authorization.

The Supervisor is the only component permitted to assign final readiness.

### Campaign Intake & Validation

This topic performs deterministic validation before specialist assessment.

Validated elements:

* campaign identity,
* duplicate processing,
* campaign status,
* launch timing,
* budget values,
* geography,
* channels,
* ownership.

Invalid campaigns terminate before specialist execution.

### Specialist child agents

#### Budget & Commercial Specialist

Evaluates:

* proposed budget,
* approved budget,
* budget variance,
* CPL thresholds,
* approval requirements,
* financial blockers.

Primary data:

* Campaign Requests
* Budget Rules
* Approval Matrix

#### Brand & Content Compliance Specialist

Evaluates:

* product naming,
* claims,
* disclaimers,
* regulatory sensitivity,
* brand approvals,
* CTA consistency.

Primary data:

* Campaign Requests
* Asset Status
* Brand Guidelines

#### Channel Readiness Specialist

Evaluates:

* mandatory channel assets,
* lead times,
* tracking readiness,
* ownership,
* channel blockers.

Primary data:

* Campaign Requests
* Channel Requirements
* Asset Status

#### Asset Readiness Specialist

Evaluates:

* asset availability,
* approval status,
* QA status,
* missing assets,
* ownership.

Primary data:

* Asset Status

### Launch Risk & Decision Specialist

This specialist receives consolidated outputs from the four domain specialists.

Responsibilities:

* risk classification,
* timing analysis,
* approval exposure,
* governance impact,
* proposed readiness.

Risk levels:

* Low
* Medium
* High
* Critical

The specialist proposes a recommendation.

The Supervisor validates it.

### Reporting & Communication Specialist

Executes only after Supervisor validation.

Responsibilities:

* Word report generation,
* Excel report update,
* Outlook notification,
* communication status reporting.

## Data architecture

### Operational data layer

The solution uses **Excel Online (Business)** as the operational data store.

Tables:

* Campaign_Requests
* Budget_Rules
* Approval_Matrix
* Channel_Requirements
* Asset_Status
* Stakeholders

Campaign_Requests acts as the operational processing queue.

### Knowledge layer

Knowledge is scoped by responsibility.

Supervisor:

* Marketing Governance Policy

Brand Specialist:

* Brand & Content Guidelines

Other specialists rely primarily on structured Excel data.

This separation reduces orchestration ambiguity.

## Orchestration architecture

### Sequential layer

Execution order:

1. Trigger
2. Intake
3. Specialists
4. Consolidation
5. Risk
6. Validation
7. Remediation / Approval
8. Reporting
9. Notification

Each stage depends on successful completion of the previous stage.

### Parallel layer

After validation, the Supervisor invokes four independent specialists.

All specialists evaluate the same campaign simultaneously from different governance perspectives.

The Supervisor waits for all mandatory results before consolidation.

### Fan-in layer

Specialist outputs are normalized into a common structure containing:

* AssessmentStatus
* EvidenceSummary
* BlockingIssues
* Conditions
* RequiredActions
* RequiredApprover
* Confidence

This enables deterministic consolidation.

## Campaign state architecture

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

State transitions are controlled exclusively by the Supervisor.

## Reassessment architecture

The remediation subsystem preserves successful specialist results.

Only affected domains are reassessed.

Example:

```text
Landing Page Corrected
        |
        v
Asset Specialist
        |
        v
Channel Specialist
        |
        v
Supervisor Recalculation
```

Budget and Brand specialists are not rerun unless their underlying data changes.

Automated reassessment is limited to two cycles.

## Integration architecture

### Excel Online (Business)

Functions:

* campaign retrieval,
* rule retrieval,
* asset retrieval,
* state updates,
* report tracking.

### Word Online (Business)

Generates:

* Campaign Launch Readiness Report.

### Outlook

Sends:

* Ready notification,
* Approval notification,
* Remediation notification,
* Not Ready notification,
* Manual Review notification.

## Failure architecture

### Specialist failure

Supervisor behavior:

* retry once,
* mark insufficient evidence,
* prevent Ready,
* route to Manual Review.

### Word failure

System behavior:

* preserve readiness,
* update Excel,
* record report failure.

### Outlook failure

System behavior:

* preserve readiness,
* preserve report,
* record notification failure.

## Security and governance

The architecture enforces strict responsibility separation.

Supervisor:

* orchestration,
* state,
* final decisions.

Child agents:

* analysis only.

Reporting:

* only after authorization.

Human approvals:

* never fabricated.

Evidence:

* required for all non-Ready outcomes.

## End-to-end execution lifecycle

```text
Pending Campaign
        |
        v
In Assessment
        |
        v
Validation
        |
        v
Parallel Specialists
        |
        v
Risk Analysis
        |
        v
Supervisor Validation
        |
        v
Ready / Approval / Remediation / Not Ready
        |
        v
Reporting
        |
        v
Completed
```

This architecture provides a deterministic, auditable, and scalable implementation of autonomous marketing campaign governance using Microsoft Copilot Studio.
