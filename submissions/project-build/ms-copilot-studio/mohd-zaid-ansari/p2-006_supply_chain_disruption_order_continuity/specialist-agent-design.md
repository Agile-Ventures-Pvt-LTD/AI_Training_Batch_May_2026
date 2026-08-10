# Specialist Agent Design

## Overview

The Specialist Agent layer contains domain-specific child agents controlled by the **Mohd Zaid Supply Continuity Supervisor**.

Each specialist performs independent analysis, uses scoped data/tools, returns structured findings, and does not make final recovery decisions.

---

# Specialist Architecture

```
Mohd Zaid Supply Continuity Supervisor
            |
 ┌──────────┼──────────┬──────────┬──────────┐
 |          |          |          |          |
Inventory  Alternate Customer  Commercial Recovery
Impact     Supplier  Impact    Impact     Planning

            |
            ▼

Reporting & Communication
```

---

# Common Output Contract

Every specialist returns:

* SpecialistName
* AssessmentStatus
* EvidenceSummary
* QuantitativeFindings
* BlockingIssues
* RecommendedAction
* ApprovalRequired
* RequiredApprover
* Confidence
* Completed

---

# 1. Inventory Impact Specialist

## Purpose

Evaluate whether available inventory can protect demand until supply recovery.

## Data

* InventoryTable
* SKUMasterTable
* PurchaseOrdersTable
* DisruptionRequestsTable

## Responsibilities

Analyzes:

* ATP quantity
* Safety stock
* Demand until recovery
* Quality hold impact
* Shortage quantity

## Output

* AvailableToPromise
* SafetyStock
* DemandUntilRecovery
* ShortageQty
* InventoryAssessment
* RecommendedInventoryAction
* Confidence

---

# 2. Alternate Supplier Specialist

## Purpose

Evaluate approved alternate supplier options.

## Data

* AlternateSuppliersTable
* SuppliersTable
* SKUMasterTable
* DisruptionRequestsTable

## Responsibilities

Checks:

* Supplier approval
* Capacity
* Lead time
* Cost
* Recovery feasibility

## Guardrail

Unapproved suppliers cannot be selected as recovery sources.

They can only return:

**Manual Supplier Qualification Required**

## Output

* SupplierID
* ApprovedStatus
* AvailableCapacity
* LeadTimes
* Cost
* CanMeetRequiredDate
* RecommendedSupplierAction

---

# 3. Customer & Order Impact Specialist

## Purpose

Evaluate customer risk and order priority.

## Data

* CustomerOrdersTable
* SKUMasterTable
* InventoryTable

## Responsibilities

Analyzes:

* All affected customer orders
* SLA commitments
* Strategic customers
* Required dates
* Revenue exposure
* Partial fulfilment rules

## Priority

1. Strategic + SLA
2. Priority
3. Standard

## Output

* AffectedOrderCount
* SLAOrdersAtRisk
* StrategicOrdersAtRisk
* RevenueAtRisk
* RankedAffectedOrders
* CustomerImpactClassification
* RecommendedCustomerAction

---

# 4. Commercial Impact Specialist

## Purpose

Evaluate financial impact of recovery options.

## Data

* PurchaseOrdersTable
* SuppliersTable
* RecoveryRulesTable

## Responsibilities

Calculates:

* Cost premium
* Incremental cost
* Expedite premium
* Revenue exposure

## Approval Rules

* Alternate premium >15% → Finance approval
* Expedite premium >10% → Supply Chain Director approval

## Output

* CostPremiumPct
* IncrementalCost
* RevenueExposure
* ApprovalRequired
* RequiredApprover
* CommercialRisk

---

# 5. Recovery Planning Specialist

## Purpose

Create recovery options after specialist fan-in.

## Inputs

* Inventory assessment
* Supplier assessment
* Customer impact
* Commercial impact
* Policy rules

## Allowed Strategies

* Use existing stock
* Approved alternate supplier
* Expedite supply
* Partial fulfilment
* Customer negotiation
* Combined recovery
* Management escalation
* Manual review

## Restrictions

Cannot:

* Place purchase orders
* Approve suppliers
* Cancel orders
* Promise customer dates
* Approve spending

## Output

* ProposedStrategy
* OrdersProtected
* RemainingRisk
* RequiredApprovals
* Actions
* Rationale
* Confidence

---

# 6. Reporting & Communication Specialist

## Purpose

Generate final report and notifications after Supervisor approval.

## Responsibilities

Creates:

* Word Supply Disruption Response Report
* Outlook stakeholder notification

## Report Includes

* Disruption details
* Supplier/SKU information
* Specialist findings
* Recovery strategy
* Approvals
* Risks
* Required actions
* Final status

## Restriction

Cannot send communication without Supervisor authorization.

---

# Failure Handling

All specialists follow:

1. Execute assessment.
2. Retry once if failed.
3. If retry fails:

   * Mark **Insufficient Evidence**
   * Prevent unsupported decisions
   * Escalate if required

Maximum attempts:

**2 per specialist**

---

# Design Principles

* Clear specialist ownership
* Independent fan-out assessments
* Structured outputs
* Scoped tools and data access
* Supervisor-controlled decisions
* No fabricated approvals or commitments

The Supervisor remains the only component responsible for final recovery decisions.
