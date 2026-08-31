# Specialist agent design

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

This document describes the design of all specialist child agents used by the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The system uses a **Supervisor-and-Specialist architecture** in which the Supervisor Agent orchestrates execution while specialist agents perform narrowly scoped domain-specific analysis.

Each specialist has:

* a single responsibility,
* limited tool access,
* deterministic outputs,
* explicit decision boundaries,
* structured communication with the Supervisor.

Specialists never invoke each other directly and never make final recovery decisions.

## Specialist architecture

```text
Supervisor Agent
        │
        ├── Validation Specialist
        ├── Scope Identification Specialist
        ├── Inventory Impact Specialist
        ├── Alternate Supplier Specialist
        ├── Customer & Order Impact Specialist
        ├── Commercial Impact Specialist
        ├── Recovery Planning Specialist
        ├── Recovery Strategy Resolution Specialist
        ├── Approval, Exception & Selective Reassessment Specialist
        └── Reporting & Communication Specialist
```

The Supervisor coordinates all specialists through structured input and output contracts.

## Design principles

### Single responsibility

Each specialist performs one business function only.

### Tool isolation

Specialists receive access only to required data sources.

### Structured outputs

All specialists return deterministic structured outputs.

### No cross-specialist dependency

Specialists do not call sibling specialists.

### Evidence-based reasoning

Recommendations must be supported by available operational evidence.

### Supervisor authority

The Supervisor remains the only orchestration and execution authority.

# 1. Disruption intake & validation specialist

## Purpose

Validate disruption integrity before operational assessment begins.

## Responsibilities

* disruption validation,
* supplier validation,
* SKU validation,
* purchase-order validation,
* relationship validation,
* duplicate detection,
* data completeness verification.

## Data access

* Disruption_Requests
* Suppliers
* SKU_Master
* Purchase_Orders

## Inputs

* DisruptionID
* SupplierID
* SKU
* AffectedPO
* AffectedQty
* ReportedDate
* ExpectedRecoveryDate
* DisruptionType

## Outputs

* ValidationStatus
* ValidationReason
* DuplicateDetected
* ValidatedSupplier
* ValidatedSKU
* ValidatedPO
* Completed

## Decision boundaries

May:

* validate records,
* reject invalid disruptions.

May not:

* analyze inventory,
* evaluate suppliers,
* prioritize customers,
* propose recovery actions.

# 2. Scope identification & order discovery specialist

## Purpose

Identify the complete operational impact of the disruption.

## Responsibilities

* affected order discovery,
* demand aggregation,
* strategic exposure,
* SLA exposure,
* operational scope preparation.

## Data access

* SKU_Master
* Inventory
* Purchase_Orders
* Customer_Orders

## Inputs

* SKU
* SupplierID
* AffectedPO
* AffectedQty
* ExpectedRecoveryDate

## Outputs

* AffectedOrders
* AffectedOrderCount
* TotalAffectedDemand
* EarliestRequiredDate
* StrategicOrderCount
* SLAOrderCount
* ScopeStatus

## Decision boundaries

May:

* discover operational impact.

May not:

* allocate inventory,
* select suppliers,
* prioritize fulfillment.

# 3. Inventory impact specialist

## Purpose

Evaluate whether inventory can protect customer demand until recovery.

## Responsibilities

* ATP calculation,
* shortage estimation,
* safety-stock evaluation,
* quality-hold exclusion,
* inventory sufficiency assessment.

## Data access

* Inventory
* SKU_Master
* Purchase_Orders

## ATP calculation

ATP = On Hand - Reserved + Inbound Within 7 Days - Quality Hold

## Inputs

* SKU
* AffectedQty
* ExpectedRecoveryDate
* TotalAffectedDemand

## Outputs

* AvailableToPromise
* SafetyStock
* DemandUntilRecovery
* ShortageQty
* QualityHoldImpact
* InventoryAssessment
* BlockingIssue
* RecommendedInventoryAction
* Confidence
* Completed

## Decision boundaries

May:

* evaluate inventory sufficiency.

May not:

* select alternate suppliers,
* prioritize customers,
* authorize inventory allocation.

# 4. Alternate supplier specialist

## Purpose

Evaluate alternate sourcing feasibility.

## Responsibilities

* approved supplier evaluation,
* capacity validation,
* lead-time analysis,
* timing feasibility,
* qualification restriction identification.

## Data access

* Alternate_Suppliers
* Suppliers
* SKU_Master

## Inputs

* SKU
* SupplierID
* AffectedQty
* EarliestRequiredDate

## Outputs

* AlternateAvailable
* ApprovedStatus
* AvailableCapacity
* StandardLeadTime
* ExpediteLeadTime
* AlternateUnitCost
* CanMeetRequiredDate
* QualificationRestriction
* RecommendedSupplierAction
* Confidence
* Completed

## Mandatory restriction

Unapproved suppliers cannot be autonomously selected.

## Decision boundaries

May:

* evaluate supplier feasibility.

May not:

* approve suppliers,
* place purchase orders,
* execute supplier changes.

# 5. Customer & order impact specialist

## Purpose

Evaluate customer commitment risk.

## Responsibilities

* strategic customer protection,
* SLA exposure,
* revenue exposure,
* order prioritization,
* fulfillment constraint analysis.

## Data access

* Customer_Orders
* SKU_Master

## Inputs

* SKU
* AffectedOrders
* TotalAffectedDemand
* EarliestRequiredDate

## Outputs

* StrategicOrdersAtRisk
* SLAOrdersAtRisk
* RevenueAtRisk
* RankedAffectedOrders
* CustomerImpactClassification
* RecommendedCustomerAction
* Confidence
* Completed

## Priority model

1. Strategic + SLA
2. Strategic
3. Priority
4. Standard

## Decision boundaries

May:

* rank customer risk.

May not:

* cancel orders,
* promise delivery,
* approve customer negotiations.

# 6. Commercial impact specialist

## Purpose

Evaluate financial recovery impact.

## Responsibilities

* cost premium calculation,
* expedite premium calculation,
* incremental procurement cost,
* approval threshold evaluation.

## Data access

* Recovery_Rules

## Inputs

* PrimaryUnitCost
* AlternateUnitCost
* RequiredAlternateQty
* ExpeditePremium
* RevenueAtRisk
* CandidateStrategy

## Outputs

* CostPremiumPct
* IncrementalCost
* RevenueExposure
* ExpeditePremiumPct
* CommercialRisk
* ApprovalRequired
* RequiredApprover
* RecommendedCommercialAction
* Confidence
* Completed

## Approval thresholds

Cost premium >15%

↓

Finance Business Partner

Expedite premium >10%

↓

Supply Chain Director

## Decision boundaries

May:

* determine approval requirements.

May not:

* approve spending,
* authorize procurement,
* override policy thresholds.

# 7. Recovery planning specialist

## Purpose

Propose recovery strategies using consolidated specialist evidence.

## Responsibilities

* strategy formulation,
* combined recovery planning,
* inventory utilization evaluation,
* alternate sourcing evaluation,
* residual risk estimation.

## Data access

None

Receives only Supervisor context.

## Inputs

* InventoryAssessment
* SupplierAssessment
* CustomerAssessment
* CommercialAssessment
* ReportedSeverity
* ExpectedRecoveryDate

## Outputs

* ProposedStrategy
* StrategyComponents
* OrdersProtected
* OrdersRemainingAtRisk
* RequiredApprovals
* ResidualRisk
* RequiredCustomerAction
* RequiredInternalActions
* Rationale
* Confidence
* Completed

## Decision boundaries

May:

* propose strategies.

May not:

* approve execution,
* bypass policy restrictions.

# 8. Recovery strategy resolution specialist

## Purpose

Resolve competing specialist recommendations.

## Responsibilities

* deterministic policy resolution,
* conflict resolution,
* final strategy validation,
* final risk classification,
* final status determination.

## Data access

None

Receives consolidated specialist evidence.

## Inputs

* InventoryAssessment
* SupplierAssessment
* CustomerAssessment
* CommercialAssessment
* ProposedStrategy
* ReportedSeverity

## Outputs

* FinalStrategy
* StrategyStatus
* FinalRisk
* ApprovalRequired
* RequiredApprover
* OrdersProtected
* OrdersRemainingAtRisk
* ResidualRisk
* ResolutionRationale
* Confidence
* Completed

## Policy precedence

1. Quality restrictions
2. Strategic/SLA commitments
3. Supplier approval
4. Inventory timing
5. Commercial approval
6. Cost optimization

## Decision boundaries

May:

* validate strategy.

May not:

* grant approvals,
* execute operational actions.

# 9. Approval, exception & selective reassessment specialist

## Purpose

Manage approval routing and reassessment.

## Responsibilities

* approval determination,
* approver identification,
* reassessment evaluation,
* retry control,
* manual review routing.

## Data access

None

Receives Supervisor context.

## Inputs

* FinalStrategy
* StrategyStatus
* FinalRisk
* ApprovalRequired
* RequiredApprover
* specialist assessments
* DataChangeEvents
* ReassessmentCycleCount

## Outputs

* ApprovalRequired
* RequiredApprover
* ApprovalReason
* ReassessmentRequired
* SpecialistsToReassess
* ReassessmentReason
* UpdatedStrategyStatus
* UpdatedFinalRisk
* ManualReviewRequired
* Completed

## Reassessment limit

Maximum automated cycles:

2

## Decision boundaries

May:

* determine approvals,
* determine reassessment.

May not:

* approve actions,
* modify operational records.

# 10. Reporting & communication specialist

## Purpose

Prepare final reporting outputs.

## Responsibilities

* executive summary,
* report preparation,
* notification determination,
* communication package preparation,
* final status recommendation.

## Data access

None

Receives validated Supervisor context.

## Inputs

* disruption summary,
* specialist assessments,
* final strategy,
* approvals,
* residual risks.

## Outputs

* ExecutiveSummary
* ReportSections
* NotificationRecipients
* NotificationSubject
* NotificationSummary
* RecommendedFinalStatus
* GenerateWordReport
* SendNotifications
* UpdateExcel
* Completed

## Decision boundaries

May:

* prepare reporting outputs.

May not:

* generate documents directly,
* send emails directly,
* update Excel directly.

Power Automate performs external execution.

## Common specialist contract

All specialists follow the same execution contract.

### Input

Receive validated structured context from the Supervisor.

### Processing

Perform only assigned domain analysis.

### Output

Return structured evidence.

### Completion

Return:

* Completed = Yes
* Completed = No

No specialist returns conversational-only outputs.

## Confidence model

Specialists return:

* High
* Medium
* Low

Confidence reflects evidence quality, not decision authority.

## Failure handling

Specialists should:

* detect missing data,
* detect inconsistent data,
* avoid fabricated values,
* return deterministic failures.

The Supervisor handles retries and fallback.

## Tool-scoping model

| Specialist          | Tool access                         |
| ------------------- | ----------------------------------- |
| Validation          | Disruption, Suppliers, SKU, PO      |
| Scope               | SKU, Inventory, PO, Orders          |
| Inventory           | Inventory, SKU, PO                  |
| Supplier            | Alternate Suppliers, Suppliers, SKU |
| Customer            | Orders, SKU                         |
| Commercial          | Recovery Rules                      |
| Recovery Planning   | None                                |
| Strategy Resolution | None                                |
| Approval            | None                                |
| Reporting           | None                                |

This minimizes unnecessary data exposure.

## Interaction pattern

```text
Supervisor
    │
Context
    │
    ▼
Specialist
    │
Evidence
    │
    ▼
Supervisor
```

Specialists never communicate directly with each other.

## Success criteria

A specialist is considered successful when it:

* performs only its assigned responsibility,
* uses only authorized data,
* returns structured outputs,
* avoids fabricated conclusions,
* respects policy boundaries,
* completes deterministic analysis,
* enables Supervisor consolidation.

## Conclusion

The specialist-agent architecture creates a modular, testable, and scalable multi-agent system.

Each specialist contributes independent operational evidence while the Supervisor remains the single orchestration and decision authority.

This design supports enterprise governance, deterministic execution, selective reassessment, and complete decision traceability.
