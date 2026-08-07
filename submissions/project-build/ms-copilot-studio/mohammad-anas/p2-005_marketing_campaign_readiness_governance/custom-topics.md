# Custom Topics

## Overview

The Campaign Readiness Governance System uses custom workflow topics to modularize the campaign readiness assessment process.

Each topic is responsible for a single workflow stage and is invoked by the Campaign Readiness Supervisor at the appropriate point in the assessment lifecycle.

This modular design improves maintainability, simplifies debugging, enables workflow reuse, and ensures clear separation of responsibilities.

---

# Topic Architecture

```
Campaign Readiness Supervisor
            │
            ▼
Campaign Intake & Validation
            │
            ▼
Specialist Assessment
            │
            ▼
Launch Risk & Decision
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
Remediation   Approval
     │             │
     └──────┬──────┘
            ▼
Reporting & Communication
```

---

# Topic 1 – Campaign Intake & Validation

## Purpose

Retrieve the next campaign requiring assessment and validate that sufficient business information exists before specialist evaluation begins.

## Responsibilities

- Retrieve campaign requests
- Identify the oldest campaign with **CampaignStatus = Pending**
- Retrieve the complete campaign record
- Validate mandatory campaign information
- Prevent assessment when required information is missing

## Input

None

## Output

- Campaign ID
- Campaign Name
- Campaign Owner
- Campaign Status
- Validation Status
- Completion Status

---

# Topic 2 – Specialist Assessment

## Purpose

Coordinate all mandatory specialist assessments required for campaign readiness evaluation.

## Responsibilities

- Invoke Budget & Commercial Specialist
- Invoke Brand & Content Compliance Specialist
- Invoke Channel Readiness Specialist
- Invoke Asset Readiness Specialist
- Wait for specialist completion
- Consolidate specialist findings

## Input

Validated campaign information

## Output

- Budget Assessment
- Brand Assessment
- Channel Assessment
- Asset Assessment
- Consolidated Specialist Findings

---

# Topic 3 – Launch Risk & Decision

## Purpose

Coordinate launch risk evaluation and determine whether additional workflow stages are required.

## Responsibilities

- Invoke Launch Risk & Decision Specialist
- Validate proposed readiness
- Determine overall campaign risk
- Decide whether remediation is required
- Decide whether management approval is required

## Input

Consolidated specialist findings

## Output

- Proposed Readiness
- Risk Level
- Required Actions
- Remediation Required
- Approval Required

---

# Topic 4 – Remediation & Selective Reassessment

## Purpose

Coordinate reassessment activities for campaigns requiring remediation.

## Responsibilities

- Update campaign status
- Identify affected assessment domains
- Invoke only required specialist agents
- Return updated assessment results

## Input

Remediation recommendations

## Output

- Updated specialist findings
- Updated readiness recommendation

---

# Topic 5 – Approval Finalisation

## Purpose

Coordinate mandatory approval activities before campaign launch.

## Responsibilities

- Identify required approver
- Process approval workflow
- Record approval outcome
- Return approval status

## Input

Campaign readiness recommendation

## Output

- Approval Status
- Required Approver
- Approval Comments

---

# Topic 6 – Reporting & Communication

## Purpose

Generate campaign readiness deliverables after Supervisor authorization.

## Responsibilities

- Generate Campaign Readiness Report
- Prepare Outlook notification
- Send stakeholder notification
- Update campaign lifecycle status

## Input

Final readiness decision

## Output

- Report Status
- Notification Status
- Generated Document Reference
- Completion Status

---

# Topic Execution Sequence

The topics execute in the following order:

1. Campaign Intake & Validation
2. Specialist Assessment
3. Launch Risk & Decision
4. Remediation & Selective Reassessment (Conditional)
5. Approval Finalisation (Conditional)
6. Reporting & Communication

Each topic completes its assigned responsibilities before control returns to the Campaign Readiness Supervisor.

---

# Design Principles

The custom topics follow these principles:

- Single Responsibility
- Sequential Workflow Execution
- Modular Design
- Reusability
- Clear Input and Output Contracts
- Supervisor-Controlled Execution
- Enterprise Governance
- Traceable Workflow Stages

---

# Benefits

The use of custom topics provides:

- Improved workflow organization
- Easier maintenance
- Simplified testing and debugging
- Reusable workflow components
- Better scalability
- Reduced orchestration complexity
- Clear separation between orchestration and business logic
- Consistent execution across campaign assessments