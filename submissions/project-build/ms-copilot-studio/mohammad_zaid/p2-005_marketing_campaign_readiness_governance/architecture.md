
# System Architecture

# 1. Introduction

The Autonomous Marketing Campaign Launch Readiness & Governance System is designed using Microsoft Copilot Studio's hierarchical multi-agent architecture. The solution follows Microsoft's recommended orchestration model in which a parent Supervisor Agent coordinates multiple specialist child agents, consolidates their outputs, applies governance policies, and authorizes the final campaign readiness decision.

The architecture combines autonomous event triggers, structured agent delegation, sequential orchestration, parallel specialist assessments, conditional routing, remediation workflows, approval handling, Microsoft 365 integrations, and enterprise knowledge grounding to automate campaign readiness assessment while maintaining governance and human oversight.

---

# 2. High-Level Architecture

```text
                           Recurrence Trigger
                                   │
                                   ▼
                  Campaign Readiness Supervisor
                                   │
                    Campaign Intake & Validation
                                   │
                      Campaign Successfully Validated?
                           │                     │
                          No                    Yes
                           │                     │
                    Reject / Hold       Mark In Assessment
                                                │
                ┌────────────────────────────────────────────────┐
                │                                                │
                ▼                                                ▼
 Budget & Commercial Specialist             Brand & Content Compliance Specialist
                │                                                │
                └───────────────────────┬────────────────────────┘
                                        │
                                        ▼
                          Channel Readiness Specialist
                                        │
                                        ▼
                          Asset Readiness Specialist
                                        │
                                        ▼
                         Supervisor Fan-In Consolidation
                                        │
                                        ▼
                     Launch Risk & Decision Specialist
                                        │
                     ┌──────────────────┼──────────────────┐
                     ▼                  ▼                  ▼
                 Ready          Remediation Required   Approval Required
                     │                  │                  │
                     │                  ▼                  ▼
                     │     Remediation &            Approval &
                     │ Selective Reassessment      Finalisation
                     │                  │                  │
                     └──────────────────┴──────────────────┘
                                        │
                                        ▼
                          Campaign Readiness Supervisor
                              Final Validation
                                        │
                                        ▼
                  Reporting & Communication Specialist
                          │                    │
                          ▼                    ▼
               Microsoft Word          Microsoft Outlook
                    Report              Notification
                          │                    │
                          └────────────┬───────┘
                                       ▼
                           Microsoft Excel Update
```

---

# 3. Architectural Principles

The solution follows the following architectural principles:

- Hierarchical multi-agent orchestration.
- Single Supervisor ownership.
- Independent specialist responsibilities.
- Sequential workflow execution.
- Parallel fan-out / fan-in assessment.
- Conditional routing.
- Governance-driven decision making.
- Enterprise knowledge grounding.
- State-based campaign management.
- Failure-aware orchestration.

---

# 4. Parent Agent

## Campaign Readiness Supervisor

The Campaign Readiness Supervisor is the central orchestration component of the solution.

Responsibilities include:

- Autonomous campaign discovery.
- Campaign intake validation.
- Campaign state management.
- Child-agent orchestration.
- Fan-out coordination.
- Fan-in consolidation.
- Governance policy enforcement.
- Conflict resolution.
- Final readiness validation.
- Approval routing.
- Remediation routing.
- Reporting authorization.
- Communication authorization.

The Supervisor is the only component permitted to assign the final campaign readiness outcome.

---

# 5. Specialist Child Agents

The solution contains six specialist child agents.

## Budget & Commercial Specialist

Responsible for:

- Budget assessment.
- Commercial validation.
- Budget variance.
- Financial approvals.
- Commercial blocking conditions.

---

## Brand & Content Compliance Specialist

Responsible for:

- Brand compliance.
- Product naming.
- Regulatory claims.
- Disclaimers.
- Brand approval.
- Content governance.

---

## Channel Readiness Specialist

Responsible for:

- Channel readiness.
- Channel prerequisites.
- Tracking validation.
- Lead-time validation.
- Channel ownership.

---

## Asset Readiness Specialist

Responsible for:

- Mandatory assets.
- Asset approval.
- Asset quality.
- Missing assets.
- Asset classification.

---

## Launch Risk & Decision Specialist

Responsible for:

- Campaign risk evaluation.
- Blocking issue analysis.
- Approval identification.
- Risk classification.
- Readiness recommendation.

This specialist proposes the readiness outcome, which is subsequently validated by the Supervisor.

---

## Reporting & Communication Specialist

Responsible for:

- Microsoft Word report generation.
- Microsoft Outlook notification.
- Communication status.
- Reporting completion.

The Reporting & Communication Specialist executes only after Supervisor validation.

---

# 6. Custom Topics

Three custom Topics support the architecture.

## Campaign Intake & Validation

Performs deterministic validation before specialist assessment.

Primary responsibilities include:

- Campaign validation.
- Duplicate prevention.
- Mandatory field validation.
- Campaign state update.

---

## Remediation & Selective Reassessment

Coordinates corrective actions when blocking findings are identified.

Responsibilities include:

- Remediation coordination.
- Specialist reassessment.
- Reassessment loop control.
- Supervisor re-entry.

---

## Approval & Finalisation

Handles campaigns requiring mandatory human approval.

Responsibilities include:

- Approval routing.
- Approval recording.
- Campaign state update.
- Supervisor return.

---

# 7. Microsoft 365 Integration

The architecture integrates with Microsoft 365 services.

## Microsoft Excel Online (Business)

Used for:

- Campaign retrieval.
- Rule retrieval.
- Asset retrieval.
- Stakeholder retrieval.
- Campaign state updates.

---

## Microsoft Word Online (Business)

Used for:

- Campaign Launch Readiness Report generation.

---

## Microsoft Outlook

Used for:

- Stakeholder notification.
- Final readiness communication.

---

# 8. Knowledge Architecture

Knowledge is distributed according to business responsibility.

| Agent                         | Knowledge Source                       |
| ----------------------------- | -------------------------------------- |
| Campaign Readiness Supervisor | NovaSphere Marketing Governance Policy |
| Budget Specialist             | Governance Policy + Budget Data        |
| Brand Specialist              | Brand & Content Guidelines             |
| Channel Specialist            | Channel Requirements                   |
| Asset Specialist              | Asset Status                           |
| Launch Risk Specialist        | Specialist Findings + Governance Rules |
| Reporting Specialist          | Final Validated Assessment             |

Knowledge is intentionally scoped to minimize unnecessary context and improve orchestration accuracy.

---

# 9. Campaign State Model

The solution maintains the following campaign lifecycle.

```text
Pending
    │
    ▼
In Assessment
    │
    ├──────────────► Awaiting Remediation
    │                        │
    │                        ▼
    │                 Reassessment
    │                        │
    ├──────────────► Awaiting Approval
    │                        │
    ▼                        ▼
Ready with Conditions      Ready
            │
            ▼
        Completed

Alternative Paths

Not Ready
Manual Review
```

The Supervisor controls all campaign state transitions to ensure governance compliance and prevent invalid progression.

---

# 10. Failure Handling

The architecture incorporates controlled failure handling.

When a specialist:

- Fails to respond.
- Returns insufficient evidence.
- Cannot access required data.

The Supervisor:

- Retries the specialist once.
- Marks the affected domain as insufficient evidence if the retry fails.
- Prevents unsupported Ready classifications.
- Routes the campaign to Manual Review where required.

---

# 11. Design Summary

The architecture combines autonomous triggers, hierarchical orchestration, specialist delegation, enterprise knowledge, Microsoft 365 connectors, governance enforcement, and structured campaign lifecycle management to provide a scalable, explainable, and policy-driven campaign launch readiness solution using Microsoft Copilot Studio.
