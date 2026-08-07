# Specialist Agent Design

![Copilot Studio Child Agents](screenshots/child_agents.png)

## Specialist 1 — Inventory Impact Specialist
### Purpose
Determine usable inventory and whether current stock can protect demand until supply recovers.

### Data
Inventory, SKU, PO data.

### Responsibilities
- Calculate ATP
- Consider projected ATP
- Check safety stock
- Identify shortage
- Exclude quality-held inventory
- Assess inventory feasibility

### Required logical output
AvailableToPromise, ProjectedATP, SafetyStock, ShortageQuantity, ShortageDate, QualityHoldImpact, InventoryAssessment, BlockingIssue, RecommendedInventoryAction, Confidence.

---

## Specialist 2 — Alternate Supplier Specialist
### Purpose
Evaluate feasible alternate suppliers.

### Data
Supplier and alternate supplier tables.

### Responsibilities
- Identify candidate suppliers
- Check approval/qualification
- Check capacity
- Check lead time
- Evaluate expedite feasibility
- Evaluate supplier risk
- Identify required-date feasibility

### Output
CandidateSuppliers, SelectedSupplierCandidate, AlternateCapacity, AlternateLeadTime, AlternateUnitCost, CanMeetRequiredDate, QualificationRestriction, SupplierRisk, RecommendedSupplierAction, BlockingIssue, Confidence.

---

## Specialist 3 — Customer & Order Impact Specialist
### Purpose
Assess customer commitments and prioritize affected orders.

### Data
CustomerOrdersTable and relevant inventory/order information.

### Responsibilities
- Count affected orders
- Identify strategic orders
- Identify SLA orders
- Calculate revenue at risk
- Identify earliest required date
- Determine partial fulfilment constraints
- Rank affected orders

### Output
AffectedOrderCount, StrategicOrdersAtRisk, SLAOrdersAtRisk, RevenueAtRisk, EarliestRequiredDate, PartialFulfillmentConstraints, RankedAffectedOrders, CustomerImpactClassification, RecommendedCustomerAction, Confidence.

---

## Specialist 4 — Commercial Impact Specialist
### Purpose
Determine financial implications of recovery options.

### Responsibilities
- Calculate alternate supplier premium %
- Calculate incremental procurement cost
- Calculate expedite premium %
- Calculate revenue exposure
- Determine commercial approval requirement

### Rules
- Alternate premium >15% → Finance Business Partner approval.
- Expedite premium >10% → Supply Chain Director approval.
- Policy is authoritative.

### Output
CostPremiumPct, IncrementalCost, RevenueExposure, ExpeditePremiumPct, CommercialRisk, ApprovalRequired, RequiredApprover, RecommendedCommercialAction, Confidence.

---

## Specialist 5 — Recovery Planning Specialist
### Execution
Runs only after fan-in.

### Inputs
- Inventory assessment
- Alternate supplier assessment
- Customer impact assessment
- Commercial assessment
- Disruption severity
- Supplier information
- Policy rules

### Permitted proposed strategies
- Use existing stock
- Reallocate inventory
- Use approved alternate supplier
- Expedite existing supply
- Expedite alternate supply
- Partial fulfilment
- Customer-date negotiation
- Combined recovery strategy
- Management escalation
- Manual review

### Restrictions
Must not place a PO, approve alternate suppliers, cancel orders, promise delivery dates, approve commercial spend, ignore quality holds, or ignore customer priority.

### Output
ProposedStrategy, StrategyComponents, OrdersProtected, OrdersRemainingAtRisk, RequiredApprovals, ResidualRisk, RequiredCustomerAction, RequiredInternalActions, Rationale, Confidence.

---

## Specialist 6 — Reporting & Communication Specialist
### Execution
Runs only after final Supervisor decision.

### Word report
![Word Document Tool Configuration](screenshots/word-tool.png)

Must contain:
- Disruption ID
- Supplier
- SKU
- Disruption type
- Affected PO
- Supplier recovery date
- Inventory assessment
- Customer impact
- Alternate supplier analysis
- Commercial analysis
- Selected recovery strategy
- Required approvals
- Orders protected
- Orders remaining at risk
- Revenue at risk
- Residual risk
- Required actions
- Evidence limitations
- Final Supervisor status

### Outlook
![Outlook Email Tool Configuration](screenshots/outlook-tool.png)

Send only after Supervisor authorization. Recipient depends on final state.

Examples:
- Recovery Plan Proposed → Supply planning + procurement
- Awaiting Approval → Required approver
- Customer Action Required → Customer Operations Lead
- Management Escalation → Supply Chain Director
- Insufficient Evidence → Responsible operational owner
- Completed → Relevant stakeholders
