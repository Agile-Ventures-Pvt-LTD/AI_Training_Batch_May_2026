# specialist-agent-design.md

# Specialist Agent Design

## P2-006 – Supply Chain Disruption Order Continuity

---

# Overview

The Supply Chain Disruption Order Continuity solution follows a **multi-agent architecture** where each specialist agent is responsible for a single business capability.

Rather than allowing one AI agent to perform all reasoning, the workflow distributes responsibilities among multiple domain experts coordinated by the Supervisor Agent.

This approach improves:

- Accuracy
- Explainability
- Scalability
- Maintainability
- Enterprise governance

---

# Specialist Agent Architecture

```text
                Supply Continuity Supervisor
                           │
                           ▼
                Recovery Planning Specialist
                           │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
Inventory      Alternate       Customer &      Commercial
Impact         Supplier        Order Impact    Impact
Specialist     Specialist      Specialist      Specialist
                           │
                           ▼
          Reporting & Communication Specialist
```

---

# Agent 1 – Inventory Impact Specialist

## Purpose

The Inventory Impact Specialist evaluates current inventory availability and determines whether existing inventory can satisfy customer demand.

---

## Responsibilities

- Check inventory availability
- Calculate Available-to-Promise (ATP)
- Evaluate safety stock
- Determine shortage quantity
- Assess inventory risk

---

## Inputs

- SKU
- Warehouse
- Inventory Quantity
- Safety Stock
- Purchase Order

---

## Outputs

- Inventory Available
- ATP Result
- Shortage Quantity
- Inventory Risk
- Safety Stock Status

---

## Business Rules

- Existing inventory is always preferred over alternate sourcing.
- Safety stock must not be violated.
- Quality-held inventory is excluded from ATP.
- Negative inventory is invalid.

---

## Connected Tools

Excel Online (Business)

Actions:

- List Rows Present in a Table
- Get a Row
- Update a Row

---

# Agent 2 – Alternate Supplier Specialist

## Purpose

Evaluate approved alternate suppliers capable of fulfilling the disrupted order.

---

## Responsibilities

- Search approved suppliers
- Compare lead times
- Evaluate supplier capacity
- Compare commercial cost
- Validate supplier approval

---

## Inputs

- Supplier ID
- SKU
- Required Date

---

## Outputs

- Alternate Supplier
- Lead Time
- Capacity
- Cost Premium
- Supplier Approval Status

---

## Business Rules

- Only approved suppliers may be recommended.
- Supplier capacity must satisfy required quantity.
- Lowest cost is not always preferred if delivery commitments are affected.

---

## Connected Tools

Excel Online (Business)

Tables

- Supplier Master
- Alternate Suppliers
- Recovery Rules

---

# Agent 3 – Customer & Order Impact Specialist

## Purpose

Assess how the disruption affects customer commitments.

---

## Responsibilities

- Evaluate affected orders
- Identify strategic customers
- Determine SLA impact
- Estimate revenue at risk

---

## Inputs

- Customer Orders
- SLA Information
- Inventory Status

---

## Outputs

- Orders At Risk
- Strategic Customers
- Revenue Impact
- Customer Priority

---

## Business Rules

- Strategic customers receive highest priority.
- SLA commitments override lower-priority orders.
- Revenue impact contributes to escalation decisions.

---

## Connected Tools

Excel Online

Tables

- Customer Orders
- Sales Orders
- Disruption Requests

---

# Agent 4 – Commercial Impact Specialist

## Purpose

Evaluate the financial implications of recovery strategies.

---

## Responsibilities

- Calculate cost premium
- Determine margin impact
- Check approval thresholds
- Assess commercial risk

---

## Inputs

- Supplier Cost
- Alternate Cost
- Recovery Strategy

---

## Outputs

- Cost Premium
- Commercial Risk
- Approval Required
- Estimated Margin Impact

---

## Business Rules

- Premium above 15% requires Finance approval.
- High commercial exposure increases escalation priority.
- Commercial approval is mandatory before execution.

---

## Connected Tools

Excel Online

Tables

- Commercial Rules
- Supplier Pricing
- Recovery Policies

---

# Agent 5 – Recovery Planning Specialist

## Purpose

Consolidate all specialist recommendations and determine the most appropriate recovery strategy.

---

## Responsibilities

- Receive specialist outputs
- Apply enterprise business rules
- Resolve conflicting recommendations
- Recommend recovery strategy

---

## Inputs

- Inventory Assessment
- Supplier Assessment
- Customer Assessment
- Commercial Assessment

---

## Outputs

- Proposed Strategy
- Required Approvals
- Residual Risk
- Recommended Actions

---

## Recovery Strategies

- Use Existing Inventory
- Reallocate Inventory
- Approved Alternate Supplier
- Expedite Existing Supplier
- Expedite Alternate Supplier
- Partial Fulfilment
- Customer Delivery Negotiation
- Manual Review
- Management Escalation

---

## Decision Logic

Priority Order

1. Inventory Availability
2. Strategic Customer Protection
3. Approved Alternate Supplier
4. Commercial Approval
5. Escalation

---

# Agent 6 – Reporting & Communication Specialist

## Purpose

Generate final business deliverables and communicate approved recovery decisions.

---

## Responsibilities

- Generate Microsoft Word report
- Update disruption status
- Notify stakeholders
- Send Outlook email
- Record workflow completion

---

## Inputs

- Final Strategy
- Final Status
- Approval Decision
- Recovery Summary

---

## Outputs

- Word Report
- Excel Update
- Outlook Notification
- Workflow Completion

---

## Connected Tools

### Word Online (Business)

Action

- Create Microsoft Word Document

---

### Outlook

Action

- Send Email (V2)

---

## Business Rules

- Reports are generated only after Supervisor approval.
- Emails are sent only after successful workflow completion.
- Failed notifications are logged for follow-up.

---

# Agent Communication Flow

```text
Supervisor Agent
        │
        ▼
Inventory Impact Specialist
        │
        ▼
Alternate Supplier Specialist
        │
        ▼
Customer & Order Impact Specialist
        │
        ▼
Commercial Impact Specialist
        │
        ▼
Recovery Planning Specialist
        │
        ▼
Reporting & Communication Specialist
```

---

# Design Principles

The specialist agents follow enterprise AI design principles.

### Single Responsibility

Each agent performs one well-defined business function.

---

### Modularity

Agents can be updated independently without affecting the overall workflow.

---

### Explainability

Each recommendation includes supporting business reasoning.

---

### Reusability

Specialist agents can be reused across other supply chain workflows.

---

### Governance

The Supervisor Agent retains authority for workflow orchestration and final decisions.

---

# Summary

The solution contains **six specialist agents**, each dedicated to a specific domain of supply disruption management.

Together, these agents enable accurate, explainable, and scalable decision support while maintaining enterprise governance and seamless integration with Microsoft 365 services.

---

# Version

**Version:** 1.0

**Status:** Completed