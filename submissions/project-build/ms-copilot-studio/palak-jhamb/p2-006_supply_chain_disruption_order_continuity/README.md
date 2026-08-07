# Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System

## Project Overview

This project implements an **Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System** using **Microsoft Copilot Studio**.

The solution continuously monitors pending supply disruptions, validates disruption requests, coordinates multiple specialist AI agents, determines the optimal recovery strategy, generates recovery documentation, and notifies stakeholders—all with minimal human intervention.

The architecture follows a **hierarchical multi-agent orchestration pattern**, where a Supervisor Agent coordinates domain-specific child agents to ensure business continuity while complying with organizational policies.

---

# Objectives

The solution aims to:

- Detect new supply disruption requests automatically.
- Validate disruption information.
- Assess inventory impact.
- Evaluate alternate suppliers.
- Analyze customer and order impact.
- Evaluate commercial implications.
- Recommend the optimal recovery strategy.
- Generate recovery reports.
- Notify stakeholders.
- Maintain complete auditability throughout the assessment lifecycle.

---

# Solution Architecture

```
Recurring Trigger
        │
        ▼
Supply Continuity Supervisor
        │
        ▼
Disruption Intake & Validation
        │
        ├───────────────────────────────────────────────┐
        ▼               ▼               ▼               ▼
Inventory      Alternate Supplier   Customer Impact   Commercial
Specialist        Specialist          Specialist      Specialist
        │               │               │               │
        └───────────────┴───────────────┴───────────────┘
                        │
                        ▼
           Recovery Planning Specialist
                        │
                        ▼
       Reporting & Communication Specialist
                        │
                        ▼
         Word Report • Outlook Notification
```

---

# Technologies Used

- Microsoft Copilot Studio
- Microsoft Power Automate
- Microsoft Excel Online (Business)
- Microsoft Word Online (Business)
- Microsoft Outlook
- Microsoft 365

---

# Agent Architecture

## Supervisor Agent

**Supply Continuity Supervisor**

Responsibilities:

- Retrieve pending disruptions
- Validate disruption requests
- Invoke specialist agents
- Consolidate assessments
- Resolve conflicts
- Validate recovery strategy
- Determine approval requirements
- Generate final decision
- Trigger reporting
- Update disruption status

---

## Child Agents

### 1. Inventory Impact Specialist

Evaluates:

- Available to Promise (ATP)
- Inventory availability
- Shortage quantity
- Safety stock impact
- Inventory recommendations

---

### 2. Alternate Supplier Specialist

Evaluates:

- Approved suppliers
- Capacity
- Lead times
- Unit cost
- Supplier risk
- Alternate sourcing feasibility

---

### 3. Customer & Order Impact Specialist

Evaluates:

- Customer priority
- Strategic customers
- SLA commitments
- Revenue at risk
- Order impact
- Partial fulfillment constraints

---

### 4. Commercial Impact Specialist

Evaluates:

- Incremental procurement cost
- Cost premium
- Revenue exposure
- Approval requirements
- Commercial risk

---

### 5. Recovery Planning Specialist

Consolidates all specialist findings and recommends:

- Existing inventory usage
- Alternate supplier sourcing
- Expedite strategy
- Partial fulfillment
- Escalation
- Manual review

---

### 6. Reporting & Communication Specialist

Responsible for:

- Recovery report generation
- Stakeholder notifications
- Final communication

---

# Topics Implemented

## Topic 1

Disruption Intake & Validation

Performs:

- Record validation
- Mandatory field validation
- Status validation
- Business rule validation

---

## Topic 2

Recovery Strategy Resolution

Responsible for:

- Strategy validation
- Conflict resolution
- Strategy recommendation
- Decision precedence

---

## Topic 3

Approval, Exception & Selective Reassessment

Responsible for:

- Approval routing
- Manual review
- Retry logic
- Selective reassessment

---

# Autonomous Workflow

1. Recurring trigger starts execution.
2. Supervisor retrieves the oldest pending disruption.
3. Validation topic validates the disruption.
4. Supervisor invokes specialist agents in parallel.
5. Supervisor waits for all specialist responses.
6. Supervisor consolidates specialist findings.
7. Recovery Planning Specialist recommends a recovery strategy.
8. Supervisor validates the recommendation.
9. Reporting Specialist generates documentation.
10. Outlook notifications are sent.
11. Disruption status is updated.

---

# Orchestration Patterns

The solution demonstrates:

- Hierarchical Multi-Agent Orchestration
- Parallel Fan-Out
- Fan-In Consolidation
- Sequential Workflow
- Conditional Routing
- Retry Mechanism
- Fallback Handling
- Selective Reassessment

---

# Data Sources

The solution uses the following Excel tables:

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

Knowledge is intentionally limited to:

- Supply Continuity Supervisor
- Recovery Planning Specialist

All remaining specialist agents rely solely on structured business data and deterministic business rules.

---

# Business Rules

The system enforces:

- Mandatory disruption validation
- Approved supplier restrictions
- Inventory-first recovery
- Customer priority protection
- Commercial approval thresholds
- Retry before escalation
- Manual review for insufficient evidence

---

# Key Features

- Autonomous execution
- Multi-agent collaboration
- Domain-specific specialists
- Policy-driven decision making
- Automated reporting
- Automated notifications
- Recovery planning
- Approval management
- Exception handling
- Auditability

---

# Project Structure

```
README.md
architecture.md
solution-summary.md
supervisor-agent-design.md
specialist-agent-design.md
custom-topics.md
orchestration-patterns.md
autonomous-trigger.md
decision-rules.md
test-report.md
known-limitations.md
ai-usage-declaration.md
```

---

# Assumptions

- Excel Online contains valid business data.
- Microsoft 365 connectors are configured.
- Copilot Studio child agents are published.
- Word and Outlook connectors are authorized.
- The recurring trigger executes successfully.

---

# Limitations

- Decisions depend on available business data.
- Missing mandatory information results in Manual Review.
- External ERP integration is outside the current implementation scope.
- Human approvals are simulated according to the project requirements.

---



# Author

**Participant:** Palak

**Project:**
Autonomous Multi-Agent Supply Chain Disruption & Order Continuity System

**Platform:**
Microsoft Copilot Studio

