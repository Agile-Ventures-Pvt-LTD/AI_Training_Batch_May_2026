# Specialist Agent Design

## 1. Inventory Impact Specialist
**Purpose:** inventory availability and recovery coverage.

**Tools:** Inventory, SKU_Master, Purchase_Orders, Disruption_Requests, Supply Continuity Policy.

**Outputs:** ATP, Safety Stock, Daily Consumption, Demand Until Recovery, Shortage Quantity, Quality-Hold Impact, Inventory Assessment.

**Restriction:** no supplier selection or final strategy.

## 2. Alternate Supplier Specialist
**Purpose:** evaluate alternate supplier feasibility.

**Tools:** Alternate_Suppliers, Suppliers, SKU_Master, Disruption_Requests, Supply Continuity Policy.

**Outputs:** approval status, capacity, standard/expedite lead time, cost, supplier risk, required-date feasibility.

**Restriction:** unapproved supplier is manual qualification only.

## 3. Customer & Order Impact Specialist
**Purpose:** evaluate all open affected customer orders.

**Tools:** Customer_Orders, SKU_Master, Inventory, Disruption_Requests, Supply Continuity Policy.

**Priority:** Strategic/SLA → Priority → Standard.

**Outputs:** affected orders, Strategic/SLA risk, revenue exposure, earliest required date, fulfilment constraints, ranked orders and customer action.

**Restriction:** no order cancellation/modification or delivery promise.

## 4. Commercial Impact Specialist
**Purpose:** financial impact and approval requirement.

**Tools:** SKU_Master, Alternate_Suppliers, Customer_Orders, Disruption_Requests, Stakeholders, Supply Continuity Policy.

**Rules:** alternate premium >15% → Finance Business Partner; expedite premium >10% → Supply Chain Director.

**Outputs:** cost premium, incremental cost, revenue exposure, expedite premium, commercial risk and approval requirement.

## 5. Recovery Planning Specialist
**Execution:** only after fan-in.

**Inputs:** four specialist findings, disruption severity, supplier information and policy.

**Strategies:** existing stock, reallocation, approved alternate, expedite, partial fulfilment, customer-date negotiation, combined strategy, management escalation or manual review.

**Restriction:** no PO placement, supplier approval, order cancellation, delivery promise or commercial approval.

## 6. Reporting & Communication Specialist
**Execution:** only after final Supervisor decision.

**Tools:** Word Online (Business), Outlook.

**Report:** disruption, supplier, SKU, PO, recovery date, inventory, customer, alternate supplier, commercial analysis, strategy, approvals, orders protected/at risk, revenue/residual risk, actions, evidence limitations and final status.

**Communication:** only after Supervisor authorization and according to final state.

## Common Specialist Output
SpecialistName, AssessmentStatus, EvidenceSummary, QuantitativeFindings, BlockingIssues, Constraints, RecommendedAction, ApprovalRequired, RequiredApprover, Confidence, Completed.
