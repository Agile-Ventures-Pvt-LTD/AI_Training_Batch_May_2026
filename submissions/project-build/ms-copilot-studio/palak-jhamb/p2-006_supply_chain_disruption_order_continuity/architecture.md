# System Architecture

## Overview

The Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System is designed using a **hierarchical multi-agent architecture** implemented in Microsoft Copilot Studio.

A single **Supervisor Agent** orchestrates the complete disruption assessment lifecycle while delegating domain-specific responsibilities to specialized child agents.

This architecture promotes modularity, scalability, maintainability, and clear separation of responsibilities.

---

# High-Level Architecture

```
                    Recurring Trigger
                           │
                           ▼
              Supply Continuity Supervisor
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ▼                                   ▼
 Disruption Intake                 Approval & Exception
   Validation Topic               Selective Reassessment
         │
         ▼
──────────────── Fan-Out ────────────────

 Inventory Impact Specialist

 Alternate Supplier Specialist

 Customer & Order Impact Specialist

 Commercial Impact Specialist

─────────────── Fan-In ────────────────

         ▼
 Recovery Planning Specialist

         ▼
 Reporting & Communication Specialist

         ▼

 Word Report
 Outlook Notification
 Excel Status Update
```

---

# Architectural Components

## 1. Recurring Trigger

Automatically starts the workflow at scheduled intervals.

Responsibilities

- Detect new disruption requests.
- Start autonomous execution.

---

## 2. Supply Continuity Supervisor

Acts as the central orchestration engine.

Responsibilities

- Validate disruptions
- Invoke child agents
- Perform Fan-Out
- Perform Fan-In
- Resolve conflicts
- Apply business policy
- Validate recovery strategy
- Trigger reporting
- Update disruption lifecycle

---

## 3. Specialist Child Agents

Each child agent performs a single business responsibility.

| Agent | Responsibility |
|---------|----------------|
| Inventory Impact Specialist | Inventory analysis |
| Alternate Supplier Specialist | Supplier evaluation |
| Customer & Order Impact Specialist | Customer impact |
| Commercial Impact Specialist | Financial assessment |
| Recovery Planning Specialist | Strategy recommendation |
| Reporting & Communication Specialist | Reporting & notification |

---

# Topics

Three custom topics support the orchestration.

## Topic 1

Disruption Intake & Validation

Responsible for validating disruption requests before assessment.

---

## Topic 2

Recovery Strategy Resolution

Responsible for evaluating and validating recovery strategies.

---

## Topic 3

Approval, Exception & Selective Reassessment

Responsible for approval routing and reassessment.

---

# Data Sources

Business data is stored in Microsoft Excel Online.

Tables used include:

- Disruption_Requests
- Inventory
- SKU_Master
- Purchase_Orders
- Customer_Orders
- Alternate_Suppliers
- Suppliers
- Recovery_Rules

---

# Knowledge Sources

Knowledge retrieval is intentionally restricted to:

- Supply Continuity Supervisor
- Recovery Planning Specialist

Other agents rely exclusively on structured business data.

---

# Design Principles

The architecture follows:

- Separation of concerns
- Least privilege
- Hierarchical orchestration
- Parallel processing
- Deterministic business rules
- Policy-driven decision making
- Autonomous execution
- Auditability

---

# Benefits

- Modular design
- Reusable specialist agents
- Easy maintenance
- Better scalability
- Faster disruption assessment
- Improved governance