# Specialist Agent Design

## Overview

The Supply Chain Disruption Order Continuity System uses specialist agents to perform domain-specific analysis.

Each specialist:

- Operates independently
- Uses workbook data as evidence
- Returns structured findings
- Follows strict constraints
- Does not make final business decisions
- Does not override policy rules

The Supervisor orchestrates specialist execution and consolidates outputs into a final recommendation.

---

# 1. Inventory Impact Specialist

## Purpose

Evaluate inventory availability and determine whether existing inventory can support customer demand during a disruption.

---

## Responsibilities

The Inventory Impact Specialist is responsible for:

- Evaluating inventory availability
- Calculating Available-To-Promise (ATP)
- Assessing inventory sufficiency
- Identifying shortages
- Evaluating safety stock consumption
- Assessing inventory risk
- Recommending inventory-based recovery actions

---

## Data Sources

The specialist retrieves data from:

- SKU Master Table
- Inventory Table
- Purchase Orders Table
- Disruption Request Table

---

## Key Calculations

### Available-To-Promise (ATP)

```text
ATP =
OnHandQty
- ReservedQty
+ InboundWithin7DaysQty
- QualityHoldQty
```

### Demand Exposure

Based on:

```text
AffectedQty
DailyConsumption
ExpectedRecoveryDate
```

---

## Outputs

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- QuantitativeFindings
- BlockingIssues
- RecommendedAction

### Inventory Outputs

- InventoryFindings
- ATPAssessment
- ShortageAssessment
- SafetyStockImpact
- InventoryRisk
- InventoryRecommendation

---

## Constraints

The specialist must not:

- Select recovery strategies
- Commit inventory
- Approve stock allocation
- Override customer priorities
- Approve safety stock usage
- Make customer commitments

---

# 2. Alternate Supplier Specialist

## Purpose

Evaluate alternate sourcing opportunities and determine whether approved supplier alternatives exist.

---

## Responsibilities

The specialist:

- Identifies alternate suppliers
- Validates supplier approval status
- Evaluates supplier capacity
- Evaluates supplier lead times
- Assesses sourcing risk
- Recommends alternate sourcing options

---

## Data Sources

The specialist retrieves data from:

- Disruption Request Table
- SKU Master Table
- Alternate Suppliers Table
- Suppliers Table

---

## Assessment Areas

### Supplier Approval

Determine:

```text
Approved Status
```

### Supplier Capacity

Determine:

```text
Available Capacity
```

### Delivery Capability

Determine:

```text
Lead Time
Expedited Lead Time
Can Meet Required Date
```

### Cost Exposure

Determine:

```text
Alternate Unit Cost
```

---

## Outputs

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- QuantitativeFindings
- BlockingIssues
- RecommendedAction

### Supplier Outputs

- AlternateAvailable
- SupplierID
- ApprovedStatus
- AvailableCapacity
- StandardLeadTime
- ExpeditedLeadTime
- AlternateUnitCost
- CanMeetRequiredDate
- QualificationRestriction
- SupplierRisk
- RecommendedSupplierAction

---

## Constraints

The specialist must not:

- Approve suppliers
- Create purchase orders
- Commit sourcing decisions
- Approve cost increases
- Override qualification rules
- Select final recovery strategies

---

# 3. Customer & Order Impact Specialist

## Purpose

Determine how the disruption affects customer commitments, protected accounts, and order fulfillment.

---

## Responsibilities

The specialist:

- Evaluates affected orders
- Applies customer priority rules
- Assesses SLA exposure
- Assesses fulfillment risk
- Identifies customer impact
- Recommends mitigation actions

---

## Data Sources

The specialist retrieves data from:

- Disruption Request Table
- SKU Master Table
- Customer Orders Table

---

## Priority Rules

Priority order:

```text
1. Strategic + SLA Protected
2. Priority
3. Standard
```

---

## Assessment Areas

Evaluate:

- Open orders
- Required dates
- Customer tier
- Revenue exposure
- SLA protection
- Partial fulfillment permission

---

## Outputs

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- QuantitativeFindings
- BlockingIssues
- RecommendedAction

### Customer Outputs

- AffectedOrderCount
- StrategicOrdersAtRisk
- SLAOrdersAtRisk
- RevenueAtRisk
- EarliestRequiredDate
- RankedAffectedOrders
- CustomerImpactClassification
- RecommendedCustomerAction

---

## Constraints

The specialist must not:

- Commit inventory
- Change delivery dates
- Make customer promises
- Override customer priorities
- Approve cancellations
- Select recovery strategies

---

# 4. Commercial Impact Specialist

## Purpose

Assess financial exposure, commercial risks, and approval requirements associated with recovery options.

---

## Responsibilities

The specialist:

- Assesses revenue exposure
- Calculates cost premiums
- Calculates incremental cost
- Assesses expedite premiums
- Determines commercial risk
- Determines approval requirements

---

## Data Sources

The specialist retrieves data from:

- Disruption Request Table
- SKU Master Table
- Customer Orders Table
- Alternate Suppliers Table
- Recovery Rules Table

---

## Key Calculations

### Cost Premium

```text
CostPremiumPct = ((AlternateUnitCost - PrimaryUnitCost) / PrimaryUnitCost) × 100
```

---

### Incremental Cost

```text
IncrementalCost = (AlternateUnitCost - PrimaryUnitCost) × RequiredAlternateQuantity
```

---

### Revenue Exposure

Calculated using:

```text
Affected Demand
Revenue_INR
```

---

### Approval Policy

Finance Business Partner Approval:

```text
CostPremiumPct > 15%
```

Supply Chain Director Approval:

```text
ExpeditePremiumPct > 10%
```

Both approvals required if both conditions are met.

---

## Outputs

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- BlockingIssues
- RecommendedAction

### Commercial Outputs

- CostPremiumPct
- IncrementalCost
- RevenueExposure
- ExpeditePremiumPct
- CommercialRisk
- RecommendedCommercialAction
- ApprovalRequired
- RequiredApprover

---

## Constraints

The specialist must not:

- Approve spending
- Approve supplier changes
- Approve contracts
- Commit financial resources
- Override customer priorities
- Select final recovery strategies

---

# 5. Recovery Planning Specialist

## Purpose

Consolidate specialist findings and determine the most appropriate recovery strategy.

---

## Responsibilities

The specialist:

- Evaluates recovery options
- Assesses feasibility
- Assesses order protection capability
- Determines required actions
- Determines residual risk
- Recommends recovery strategies

---

## Required Inputs

The following assessments must be available:

- Inventory Assessment
- Alternate Supplier Assessment
- Customer Impact Assessment
- Commercial Impact Assessment

---

## Missing Assessment Rule

If any assessment is missing:

```text
ProposedStrategy = Cannot Assess
ResidualRisk = Unknown
Confidence = Low
```

A Manual Review recommendation must be returned.

---

## Recovery Strategies

Only the following strategies may be used:

```text
Use Existing Stock
Reallocate Inventory
Approved Alternate Supplier
Expedite Existing Supply
Expedite Alternate Supply
Partial Fulfillment
Customer Date Negotiation
Combined Recovery Strategy
Management Escalation
Manual Review
```

---

## Evaluation Criteria

Recovery options are evaluated using:

- Inventory availability
- Supplier capability
- Customer impact
- Commercial impact
- Policy restrictions
- Approval requirements

---

## Outputs

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- BlockingIssues
- RecommendedAction

### Recovery Outputs

- OrdersProtected
- OrdersRemainingAtRisk
- StrategyComponents
- ResidualRisk
- RequiredCustomerAction
- RequiredInternalActions
- ProposedStrategy
- Rationale
- ApprovalRequired
- RequiredApprovals

---

## Constraints

The specialist must not:

- Place purchase orders
- Approve suppliers
- Approve expenditures
- Approve contract changes
- Commit inventory
- Ignore policy rules
- Override specialist findings

---

# 6. Reporting & Communication Specialist

## Purpose

Generate disruption reports and communicate approved outcomes to stakeholders.

---

## Responsibilities

The specialist:

- Creates final disruption reports
- Generates stakeholder communications
- Sends Outlook notifications
- Returns execution status

---

## Data Sources

Inputs provided by:

- Supervisor
- Approved Specialist Findings
- Final Recovery Recommendation

---

## Reporting Contents

The generated report includes:

- Disruption ID
- Supplier
- SKU
- Disruption Type
- Affected PO
- Recovery Date
- Inventory Summary
- Customer Impact Summary
- Supplier Summary
- Commercial Summary
- Selected Strategy
- Approval Requirements
- Orders Protected
- Orders Remaining At Risk
- Revenue At Risk
- Residual Risk
- Required Actions
- Final Status

---

## Outputs

### Execution Outputs

- ReportGenerated
- ReportLocation
- NotificationSent
- NotificationRecipients

### Core Outputs

- AssessmentStatus
- EvidenceSummary
- BlockingIssues
- RecommendedAction
- ApprovalRequired
- RequiredApprover

---

## Constraints

The specialist must not:

- Reassess disruption conditions
- Modify specialist findings
- Change selected recovery strategies
- Approve recovery actions
- Update workbook status records
- Override supervisor decisions

---

# Common Specialist Output Contract

Every specialist returns a standard response structure.

## Mandatory Fields

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

---

## Assessment Status Values

```text
Pass
Condition
Block
Insufficient Evidence
```

---

## Confidence Values

```text
High
Medium
Low
```

---

## Approval Required Values

```text
Yes
No
```

---

## Evidence Principles

All specialists must follow these rules:

- Use workbook data only.
- Do not invent information.
- Do not estimate unavailable values.
- Identify missing evidence clearly.
- Return Insufficient Evidence when required data is unavailable.
- Provide traceable supporting evidence.

---

# Specialist Interaction Model

```text
                        Supervisor
                            |
    +-----------------------------------------------+
    |           |           |           |           |                
    V           V           V           V           V            

Inventory    Supplier   Customer   Commercial  Recovery Planning

    +-----------+------------+----------+------------+
                            |
                            V

                    Recovery Planning

                            |
                            V

                        Supervisor
```

The Supervisor remains the single orchestration authority while specialists provide evidence-based domain assessments.