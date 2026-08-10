# Architecture

# P2-006 – Supply Chain Disruption Order Continuity

## System Architecture

---

# Overview

The Supply Chain Disruption Order Continuity solution is designed as a **hierarchical multi-agent architecture** implemented using **Microsoft Copilot Studio**.

The architecture separates responsibilities across multiple specialist AI agents while maintaining centralized orchestration through a Supervisor Agent. This modular design improves scalability, maintainability, and decision quality.

---

# High-Level Architecture

```text
                          +--------------------------------+
                          |  Supply Continuity Supervisor  |
                          +--------------------------------+
                                      |
        ---------------------------------------------------------------
        |                            |                               |
        v                            v                               v
+--------------------+    +--------------------------+    +---------------------------+
| Topic 1            |    | Topic 2                  |    | Topic 3                   |
| Intake & Validation|    | Recovery Resolution      |    | Approval & Reassessment   |
+--------------------+    +--------------------------+    +---------------------------+
                                      |
                                      v
                     +-------------------------------------+
                     | Recovery Planning Specialist        |
                     +-------------------------------------+
                                      |
       --------------------------------------------------------------------
       |                         |                      |                   |
       v                         v                      v                   v
+------------------+   +-----------------------+  +----------------+  +---------------------+
| Inventory Impact |   | Alternate Supplier    |  | Customer &     |  | Commercial Impact   |
| Specialist       |   | Specialist            |  | Order Impact   |  | Specialist          |
+------------------+   +-----------------------+  | Specialist     |  +---------------------+
                                                  +----------------+
                                      |
                                      v
                +-----------------------------------------------+
                | Reporting & Communication Specialist          |
                +-----------------------------------------------+
                       |                     |                  |
                       v                     v                  v
                 Excel Online         Word Online          Outlook
```

---

# Architectural Layers

The solution is divided into four logical layers.

---

## 1. Orchestration Layer

The orchestration layer contains the **Supply Continuity Supervisor**, which coordinates the complete workflow.

### Responsibilities

- Initiate workflow execution
- Invoke custom topics
- Coordinate specialist agents
- Manage approvals
- Handle workflow completion

---

## 2. Business Logic Layer

Business logic is implemented using three custom topics.

### Topic 1 – Disruption Intake & Validation

Purpose:

- Validate disruption requests
- Prevent duplicate processing
- Verify required business information

---

### Topic 2 – Recovery Strategy Resolution

Purpose:

- Consolidate specialist recommendations
- Apply business rules
- Determine the optimal recovery strategy

---

### Topic 3 – Approval, Exception & Selective Reassessment

Purpose:

- Manage approvals
- Handle reassessment
- Process exceptions
- Complete workflow

---

## 3. Specialist Agent Layer

The specialist layer contains domain-specific AI agents.

| Agent | Primary Responsibility |
|--------|------------------------|
| Inventory Impact Specialist | Inventory availability assessment |
| Alternate Supplier Specialist | Alternate supplier evaluation |
| Customer & Order Impact Specialist | Customer impact assessment |
| Commercial Impact Specialist | Commercial analysis |
| Recovery Planning Specialist | Recovery recommendation |
| Reporting & Communication Specialist | Report generation and communication |

---

## 4. Integration Layer

The integration layer connects Microsoft Copilot Studio with Microsoft 365 services.

### Excel Online (Business)

Used for:

- Reading disruption records
- Updating workflow status
- Maintaining operational data

---

### Word Online (Business)

Used for:

- Generating disruption reports
- Creating recovery documentation

---

### Outlook

Used for:

- Sending approval notifications
- Informing stakeholders
- Workflow completion emails

---

# Data Flow

The solution follows the data flow shown below.

```text
Excel Disruption Request
          │
          ▼
Topic 1 – Validation
          │
          ▼
Recovery Planning Specialist
          │
          ├──────── Inventory Specialist
          ├──────── Alternate Supplier Specialist
          ├──────── Customer Impact Specialist
          └──────── Commercial Impact Specialist
          │
          ▼
Topic 2 – Recovery Strategy Resolution
          │
          ▼
Topic 3 – Approval Workflow
          │
          ▼
Reporting & Communication Specialist
          │
      ┌───┴───────────────┐
      ▼                   ▼
 Word Report        Outlook Email
      │
      ▼
 Excel Status Update
```

---

# Architecture Principles

The solution follows key enterprise architecture principles.

## Separation of Responsibilities

Each child agent is responsible for a single business capability.

---

## Modularity

Agents and topics are independent, making the solution easy to extend and maintain.

---

## Scalability

Additional specialist agents or business rules can be introduced without redesigning the architecture.

---

## Reusability

Each specialist agent can be reused in other Copilot Studio solutions.

---

## Governance

The Supervisor Agent retains control over workflow orchestration and final decision making.

---

# Orchestration Model

The solution combines several orchestration patterns.

### Sequential Processing

Validation → Recovery Planning → Approval → Reporting

### Parallel Specialist Assessment

Inventory, Alternate Supplier, Customer Impact, and Commercial Impact assessments execute independently before consolidation.

### Fan-In Consolidation

Recovery Planning Specialist consolidates specialist outputs into a single recommendation.

### Conditional Routing

Business rules determine routing based on inventory availability, supplier approval, customer priority, and commercial thresholds.

### Exception Handling

Failures trigger retries, reassessment, manual review, or management escalation as required.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| AI Platform | Microsoft Copilot Studio |
| Orchestration | Supervisor Agent |
| Specialist Layer | Child Agents |
| Business Logic | Custom Topics |
| Data Source | Excel Online (Business) |
| Reporting | Word Online (Business) |
| Communication | Outlook |
| Evaluation | Copilot Studio Evaluation |

---

# Benefits

The architecture provides:

- Enterprise-grade workflow orchestration
- Autonomous decision support
- Modular specialist agents
- Microsoft 365 integration
- Improved governance
- Faster disruption response
- Reduced manual effort
- Scalable AI architecture

---

# Architecture Version

**Version:** 1.0

**Status:** Completed
