# Decision Rules & Policy Matrix

This document defines the deterministic rules, classification logic, and threshold metrics derived from the **NovaSphere Supply Continuity Policy**. These rules override any generative language-model decisions.

---

## 1. Inventory & Sourcing Calculations

### Available to Promise (ATP)
Usable inventory is calculated using the following formula:
$$\text{ATP} = \text{On Hand} - \text{Reserved} + \text{Inbound Within 7 Days} - \text{Quality Hold}$$

* **Safety Stock**: Minimum stock required for buffer. If demand consumes safety stock, a flag `SafetyStockConsumed` is set to `True`.
* **Quality Hold Exclusion**: Any inbound shipment or warehouse stock with `QualityHold = Yes` is excluded from the calculation.

---

## 2. Customer Prioritization & Order Ranking
When supply is insufficient to satisfy all open orders, inventory is allocated using the following hierarchy:

| Rank | Customer Tier | SLA Status | Priority Level | Allocation Action |
|---|---|---|---|---|
| **1** | Strategic Customer | SLA Protected | **Highest** | Allocate available stock first. Split-fulfillment prohibited if customer profile restricts it. |
| **2** | Strategic Customer | None | **High** | Allocate remaining stock. |
| **3** | Priority Customer | SLA Protected | **Medium** | Allocate remaining stock. |
| **4** | Priority Customer | None | **Medium-Low** | Evaluate alternate sourcing or expedites. |
| **5** | Standard Customer | SLA Protected | **Low-Medium** | Evaluate alternate sourcing. |
| **6** | Standard Customer | None | **Lowest** | Route to customer-date negotiation. |

---

## 3. Commercial Sourcing & Approval Thresholds
Sourcing recovery options are subject to financial limits. If a threshold is exceeded, the Supervisor routes the case to the `Awaiting Approval` state and notifies the designated approver:

| Cost Metric | Threshold | Required Action | Assigned Approver |
|---|---|---|---|
| **Alternate Unit-Cost Premium** | $>15.0\%$ | Seek Commercial Approval | Finance Business Partner |
| **Expediting Freight Premium** | $>10.0\%$ | Seek Expediting Approval | Supply Chain Director |
| **Unapproved Supplier Option** | Any quantity | Prevent Autonomous Sourcing | Supply Chain Director (Manual Qualification) |
| **Safety Stock Consumption** | For Strategic/SLA | Route for Operational Review | Supply Chain Director |

---

## 4. Final Risk Classification Matrix
The Supervisor assigns one of four risk levels to the disruption, providing a written rationale for any classification of `High` or `Critical`.

| Risk Level | Triggering Conditions | Required Action / Rationale |
|---|---|---|
| **Low** | Existing ATP covers all customer commitments during the recovery window. No alternate premiums or expediting fees. | Resolve with existing supply. Rationale: "Inventory is adequate to protect all commitments." |
| **Medium** | Shortage exists, but an approved alternate can meet the date within the standard approval thresholds (premium $\le 15\%$, expedite $\le 10\%$). | Propose Recovery Plan. Rationale: "Alternate supplier resolves shortage within approved cost limits." |
| **High** | Shortage impacts Priority customers, or alternate sourcing requires commercial approval (premium $>15\%$ or expedite $>10\%$), or requires consuming safety stock. | Route to Awaiting Approval. Rationale: "Alternate supplier exceeds commercial premium limits (Cost: [X]%, Expedite: [Y]%) requiring human approval." |
| **Critical** | Strategic/SLA-protected customer commitments will fail with no viable recovery option, or there is a supplier cancellation on a critical SKU with no alternate. | Escalate immediately. Rationale: "Critical SLA order for Strategic Customer is at risk with zero viable recovery options." |

---

## 5. Final Strategy Status Mappings
The system assigns exactly one final status at the end of the orchestration cycle:

* **Resolved with Existing Supply**: Inventory ATP covers demand; no external actions required.
* **Recovery Plan Proposed**: A viable strategy utilizing approved alternates or expedites has been identified and lies within cost thresholds.
* **Awaiting Approval**: Recovery plan is proposed but requires human authorization.
* **Customer Action Required**: Requires customer approval for split-shipment or delivery date changes.
* **Management Escalation**: No approved recovery path exists; critical SLA risk.
* **Insufficient Evidence**: Essential data is missing or a specialist failed twice.
* **Manual Review**: Reassessment loops are exhausted (max 2) or validation requires human correction.
* **Completed**: Report is generated, status is written, and stakeholders have been notified.
