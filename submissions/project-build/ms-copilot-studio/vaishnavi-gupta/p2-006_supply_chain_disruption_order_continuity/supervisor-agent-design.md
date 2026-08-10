# Supervisor Agent Design

## Overview

The **Supply Continuity Supervisor** is the central orchestrator of the Autonomous Supply Chain Disruption & Order Continuity Response System. It is responsible for managing the complete workflow from disruption detection through final reporting and communication. The Supervisor coordinates specialist agents, applies business rules, resolves conflicting recommendations, manages approvals, and authorizes final actions. 

---

# Agent Details

| Attribute | Value |
|------------|---------|
| Agent Name | Supply Continuity Supervisor |
| Agent Type | Parent / Orchestrator Agent |
| Platform | Microsoft Copilot Studio |
| Role | Workflow Orchestration and Decision Management |

---

# Core Responsibilities

The Supervisor is responsible for:

- Receiving autonomous trigger events
- Selecting pending disruption records
- Invoking validation processes
- Managing disruption states
- Identifying affected SKUs and orders
- Invoking specialist child agents
- Coordinating fan-out and fan-in activities
- Consolidating specialist findings
- Resolving recommendation conflicts
- Determining approval requirements
- Managing reassessment decisions
- Validating recovery strategies
- Classifying final risk levels
- Authorizing reports and notifications
- Updating final workflow status


---

# Workflow Ownership

The Supervisor controls the complete orchestration flow.

```text
Recurrence Trigger
        ↓
Validation
        ↓
Scope Identification
        ↓
Specialist Assessments
        ↓
Fan-In Consolidation
        ↓
Recovery Planning
        ↓
Conflict Resolution
        ↓
Approval Handling
        ↓
Final Decision
        ↓
Reporting & Communication
```


---

# Child Agent Management

The Supervisor invokes and manages the following specialist agents:

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist
- Recovery Planning Specialist
- Reporting & Communication Specialist

The Supervisor remains responsible for all final decisions and approvals. 

---

# Fan-Out Responsibilities

After validation and scope identification, the Supervisor initiates parallel specialist assessments.

```text
Supervisor
    │
 ┌──┼─────────┬─────────┬─────────┐
 ▼  ▼         ▼         ▼
Inventory  Alternate  Customer  Commercial
```

The Supervisor waits for all required assessments before continuing. 

---

# Fan-In Responsibilities

After specialist execution, the Supervisor:

- Collects specialist outputs
- Validates completion status
- Retries failed specialists when required
- Identifies conflicting findings
- Consolidates evidence
- Creates a unified assessment package

The consolidated result is then forwarded for recovery planning. 

---

# Conflict Resolution

When specialist recommendations conflict, the Supervisor applies policy-based precedence.

## Decision Order

```text
1. Safety & Quality Restrictions
2. Strategic/SLA Commitments
3. Supplier Approval Restrictions
4. Inventory Availability
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience
```

The Supervisor never averages conflicting recommendations and always follows business policy precedence. 
---

# Approval Management

The Supervisor determines whether human approval is required.

## Approval Triggers

- Cost premium exceeds 15%
- Expedite premium exceeds 10%
- Strategic demand requires safety stock usage
- No approved alternate supplier exists
- Partial fulfillment restrictions apply
- Critical demand cannot be protected

If approval is required, the Supervisor moves the case to **Awaiting Approval** and records the reason. 

---

# Selective Reassessment

When source data changes, the Supervisor:

1. Identifies stale assessments.
2. Determines impacted specialists.
3. Reinvokes only affected agents.
4. Performs fan-in consolidation again.
5. Recalculates the final strategy.

Maximum reassessment cycles: **2**. Unresolved cases are routed to **Manual Review**. 

---

# Risk Classification

The Supervisor assigns one final risk level:

- Low
- Medium
- High
- Critical

Each classification is supported by specialist findings and documented rationale. 

---

# State Management

The Supervisor controls all valid state transitions.

### Supported States

```text
Pending
In Assessment
Awaiting Approval
Recovery Plan Proposed
Customer Action Required
Management Escalation
Insufficient Evidence
Manual Review
Completed
```

Invalid workflow transitions are prevented. 【1-969174】

---

# Guardrails

The Supervisor must not:

- Invent missing specialist evidence
- Assume approvals are granted
- Approve suppliers
- Place purchase orders
- Cancel customer orders
- Commit delivery dates
- Authorize commercial spending

All governed business actions require human approval where applicable. 

---

# Failure Handling

The Supervisor manages:

- Validation failures
- Specialist failures
- Duplicate processing attempts
- Missing data conditions
- Connector failures
- Reassessment limits

Failed specialist assessments are retried once before escalation to **Insufficient Evidence** or **Manual Review**. 

---

# Summary

The Supply Continuity Supervisor serves as the central orchestration and governance component of the solution. It coordinates all agent interactions, applies business policies, manages approvals, resolves conflicts, validates recovery strategies, and authorizes final outputs, ensuring every recommendation remains compliant, traceable, and aligned with organizational supply continuity requirements. 