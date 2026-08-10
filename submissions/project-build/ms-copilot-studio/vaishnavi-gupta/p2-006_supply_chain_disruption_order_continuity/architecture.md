# Solution Architecture

## Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System is implemented as a hierarchical multi-agent architecture in Microsoft Copilot Studio. The solution uses a central Supervisor Agent to orchestrate multiple specialist child agents, apply business rules, consolidate findings, manage approvals, and coordinate reporting activities. The architecture follows Microsoft's recommended orchestrator-subagent model and implements sequential, parallel, conditional, and hierarchical orchestration patterns. 【1-ef0424】

---

# Architectural Goals

The architecture is designed to:

- Automatically detect and process supply chain disruptions
- Minimize manual intervention during analysis
- Maintain deterministic business rule enforcement
- Provide specialist-driven assessments
- Support conflict resolution and approval workflows
- Generate auditable recommendations
- Ensure traceability and explainability
- Respect human approval boundaries
- Handle failures through retry and escalation mechanisms



---

# High-Level Architecture

```text
┌──────────────────────────────┐
│   Recurrence Event Trigger   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Supply Continuity Supervisor │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Disruption Intake Validation │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ SKU, PO & Order Identification│
└──────────────┬───────────────┘
               │
       ┌───────┼────────┬────────┬────────┐
       ▼       ▼        ▼        ▼
 ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
 │Inventory│ │Alternate│ │Customer│ │Commercial│
 │Impact   │ │Supplier │ │Impact  │ │Impact    │
 │Agent    │ │Agent    │ │Agent   │ │Agent     │
 └────┬────┘ └────┬────┘ └────┬───┘ └────┬────┘
      └───────────┴───────────┴──────────┘
                       │
                       ▼
            ┌──────────────────┐
            │ Fan-In & Merge   │
            └────────┬─────────┘
                     │
                     ▼
       ┌────────────────────────────┐
       │ Recovery Planning Agent    │
       └─────────────┬──────────────┘
                     │
                     ▼
       ┌────────────────────────────┐
       │ Supervisor Validation      │
       └─────────────┬──────────────┘
                     │
        ┌────────────┼─────────────┐
        ▼            ▼             ▼
   Approved     Approval      Escalation
                Required
        │            │             │
        └────────────┴─────────────┘
                     │
                     ▼
   ┌────────────────────────────────┐
   │ Reporting & Communication Agent│
   └───────────────┬────────────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Word Report      Outlook Email
                   │
                   ▼
            Excel Status Update
```


---

# Component Architecture

## 1. Autonomous Trigger Layer

### Purpose

The trigger layer initiates the entire workflow without requiring user interaction.

### Responsibilities

- Execute on a recurring schedule
- Read disruption records from Excel
- Identify the oldest Pending disruption
- Prevent duplicate processing
- Update status to **In Assessment**
- Invoke the Supervisor Agent

### Technology

- Copilot Studio Recurrence Trigger
- Excel Online (Business)


---

## 2. Supervisor Layer

### Agent

**Supply Continuity Supervisor**

The Supervisor Agent acts as the orchestration controller for the entire solution.

### Responsibilities

- Workflow orchestration
- State management
- Validation control
- Specialist invocation
- Fan-out execution
- Fan-in consolidation
- Conflict resolution
- Risk classification
- Approval routing
- Reassessment decisions
- Report authorization
- Notification authorization

### Governance

The Supervisor is the only component allowed to:

- Approve final recommendations
- Determine workflow state
- Initiate approvals
- Classify final risk
- Authorize communications


---

## 3. Validation Layer

### Component

**Disruption Intake & Validation Topic**

### Purpose

Performs deterministic validation before specialist processing begins.

### Validation Rules

- Disruption ID exists
- Disruption record is unique
- Status equals Pending
- Supplier exists
- SKU exists
- Purchase Order exists
- Reported dates are valid
- Quantities are positive
- Supplier, SKU, and PO relationships match

### Outputs

- Validation Status
- Duplicate Detection Flag
- Assessment Eligibility

Invalid records are routed to Manual Review or Insufficient Evidence states.


---

# Specialist Assessment Layer

The assessment layer consists of four independent specialist agents running under Supervisor control.

---

## Inventory Impact Specialist

### Purpose

Determines inventory availability and supply protection capability.

### Data Sources

- Inventory Table
- SKU Master Table
- Purchase Orders
- Disruption Requests

### Key Analysis

```text
ATP = On Hand
      - Reserved
      + Inbound Within 7 Days
      - Quality Hold
```

### Deliverables

- Available inventory
- Safety stock consumption
- Shortage estimation
- Inventory risk assessment


---

## Alternate Supplier Specialist

### Purpose

Evaluates supplier replacement options.

### Data Sources

- Alternate Suppliers
- Suppliers
- SKU Master

### Key Rules

- Approved suppliers may be recommended
- Unapproved suppliers cannot be autonomously selected

### Deliverables

- Alternate availability
- Capacity validation
- Lead time analysis
- Cost comparison


---

## Customer & Order Impact Specialist

### Purpose

Determines customer commitment risks.

### Prioritization Logic

```text
Strategic + SLA Protected
        ↓
Priority
        ↓
Standard
```

### Deliverables

- Orders at risk
- Strategic customer exposure
- Revenue exposure
- Fulfillment constraints


---

## Commercial Impact Specialist

### Purpose

Analyzes financial implications of recovery options.

### Approval Rules

```text
Cost Premium > 15%
   → Finance Approval

Expedite Premium > 10%
   → Supply Chain Director Approval
```

### Deliverables

- Cost impact
- Commercial risk
- Approval requirements
- Recommended commercial actions


---

# Fan-Out / Fan-In Architecture

## Fan-Out Stage

The Supervisor invokes four independent assessment agents simultaneously from a logical orchestration perspective.

```text
Supervisor
     │
 ┌───┼─────────────┬─────────────┬─────────────┐
 ▼   ▼             ▼             ▼
Inventory   Alternate     Customer     Commercial
```

### Benefits

- Separation of responsibilities
- Independent domain evaluation
- Reduced analysis bias
- Modular scalability


---

## Fan-In Stage

The Supervisor waits for all required specialist outputs before continuing.

### Fan-In Activities

- Collect findings
- Validate completion
- Retry failed specialists
- Detect conflicts
- Consolidate evidence
- Build unified case assessment

### Output

A consolidated assessment package for recovery planning.


---

# Recovery Planning Layer

## Agent

**Recovery Planning Specialist**

### Purpose

Generate feasible recovery strategies using consolidated specialist findings.

### Allowed Strategies

- Use existing inventory
- Reallocate inventory
- Approved alternate supplier
- Expedite existing supply
- Expedite alternate supply
- Partial fulfillment
- Customer date negotiation
- Combined recovery strategy
- Management escalation
- Manual review

### Restrictions

The agent cannot:

- Place purchase orders
- Approve suppliers
- Cancel customer orders
- Promise delivery dates
- Authorize spending


---

# Decision & Approval Layer

## Recovery Strategy Resolution Topic

This component resolves conflicting specialist recommendations using deterministic business rules.

### Decision Precedence

```text
1. Safety & Quality Restrictions
2. Strategic/SLA Commitments
3. Supplier Approval Restrictions
4. Inventory Availability
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience
```

### Example

If an alternate supplier can satisfy demand but carries an 18% premium, the supplier may be technically viable but still requires business approval before implementation.


---

## Approval & Exception Topic

### Handles

- Approval routing
- Escalations
- Retry management
- Reassessment requests
- State transitions

### Approval Triggers

- Premium Cost > 15%
- Expedite Premium > 10%
- Strategic inventory consumption
- Unapproved supplier identified
- Restricted fulfillment conditions


---

# Communication Layer

## Reporting Specialist

Responsible for creating the final Supply Disruption Response Report.

### Report Content

- Disruption information
- Supplier details
- Inventory findings
- Customer impact
- Commercial analysis
- Selected strategy
- Residual risks
- Required approvals
- Supervisor decision


---

## Notification Services

### Outlook Integration

Notifications are sent only after Supervisor authorization.

### Notification Scenarios

| State | Recipient |
|---------|-----------|
| Recovery Plan Proposed | Procurement & Planning |
| Awaiting Approval | Required Approver |
| Customer Action Required | Customer Operations Lead |
| Management Escalation | Supply Chain Director |
| Completed | Relevant Stakeholders |


---

# Data Architecture

## Excel-Based Operational Repository

The solution uses Excel Online (Business) tables stored in OneDrive or SharePoint.

### Core Tables

- DisruptionRequestsTable
- SuppliersTable
- SKUMasterTable
- InventoryTable
- PurchaseOrdersTable
- CustomerOrdersTable
- AlternateSuppliersTable
- RecoveryRulesTable
- StakeholdersTable

### Knowledge Source

- NovaSphere Supply Continuity Policy

Deterministic policy rules always take precedence over generative reasoning.


---

# Failure Handling Architecture

## Failure Categories

The system manages:

- Missing disruption records
- Duplicate requests
- Validation failures
- Specialist failures
- Excel connector failures
- Report generation failures
- Email delivery failures
- Missing approvers
- Reassessment exhaustion

### Retry Logic

```text
Attempt 1
     ↓
Failure
     ↓
Retry Once
     ↓
Success → Continue

Failure Again
     ↓
Insufficient Evidence
     ↓
Manual Review / Escalation
```

Maximum specialist invocation attempts: **2**


---

# Security and Governance

The architecture includes mandatory guardrails to prevent unauthorized autonomous actions.

### The system may:

- Assess disruptions
- Recommend actions
- Generate reports
- Request approvals

### The system must not:

- Place purchase orders
- Approve suppliers
- Cancel customer orders
- Commit delivery dates
- Authorize spending

Human approval remains mandatory for all protected business decisions.


---

# Architecture Summary

The solution implements an event-driven, hierarchical multi-agent architecture where a central Supply Continuity Supervisor coordinates independent specialist agents, consolidates findings through fan-in orchestration, applies deterministic business policies, manages approvals, and generates operational outputs. The architecture ensures reliability, traceability, explainability, and governance while providing autonomous disruption assessment and continuity planning capabilities.

