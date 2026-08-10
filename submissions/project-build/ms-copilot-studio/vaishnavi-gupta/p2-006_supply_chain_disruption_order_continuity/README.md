# P2-006: Autonomous Supply Chain Disruption & Order Continuity Response System

## Project Information

| Item | Details |
|--------|--------|
| Project ID | P2-006 |
| Project Name | Autonomous Supply Chain Disruption & Order Continuity Response System |
| Platform | Microsoft Copilot Studio |
| Architecture | Autonomous Multi-Agent System |
| Orchestration Patterns | Sequential, Parallel Fan-Out/Fan-In, Hierarchical, Conditional Routing, Conflict Resolution, Selective Reassessment, Retry/Fallback |
| Organization | NovaSphere Technologies Pvt. Ltd. |
| Version | 1.0 |

---

# Executive Summary

This project implements an autonomous supply chain disruption management solution using Microsoft Copilot Studio. The system continuously monitors disruption requests, validates records, performs multi-agent assessments, determines business impact, recommends recovery strategies, manages approval workflows, generates reports, updates operational records, and communicates outcomes to stakeholders.

The solution leverages Microsoft's recommended Supervisor-Subagent orchestration model, where a central Supply Continuity Supervisor Agent coordinates specialized child agents responsible for inventory analysis, supplier evaluation, customer impact analysis, commercial risk assessment, recovery planning, and communication management. The design follows strict governance requirements and prevents autonomous execution of activities requiring human approval. 【1-65f028】

---

# Business Scenario

NovaSphere Technologies Pvt. Ltd. relies on multiple suppliers for manufacturing components used across customer products. Supply chain disruptions can occur due to:

- Supplier delays
- Shipment delays
- Partial shipments
- Supplier cancellations
- Material shortages
- Quality holds
- Capacity constraints

These disruptions may affect:

- Available inventory
- Open purchase orders
- Customer commitments
- Strategic customer agreements
- SLA-protected orders
- Production schedules
- Procurement costs
- Alternate supplier requirements

The organization requires an autonomous solution capable of analyzing disruptions and proposing continuity strategies while maintaining clear human approval boundaries and operational governance. 

---

# Project Objectives

The solution must autonomously:

- Detect unprocessed disruptions
- Validate disruption records
- Prevent duplicate processing
- Identify affected SKUs
- Identify impacted purchase orders
- Analyze customer order impact
- Assess inventory availability
- Evaluate alternate supplier options
- Assess customer and SLA risks
- Evaluate commercial implications
- Consolidate specialist findings
- Resolve conflicting recommendations
- Recommend continuity strategies
- Route approval requests when required
- Support selective reassessment
- Handle tool and agent failures
- Generate Word reports
- Update disruption status records
- Send conditional Outlook notifications
- Escalate cases requiring human intervention


---

# Solution Architecture

## High-Level Flow

```text
Recurrence Trigger
        │
        ▼
Supply Continuity Supervisor
        │
        ▼
Disruption Intake & Validation
        │
        ▼
Identify SKU, PO & Customer Orders
        │
 ┌──────┼────────┬────────┬────────┐
 ▼      ▼        ▼        ▼
Inventory  Alternate  Customer  Commercial
Specialist Supplier   Impact    Impact
           Specialist Specialist Specialist
 └──────┴────────┴────────┴────────┘
                    │
                    ▼
              Fan-In Stage
                    │
                    ▼
     Recovery Planning Specialist
                    │
                    ▼
          Supervisor Validation
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Approved     Awaiting Approval  Escalation
      │             │             │
      └─────────────┴─────────────┘
                    │
                    ▼
      Reporting & Communication
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
      Word Report          Outlook Email
                    │
                    ▼
             Excel Update
```

【1-65f028】

---

# Supervisor Agent Design

## Agent Name

**Supply Continuity Supervisor**

### Responsibilities

The Supervisor owns the entire orchestration lifecycle and is responsible for:

- Trigger handling
- Pending disruption selection
- Validation invocation
- State management
- Specialist coordination
- Fan-out orchestration
- Fan-in consolidation
- Conflict resolution
- Recovery strategy validation
- Approval routing
- Selective reassessment decisions
- Final risk classification
- Report authorization
- Communication authorization
- Final state updates

The Supervisor never fabricates missing specialist evidence and cannot bypass required approval rules. 

---

# Specialist Agents

## 1. Inventory Impact Specialist

### Purpose

Determine available inventory and assess whether demand can be protected until supply recovery.

### Data Sources

- SKU Master
- Inventory
- Purchase Orders
- Disruption Requests

### Calculations

```text
Available to Promise (ATP)
=
On Hand
- Reserved
+ Inbound Within 7 Days
- Quality Hold
```

### Outputs

- AvailableToPromise
- SafetyStock
- DemandUntilRecovery
- ShortageQty
- QualityHoldImpact
- InventoryAssessment
- BlockingIssue
- RecommendedInventoryAction
- Confidence


---

## 2. Alternate Supplier Specialist

### Purpose

Evaluate alternate supplier availability and suitability.

### Data Sources

- Alternate Suppliers
- Suppliers
- SKU Master
- Disruption Requests

### Guardrail

Unapproved suppliers can never be selected autonomously as the final recovery source.

### Outputs

- AlternateAvailable
- SupplierID
- ApprovedStatus
- AvailableCapacity
- StandardLeadTime
- ExpediteLeadTime
- AlternateUnitCost
- CanMeetRequiredDate
- QualificationRestriction
- RecommendedSupplierAction
- Confidence


---

## 3. Customer & Order Impact Specialist

### Purpose

Assess customer commitments and prioritize demand.

### Priority Order

```text
Strategic + SLA Protected
        ↓
Priority
        ↓
Standard
```

### Outputs

- AffectedOrderCount
- StrategicOrdersAtRisk
- SLAOrdersAtRisk
- RevenueAtRisk
- EarliestRequiredDate
- PartialFulfillmentConstraints
- RankedAffectedOrders
- CustomerImpactClassification
- RecommendedCustomerAction
- Confidence


---

## 4. Commercial Impact Specialist

### Purpose

Analyze financial implications of recovery options.

### Approval Rules

- Cost Premium > 15% → Finance Business Partner Approval
- Expedite Premium > 10% → Supply Chain Director Approval

### Outputs

- CostPremiumPct
- IncrementalCost
- RevenueExposure
- ExpeditePremiumPct
- CommercialRisk
- ApprovalRequired
- RequiredApprover
- RecommendedCommercialAction
- Confidence


---

## 5. Recovery Planning Specialist

### Purpose

Generate the optimal recovery strategy based on consolidated specialist findings.

### Permitted Strategies

- Use existing stock
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

The agent must not:

- Place purchase orders
- Approve suppliers
- Cancel customer orders
- Promise delivery dates
- Approve commercial spend

### Outputs

- ProposedStrategy
- StrategyComponents
- OrdersProtected
- OrdersRemainingAtRisk
- RequiredApprovals
- ResidualRisk
- RequiredCustomerAction
- RequiredInternalActions
- Rationale
- Confidence


---

## 6. Reporting & Communication Specialist

### Responsibilities

#### Microsoft Word

Generate a Supply Disruption Response Report containing:

- Disruption information
- Inventory analysis
- Customer impact
- Alternate supplier assessment
- Commercial assessment
- Recovery strategy
- Required approvals
- Orders protected
- Orders at risk
- Revenue exposure
- Residual risk
- Evidence limitations
- Final supervisor status

#### Microsoft Outlook

Send notifications after supervisor authorization based on workflow state.


---

# Orchestration Patterns

## Sequential Pattern

The following stages execute strictly in sequence:

```text
Trigger
→ Validation
→ Scope Identification
→ Specialist Assessments
→ Fan-In
→ Recovery Planning
→ Supervisor Decision
→ Approval Handling
→ Report Generation
→ Excel Update
→ Notification
```

Dependencies ensure that no downstream process executes before required upstream validations and decisions are completed. 【1-65f028】

---

## Parallel Fan-Out / Fan-In

### Fan-Out

The Supervisor independently invokes:

- Inventory Specialist
- Alternate Supplier Specialist
- Customer Impact Specialist
- Commercial Impact Specialist

### Fan-In

The Supervisor waits for all required responses before:

- Consolidating results
- Performing conflict analysis
- Starting recovery planning


---

## Hierarchical Pattern

```text
Supply Continuity Supervisor
│
├── Inventory Specialist
├── Alternate Supplier Specialist
├── Customer Impact Specialist
├── Commercial Impact Specialist
├── Recovery Planning Specialist
└── Reporting Specialist
```

The Supervisor exclusively owns:

- Final strategy approval
- Conflict resolution
- Risk classification
- Approval routing
- Communication authorization


---

## Conditional Routing

Examples include:

### Branch A

Inventory sufficient

```text
Use Existing Inventory
```

### Branch B

Partial inventory availability

```text
Protect Priority Orders
+
Evaluate Alternate Supply
```

### Branch C

Approved alternate available

```text
Alternate Supply Evaluation
```

### Branch D

Only unapproved alternate available

```text
Manual Review
+
Supplier Qualification
```

### Branch E

No viable recovery path

```text
Management Escalation
```


---

## Conflict Resolution

Decision precedence:

```text
1. Safety & Quality Constraints
2. Strategic/SLA Commitments
3. Supplier Approval Restrictions
4. Inventory Availability
5. Commercial Approval Requirements
6. Cost Optimization
7. Customer Convenience
```

Conflicting specialist outputs are never averaged.


---

## Retry and Fallback

Rules:

- Retry failed specialist once.
- Maximum execution attempts = 2.
- If failure persists:
  - Mark as Insufficient Evidence.
  - Block unsupported recommendations.
  - Escalate when necessary.


---

## Selective Reassessment

When source data changes:

```text
Detect Change
       ↓
Identify Stale Assessment
       ↓
Re-run Only Impacted Specialists
       ↓
Fan-In Updated Results
       ↓
Recalculate Strategy
```

Maximum reassessment cycles: **2**

After two unsuccessful reassessments:

```text
Manual Review
```

【1-65f028】

---

# State Management

Allowed states:

| State | Description |
|---------|---------|
| Pending | Awaiting assessment |
| In Assessment | Active assessment |
| Awaiting Approval | Human approval required |
| Recovery Plan Proposed | Proposed valid strategy |
| Customer Action Required | Customer decision needed |
| Management Escalation | No safe autonomous resolution |
| Insufficient Evidence | Missing information |
| Manual Review | Escalation after automation limit |
| Completed | Fully processed |

Invalid state transitions are blocked by the Supervisor. 【1-65f028】

---

# Data Sources

The solution uses Excel Online (Business) tables hosted in SharePoint or OneDrive.

## Tables

- DisruptionRequestsTable
- SuppliersTable
- SKUMasterTable
- InventoryTable
- PurchaseOrdersTable
- CustomerOrdersTable
- AlternateSuppliersTable
- RecoveryRulesTable
- StakeholdersTable

【1-65f028】

---

# Risk Classification

The final risk level must be:

- Low
- Medium
- High
- Critical

Every High and Critical classification includes detailed rationale supported by specialist evidence. 【1-65f028】

---

# Reporting

## Word Report

The generated report contains:

- Disruption details
- Inventory impact findings
- Customer impact findings
- Alternate supplier analysis
- Commercial analysis
- Recovery recommendation
- Approvals required
- Residual risk
- Evidence limitations
- Final supervisor decision

## Outlook Notification

Notifications are sent only after supervisor authorization and are conditional based on the final workflow state. 【1-65f028】

---

# Failure Handling

Handled scenarios include:

- No pending disruption
- Duplicate processing attempt
- Missing supplier
- Missing SKU
- Missing purchase order
- Validation failures
- Specialist failures
- Excel read failures
- Excel update failures
- Word generation failures
- Outlook failures
- Missing approver
- Reassessment limit reached

The system never reports successful completion for failed actions. 【1-65f028】

---

# Testing Coverage

The implementation validates:

- Sequential orchestration
- Parallel fan-out/fan-in
- Hierarchical orchestration
- Conditional routing
- Conflict resolution
- Retry/fallback handling
- Selective reassessment
- Autonomous trigger execution
- Approval routing
- Reporting workflow

A minimum of 18 documented test cases are executed to satisfy project requirements. 【1-65f028】

---

# Technologies Used

- Microsoft Copilot Studio
- Copilot Studio Event Triggers
- Copilot Studio Topics
- Copilot Studio Child Agents
- Copilot Studio Generative Orchestration
- Excel Online (Business)
- Word Online (Business)
- Outlook Connector
- OneDrive for Business
- SharePoint Online


---

# Repository Structure

```text
p2-006_supply_chain_disruption_order_continuity/
│
├── README.md
├── solution-summary.md
├── architecture.md
├── orchestration-patterns.md
├── supervisor-agent-design.md
├── specialist-agent-design.md
├── custom-topics.md
├── autonomous-trigger.md
├── decision-rules.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
│
├── data/
│   └── dataset-notes.md
│
└── screenshots/
    ├── supervisor-agent.png
    ├── child-agents.png
    ├── recurrence-trigger.png
    ├── intake-validation-topic.png
    ├── fan-out-specialists.png
    ├── fan-in-consolidation.png
    ├── recovery-strategy-topic.png
    ├── approval-reassessment-topic.png
    ├── excel-tools.png
    ├── word-tool.png
    ├── outlook-tool.png
    └── final-response.png
```


---

# Acceptance Criteria

The project is considered complete when:

- Supervisor Agent exists
- Four or more specialist agents exist
- Generative orchestration is enabled
- Recurrence trigger is configured
- Pending disruptions are autonomously processed
- Duplicate processing is prevented
- Validation topic is implemented
- Fan-out/fan-in orchestration is demonstrated
- Hierarchical delegation is demonstrated
- Recovery strategy resolution exists
- Approval routing is implemented
- Selective reassessment is implemented
- Retry/fallback behavior is implemented
- Unapproved supplier protection is enforced
- Quality hold inventory is excluded
- Final risk classification is generated
- Word reports are generated
- Outlook notifications are conditional
- Excel updates are completed
- Minimum testing requirements are fulfilled


---

# Author

**Vaishnavi Gupta**

Microsoft Copilot Studio Project Build

Project ID: P2-006  
Project Name: Autonomous Supply Chain Disruption & Order Continuity Response System