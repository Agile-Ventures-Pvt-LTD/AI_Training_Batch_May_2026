# Architecture

## Project Name

**Marketing Campaign Readiness Governance**

---

# Solution Architecture Overview

The Marketing Campaign Readiness Governance solution is implemented using a **Supervisor–Specialist Multi-Agent Architecture** in Microsoft Copilot Studio.

The architecture separates orchestration responsibilities from domain-specific evaluations by introducing a central supervisor agent that coordinates multiple specialist agents.

This design improves modularity, scalability, maintainability, and allows each agent to focus on a single business capability.

---

# High-Level Architecture

```
                           ┌─────────────────────────────┐
                           │  Scheduled Trigger          │
                           │ (Autonomous Execution)      │
                           └──────────────┬──────────────┘
                                          │
                                          ▼
                    ┌────────────────────────────────────┐
                    │ Campaign Readiness Supervisor      │
                    └────────────────────────────────────┘
                                      │
                 ┌────────────────────┼─────────────────────┐
                 │                    │                     │
                 ▼                    ▼                     ▼
        Topic 1                 Specialist Agents       Topic 2
Campaign Intake & Validation                         Remediation &
                                                    Selective Reassessment
                 │                    │                     │
                 │                    ▼                     │
                 │         Budget & Commercial              │
                 │         Brand & Compliance               │
                 │         Asset Readiness                  │
                 │         Channel Readiness                │
                 │         Launch Risk                      │
                 │         Reporting                        │
                 │                    │                     │
                 └────────────────────┼─────────────────────┘
                                      │
                                      ▼
                         Topic 3 – Approval & Finalisation
                                      │
                                      ▼
                             Final Readiness Decision
                                      │
                                      ▼
                             Excel Status Update
```

---

# Architectural Principles

The implementation follows the following design principles:

- Separation of Responsibilities
- Modular Agent Design
- Deterministic Validation
- Sequential Orchestration
- Reusable Specialist Agents
- Enterprise Governance
- Human Approval Integration

---

# Supervisor Agent

The Campaign Readiness Supervisor is the central orchestrator.

Responsibilities include:

- Receiving campaign requests
- Triggering validation
- Coordinating specialist agents
- Managing remediation
- Managing approval workflow
- Determining final readiness
- Updating campaign status

The supervisor **does not perform specialist evaluations itself**.

---

# Specialist Agent Layer

Six specialist agents perform independent domain assessments.

| Agent | Responsibility |
|---------|----------------|
| Budget & Commercial Specialist | Budget validation and commercial readiness |
| Brand & Content Compliance Specialist | Brand compliance and regulatory validation |
| Asset Readiness Specialist | Creative assets and landing page readiness |
| Channel Readiness Specialist | Marketing channel validation |
| Launch Risk & Decision Specialist | Operational risk assessment |
| Reporting & Communication Specialist | Reporting and campaign summary |

Each specialist evaluates only its assigned business domain.

---

# Custom Topic Layer

Three mandatory custom topics implement workflow governance.

## Topic 1

Campaign Intake & Validation

Responsibilities:

- Campaign validation
- Mandatory field verification
- Duplicate prevention
- Initial status update

---

## Topic 2

Remediation & Selective Reassessment

Responsibilities:

- Detect remediation
- Preserve passed assessments
- Rerun failed specialists
- Manual Review escalation

---

## Topic 3

Approval & Finalisation

Responsibilities:

- Evaluate approval conditions
- Awaiting Approval workflow
- Human approval enforcement
- Final campaign status

---

# Data Layer

The implementation stores campaign information in:

**Excel Online (Business)**

Primary table:

```
CampaignRequestsTable
```

Important fields include:

- CampaignID
- CampaignName
- Product
- CampaignStatus
- ProposedBudget
- ApprovedBudget
- TargetCPL
- Geography
- RegulatorySensitivity
- CampaignOwner

---

# Data Flow

```
Campaign Request
        │
        ▼
Excel Table
        │
        ▼
Campaign Intake Validation
        │
        ▼
Validated Campaign
        │
        ▼
Specialist Assessments
        │
        ▼
Approval / Remediation
        │
        ▼
Final Readiness
        │
        ▼
Campaign Status Updated
```

---

# Orchestration Flow

```
Start

↓

Topic 1

↓

Budget Specialist

↓

Brand Specialist

↓

Asset Specialist

↓

Channel Specialist

↓

Launch Risk Specialist

↓

Reporting Specialist

↓

Topic 2 (If Required)

↓

Topic 3 (If Required)

↓

Ready Decision

↓

Update Excel

↓

End
```

---

# Approval Workflow

When any mandatory approval rule is triggered:

- Campaign Status becomes **Awaiting Approval**
- Ready status is blocked
- Human approval is required
- Campaign returns to the Supervisor after approval

---

# Remediation Workflow

When one or more specialist assessments fail:

- Campaign Status becomes **Awaiting Remediation**
- Failed specialist domains are identified
- Only affected specialists are reassessed
- Maximum of two automated reassessment cycles
- Manual Review after two unsuccessful attempts

---

# Final Readiness Decision

The solution follows the mandatory precedence defined in the project requirements.

Priority:

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

The supervisor always returns the highest-priority outcome.

---

# Benefits of the Architecture

- Modular implementation
- High maintainability
- Easy scalability
- Independent specialist agents
- Enterprise governance
- Reduced duplicate processing
- Human approval support
- Automated campaign lifecycle

---

# Conclusion

The Marketing Campaign Readiness Governance solution adopts a scalable Supervisor–Specialist architecture that combines deterministic validation, multi-agent collaboration, approval workflows, remediation management, and automated orchestration to provide a robust enterprise campaign governance platform.