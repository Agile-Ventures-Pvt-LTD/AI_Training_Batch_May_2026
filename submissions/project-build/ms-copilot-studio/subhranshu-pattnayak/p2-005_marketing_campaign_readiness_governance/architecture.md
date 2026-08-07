# Architecture.md

## Solution Architecture

### Overview

The Campaign Launch Readiness Orchestrator uses a Supervisor-Agent architecture implemented in Microsoft Copilot Studio.

The architecture separates orchestration responsibilities from specialist assessment responsibilities to ensure governance-driven, consistent, and scalable campaign readiness reviews.

The Supervisor controls the overall workflow while specialist agents evaluate specific readiness domains.

---

## High-Level Architecture

```text
Campaign Request
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Campaign Readiness Supervisor
        │
        ├───────────────────────────────────────────────────────────────┐
        │                                                               │
        ▼                                                               │
Parallel Specialist Assessments                                         │
        │                                                               │
        ├─ Budget & Commercial Specialist                               │
        ├─ Brand & Content Compliance Specialist                        │
        ├─ Channel Readiness Specialist                                 │
        └─ Asset Readiness Specialist                                   │
        │                                                               │
        ▼                                                               │
Launch Risk & Decision Specialist                                       │
        │                                                               │
        ▼                                                               │
Approval & Escalation                                                   │
        │                                                               │
        ▼                                                               │
Remediation & Selective Reassessment                                    │
        │                                                               │
        ▼                                                               │
Final Readiness Determination                                           │
        │                                                               │
        ▼                                                               │
Reporting & Communication Specialist                                    │
        │                                                               │
        └───────────────────────────────────────────────────────────────┘
        │
        ▼
Update Excel with Final Readiness Status
        │
        ▼
       END
```

---

# Architectural Principles

The solution is based on the following principles:

### Separation of Responsibilities

The Supervisor coordinates assessments.

Specialists perform domain-specific analysis.

No specialist is allowed to assign final readiness status.

---

### Governance-Driven Decisions

All final readiness decisions must comply with:

- Governance Policy
- Approval requirements
- Escalation requirements
- Risk assessment outcomes

Governance Policy acts as the authoritative source.

---

### Parallel Specialist Orchestration

Independent readiness domains are evaluated simultaneously.

This reduces assessment time and improves scalability.

Parallel specialists:

- Budget & Commercial
- Brand & Content Compliance
- Channel Readiness
- Asset Readiness

---

### Controlled Reassessment Looping

Only affected domains are reassessed.

Reassessment cycles are limited.

This prevents infinite remediation loops.

---

# Component Architecture

## 1. Campaign Intake & Validation Topic

### Purpose

Acts as the system entry point.

Validates campaign readiness inputs before specialist assessment begins.

---

### Responsibilities

Validate:

- Campaign existence
- Mandatory fields
- Launch date
- Budget information
- Geography
- Channels
- Campaign ownership

---

### Outputs

Produces:

- Validation Status
- Campaign Metadata
- Days To Launch
- Budget Variance
- Campaign Context

---

### Failure Behavior

If validation fails:

```text
Stop Assessment and go straight to update status in Excel.
```

No specialist agents are invoked.

---

## 2. Campaign Readiness Supervisor

### Purpose

Acts as the orchestration layer.

Coordinates the complete readiness workflow.

---

### Responsibilities

- Intake coordination
- Specialist orchestration
- Assessment consolidation
- Approval routing
- Remediation management
- Governance application
- Final readiness determination
- Reporting initiation

---

### Decision Authority

Only the Supervisor may assign:

```text
Final Readiness Status
```

---

## 3. Budget & Commercial Specialist

### Purpose

Evaluate commercial and budget readiness.

---

### Data Sources

- Campaign Requests
- Budget Rules
- Approval Matrix

---

### Responsibilities

Evaluate:

- Proposed Budget
- Approved Budget
- Budget Variance
- CPL Targets
- Expected Leads
- Approval Requirements
- Financial Blockers

---

### Outputs

Returns:

- Assessment Status
- Budget Findings
- Approval Requirements
- Blocking Issues
- Evidence

---

## 4. Brand & Content Compliance Specialist

### Purpose

Evaluate campaign content compliance.

---

### Knowledge Source

Mandatory:

```text
NovaSphere Brand & Content Guidelines
```

---

### Responsibilities

Evaluate:

- Product Naming
- Campaign Claims
- Regulatory Sensitivity
- Disclaimers
- Brand Approval Requirements
- Restricted Claims
- Unsupported Claims
- CTA Consistency

---

### Outputs

Returns:

- Compliance Findings
- Required Approvals
- Blocking Issues
- Evidence

---

## 5. Channel Readiness Specialist

### Purpose

Evaluate launch channel readiness.

---

### Data Sources

- Campaign Requests
- Channel Requirements
- Asset Status

---

### Responsibilities

Evaluate:

- Required Assets
- Tracking Requirements
- Lead Times
- Channel Ownership
- Launch Prerequisites
- Channel Blockers

---

### Outputs

Returns:

- Readiness Findings
- Missing Prerequisites
- Blocking Issues
- Evidence

---

## 6. Asset Readiness Specialist

### Purpose

Evaluate asset readiness.

---

### Data Sources

- Asset Status
- Campaign Requests

---

### Responsibilities

Evaluate:

- Asset Availability
- Asset Approval Status
- Pending QA
- Missing Assets
- Required Changes

---

### Asset Classifications

Assets are classified as:

```text
Ready
Condition
Blocking
Missing
```

---

### Outputs

Returns:

- Asset Findings
- Aggregate Counts
- Blocking Issues
- Evidence

---

## 7. Launch Risk & Decision Specialist

### Purpose

Evaluate overall campaign launch risk.

---

### Inputs

Receives:

- Budget Results
- Brand Results
- Channel Results
- Asset Results
- Geography
- Sensitivity
- Days To Launch
- Pending Approvals

---

### Responsibilities

Identify:

- Timing Risk
- Approval Risk
- Readiness Risk
- Blocking Issues
- Unresolved Evidence

---

### Risk Levels

```text
Low
Medium
High
Critical
```

---

### Outputs

Returns:

- Risk Classification
- Proposed Outcome
- Risk Findings

---

### Limitation

The proposed outcome is advisory only.

Final readiness determination remains the responsibility of the Supervisor.

---

## 8. Approval & Escalation Topic

### Purpose

Determine whether mandatory approvals are required.

---

### Responsibilities

Evaluate:

- Budget Thresholds
- CPL Thresholds
- Regulatory Sensitivity
- Specialist Approval Requests

---

### Outputs

Returns:

- Approval Required
- Required Approver
- Approval Reason
- Finalisation Status

---

## 9. Remediation & Selective Reassessment Topic

### Purpose

Manage reassessment eligibility.

---

### Responsibilities

Determine:

- Whether reassessment is allowed
- Which specialist requires reassessment
- Whether manual review is required

---

### Reassessment Logic

Maximum reassessment cycles:

```text
2
```

After second unsuccessful reassessment:

```text
Manual Review Required
```

---

### Outputs

Returns:

- Reassessment Allowed
- Domains To Reassess
- Remediation Status

---

## 10. Reporting & Communication Specialist

### Purpose

Generate readiness documentation and notifications.

---

### Responsibilities

Generate:

- Campaign Launch Readiness Report
- Stakeholder Notifications
- Readiness Summary
- Recommended Actions

---

### Report Contents

Include:

- Campaign Information
- Risk Classification
- Readiness Status
- Blocking Issues
- Conditions
- Required Approvals
- Recommended Actions

---

# Assessment Flow

## Stage 1

Campaign Intake & Validation

---

## Stage 2

Parallel Specialist Assessment

- Budget Specialist
- Brand Specialist
- Channel Specialist
- Asset Specialist

---

## Stage 3

Assessment Consolidation

Supervisor consolidates findings.

---

## Stage 4

Launch Risk Assessment

Launch Risk & Decision Specialist executes.

---

## Stage 5

Approval Evaluation

Approval & Escalation Topic executes.

---

## Stage 6

Remediation & Reassessment

Affected specialists may be reassessed.

---

## Stage 7

Final Readiness Determination

Supervisor applies:

- Governance Policy
- Approval Outcomes
- Risk Findings
- Specialist Findings
- Remediation Outcomes

---

## Stage 8

Reporting & Communication

Final outputs are generated.

---

# Final Readiness Determination

The Supervisor applies the following precedence order:

```text
1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready With Conditions
5. Ready
```

Highest-precedence outcome always wins.

Specialist results are never averaged.

---

# Technology Architecture

## Platform

Microsoft Copilot Studio

---

## Data Layer

Excel Online (Business)

Tables:

- Campaign Requests
- Budget Rules
- Approval Matrix
- Channel Requirements
- Asset Status

---

## Knowledge Layer

Knowledge Sources:

- Governance Policy
- NovaSphere Brand & Content Guidelines

---

## Integration Layer

- Excel Online (Business)
- Word Online (Business)
- Outlook
- OneDrive

---

## AI Layer

- Campaign Readiness Supervisor
- Six Specialist Agents
- Three Supporting Topics

---