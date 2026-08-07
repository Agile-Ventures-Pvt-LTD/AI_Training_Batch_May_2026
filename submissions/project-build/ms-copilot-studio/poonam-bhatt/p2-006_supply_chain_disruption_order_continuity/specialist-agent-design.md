# Specialist Agent Design

This document details the configuration, tool scoping, and output contracts for the child specialist agents.

---

## Specialist Agent 1 — Inventory Impact Specialist
- **Purpose**: Calculates available stock levels and determines if existing inventory can cover the disruption period.
- **Inputs**: `SKU`, `ExpectedRecoveryDate`, `ReportedDate`, `AffectedQty`
- **Required Calculations**:
  - `DailyConsumption` = Read from `SKU_Master`
  - `DisruptionDuration` = `ExpectedRecoveryDate` - `ReportedDate` (in days)
  - `DemandDuringDisruption` = `DailyConsumption` * `DisruptionDuration`
  - `AvailableToPromise` = `OnHandQty` - `ReservedQty` + `InboundWithin7DaysQty` - `QualityHoldQty`
  - `ShortageQuantity` = `DemandDuringDisruption` - `AvailableToPromise` (if positive)
- **Output Contract**:
  - `AvailableToPromiseQty` (Integer)
  - `SafetyStockQty` (Integer)
  - `DemandUntilRecovery` (Integer)
  - `ShortageQty` (Integer)
  - `QualityHoldImpact` (String: "None" or "Block")

---

## Specialist Agent 2 — Alternate Supplier Specialist
- **Purpose**: Identifies approved alternate suppliers and evaluates their lead time, cost, and capacity.
- **Inputs**: `SKU`, `RequiredDate`
- **Mandatory Restrictions**: If an alternate supplier is marked `Approved = No` (e.g. SUP-04 for SKU-1003 or SUP-02 for SKU-1008), the agent **must not** select it autonomously. It may only return it with status `Manual supplier qualification option`.
- **Output Contract**:
  - `AlternateAvailable` (Boolean)
  - `SupplierID` (String)
  - `ApprovedStatus` (String: "Yes" or "No")
  - `AvailableCapacityQty` (Integer)
  - `LeadTimeDays` (Integer)
  - `ExpediteLeadTimeDays` (Integer)
  - `CanMeetRequiredDate` (Boolean)
  - `UnitCost_INR` (Decimal)

---

## Specialist Agent 3 — Customer & Order Impact Specialist
- **Purpose**: Evaluates threatened customer orders, ranks them by priority, and checks for partial fulfillment permissions.
- **Inputs**: `SKU`, `ShortageQty`
- **Prioritization Order**:
  1. Strategic Customer + SLA Protected (Highest Priority)
  2. Priority Customer (Medium Priority)
  3. Standard Customer (Lowest Priority)
- **Output Contract**:
  - `AffectedOrderCount` (Integer)
  - `StrategicOrdersAtRisk` (Integer)
  - `SLAOrdersAtRisk` (Integer)
  - `RevenueAtRisk` (Decimal)
  - `PartialFulfillmentConstraints` (String: "Allowed" or "Prohibited")
  - `RankedAffectedOrders` (Array of JSON)

---

## Specialist Agent 4 — Commercial Impact Specialist
- **Purpose**: Calculates cost premiums and determines which business leader must approve the expenditure.
- **Inputs**: `PrimaryUnitCost`, `AlternateUnitCost`, `RequiredQty`, `ExpeditePremiumPct`
- **Threshold Rules**:
  - Alternate unit-cost premium = (`AlternateUnitCost` - `PrimaryUnitCost`) / `PrimaryUnitCost`
  - If Alternate unit-cost premium > 15% -> Approval: Finance Business Partner.
  - If Expedite premium > 10% -> Approval: Supply Chain Director.
- **Output Contract**:
  - `CostPremiumPct` (Decimal)
  - `IncrementalCost` (Decimal)
  - `ExpeditePremiumPct` (Decimal)
  - `ApprovalRequired` (Boolean)
  - `RequiredApprover` (String: "Finance Business Partner", "Supply Chain Director", "Procurement Manager", "None")

---

## Specialist Agent 5 — Recovery Planning Specialist
- **Purpose**: Formulates the optimal recovery recommendation based on consolidated specialist data.
- **Inputs**: Consolidated findings from agents 1, 2, 3, and 4.
- **Output Contract**:
  - `ProposedStrategy` (String)
  - `ResidualRisk` (String: "Low", "Medium", "High", "Critical")
  - `RequiredApprovals` (String)
  - `Rationale` (String)

---

## Specialist Agent 6 — Reporting & Communication Specialist
- **Purpose**: Generates the final Word report and formats/sends Outlook notifications appropriate to the disruption state.
- **Connector Actions**:
  - **Word Online**: Creates `Supply_Disruption_Response_Report.docx` in SharePoint.
  - **Outlook**: Sends emails to appropriate stakeholders based on final status:
    - *Recovery Plan Proposed* -> Recipient: Supply Planning + Procurement.
    - *Awaiting Approval* -> Recipient: Required Approver (e.g. Finance Business Partner).
    - *Management Escalation* -> Recipient: Supply Chain Director.
- **Output Contract**:
  - `ReportCreated` (Boolean)
  - `EmailNotificationSent` (Boolean)
