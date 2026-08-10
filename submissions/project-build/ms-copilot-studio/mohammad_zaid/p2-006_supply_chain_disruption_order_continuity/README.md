
# P2-006 — Autonomous Supply Chain Disruption & Order Continuity Response System

Agent link: [link](https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/20e9e7b7-6092-f111-b8dc-000d3af21e08/overview)

## Project Overview

This project implements an Autonomous Supply Chain Disruption & Order Continuity Response System using Microsoft Copilot Studio. The solution enables NovaSphere Technologies Pvt. Ltd. to automatically identify supply disruptions, evaluate their operational impact through multiple AI specialists, determine the most appropriate recovery strategy, and generate business reports while maintaining required approval boundaries.

The solution follows Microsoft's Multi-Agent Orchestration pattern using a Supervisor Agent that coordinates multiple specialized child agents, custom topics, event triggers, and Microsoft 365 connectors.

---

# Business Problem

Supply disruptions such as supplier delays, shipment delays, quality holds, supplier cancellations, material shortages, and partial shipments can significantly impact production schedules and customer commitments.

Traditionally, planners manually inspect multiple spreadsheets before deciding how to recover from a disruption.

This solution automates that assessment process while ensuring deterministic business rules, approval boundaries, and human oversight are preserved.

---

# Solution Architecture

The solution consists of:

- 1 Supervisor Agent
- 6 Specialist Child Agents
- 3 Custom Topics
- 1 Autonomous Recurrence Trigger
- Microsoft Excel Online (Business)
- Microsoft Word Online (Business)
- Microsoft Outlook
- NovaSphere Supply Continuity Policy Knowledge Base

The Supervisor Agent orchestrates the complete assessment lifecycle and delegates domain-specific analysis to specialist agents.

---

# Implemented Agents

## Supervisor Agent

**Supply Continuity Supervisor**

Responsible for:

- Receiving autonomous trigger events
- Coordinating orchestration
- Managing workflow state
- Invoking custom topics
- Delegating work to specialists
- Validating recovery strategy
- Authorizing reporting
- Updating disruption status
- Triggering stakeholder communication

---

## Specialist Agents

### Inventory Impact Specialist

Evaluates:

- Available inventory
- Safety stock
- Purchase orders
- Inventory shortages
- Recommended inventory actions

---

### Alternate Supplier Specialist

Evaluates:

- Approved alternate suppliers
- Supplier capacity
- Lead time
- Supplier risk
- Alternate sourcing feasibility

---

### Customer & Order Impact Specialist

Evaluates:

- Customer commitments
- Strategic customers
- SLA protected orders
- Revenue exposure
- Customer prioritization

---

### Commercial Impact Specialist

Evaluates:

- Cost premium
- Commercial approval
- Financial impact
- Recovery cost
- Commercial risk

---

### Recovery Planning Specialist

Consolidates all specialist findings and recommends:

- Recovery strategy
- Residual risk
- Required approvals
- Internal actions
- Customer actions

---

### Reporting & Communication Specialist

Responsible for:

- Creating Word reports
- Sending Outlook notifications
- Preparing final response summary

---

# Custom Topics

## 1. Disruption Intake & Validation

Responsibilities:

- Read pending disruption
- Validate mandatory fields
- Verify disruption integrity
- Prevent duplicate processing
- Move disruption to "In Assessment"

---

## 2. Recovery Strategy Resolution

Responsibilities:

- Execute specialist assessments
- Perform logical fan-in
- Invoke Recovery Planning Specialist
- Consolidate findings
- Determine recovery recommendation

---

## 3. Approval, Exception & Selective Reassessment

Responsibilities:

- Evaluate approval requirements
- Handle exception scenarios
- Control reassessment logic
- Manage escalation
- Return workflow decision

---

# Autonomous Trigger

The solution uses a Copilot Studio Recurrence Trigger that:

- Periodically monitors pending disruption requests
- Retrieves the oldest pending disruption
- Starts orchestration automatically
- Processes one disruption per execution cycle

---

# Microsoft Connectors Used

- Excel Online (Business)
- Word Online (Business)
- Outlook
- Microsoft Copilot Studio Knowledge Base

---

# Excel Tables Used

- DisruptionRequestsTable
- InventoryTable
- PurchaseOrdersTable
- CustomerOrdersTable
- AlternateSuppliersTable
- SuppliersTable
- SKUMasterTable
- RecoveryRulesTable
- StakeholdersTable

---

# Orchestration Patterns Demonstrated

- Sequential Orchestration
- Logical Parallel Fan-Out/Fan-In
- Hierarchical Supervisor Pattern
- Conditional Routing
- Conflict Resolution
- Retry/Fallback
- Selective Reassessment

---

# Business Rules

The implementation enforces:

- Deterministic decision making
- Customer priority protection
- Commercial approval thresholds
- Supplier approval restrictions
- Inventory availability validation
- Quality hold restrictions
- Human approval boundaries

---

# Final Outputs

The completed orchestration produces:

- Recovery Strategy
- Final Risk Classification
- Required Approvals
- Orders Protected
- Orders Remaining At Risk
- Supply Disruption Response Report
- Updated Excel Status
- Conditional Outlook Notification

---

# Technologies Used

- Microsoft Copilot Studio
- Microsoft Excel Online (Business)
- Microsoft Word Online (Business)
- Microsoft Outlook
- Microsoft 365
- OneDrive for Business

---

# Project Structure

```
p2-006_supply_chain_disruption_order_continuity/

│── README.md
│── solution-summary.md
│── architecture.md
│── orchestration-patterns.md
│── supervisor-agent-design.md
│── specialist-agent-design.md
│── custom-topics.md
│── autonomous-trigger.md
│── decision-rules.md
│── test-report.md
│── known-limitations.md
│── ai-usage-declaration.md
│
├── data/
│   └── dataset-notes.md
│
└── screenshots/
```

---

# Outcome

The solution demonstrates an enterprise-grade autonomous multi-agent orchestration system capable of detecting supply disruptions, coordinating specialized assessments, applying deterministic business rules, generating recovery recommendations, producing reports, and supporting human decision-making while adhering to Microsoft Copilot Studio orchestration principles.
