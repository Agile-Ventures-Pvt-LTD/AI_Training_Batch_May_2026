# Specialist Agent Design Cards

This document outlines the purpose, datasets, calculations, constraints, and output contracts for the six specialist child agents coordinated by the Supply Continuity Supervisor.

---

## 1. Inventory Impact Specialist

### Purpose
Evaluate available inventory, safety stock, daily consumption, and expected inbound POs to determine if current stock can cover demand until the supplier recovers.

### Data Inputs
* `SKU_Master`
* `Inventory`
* `Purchase_Orders`
* `Disruption_Requests`

### Calculations & Logic
* **Available to Promise (ATP)**:
  $$\text{ATP} = \text{On Hand} - \text{Reserved} + \text{Inbound Within 7 Days} - \text{Quality Hold}$$
* **Daily Consumption Rate**: Average quantity consumed per day based on historical customer order patterns.
* **Demand Until Recovery**: Daily Consumption Rate multiplied by the number of days until the expected recovery date.
* **Estimated Shortage Qty**: $\text{Demand Until Recovery} - \text{ATP}$ (if positive).
* **Quality Hold Impact**: Flag and exclude any inbound quantity that is on Quality Hold.

### Output Contract
* `AvailableToPromise` (Decimal)
* `SafetyStock` (Decimal)
* `DemandUntilRecovery` (Decimal)
* `ShortageQty` (Decimal)
* `QualityHoldImpact` (Boolean)
* `InventoryAssessment` (String)
* `BlockingIssue` (String)
* `RecommendedInventoryAction` (String)
* `Confidence` (High / Medium / Low)
* `Completed` (Yes / No)

---

## 2. Alternate Supplier Specialist

### Purpose
Identify alternate suppliers capable of delivering the required SKU, comparing lead times, capacities, and costs.

### Data Inputs
* `Alternate_Suppliers`
* `Suppliers`
* `SKU_Master`
* `Disruption_Requests`

### Calculations & Logic
* **Supplier Approved Check**: Verify if `Approved = Yes`.
* **Lead Time Comparison**: Compare standard lead time vs. expedited lead time.
* **Capacity Validation**: Ensure alternate capacity exceeds the disruption shortage quantity.
* **Mandatory Constraint**: If a supplier is marked `Approved = No`, they must *never* be autonomously recommended. Sourcing can only flag them as a `Manual supplier qualification option`.

### Output Contract
* `AlternateAvailable` (Boolean)
* `SupplierID` (String)
* `ApprovedStatus` (Boolean)
* `AvailableCapacity` (Decimal)
* `StandardLeadTime` (Integer)
* `ExpediteLeadTime` (Integer)
* `AlternateUnitCost` (Decimal)
* `CanMeetRequiredDate` (Boolean)
* `QualificationRestriction` (String)
* `RecommendedSupplierAction` (String)
* `Confidence` (High / Medium / Low)
* `Completed` (Yes / No)

---

## 3. Customer & Order Impact Specialist

### Purpose
Determine which customer delivery commitments are threatened and rank the open orders based on priority tiers and SLAs.

### Data Inputs
* `Customer_Orders`
* `SKU_Master`
* `Inventory`
* `Disruption_Requests`

### Calculations & Logic
* **Order Prioritization Rule**:
  1. Strategic Customer + SLA Protected (Highest Priority)
  2. Priority Customer (Medium Priority)
  3. Standard Customer (Lowest Priority)
* **Revenue Exposure**: Sum of the order values of all orders at risk due to shortage.
* **Partial Fulfillment Permission**: Check if the customer order permits split shipments (`PartialFulfillment = Yes`). If `No`, the order must be shipped complete or delayed.

### Output Contract
* `AffectedOrderCount` (Integer)
* `StrategicOrdersAtRisk` (Integer)
* `SLAOrdersAtRisk` (Integer)
* `RevenueAtRisk` (Decimal)
* `EarliestRequiredDate` (Date)
* `PartialFulfillmentConstraints` (String)
* `RankedAffectedOrders` (String / JSON)
* `CustomerImpactClassification` (Low / Medium / High / Critical)
* `RecommendedCustomerAction` (String)
* `Confidence` (High / Medium / Low)
* `Completed` (Yes / No)

---

## 4. Commercial Impact Specialist

### Purpose
Assess the financial impact of using alternate suppliers or expedited shipping, routing cases to human approvers if thresholds are exceeded.

### Data Inputs
* `Primary Unit Cost` (from primary supplier)
* `Alternate Unit Cost` (from alternate supplier)
* `Required Alternate Quantity`
* `Expedite Premium` (freight/logistics premium)
* `Revenue at Risk`

### Calculations & Logic
* **Alternate Unit-Cost Premium %**:
  $$\text{Cost Premium \%} = \frac{\text{Alternate Unit Cost} - \text{Primary Unit Cost}}{\text{Primary Unit Cost}} \times 100$$
* **Incremental Procurement Cost**:
  $$\text{Incremental Cost} = (\text{Alternate Unit Cost} - \text{Primary Unit Cost}) \times \text{Required Alternate Qty}$$
* **Expedite Premium %**:
  $$\text{Expedite Premium \%} = \frac{\text{Expedite Premium}}{\text{Primary Sourcing Cost}} \times 100$$
* **Approval Threshold Enforcement**:
  * If Cost Premium > 15% ➔ Set `RequiredApprover = 'Finance Business Partner'`
  * If Expedite Premium > 10% ➔ Set `RequiredApprover = 'Supply Chain Director'`

### Output Contract
* `CostPremiumPct` (Decimal)
* `IncrementalCost` (Decimal)
* `RevenueExposure` (Decimal)
* `ExpeditePremiumPct` (Decimal)
* `CommercialRisk` (Low / Medium / High)
* `ApprovalRequired` (Boolean)
* `RequiredApprover` (String)
* `RecommendedCommercialAction` (String)
* `Confidence` (High / Medium / Low)
* `Completed` (Yes / No)

---

## 5. Recovery Planning Specialist

### Purpose
Execute sequentially *after* the fan-in consolidation. Propose an integrated recovery plan utilizing consolidated specialists' findings and the Supply Continuity Policy.

### Data Inputs
* Consolidated assessments from: Inventory, Alternate Supplier, Customer, and Commercial specialists.
* Severity, Supplier information, and Policy rules.

### Permitted Strategies
* **Use Existing Stock**: Reallocate stock to protect Strategic/SLA orders.
* **Use Approved Alternate**: Source shortage from an approved alternate supplier.
* **Expedite Existing PO**: Request expedited shipping on the primary PO.
* **Partial Fulfillment**: Ship partial quantities to permitted customers.
* **Customer Date Negotiation**: Delay shipping dates for standard customers.
* **Management Escalation / Manual Review**: Triggered if no viable routes exist.

### Restricted Sourcing Actions (Strict Governance Guardrails)
* Cannot place a Purchase Order in the database.
* Cannot change supplier approval flags.
* Cannot cancel customer orders.
* Cannot promise specific delivery dates without approval.
* Cannot bypass quality hold or spend limits.

### Output Contract
* `ProposedStrategy` (String)
* `StrategyComponents` (String)
* `OrdersProtected` (Integer)
* `OrdersRemainingAtRisk` (Integer)
* `RequiredApprovals` (String)
* `ResidualRisk` (Low / Medium / High / Critical)
* `RequiredCustomerAction` (String)
* `RequiredInternalActions` (String)
* `Rationale` (String)
* `Confidence` (High / Medium / Low)
* `Completed` (Yes / No)

---

## 6. Reporting & Communication Specialist

### Purpose
Compile the final disruption response details into a Word document report and send email notifications to stakeholders.

### Operations
* **Microsoft Word Report**: Uses the Word Online (Business) connector to generate a standardized report file containing:
  * Disruption ID, Affected SKU, Supplier, Disruption Type, Expected Recovery Date.
  * Inventory Shortages, Customer SLA Risk, Sourcing Options, Commercial Cost Premium.
  * Proposed Strategy, Required Approvals, Risk Rationale.
* **Outlook Notification**: Sends email notifications depending on the disruption's final state:
  * **Recovery Plan Proposed** ➔ Notify Supply Planning + Procurement teams.
  * **Awaiting Approval** ➔ Send approval request to the designated Approver.
  * **Customer Action Required** ➔ Email Customer Operations Lead.
  * **Management Escalation** ➔ Escalate to Supply Chain Director.
  * **Insufficient Evidence** ➔ Email Operational Owner for data corrections.
