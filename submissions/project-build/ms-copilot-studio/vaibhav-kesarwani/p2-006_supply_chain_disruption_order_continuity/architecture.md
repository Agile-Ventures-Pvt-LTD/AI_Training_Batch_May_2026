# System architecture

## NovaSphere supply continuity autonomous multi-agent system

## Architecture overview

The NovaSphere Supply Continuity System is a hierarchical multi-agent orchestration platform built using Microsoft Copilot Studio and Power Automate.

The architecture follows a **Supervisor → Specialist Child Agent** pattern where a single Supervisor Agent coordinates multiple domain-specific specialists, consolidates independent assessments, applies deterministic policy rules, manages approvals, and produces the final operational response.

The system is event-driven and autonomously processes supply disruptions without requiring user initiation.

## High-level architecture

```text
                    Microsoft Copilot Studio

                          Recurrence Trigger
                                 │
                                 ▼
                 Supply Continuity Supervisor Agent
                                 │
                ─────────────────┼─────────────────
                                 │
                                 ▼
         Disruption Intake & Validation Specialist
                                 │
                                 ▼
    Scope Identification & Order Discovery Specialist
                                 │
                  Parallel Specialist Execution
                                 │
        ┌──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
 Inventory Impact   Alternate      Customer &     Commercial
   Specialist       Supplier       Order Impact      Impact
                    Specialist      Specialist      Specialist
        └──────────────┴──────────────┴──────────────┴──────────────┘
                                 │
                                 ▼
                     Supervisor Fan-In Consolidation
                                 │
                                 ▼
                  Recovery Planning Specialist
                                 │
                                 ▼
             Recovery Strategy Resolution Specialist
                                 │
                                 ▼
 Approval, Exception & Selective Reassessment Specialist
                                 │
                                 ▼
        Reporting & Communication Specialist
                                 │
                                 ▼
                     Microsoft Power Automate
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼
    Word Report    Excel Update    Outlook Notification
```

## Architectural principles

### Hierarchical orchestration

The Supervisor Agent owns orchestration and governance.

Specialist agents own domain-specific analysis.

The Supervisor never performs specialist responsibilities directly.

### Deterministic policy enforcement

Final recovery decisions are based on deterministic business rules rather than unconstrained generative reasoning.

### Parallel execution

Independent specialist assessments execute concurrently to reduce assessment latency.

### Controlled fan-in

Recovery planning begins only after required specialist outputs have been consolidated.

### Approval governance

Human approval boundaries cannot be bypassed.

### Selective reassessment

Only stale specialist assessments are rerun when operational conditions change.

## Supervisor responsibilities

The Supervisor Agent controls the complete disruption lifecycle.

### Orchestration

* trigger management,
* disruption selection,
* specialist invocation,
* parallel coordination,
* fan-in consolidation,
* conflict detection,
* recovery validation,
* reporting authorization.

### Governance

* approval routing,
* reassessment control,
* state transitions,
* retry management,
* evidence validation,
* audit traceability.

### Execution control

* process one disruption per cycle,
* prevent duplicate processing,
* preserve deterministic execution order,
* authorize final outputs.

## Child-agent architecture

### 1. Disruption Intake & Validation Specialist

Purpose:

Validate disruption integrity before operational assessment.

Responsibilities:

* supplier validation,
* SKU validation,
* purchase-order validation,
* relationship validation,
* duplicate detection,
* data completeness validation.

Outputs:

* ValidationStatus
* ValidationReason
* DuplicateDetected
* Validated identifiers

### 2. Scope Identification & Order Discovery Specialist

Purpose:

Identify the complete operational impact of the disruption.

Responsibilities:

* affected customer orders,
* total demand,
* earliest required date,
* strategic exposure,
* SLA exposure,
* order discovery.

Outputs:

* AffectedOrders
* TotalAffectedDemand
* StrategicOrderCount
* SLAOrderCount
* EarliestRequiredDate

### 3. Inventory Impact Specialist

Purpose:

Evaluate inventory protection capability.

Responsibilities:

* available-to-promise,
* shortage estimation,
* safety-stock consumption,
* quality-hold exclusion,
* inventory sufficiency.

ATP formula:

ATP = On Hand - Reserved + Inbound Within 7 Days - Quality Hold

Outputs:

* AvailableToPromise
* ShortageQty
* InventoryAssessment
* QualityHoldImpact

### 4. Alternate Supplier Specialist

Purpose:

Evaluate alternate sourcing feasibility.

Responsibilities:

* approved supplier validation,
* capacity evaluation,
* lead-time evaluation,
* timing feasibility,
* qualification restrictions.

Mandatory restriction:

Unapproved suppliers cannot be autonomously selected.

Outputs:

* AlternateAvailable
* ApprovedStatus
* CanMeetRequiredDate
* RecommendedSupplierAction

### 5. Customer & Order Impact Specialist

Purpose:

Evaluate customer commitment risk.

Responsibilities:

* strategic customer protection,
* SLA exposure,
* revenue exposure,
* order prioritization,
* partial fulfillment constraints.

Priority order:

1. Strategic + SLA
2. Strategic
3. Priority
4. Standard

Outputs:

* RevenueAtRisk
* StrategicOrdersAtRisk
* SLAOrdersAtRisk
* RankedAffectedOrders

### 6. Commercial Impact Specialist

Purpose:

Evaluate financial recovery impact.

Responsibilities:

* cost premiums,
* expedite premiums,
* incremental procurement cost,
* approval requirements.

Approval thresholds:

* Cost premium >15% → Finance Business Partner
* Expedite premium >10% → Supply Chain Director

Outputs:

* CostPremiumPct
* IncrementalCost
* ApprovalRequired
* RequiredApprover

### 7. Recovery Planning Specialist

Purpose:

Propose recovery strategies using consolidated specialist evidence.

Responsibilities:

* strategy formulation,
* inventory utilization,
* alternate sourcing,
* combined recovery planning,
* residual risk evaluation.

Outputs:

* ProposedStrategy
* StrategyComponents
* OrdersProtected
* ResidualRisk

### 8. Recovery Strategy Resolution Specialist

Purpose:

Resolve competing specialist recommendations.

Responsibilities:

* policy precedence,
* conflict resolution,
* strategy validation,
* final risk classification,
* final status determination.

Outputs:

* FinalStrategy
* StrategyStatus
* FinalRisk
* ResolutionRationale

### 9. Approval, Exception & Selective Reassessment Specialist

Purpose:

Manage approval routing and reassessment.

Responsibilities:

* approval determination,
* approver identification,
* selective reassessment,
* retry control,
* manual review routing.

Maximum reassessment cycles:

2

Outputs:

* ReassessmentRequired
* SpecialistsToReassess
* UpdatedStrategyStatus

### 10. Reporting & Communication Specialist

Purpose:

Prepare final reporting outputs.

Responsibilities:

* executive summary,
* report preparation,
* notification determination,
* final status recommendation.

Outputs:

* ExecutiveSummary
* NotificationRecipients
* RecommendedFinalStatus

## Data architecture

### Primary data source

Excel Online (Business)

Workbook:

P2-006_Supply_Chain_Continuity_Lab_Data.xlsx

### Operational tables

| Table               | Purpose              |
| ------------------- | -------------------- |
| Disruption_Requests | Trigger source       |
| Suppliers           | Supplier master      |
| SKU_Master          | Product master       |
| Inventory           | Inventory records    |
| Purchase_Orders     | Inbound supply       |
| Customer_Orders     | Customer commitments |
| Alternate_Suppliers | Alternate sourcing   |
| Recovery_Rules      | Policy thresholds    |
| Stakeholders        | Notification routing |

## Tool-scoping model

Each child agent receives access only to required tables.

### Validation

* Disruption_Requests
* Suppliers
* SKU_Master
* Purchase_Orders

### Scope

* SKU_Master
* Inventory
* Purchase_Orders
* Customer_Orders

### Inventory

* Inventory
* SKU_Master
* Purchase_Orders

### Supplier

* Alternate_Suppliers
* Suppliers
* SKU_Master

### Customer

* Customer_Orders
* SKU_Master

### Commercial

* Recovery_Rules

### Reporting

No direct operational table access.

This minimizes unnecessary data exposure.

## Orchestration sequence

### Stage 1: Trigger

Recurrence event

↓

Read pending disruptions

↓

Select oldest pending disruption

↓

Update status to In Assessment

### Stage 2: Validation

Supervisor

↓

Validation Specialist

↓

Pass / Fail

### Stage 3: Scope identification

Supervisor

↓

Scope Specialist

↓

Affected order package

### Stage 4: Parallel assessment

Supervisor

↓

Inventory

Supplier

Customer

Commercial

↓

Independent evidence packages

### Stage 5: Fan-in

Supervisor waits for:

* inventory,
* supplier,
* customer,
* commercial.

Retry failed specialists once.

Build consolidated assessment.

### Stage 6: Recovery planning

Consolidated assessment

↓

Recovery Planning Specialist

↓

Proposed strategy

### Stage 7: Strategy resolution

Recovery Planning output

↓

Recovery Strategy Resolution Specialist

↓

Validated strategy

### Stage 8: Approval and reassessment

Validated strategy

↓

Approval Specialist

↓

Approval routing

or

Selective reassessment

or

Manual review

### Stage 9: Reporting

Validated strategy

↓

Reporting Specialist

↓

Power Automate

↓

Word report

Excel update

Outlook notification

## Fan-out and fan-in pattern

### Fan-out

Specialists execute independently.

No specialist may overwrite another specialist's evidence.

### Fan-in

Supervisor consolidates evidence.

Conflict resolution occurs centrally.

Recovery planning begins after consolidation.

This architecture improves:

* modularity,
* maintainability,
* testing,
* explainability.

## Deterministic decision pipeline

The system uses a deterministic pipeline.

Validation

↓

Scope

↓

Specialist evidence

↓

Consolidation

↓

Recovery proposal

↓

Policy resolution

↓

Approval evaluation

↓

Reporting

↓

Execution outputs

The Supervisor remains the single decision authority.

## Policy precedence engine

Conflict resolution uses this order.

1. Quality restrictions
2. Strategic and SLA commitments
3. Supplier approval restrictions
4. Inventory availability
5. Commercial approval requirements
6. Cost optimization
7. Lower-priority customer convenience

This precedence is enforced before final strategy selection.

## State management

Valid disruption states:

* Pending
* In Assessment
* Recovery Plan Proposed
* Awaiting Approval
* Customer Action Required
* Management Escalation
* Insufficient Evidence
* Manual Review
* Completed

Invalid transitions are rejected.

Completed cannot occur while approvals remain outstanding.

## Approval architecture

Approval decisions are externalized.

The system determines:

* whether approval is required,
* who must approve,
* why approval is required.

The system never grants approval.

## Reassessment architecture

Only affected specialists are rerun.

Examples:

Inventory change

↓

Inventory Specialist only

Supplier capacity change

↓

Supplier Specialist

Commercial Specialist if cost changed

Customer order change

↓

Customer Specialist

Unchanged specialist evidence is preserved.

## Power Automate integration

### Generate Supply Continuity Report

Input:

Validated reporting package

Output:

Executive Word document

### Update Disruption Status

Input:

Final validated status

Output:

Updated Excel record

### Send Disruption Notification

Input:

Notification package

Output:

Stakeholder email with report attachment

## Security boundaries

The system never fabricates:

* supplier approval,
* customer agreement,
* commercial approval,
* executive approval,
* inventory availability,
* delivery commitments,
* purchase-order execution.

All outputs must be traceable to validated specialist evidence.

## Scalability

The architecture supports future integration with:

* Dataverse,
* SharePoint,
* SAP,
* Dynamics 365,
* Azure Event Grid,
* Microsoft Fabric,
* enterprise approval systems.

Additional specialists can be added without changing the Supervisor orchestration model.

## Success criteria

A successful execution:

* validates the disruption,
* identifies operational scope,
* completes parallel specialist assessment,
* consolidates evidence,
* resolves conflicts deterministically,
* respects approval boundaries,
* produces one validated strategy,
* generates the executive report,
* updates operational records,
* notifies stakeholders,
* preserves complete decision traceability.
