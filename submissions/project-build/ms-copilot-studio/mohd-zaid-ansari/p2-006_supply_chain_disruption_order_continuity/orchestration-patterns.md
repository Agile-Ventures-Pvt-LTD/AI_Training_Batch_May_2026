# Orchestration Patterns

## Overview

The **Supply Chain Continuity Management System** follows a **Supervisor–Specialist Multi-Agent Orchestration Pattern** implemented using **Microsoft Copilot Studio**.

Instead of allowing each agent to communicate independently, a single **Mohd Zaid Supply Continuity Supervisor** controls the complete workflow. This ensures consistent decision-making, modular design, and easier maintenance.

The orchestration combines **Autonomous Triggering**, **Topic-Based Workflow Control**, **Specialist Agent Delegation**, and **Excel Online (Business) Tool Integration**.

---

# Orchestration Model

```
                    Recurrence Trigger
                            │
                            ▼
             Supply Continuity Supervisor
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
  Supervisor Topics    Specialist Agents    Excel Tools
        │                   │                    │
        └───────────────┬───┴────────────────────┘
                        │
                        ▼
               Final Recovery Decision
                        │
                        ▼
              Update Disruption Status
```

---

# Primary Orchestration Pattern

The project uses a **Hierarchical Supervisor Pattern**.

The **Supply Continuity Supervisor** acts as the single orchestration layer responsible for:

- Starting the workflow
- Managing execution order
- Delegating business analysis
- Coordinating specialist agents
- Invoking reusable topics
- Accessing Excel tools
- Producing the final response

The Supervisor never performs specialist analysis directly.

---

# Pattern 1 – Autonomous Trigger Pattern

## Purpose

Automatically start the workflow without requiring user interaction.

### Component

```
Recurrence Trigger
```

Responsibilities

- Execute according to schedule.
- Start the Supervisor Agent.
- Process one disruption request per execution.

---

# Pattern 2 – Supervisor Orchestration Pattern

The Supervisor coordinates the entire workflow.

Responsibilities

- Receive trigger event.
- Invoke workflow topics.
- Call specialist agents.
- Collect assessment results.
- Select recovery strategy.
- Generate reports.
- Complete the workflow.

The Supervisor acts as the single control point.

---

# Pattern 3 – Topic-Based Workflow Pattern

Reusable workflow stages are implemented as Supervisor Topics.

Topics simplify orchestration by grouping related business activities.

---

## Topic 1

### /Disruption Intake & Validation

Purpose

- Retrieve disruption information.
- Validate request completeness.
- Verify purchase order information.

Tools

- /Get Pending Disruption
- /Get Disruption Details
- /Get Purchase Order

Output

Validated disruption request.

---

## Topic 2

### /Recovery Strategy Resolution

Purpose

- Compare recovery strategies.
- Evaluate recommendations.
- Select the preferred recovery option.

Output

Recommended recovery strategy.

---

## Topic 3

### /Approval Exception Reassessment

Purpose

- Validate approval rules.
- Verify escalation requirements.
- Ensure policy compliance.

Tool

- /Get Recovery Rules

Output

Approval decision requirements.

---

# Pattern 4 – Specialist Delegation Pattern

The Supervisor delegates business analysis to specialist agents.

```
Supervisor
     │
     ├────────► Inventory Specialist
     │
     ├────────► Alternate Supplier Specialist
     │
     ├────────► Customer & Order Specialist
     │
     ├────────► Commercial Specialist
     │
     ├────────► Recovery Planning Specialist
     │
     └────────► Reporting Specialist
```

Each specialist performs one business function only.

---

# Pattern 5 – Parallel Assessment Pattern

The following agents perform independent assessments and can execute in parallel:

- /Inventory Impact Specialist
- /Alternate Supplier Specialist
- /Customer & Order Impact Specialist
- /Commercial Impact Specialist

The Supervisor waits until all assessments are completed before continuing.

```
                    Supervisor
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Inventory      Alternate Supplier   Customer Impact
        │               │                │
        └───────────────┼────────────────┘
                        │
                        ▼
             Commercial Impact Specialist
                        │
                        ▼
           Recovery Planning Specialist
```

---

# Pattern 6 – Tool Invocation Pattern

Each agent retrieves data through dedicated Excel Online (Business) tools.

No agent accesses Excel directly.

```
Agent
   │
   ▼
Excel Business Tool
   │
   ▼
Excel Table
```

Examples

| Agent | Tool | Excel Table |
|--------|------|-------------|
| Supervisor | /Get Pending Disruption | DisruptionRequestsTable |
| Supervisor | /Get Disruption Details | DisruptionRequestsTable |
| Supervisor | /Get Purchase Order | PurchaseOrdersTable |
| Inventory Specialist | /Get Inventory | InventoryTable |
| Alternate Supplier Specialist | /Get Supplier | SuppliersTable |
| Alternate Supplier Specialist | /Get Alternate Supplier | AlternateSuppliersTable |
| Customer Specialist | /Get Customer Orders | CustomerOrdersTable |
| Reporting Specialist | /Get Stakeholders | StakeholdersTable |

---

# Pattern 7 – Decision Aggregation Pattern

The Supervisor combines outputs from multiple specialist agents before selecting a recovery strategy.

Inputs include:

- Inventory assessment
- Supplier assessment
- Customer impact
- Commercial impact

These are passed to:

```
/Recovery Planning Specialist
```

The resulting recovery options are then reviewed in:

```
/Recovery Strategy Resolution
```

---

# Pattern 8 – Approval Gate Pattern

Business approvals are isolated from recovery planning.

Workflow

```
Recovery Planning
        │
        ▼
Recovery Strategy Resolution
        │
        ▼
Approval Exception Reassessment
        │
        ▼
Get Recovery Rules
```

This separation ensures that recovery recommendations are evaluated before approval policies are applied.

---

# Pattern 9 – Reporting Pattern

Once a recovery strategy is selected and approval requirements are determined, the Supervisor invokes:

```
/Reporting & Communication Specialist
```

Outputs

- Executive Summary
- Stakeholder Communication
- Recovery Recommendation
- Business Impact Summary

---

# Pattern 10 – Controlled Update Pattern

Only one tool is permitted to modify operational data.

```
/Update Disruption Status
```

Purpose

- Update disruption workflow status.
- Record workflow completion.
- Mark requests for manual review when necessary.

This pattern ensures controlled write access to the Excel workbook.

---

# Complete Execution Sequence

```
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
┌────────────────────────────────────────────┐
│ Parallel Specialist Assessment             │
│                                            │
│ /Inventory Impact Specialist               │
│ /Alternate Supplier Specialist             │
│ /Customer & Order Impact Specialist        │
│ /Commercial Impact Specialist              │
└────────────────────────────────────────────┘
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

# Benefits of the Orchestration Design

- Autonomous workflow execution
- Clear separation of responsibilities
- Reusable workflow topics
- Modular specialist agents
- Scalable architecture
- Controlled data access
- Centralized orchestration
- Easier maintenance and future enhancements
- Improved traceability and governance
- Consistent decision-making across the workflow

---

# Design Principles

The orchestration follows these principles:

- **Single Orchestrator:** Only the Supervisor controls workflow execution.
- **Delegation:** Specialist agents perform domain-specific analysis.
- **Reusability:** Common workflow stages are implemented as topics.
- **Tool Abstraction:** All data access is through Excel Online (Business) tools.
- **Controlled Updates:** Only designated update tools modify operational data.
- **Autonomy:** The Recurrence Trigger initiates workflow execution without user intervention.
- **Sequential Governance with Parallel Analysis:** Validation and approval steps are sequential, while independent impact assessments can execute in parallel before results are aggregated.