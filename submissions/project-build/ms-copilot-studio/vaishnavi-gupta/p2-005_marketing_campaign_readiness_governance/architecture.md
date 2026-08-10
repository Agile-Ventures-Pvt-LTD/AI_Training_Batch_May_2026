# Architecture

## Overview
The P2-005 Autonomous Marketing Campaign Launch Readiness & Governance System uses a multi-agent architecture implemented in Microsoft Copilot Studio.

The architecture is centered around a Campaign Readiness Supervisor that coordinates campaign validation, specialist assessments, decision-making, remediation, approvals, reporting, and communication.

## High level architecture

                    ┌──────────────────────┐
                    │   Recurrence Trigger │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌──────────────────────────────┐
              │ Campaign Readiness Supervisor │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Campaign Intake & Validation │
              └──────────────┬───────────────┘
                             │
                      Validation Passed?
                         /          \
                       No            Yes
                       │              │
                       ▼              ▼
                    Stop/Hold   In Assessment
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
                     ▼                ▼                ▼
                 Budget            Brand           Channel
                Specialist       Specialist       Specialist
                     │                │                │
                     └────────────────┼────────────────┘
                                      │
                                      ▼
                              Asset Specialist
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │ Launch Risk & Decision │
                         └────────────┬───────────┘
                                      │
                       ┌──────────────┼──────────────┐
                       │              │              │
                       ▼              ▼              ▼
                    Ready       Remediation      Approval
                       │              │              │
                       │              ▼              │
                       │       Selective           │
                       │       Reassessment        │
                       │              │              │
                       └──────────────┼──────────────┘
                                      │
                                      ▼
                         Supervisor Final Validation
                                      │
                                      ▼
                         Reporting & Communication
                              /               \
                             ▼                 ▼
                       Word Report          Outlook
                             │                 │
                             └────────┬────────┘
                                      ▼
                               Excel Register


## Core Components
### Recurrence Trigger

The recurrence trigger automatically starts the campaign assessment process.

Its responsibilities are:

Retrieve campaign records.
Identify campaigns with CampaignStatus = Pending.
Select the oldest eligible campaign.
Process only one campaign per execution.
Pass the selected campaign to the Supervisor.

The trigger is implemented directly in Microsoft Copilot Studio.

### Campaign Readiness Supervisor

The Supervisor is the central orchestration component.

It is responsible for:

Campaign intake.
Validation.
State management.
Specialist delegation.
Parallel assessment coordination.
Result consolidation.
Risk and readiness decision orchestration.
Remediation handling.
Approval handling.
Selective reassessment.
Final validation.
Reporting and communication authorization.

The Supervisor is the only component responsible for the final readiness classification.

### Specialist Agent Layer

The Supervisor delegates domain-specific work to specialist agents.

### Budget & Commercial Specialist

Evaluates:

Proposed budget.
Approved budget.
Budget variance.
Target CPL.
Required financial approvals.


### Brand & Content Compliance Specialist

Evaluates:

Product naming.
Campaign claims.
Disclaimers.
Brand compliance.
Regulatory sensitivity.
Content approval requirements.


### Channel Readiness Specialist

Evaluates every campaign channel for:

Required assets.
Tracking requirements.
Minimum lead time.
Channel-specific prerequisites.
Channel ownership.


### Asset Readiness Specialist

Evaluates:

Mandatory assets.
Asset availability.
Approval status.
QA status.
Missing or blocking assets.


### Launch Risk & Decision Specialist

Consolidates specialist findings and evaluates:

Blocking issues.
Non-blocking conditions.
Approval requirements.
Timing risks.
Overall campaign risk.

The final classification is validated by the Supervisor.

### Reporting & Communication Specialist

Handles:

Campaign Launch Readiness Report generation.
Stakeholder communication.
Outlook notification after Supervisor approval.


## Data and Integration Layer

The architecture uses external operational tools and knowledge sources.

                 ┌─────────────────────┐
                 │ Microsoft Copilot    │
                 │ Studio               │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   Excel Online        Word Online         Outlook
   (Business)          (Business)
          │
          ▼
 Campaign Requests
 Budget Rules
 Channel Requirements
 Asset Status
 Approval Matrix
 Stakeholders
Excel Online (Business)

Used for operational campaign data, including:

Campaign Requests.
Budget Rules.
Channel Requirements.
Asset Status.
Approval information.
Stakeholder information.
Word Online (Business)

Used to generate the final Campaign Launch Readiness Report.

## Outlook

Used to send stakeholder notifications after the Supervisor authorizes communication.

## Knowledge Layer

The solution uses governance and brand/content knowledge sources.

NovaSphere Marketing Governance Policy

Provides rules for:

Readiness classification.
Budget approval.
Timing.
Assets.
Geography.
Sensitivity.
Reassessment.
Autonomous processing.
NovaSphere Brand & Content Guidelines

Provides rules for:

Product naming.
Claims.
Brand terminology.
Content requirements.
Evidence requirements.
Channel-specific content rules.


## Custom Topic Layer

Three major custom topics support the orchestration.

Campaign Intake & Validation

Performs pre-assessment validation and prevents invalid or duplicate processing.

Remediation & Selective Reassessment

Handles:

Remediation actions.
Corrected data.
Affected-domain identification.
Selective reassessment.
Reassessment limits.
Approval & Finalisation

Handles:

Required approvals.
Approval routing.
Finalisation conditions.
Supervisor return for final validation.


## Orchestration Architecture

The architecture demonstrates multiple orchestration patterns.

Sequential
Trigger
  ↓
Validation
  ↓
Specialist Assessment
  ↓
Risk Decision
  ↓
Final Validation
  ↓
Reporting
  ↓
Communication
Parallel Fan-Out
                 Supervisor
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
    Budget          Brand         Channel
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                    Asset

The Supervisor waits for the required specialist results before continuing.

Hierarchical
Supervisor
    ├── Budget Specialist
    ├── Brand Specialist
    ├── Channel Specialist
    ├── Asset Specialist
    ├── Risk & Decision Specialist
    └── Reporting & Communication Specialist
Conditional

Different conditions route the campaign to:

Approval.
Remediation.
Ready.
Ready with Conditions.
Not Ready.
Manual Review.
Reassessment Loop
Issue Found
    ↓
Remediation
    ↓
Correction
    ↓
Affected Specialist Reassessment
    ↓
Supervisor Recalculation

Automated reassessment is limited to two cycles.

Fallback
Specialist Failure
       ↓
Retry Once
       ↓
Success → Continue
       ↓
Failure
       ↓
Insufficient Evidence / Manual Review


## Campaign State Architecture

Campaign status is maintained throughout the lifecycle.

Pending
   ↓
In Assessment
   ↓
┌───────────────┬─────────────────┐
│               │                 │
▼               ▼                 ▼
Ready      Awaiting Remediation  Awaiting Approval
│               │                 │
│               └───────┬─────────┘
│                       ▼
│                 Reassessment
│                       │
└───────────────────────┘
        │
        ▼
Ready with Conditions
        │
        ▼
Completed

Not Ready and Manual Review are terminal outcomes for the relevant assessment path.

## Final Decision Architecture

The final readiness decision follows the required precedence:

Not Ready
    ↓
Management Approval Required
    ↓
Remediation Required
    ↓
Ready with Conditions
    ↓
Ready

A blocking finding from one specialist cannot be overridden simply because another specialist returns Pass.

For example:

Budget  → Pass
Brand   → Block
Channel → Pass
Asset   → Pass

The campaign cannot be classified as Ready.

## Failure Handling

The architecture provides controlled handling for:

Missing campaign data.
Duplicate campaigns.
Excel failures.
Specialist failures.
Missing evidence.
Word report failures.
Outlook failures.
Unsuccessful remediation.
Unresolved approvals.

The system must not claim successful completion when an underlying tool operation fails.

## End-to-End Architecture

The complete architecture can therefore be summarized as:

             ┌────────────────────┐
             │ Recurrence Trigger │
             └─────────┬──────────┘
                       ▼
             ┌────────────────────┐
             │     Supervisor     │
             └─────────┬──────────┘
                       ▼
             ┌────────────────────┐
             │ Intake & Validation│
             └─────────┬──────────┘
                       ▼
             ┌────────────────────┐
             │ Mark In Assessment │
             └─────────┬──────────┘
                       ▼
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Budget          Brand          Channel
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                     Asset
                       │
                       ▼
             ┌────────────────────┐
             │ Risk & Decision    │
             └─────────┬──────────┘
                       ▼
              Conditional Routing
                 /     |      \
                /      |       \
               ▼       ▼        ▼
            Ready   Remediate  Approval
               \      |        /
                \     |       /
                 ▼    ▼      ▼
              Final Supervisor
                  Validation
                       │
                       ▼
             Reporting & Communication
                 /             \
                ▼               ▼
             Word Report      Outlook
                │               │
                └───────┬───────┘
                        ▼
                  Excel Register

This architecture provides the required separation of responsibilities, controlled orchestration, governance enforcement, exception handling, and autonomous campaign-readiness assessment defined for P2-005.