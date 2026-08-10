# Specialist Agent Design

## Overview

The solution uses six specialist child agents managed by the Supply Continuity Supervisor. Each agent has a clearly defined responsibility, dedicated data sources, and structured outputs to support accurate and auditable decision-making. Specialist agents provide recommendations but do not make final business decisions. The Supervisor remains responsible for orchestration, validation, conflict resolution, and final approval. 【1-18ad46】

---

# 1. Inventory Impact Specialist

## Purpose

Determines inventory availability and assesses whether existing stock can protect customer demand until supply recovery. 【1-18ad46】

## Data Sources

- Inventory Table
- SKU Master Table
- Purchase Orders
- Disruption Requests

## Key Responsibilities

- Calculate Available-to-Promise (ATP)
- Assess safety stock usage
- Determine shortage quantities
- Identify inventory risks
- Exclude quality-held inventory

## Outputs

- AvailableToPromise
- SafetyStock
- DemandUntilRecovery
- ShortageQty
- InventoryAssessment
- RecommendedInventoryAction
- Confidence


---

# 2. Alternate Supplier Specialist

## Purpose

Evaluates whether approved alternate suppliers can reduce disruption impact. 【1-18ad46】

## Data Sources

- Alternate Suppliers Table
- Suppliers Table
- SKU Master Table
- Disruption Requests

## Key Responsibilities

- Validate supplier approval status
- Assess supplier capacity
- Compare lead times
- Evaluate delivery feasibility
- Identify sourcing alternatives

## Outputs

- AlternateAvailable
- SupplierID
- ApprovedStatus
- AvailableCapacity
- StandardLeadTime
- AlternateUnitCost
- CanMeetRequiredDate
- RecommendedSupplierAction
- Confidence

## Guardrail

Unapproved suppliers cannot be autonomously selected as the final recovery source. 【1-18ad46】

---

# 3. Customer & Order Impact Specialist

## Purpose

Determines customer commitment risks and prioritizes demand protection. 【1-18ad46】

## Data Sources

- Customer Orders Table
- Inventory Table
- SKU Master Table
- Disruption Requests

## Key Responsibilities

- Identify impacted orders
- Evaluate SLA commitments
- Assess strategic customer exposure
- Calculate revenue at risk
- Rank customer orders

## Outputs

- AffectedOrderCount
- StrategicOrdersAtRisk
- SLAOrdersAtRisk
- RevenueAtRisk
- RankedAffectedOrders
- CustomerImpactClassification
- RecommendedCustomerAction
- Confidence

## Priority Model

```text
Strategic + SLA Protected
        ↓
Priority
        ↓
Standard
```



---

# 4. Commercial Impact Specialist

## Purpose

Analyzes the financial impact of recovery options and determines approval requirements. 【1-18ad46】

## Inputs

- Supplier Costs
- Alternate Supplier Costs
- Revenue Exposure
- Expedite Costs
- Recovery Strategy Options

## Key Responsibilities

- Calculate cost premiums
- Determine financial exposure
- Assess commercial risk
- Identify approval requirements

## Outputs

- CostPremiumPct
- IncrementalCost
- RevenueExposure
- CommercialRisk
- ApprovalRequired
- RequiredApprover
- RecommendedCommercialAction
- Confidence

## Approval Rules

- Cost Premium > 15% → Finance Business Partner Approval
- Expedite Premium > 10% → Supply Chain Director Approval



---

# 5. Recovery Planning Specialist

## Purpose

Generates the most appropriate recovery strategy after all specialist assessments have been consolidated. 

## Inputs

- Inventory Assessment
- Alternate Supplier Assessment
- Customer Impact Assessment
- Commercial Assessment
- Policy Rules

## Key Responsibilities

- Evaluate recovery options
- Recommend continuity strategies
- Identify residual risks
- Define required actions

## Outputs

- ProposedStrategy
- StrategyComponents
- OrdersProtected
- OrdersRemainingAtRisk
- RequiredApprovals
- ResidualRisk
- RequiredInternalActions
- Rationale
- Confidence

## Restrictions

The agent cannot:

- Place purchase orders
- Approve suppliers
- Cancel customer orders
- Commit delivery dates
- Authorize spending


---

# 6. Reporting & Communication Specialist

## Purpose

Generates final documentation and stakeholder communications after Supervisor approval. 【1-18ad46】

## Tools

- Word Online (Business)
- Outlook

## Key Responsibilities

- Generate Supply Disruption Response Report
- Prepare stakeholder notifications
- Support workflow completion

## Outputs

### Word Report

- Disruption Details
- Inventory Assessment
- Customer Impact
- Supplier Analysis
- Commercial Analysis
- Recovery Strategy
- Risk Assessment
- Supervisor Decision

### Outlook Notification

Sends notifications based on the final workflow status after Supervisor authorization.


---

# Standard Output Structure

All specialist agents return a consistent response structure.

```text
SpecialistName
AssessmentStatus
EvidenceSummary
QuantitativeFindings
BlockingIssues
Constraints
RecommendedAction
ApprovalRequired
RequiredApprover
Confidence
Completed
```

This standardized format simplifies fan-in consolidation, conflict resolution, and Supervisor decision-making. 

---

# Summary

The specialist-agent architecture separates responsibilities across inventory, sourcing, customer impact, commercial assessment, recovery planning, and reporting domains. This design improves maintainability, reduces tool ambiguity, supports parallel processing, and enables the Supervisor Agent to make policy-compliant decisions using structured specialist evidence. 