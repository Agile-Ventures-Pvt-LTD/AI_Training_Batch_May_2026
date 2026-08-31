# Architecture

## 1. High-Level Architecture

```text
                    +----------------------+
                    | Recurrence Trigger   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Intake & Validation  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Campaign Readiness   |
                    | Supervisor            |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
        Budget Agent     Brand Agent      Channel Agent
              |                |                |
              +----------------+----------------+
                               |
                               v
                         Asset Agent
                               |
                               v
                    +----------------------+
                    | Fan-In Consolidation  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Launch Risk &         |
                    | Decision Specialist   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Supervisor Final      |
                    | Decision              |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       Remediation Topic              Approval Topic
                |                             |
                +--------------+--------------+
                               |
                               v
                    Supervisor Validation
                               |
                               v
              Reporting & Communication Agent
                        /              \
                       v                v
                    Word             Outlook
                       \                /
                        +------ Excel -+
```

## 2. Autonomous Trigger

A Copilot Studio Recurrence event trigger starts the process.

For each trigger:

1. Retrieve campaign requests from Excel.
2. Find campaigns with `CampaignStatus = Pending`.
3. Select the oldest eligible Pending campaign.
4. Process one campaign per trigger.
5. Update the campaign state before specialist analysis.

No separate Power Automate workflow is required by the PRD.

## 3. Supervisor Layer

The Supervisor controls:

- Campaign state
- Intake validation
- Child-agent invocation
- Fan-out/fan-in
- Conflict resolution
- Reassessment
- Approval routing
- Final readiness
- Word generation authorisation
- Outlook communication authorisation

## 4. Specialist Layer

The first four domain specialists perform independent assessments:

```text
Budget
Brand
Channel
Asset
```

Their results are consolidated before Launch Risk assessment.

## 5. Sequential Stage

The Launch Risk Specialist runs after the first four specialist results are available.

The Reporting & Communication Specialist runs only after Supervisor validation.

## 6. State Model

The required campaign states are:

- Pending
- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Ready with Conditions
- Ready
- Not Ready
- Manual Review
- Completed

Invalid state progression must be prevented.

For example:

```text
Pending → Ready
```

without assessment is not allowed.

## 7. Tool Layer

| Component | Main Capability |
|---|---|
| Supervisor | Orchestration and campaign-state control |
| Budget Specialist | Excel financial/rule data |
| Brand Specialist | Brand knowledge + campaign/asset data |
| Channel Specialist | Excel channel requirements |
| Asset Specialist | Excel asset status |
| Risk Specialist | Consolidated specialist outputs |
| Reporting Specialist | Word + Outlook |

Tools should not be exposed indiscriminately to every child agent.

## 8. Knowledge Layer

The Governance Policy is authoritative for readiness, approval, timing, assets, geography, sensitivity, autonomous processing, and reassessment.

The Brand & Content Guidelines are authoritative for brand/content compliance.

## 9. Final Decision

Only the Supervisor assigns the final readiness outcome.
