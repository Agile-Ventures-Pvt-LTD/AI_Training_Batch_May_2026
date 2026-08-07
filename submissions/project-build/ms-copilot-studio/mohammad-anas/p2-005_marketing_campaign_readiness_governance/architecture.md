# System Architecture

## Overview

The Campaign Readiness Governance System is an autonomous multi-agent solution implemented using Microsoft Copilot Studio.

The architecture follows a Supervisor–Specialist pattern in which a single Supervisor Agent coordinates the complete campaign readiness assessment while delegating domain-specific responsibilities to dedicated specialist child agents.

The solution also integrates Microsoft 365 services for business data retrieval, report generation, and stakeholder communication.

---

# High-Level Architecture

```
                    Recurrence Trigger
                            │
                            ▼
          Campaign Readiness Supervisor
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Campaign Intake      Specialist          Launch Risk &
 Validation Topic    Assessment Topic    Decision Topic
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Budget &            Brand & Content      Channel
 Commercial          Compliance           Readiness
 Specialist          Specialist           Specialist
                            │
                            ▼
                 Asset Readiness Specialist
                            │
                            ▼
             Launch Risk & Decision Specialist
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
     Remediation Topic        Approval Topic
                │                       │
                └───────────┬───────────┘
                            ▼
        Reporting & Communication Topic
                            │
                            ▼
        Reporting & Communication Specialist
                            │
                            ▼
                  Update Campaign Status
                            │
                            ▼
                       Workflow Ends
```

---

# Architecture Components

## 1. Recurrence Trigger

The workflow is initiated automatically using a Recurrence Trigger.

Responsibilities:

- Monitor execution schedule
- Automatically invoke the Supervisor
- Eliminate manual execution
- Process one campaign per execution

---

## 2. Campaign Readiness Supervisor

The Campaign Readiness Supervisor is the central orchestration component.

Responsibilities include:

- Workflow orchestration
- Campaign state management
- Topic invocation
- Child agent coordination
- Assessment consolidation
- Conflict resolution
- Governance validation
- Final readiness decision
- Report authorization
- Communication authorization

The Supervisor does not perform domain-specific assessments.

---

## 3. Workflow Topics

The implementation divides the workflow into modular execution stages.

### Campaign Intake & Validation

Responsible for:

- Retrieving campaign requests
- Selecting the oldest pending campaign
- Validating campaign completeness

---

### Specialist Assessment

Responsible for:

- Invoking mandatory specialist agents
- Coordinating specialist execution
- Returning consolidated assessment results

---

### Launch Risk & Decision

Responsible for:

- Invoking the Launch Risk Specialist
- Validating readiness recommendations
- Determining whether remediation or approvals are required

---

### Remediation & Selective Reassessment

Responsible for:

- Coordinating reassessment activities
- Executing only required reassessments
- Returning updated assessment findings

---

### Approval Finalisation

Responsible for:

- Managing mandatory approval workflow
- Recording approval outcomes

---

### Reporting & Communication

Responsible for:

- Coordinating report generation
- Preparing stakeholder communication
- Updating campaign status

---

# Specialist Agents

## Budget & Commercial Specialist

Business Domain:

Financial governance

Responsibilities:

- Budget validation
- Budget variance analysis
- Commercial readiness
- Approval requirements
- Target CPL validation

---

## Brand & Content Compliance Specialist

Business Domain:

Marketing compliance

Responsibilities:

- Brand compliance
- Product naming
- Campaign claims
- Regulatory sensitivity
- CTA validation
- Disclaimer validation

---

## Channel Readiness Specialist

Business Domain:

Operational readiness

Responsibilities:

- Channel validation
- Tracking readiness
- Operational dependencies
- Lead time assessment
- Channel blockers

---

## Asset Readiness Specialist

Business Domain:

Creative asset governance

Responsibilities:

- Asset availability
- Asset approvals
- QA status
- Missing assets
- Production readiness

---

## Launch Risk & Decision Specialist

Business Domain:

Risk analysis

Responsibilities:

- Consolidate specialist findings
- Risk classification
- Proposed readiness outcome

---

## Reporting & Communication Specialist

Business Domain:

Business communication

Responsibilities:

- Report generation
- Outlook notification
- Stakeholder communication

---

# Microsoft 365 Integration

## Excel Online (Business)

Used for:

- Campaign Requests
- Budget Rules
- Approval Matrix
- Asset Status
- Channel Requirements
- Campaign Status Updates

---

## Word Online (Business)

Used for:

- Campaign Readiness Report generation

---

## Office 365 Outlook

Used for:

- Draft email generation
- Stakeholder notification

---

# Knowledge Sources

The architecture incorporates enterprise knowledge sources.

## NovaSphere Marketing Governance Policy

Provides:

- Readiness policies
- Approval rules
- Budget governance
- Operational controls
- Campaign governance standards

---

## NovaSphere Brand & Content Guidelines

Provides:

- Product naming standards
- Brand terminology
- Regulatory requirements
- Claims validation
- CTA standards
- Content governance

---

# Data Flow

1. Recurrence Trigger initiates execution.
2. Campaign Intake retrieves and validates campaign information.
3. Specialist Assessment coordinates domain-specific evaluations.
4. Launch Risk consolidates specialist findings.
5. Remediation executes if required.
6. Approval workflow executes if required.
7. Reporting generates campaign documentation.
8. Campaign status is updated.
9. Workflow completes.

---

# Design Principles

The architecture follows the following principles:

- Separation of Responsibilities
- Modular Workflow Design
- Autonomous Orchestration
- Policy-Driven Decision Making
- Single Supervisor Coordination
- Specialist Domain Isolation
- Microsoft 365 Integration
- Enterprise Governance
- Traceable Decision Making
- Reusable Workflow Components

---

# Benefits

The architecture provides:

- Autonomous campaign governance
- Consistent readiness assessments
- Modular workflow execution
- Reusable specialist agents
- Improved maintainability
- Enterprise scalability
- Clear separation of responsibilities
- Reduced operational complexity
- Improved governance compliance
- End-to-end traceability