# P2-006 – Supply Chain Disruption Order Continuity

## Overview

**Project ID:** P2-006

**Project Name:** Supply Chain Disruption Order Continuity

**Platform:** Microsoft Copilot Studio

**Participant:** Mohammad Anas

The Supply Chain Disruption Order Continuity solution is an autonomous multi-agent system developed using Microsoft Copilot Studio. The solution continuously monitors supply chain disruption requests, performs comprehensive disruption impact assessments, determines appropriate recovery strategies, generates executive-ready continuity reports, updates disruption lifecycle information, and notifies stakeholders without requiring manual intervention.

The implementation follows the autonomous orchestration model defined in the Project Requirements Document (PRD) by separating responsibilities between a Supervisor Agent and specialized child agents. Each specialist evaluates a specific operational domain while the Supervisor coordinates the overall workflow and determines the final disruption outcome.

---

# Business Objective

The objective of this project is to minimize operational disruption caused by supplier or inventory issues by autonomously evaluating disruption requests and recommending an appropriate business continuity strategy.

The solution enables organizations to:

- Detect pending supply chain disruptions automatically.
- Assess inventory impact.
- Evaluate alternate supplier availability.
- Assess customer and order impact.
- Evaluate commercial and financial exposure.
- Recommend the optimal recovery strategy.
- Generate standardized assessment reports.
- Notify stakeholders automatically.
- Maintain disruption lifecycle tracking.

---

# Solution Architecture

The solution follows a hierarchical multi-agent architecture consisting of one Supervisor Agent and six specialist child agents.

## Supervisor Agent

- Anas_Supply_Chain_Continuity_Governance

The Supervisor coordinates the complete disruption assessment workflow and is responsible for:

- Workflow orchestration
- Specialist coordination
- Recovery validation
- Approval management
- Report authorization
- Stakeholder communication authorization
- Disruption lifecycle management

---

## Specialist Agents

The implementation includes the following specialist agents:

1. Inventory Impact Specialist
2. Alternate Supplier Specialist
3. Customer & Order Impact Specialist
4. Commercial Impact Specialist
5. Recovery Planning Specialist
6. Reporting & Communication Specialist

Each specialist performs a single responsibility and returns structured findings to the Supervisor.

---

# Custom Topics

The solution implements three reusable custom topics.

## 1. Disruption Intake & Validation

Responsible for:

- Retrieving pending disruption requests
- Validating disruption data
- Updating disruption status to "In Assessment"

---

## 2. Recovery Strategy Resolution

Responsible for:

- Coordinating specialist assessments
- Consolidating findings
- Validating recovery strategy
- Preparing recovery recommendations

---

## 3. Approval & Exception Management

Responsible for:

- Processing approval requirements
- Handling policy exceptions
- Managing selective reassessment
- Authorizing reporting
- Finalizing disruption lifecycle

---

# Autonomous Trigger

The solution is initiated through a Recurrence Trigger configured in Microsoft Copilot Studio.

The trigger periodically checks for pending disruption requests and automatically starts the Supervisor workflow without requiring user interaction.

Only one pending disruption request is processed during each execution.

---

# Microsoft 365 Components Used

The solution integrates with Microsoft 365 services including:

- Microsoft Excel Online (Business)
- Microsoft Word Online (Business)
- Microsoft Outlook
- Microsoft Graph

---

# Knowledge Sources

The implementation uses the following knowledge source:

- NovaSphere Supply Continuity Policy

The policy is used by the Supervisor and specialist agents to ensure that recovery decisions follow organizational governance and business continuity requirements.

---

# Excel Data Sources

The solution operates on the following operational datasets:

- Disruption Requests
- Suppliers
- SKU Master
- Inventory
- Purchase Orders
- Customer Orders
- Alternate Suppliers
- Recovery Rules
- Stakeholders

---

# Workflow

The high-level execution flow is:

```text
Recurrence Trigger
        │
        ▼
Disruption Intake & Validation
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
Recovery Strategy Resolution
        │
        ▼
Approval & Exception Management
        │
        ▼
Reporting & Communication Specialist
        │
        ▼
Update Disruption Status
        │
        ▼
Workflow Complete
```

---

# Key Features

- Autonomous workflow execution
- Multi-agent orchestration
- Structured specialist assessments
- Policy-driven recovery planning
- Executive approval handling
- Selective reassessment
- Microsoft Word report generation
- Outlook stakeholder notifications
- Automated disruption lifecycle updates
- Enterprise governance compliance


---

# Technologies Used

- Microsoft Copilot Studio
- Microsoft Excel Online (Business)
- Microsoft Word Online (Business)
- Microsoft Outlook
- Microsoft 365 Connectors

---

# Author

**Mohammad Anas**

---

# License

This project has been developed exclusively for academic training and evaluation purposes as part of the Microsoft Copilot Studio Enterprise Agent Development Program.