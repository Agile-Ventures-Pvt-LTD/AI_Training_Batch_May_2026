# Specialist Agent Design

## Overview

The solution uses six domain-specific specialist agents coordinated by the **Supply Continuity Supervisor**. Each specialist is responsible for a single business domain and uses only the tools required for its assessment.

This modular architecture improves maintainability, scalability, and separation of concerns while allowing the Supervisor to orchestrate the complete disruption assessment lifecycle.

---

# 1. Inventory Impact Specialist

## Purpose

Determine whether existing inventory can satisfy the disruption until normal supply resumes.

## Responsibilities

- Retrieve disruption details
- Evaluate inventory availability
- Calculate Available-to-Promise (ATP)
- Assess safety stock impact
- Evaluate inventory shortages
- Recommend inventory actions

## Tools

| Tool | Purpose |
|------|---------|
| Get Disruption Details | Retrieve disruption information using the DisruptionID |
| Get Inventory by SKU | Retrieve inventory for the affected SKU |
| Get Purchase Orders for SKU | Retrieve inbound purchase orders |
| Get SKU Master Details | Retrieve safety stock and daily consumption information |

## Knowledge Source

None

The agent relies entirely on structured business data and deterministic inventory rules.

---

# 2. Alternate Supplier Specialist

## Purpose

Determine whether an approved alternate supplier can reduce the disruption.

## Responsibilities

- Retrieve alternate suppliers
- Evaluate supplier approval
- Assess supplier capacity
- Compare lead times
- Evaluate supplier risk
- Recommend alternate sourcing options

## Tools

| Tool | Purpose |
|------|---------|
| Get Disruption Context | Retrieve disruption information |
| Get Alternate Suppliers | Retrieve alternate supplier records |
| Get Supplier Details | Retrieve supplier information |
| Get SKU Details | Retrieve SKU information |

## Knowledge Source

None

The agent evaluates supplier information using structured Excel data only.

---

# 3. Customer & Order Impact Specialist

## Purpose

Determine how the disruption affects customer commitments and prioritize affected orders.

## Responsibilities

- Retrieve affected customer orders
- Evaluate customer priorities
- Assess SLA commitments
- Determine revenue exposure
- Evaluate partial fulfilment constraints
- Prioritize customer orders

## Tools

| Tool | Purpose |
|------|---------|
| Get Disruption Details | Retrieve disruption information |
| Get Customer Orders | Retrieve customer orders for the affected SKU |
| Get Inventory Details | Retrieve available inventory |
| Get SKU Details | Retrieve SKU planning information |

## Knowledge Source

None

The agent follows deterministic business rules for customer prioritization.

---

# 4. Commercial Impact Specialist

## Purpose

Evaluate the financial impact of potential recovery options.

## Responsibilities

- Compare sourcing costs
- Calculate procurement premium
- Evaluate revenue exposure
- Determine approval requirements
- Assess commercial risk

## Tools

| Tool | Purpose |
|------|---------|
| Get Disruption Detail | Retrieve disruption information |
| Get Alternate Supplier Costs | Retrieve alternate supplier pricing |
| Get Revenue Exposure | Retrieve affected customer revenue |
| Get Commercial Rules | Retrieve commercial approval thresholds |

## Knowledge Source

None

Commercial approval thresholds are enforced through structured business rules.

---

# 5. Recovery Planning Specialist

## Purpose

Recommend the most appropriate recovery strategy using the consolidated findings from all specialist agents.

## Responsibilities

- Review inventory assessment
- Review supplier assessment
- Review customer impact
- Review commercial assessment
- Recommend recovery strategy
- Identify approvals
- Assess residual risks

## Tools

None

The Recovery Planning Specialist receives consolidated assessments from the Supervisor Agent.

## Knowledge Source

NovaSphere Supply Continuity Policy

The knowledge source is used to:

- Apply recovery policies
- Validate recommendations
- Determine approval requirements
- Recommend compliant recovery strategies

---

# 6. Reporting & Communication Specialist

## Purpose

Generate the final recovery documentation and communicate the approved outcome.

## Responsibilities

- Generate disruption assessment report
- Prepare stakeholder notifications
- Communicate approved recovery strategy
- Return execution status

## Tools

| Tool | Purpose |
|------|---------|
| Generate Recovery Report | Generate the Microsoft Word recovery report |
| Send Stakeholder Notification | Notify stakeholders using Outlook |


## Knowledge Source

None

The agent formats and communicates only the information approved by the Supervisor.

---

# Knowledge Source Distribution

| Agent | Knowledge Source |
|--------|------------------|
| Inventory Impact Specialist | None |
| Alternate Supplier Specialist | None |
| Customer & Order Impact Specialist | None |
| Commercial Impact Specialist | None |
| Recovery Planning Specialist | NovaSphere Supply Continuity Policy |
| Reporting & Communication Specialist | None |

---

# Design Principles

All specialist agents follow the same architectural principles:

- Single Responsibility Principle
- Least Privilege Tool Access
- Deterministic Business Rules
- Independent Execution
- Evidence-Based Recommendations
- No Direct Communication Between Child Agents
- Final Decisions Made Only by the Supervisor

---

# Interaction Flow

```
                 Supply Continuity Supervisor
                            │
     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     │              │              │              │
     ▼              ▼              ▼              ▼
Inventory     Alternate      Customer       Commercial
Specialist    Supplier       Impact         Impact
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                            │
                            ▼
             Recovery Planning Specialist
                            │
                            ▼
      Reporting & Communication Specialist
```

---

# Benefits of the Specialist Design

- Clear separation of business responsibilities
- Minimal tool access for each agent
- Improved maintainability and scalability
- Reusable specialist agents
- Faster parallel assessments
- Easier debugging and testing
- Policy-compliant decision making
- Centralized governance through the Supervisor Agent