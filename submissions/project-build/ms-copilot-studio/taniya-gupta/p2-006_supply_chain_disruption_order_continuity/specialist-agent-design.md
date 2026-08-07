# Specialist Agent Design — Child Agents Specifications

## Overview
The architecture incorporates **6 specialist child agents**, each scoped strictly to its functional domain to prevent tool ambiguity and enforce separation of responsibilities.

---

### Specialist 1: Inventory Impact Specialist
- **Role:** Evaluates usable inventory, ATP, safety stock, daily consumption, and shortage risk.
- **Key Formula:** `ATP = On Hand - Reserved + Inbound Within 7 Days - Quality Hold`
- **Strict Guardrail:** Quality-held stock (`QualityHold = Yes`) MUST be excluded from ATP.
- **Tools Scoped:** `InventoryTable`, `SKUMasterTable`, `PurchaseOrdersTable`.

---

### Specialist 2: Alternate Supplier Specialist
- **Role:** Evaluates alternate supplier options, capacity, lead times, and unit costs.
- **Strict Guardrail:** If `Approved = No`, supplier MUST NOT be recommended as autonomous recovery source. Qualification restriction `Manual supplier qualification option required` must be returned.
- **Tools Scoped:** `AlternateSuppliersTable`, `SuppliersTable`, `SKUMasterTable`.

---

### Specialist 3: Customer & Order Impact Specialist
- **Role:** Evaluates all open customer orders for the affected SKU and ranks demand prioritization.
- **Priority Hierarchy:**
  1. Strategic + SLA Protected
  2. Priority
  3. Standard
- **Strict Guardrail:** Evaluates ALL open orders for the SKU. Respects `PartialFulfillmentAllowed = No` constraints.
- **Tools Scoped:** `CustomerOrdersTable`, `SKUMasterTable`, `InventoryTable`.

---

### Specialist 4: Commercial Impact Specialist
- **Role:** Calculates financial impact metrics and evaluates approval thresholds.
- **Key Calculations:**
  - `CostPremiumPct = ((Alternate Unit Cost - Primary Cost) / Primary Cost) * 100`
  - `IncrementalCost = (Alternate Unit Cost - Primary Cost) * Required Quantity`
  - `ExpeditePremiumPct = ((Expedited Cost - Standard Cost) / Standard Cost) * 100`
- **Threshold Rules:**
  - Alternate Cost Premium > 15% → `Finance Business Partner` approval required.
  - Expedite Premium > 10% → `Supply Chain Director` approval required.
- **Tools Scoped:** `RecoveryRulesTable`, `SKUMasterTable`.

---

### Specialist 5: Recovery Planning Specialist
- **Role:** Synthesizes consolidated outputs after fan-in into a policy-compliant recovery plan.
- **Execution Timing:** Sequential, strictly after fan-in.
- **Permitted Strategies:** Use existing stock, reallocate inventory, use approved alternate, expedite supply, partial fulfillment, customer date negotiation, combined strategy, management escalation.
- **Strict Restrictions:** Cannot place POs, approve unapproved suppliers, cancel orders, or approve spend.
- **Knowledge Source:** `NovaSphere Supply Continuity Policy`.

---

### Specialist 6: Reporting & Communication Specialist
- **Role:** Creates Word report and sends state-mapped Outlook emails.
- **Execution Timing:** Sequential, strictly after Supervisor decision validation.
- **Recipient Mapping:**
  - `Recovery Plan Proposed` → Supply Planning + Procurement
  - `Awaiting Approval` → Required Approver (Finance / Director)
  - `Customer Action Required` → Customer Operations Lead
  - `Management Escalation` → Supply Chain Director
  - `Insufficient Evidence` → Responsible Operational Owner
- **Tools Scoped:** Word Online (Business), Office 365 Outlook.
