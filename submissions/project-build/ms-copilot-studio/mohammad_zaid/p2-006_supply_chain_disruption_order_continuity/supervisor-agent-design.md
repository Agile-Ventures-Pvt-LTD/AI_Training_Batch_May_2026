
# Supervisor Agent Design

# Agent Information

| Property             | Value                                  |
| -------------------- | -------------------------------------- |
| Agent Name           | Supply Continuity Supervisor           |
| Agent Type           | Supervisor Agent                       |
| Platform             | Microsoft Copilot Studio               |
| Architecture Pattern | Hierarchical Multi-Agent Orchestration |
| Role                 | Central Workflow Orchestrator          |

---

# Overview

The Supply Continuity Supervisor is the central intelligence of the Autonomous Supply Chain Disruption & Order Continuity Response System.

It is responsible for coordinating the complete disruption assessment lifecycle, maintaining workflow state, invoking deterministic custom topics, delegating work to specialist child agents, validating recovery recommendations, managing approvals, and completing the orchestration process.

The Supervisor never performs domain-specific analysis itself. Instead, it delegates specialized assessments to child agents and combines their outputs into a single business decision.

---

# Business Responsibilities

The Supervisor is responsible for:

- Monitoring new disruption requests
- Starting autonomous orchestration
- Executing custom topics
- Maintaining workflow state
- Validating disruption records
- Delegating specialist assessments
- Coordinating recovery planning
- Evaluating approval requirements
- Managing workflow exceptions
- Invoking reporting
- Updating disruption status
- Completing the workflow

---

# Architectural Position

```
                  Recurrence Trigger
                           │
                           ▼
            Supply Continuity Supervisor
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
 Custom Topics      Specialist Agents      Knowledge Base
                           │
                           ▼
          Reporting & Communication
```

The Supervisor is the only orchestration controller within the solution.

---

# Child Agents Managed

The Supervisor coordinates the following child agents:

1. Inventory Impact Specialist
2. Alternate Supplier Specialist
3. Customer & Order Impact Specialist
4. Commercial Impact Specialist
5. Recovery Planning Specialist
6. Reporting & Communication Specialist

Each child agent performs domain-specific reasoning and returns structured outputs to the Supervisor.

---

# Custom Topics Executed

The Supervisor executes three deterministic custom topics.

## 1. Disruption Intake & Validation

Purpose:

- Retrieve pending disruptions
- Validate mandatory fields
- Prevent duplicate processing
- Update workflow state

Outputs:

- Validated disruption
- Workflow status

---

## 2. Recovery Strategy Resolution

Purpose:

- Coordinate specialist execution
- Collect specialist findings
- Invoke Recovery Planning Specialist
- Produce recovery recommendation

Outputs:

- Recovery strategy
- Risk assessment
- Approval requirement

---

## 3. Approval, Exception & Selective Reassessment

Purpose:

- Evaluate approval requirements
- Handle workflow exceptions
- Control reassessment
- Return workflow outcome

Outputs:

- Final workflow status
- Escalation decision
- Approval outcome

---

# Workflow Lifecycle

```
Recurrence Trigger
        │
        ▼
Retrieve Pending Disruption
        │
        ▼
Execute Topic 1
        │
        ▼
Invoke Specialist Agents
        │
        ▼
Execute Topic 2
        │
        ▼
Execute Topic 3
        │
        ▼
Reporting Specialist
        │
        ▼
Update Excel
        │
        ▼
Send Notification
        │
        ▼
Complete Workflow
```

---

# Tools Configured

The Supervisor uses the following tools:

### SUP - Get Pending Disruptions

Purpose:

Retrieve disruption requests from the `DisruptionRequestsTable`.

Connector:

Excel Online (Business)

---

### SUP - Update Disruption Status

Purpose:

Update the workflow status of a disruption request.

Connector:

Excel Online (Business)

---

# Knowledge Source

Knowledge Base:

NovaSphere Supply Continuity Policy

Purpose:

- Validate recovery recommendations
- Enforce business policies
- Guide orchestration decisions
- Support deterministic reasoning

The knowledge base is attached only to the Supervisor because policy interpretation is centralized at the orchestration layer.

---

# Workflow States

The Supervisor manages the following disruption states:

- Pending
- In Assessment
- Recovery Strategy Available
- Awaiting Approval
- Completed
- Insufficient Evidence
- Manual Review
- No Viable Recovery
- Escalation Required

Each state transition is controlled by the Supervisor.

---

# Decision Responsibilities

The Supervisor is responsible for determining:

- Whether a disruption is valid
- Which specialists should be executed
- Whether recovery is possible
- Whether approval is required
- Whether reassessment is needed
- Whether escalation is required
- When reporting should begin
- When workflow execution is complete

The Supervisor does not perform specialist analysis; it only orchestrates and validates the overall decision process.

---

# Inputs

Primary inputs include:

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- WorkflowStatus

These inputs are retrieved from the Disruption Requests table and propagated to child agents as required.

---

# Outputs

The Supervisor produces the following outputs:

- Final Recovery Strategy
- Final Risk Classification
- Approval Requirement
- Workflow Status
- Recovery Summary
- Orders Protected
- Orders At Risk
- Revenue At Risk
- Report Generation Status
- Notification Status

---

# Error Handling

The Supervisor handles:

- Missing disruption information
- Invalid workflow states
- Missing specialist outputs
- No viable recovery strategy
- Approval rejection
- Reassessment limit exceeded

When an unrecoverable condition is detected, the Supervisor routes the disruption to Manual Review or Escalation as appropriate.

---

# Design Principles

The Supervisor follows these principles:

- Single orchestration authority
- Separation of responsibilities
- Deterministic workflow execution
- Explainable AI decision-making
- Policy-driven validation
- Reusable specialist agents
- Modular workflow design
- Enterprise scalability

---

# Summary

The Supply Continuity Supervisor serves as the orchestration backbone of the solution. It coordinates every stage of the disruption lifecycle, invokes deterministic custom topics, delegates specialized analysis to child agents, validates recovery recommendations using the organizational policy knowledge base, and ensures that each disruption is processed consistently, transparently, and in accordance with enterprise business rules.
