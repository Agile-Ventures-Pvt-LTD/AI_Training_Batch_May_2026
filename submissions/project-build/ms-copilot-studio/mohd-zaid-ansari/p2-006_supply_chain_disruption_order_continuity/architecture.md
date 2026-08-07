# System Architecture

## Overview

The Supply Chain Continuity Management System is built using a **Supervisor–Specialist Multi-Agent Architecture** in Microsoft Copilot Studio. The solution autonomously monitors supply disruptions, coordinates specialist agents, evaluates recovery strategies, validates approval requirements, generates business reports, and updates disruption records stored in Excel Online (Business).

The architecture separates orchestration, business logic, data access, and reporting into dedicated components, making the solution modular, scalable, and easier to maintain.

---

# High-Level Architecture

```text
                    ┌─────────────────────────────┐
                    │      Recurrence Trigger     │
                    │ (Runs on configured schedule)│
                    └──────────────┬──────────────┘
                                   │
                                   ▼
               ┌────────────────────────────────────────┐
               │ Supply Continuity Supervisor Agent     │
               │ • Workflow Orchestration               │
               │ • Agent Coordination                  │
               │ • Decision Making                     │
               └──────────────┬─────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐   ┌──────────────────┐  ┌────────────────────────┐
│ Topic           │   │ Specialist Agents │  │ Supervisor Tools       │
│ Disruption      │   │                  │  │                        │
│ Intake &        │   │ Inventory        │  │ Get Pending            │
│ Validation      │   │ Alternate        │  │ Get Disruption         │
└─────────────────┘   │ Customer         │  │ Get Purchase Order     │
                      │ Commercial       │  │ Get Recovery Rules     │
                      │ Recovery         │  │ Update Status          │
                      │ Reporting        │  └────────────────────────┘
                      └─────────┬────────┘
                                │
                                ▼
                 ┌────────────────────────────┐
                 │      Excel Online          │
                 │     (Business Tables)      │
                 └────────────────────────────┘
```

---

# Architecture Layers

## Layer 1 – Autonomous Trigger

The workflow begins with the **Recurrence Trigger**, which automatically starts the Supply Continuity Supervisor according to the configured schedule.

Responsibilities:

- Monitor for new disruption requests.
- Start the workflow automatically.
- Process one disruption request per execution.

---

## Layer 2 – Supervisor Agent

The **Supply Continuity Supervisor** is the central orchestration component.

Responsibilities include:

- Coordinating the complete workflow.
- Invoking topics.
- Calling specialist agents.
- Using Excel Online (Business) tools.
- Selecting recovery strategies.
- Managing workflow completion.

The Supervisor never performs detailed business analysis directly; it delegates these responsibilities to specialist agents.

---

# Supervisor Topics

The Supervisor uses three reusable topics to organize workflow execution.

---

## Topic 1

### Disruption Intake & Validation

Purpose

- Retrieve disruption information.
- Validate disruption records.
- Verify purchase order information.
- Determine whether workflow should continue.

Tools used

- /Get Pending Disruption
- /Get Disruption Details
- /Get Purchase Order

---

## Topic 2

### Recovery Strategy Resolution

Purpose

- Compare recovery strategies.
- Select the most suitable recovery option.
- Return the recommended recovery strategy.

---

## Topic 3

### Approval Exception Reassessment

Purpose

- Validate business approval requirements.
- Review escalation rules.
- Verify policy compliance.

Tool used

- /Get Recovery Rules

---

# Specialist Agents

Each specialist agent focuses on a single business domain.

---

## Inventory Impact Specialist

Responsibilities

- Inventory availability
- Safety stock analysis
- Inventory shortages

Primary Tool

- /Get Inventory

---

## Alternate Supplier Specialist

Responsibilities

- Supplier evaluation
- Alternate supplier identification
- Supplier capability assessment

Primary Tools

- /Get Supplier
- /Get Alternate Supplier

---

## Customer & Order Impact Specialist

Responsibilities

- Customer order analysis
- Order prioritization
- Delivery impact assessment

Primary Tool

- /Get Customer Orders

---

## Commercial Impact Specialist

Responsibilities

- Commercial impact
- Financial exposure
- Revenue risk

Primary Tools

- /Get Supplier
- /Get Purchase Order

---

## Recovery Planning Specialist

Responsibilities

- Generate recovery options
- Compare strategies
- Rank recommendations

Inputs

- Inventory Assessment
- Supplier Assessment
- Customer Assessment
- Commercial Assessment

Output

- Ranked Recovery Strategies

---

## Reporting & Communication Specialist

Responsibilities

- Executive summary generation
- Stakeholder communication
- Recovery reporting

Primary Tool

- /Get Stakeholders

---

# Excel Online (Business)

The solution stores operational data inside:

```
P2-006_Supply_Chain_Continuity_Lab_Data.xlsx
```

Tables

| Table | Purpose |
|--------|---------|
| DisruptionRequestsTable | Active disruption requests |
| SuppliersTable | Supplier information |
| SKUMasterTable | Product master data |
| InventoryTable | Inventory levels |
| PurchaseOrdersTable | Purchase order information |
| CustomerOrdersTable | Customer orders |
| AlternateSuppliersTable | Alternate supplier options |
| RecoveryRulesTable | Approval and recovery rules |
| StakeholdersTable | Stakeholder contacts |

---

# Supervisor Tools

| Tool | Excel Table |
|------|-------------|
| /Get Pending Disruption | DisruptionRequestsTable |
| /Get Disruption Details | DisruptionRequestsTable |
| /Get Purchase Order | PurchaseOrdersTable |
| /Get Recovery Rules | RecoveryRulesTable |
| /Update Disruption Status | DisruptionRequestsTable |

---

# Workflow Sequence

```text
Recurrence Trigger
        │
        ▼
Supply Continuity Supervisor
        │
        ▼
/Disruption Intake & Validation
        │
        ├── /Get Pending Disruption
        ├── /Get Disruption Details
        └── /Get Purchase Order
        │
        ▼
/Inventory Impact Specialist
        │
        ▼
/Alternate Supplier Specialist
        │
        ▼
/Customer & Order Impact Specialist
        │
        ▼
/Commercial Impact Specialist
        │
        ▼
/Recovery Planning Specialist
        │
        ▼
/Recovery Strategy Resolution
        │
        ▼
/Approval Exception Reassessment
        │
        └── /Get Recovery Rules
        │
        ▼
/Reporting & Communication Specialist
        │
        ▼
/Update Disruption Status
        │
        ▼
Workflow Complete
```

---

# Design Principles

The architecture follows these principles:

- Separation of responsibilities between orchestration, analysis, and reporting.
- Modular specialist agents for individual business domains.
- Reusable topics for common workflow stages.
- Centralized workflow orchestration through the Supervisor Agent.
- Excel Online (Business) as the operational data source.
- Autonomous execution using a Recurrence Trigger.
- Controlled data updates through dedicated update tools.

---

# Benefits

- Autonomous disruption monitoring
- Modular multi-agent architecture
- Scalable workflow orchestration
- Improved decision support
- Reduced manual intervention
- Consistent recovery planning
- Structured reporting
- Easier maintenance and future expansion
```