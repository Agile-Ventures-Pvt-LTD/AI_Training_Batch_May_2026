# Orchestration Patterns

## Overview

The Campaign Readiness Governance System follows a Supervisor–Specialist orchestration pattern implemented using Microsoft Copilot Studio.

The solution separates orchestration logic from business analysis by assigning workflow coordination to the Campaign Readiness Supervisor while delegating domain-specific responsibilities to specialist child agents.

This architecture provides modularity, scalability, governance, and maintainability.

---

# Orchestration Model

The implementation follows the workflow below.

```
Recurrence Trigger
        │
        ▼
Campaign Readiness Supervisor
        │
        ▼
Campaign Intake & Validation Topic
        │
        ▼
Specialist Assessment Topic
        │
        ▼
Launch Risk & Decision Topic
        │
        ├──────────────┐
        │              │
        ▼              ▼
Remediation      Approval
Topic            Topic
        │              │
        └──────┬───────┘
               ▼
Reporting & Communication Topic
               │
               ▼
Campaign Status Update
               │
               ▼
Workflow Complete
```

---

# Supervisor Orchestration

The Campaign Readiness Supervisor coordinates the complete workflow.

Its responsibilities include:

- Initiating workflow execution
- Invoking workflow topics
- Managing campaign lifecycle state
- Coordinating specialist agents
- Consolidating assessment findings
- Resolving conflicting specialist outputs
- Applying governance policies
- Determining the final readiness decision
- Authorizing reporting
- Updating campaign status

The Supervisor does not perform domain-specific assessments.

---

# Topic-Based Orchestration

The solution divides the overall workflow into reusable topics.

## Campaign Intake & Validation

Responsibilities:

- Retrieve campaign requests
- Identify the oldest pending campaign
- Retrieve campaign details
- Validate mandatory information

---

## Specialist Assessment

Responsibilities:

- Invoke Budget & Commercial Specialist
- Invoke Brand & Content Compliance Specialist
- Invoke Channel Readiness Specialist
- Invoke Asset Readiness Specialist
- Collect assessment results

---

## Launch Risk & Decision

Responsibilities:

- Invoke Launch Risk & Decision Specialist
- Validate proposed readiness
- Determine remediation requirements
- Determine approval requirements

---

## Remediation & Selective Reassessment

Responsibilities:

- Execute only required reassessments
- Coordinate selective specialist execution
- Return updated findings

---

## Approval Finalisation

Responsibilities:

- Coordinate mandatory approval workflow
- Record approval outcomes

---

## Reporting & Communication

Responsibilities:

- Generate campaign readiness report
- Prepare stakeholder notification
- Update campaign lifecycle

---

# Specialist Coordination Pattern

The Supervisor delegates responsibilities to specialist agents according to their domain expertise.

| Specialist Agent | Primary Responsibility |
|------------------|------------------------|
| Budget & Commercial Specialist | Financial readiness assessment |
| Brand & Content Compliance Specialist | Brand and regulatory compliance |
| Channel Readiness Specialist | Operational channel readiness |
| Asset Readiness Specialist | Asset availability and approval |
| Launch Risk & Decision Specialist | Risk consolidation and readiness recommendation |
| Reporting & Communication Specialist | Report generation and stakeholder communication |

Each specialist performs only its assigned business function and returns structured findings to the Supervisor.

---

# Workflow Sequencing

The workflow follows a deterministic execution sequence.

1. Campaign retrieval
2. Campaign validation
3. Specialist assessments
4. Risk consolidation
5. Remediation (if required)
6. Approval (if required)
7. Reporting
8. Campaign status update

Each stage must complete successfully before the next stage begins.

---

# Decision Flow

```
Campaign Retrieved
        │
        ▼
Validation Passed?
        │
 ┌──────┴──────┐
 │             │
No            Yes
 │             │
 ▼             ▼
Terminate   Specialist Assessment
                    │
                    ▼
          Launch Risk Assessment
                    │
                    ▼
        Remediation Required?
           │              │
          Yes            No
           │              │
           ▼              ▼
Remediation Topic     Approval Required?
                            │
                     ┌──────┴──────┐
                     │             │
                    Yes           No
                     │             │
                     ▼             ▼
              Approval Topic   Reporting
                     │             │
                     └──────┬──────┘
                            ▼
                   Update Campaign Status
                            │
                            ▼
                          Finish
```

---

# Error Handling

The Supervisor terminates workflow execution when:

- No pending campaign exists
- Campaign validation fails
- Mandatory specialist assessment fails
- Required evidence is unavailable
- Reporting fails

The workflow never fabricates business data or specialist findings.

---

# Design Benefits

The orchestration pattern provides:

- Centralized workflow management
- Modular execution
- Reusable workflow components
- Independent specialist agents
- Policy-driven decision making
- Enterprise governance
- Improved maintainability
- Better scalability
- End-to-end traceability