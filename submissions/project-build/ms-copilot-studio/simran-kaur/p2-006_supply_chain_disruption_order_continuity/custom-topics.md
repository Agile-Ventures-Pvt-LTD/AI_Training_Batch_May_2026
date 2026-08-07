# Custom Topics Design

This document details the configuration, variables, logic flow, and edge-case handling for the three custom topics implemented within Microsoft Copilot Studio.

---

## Topic 1: Disruption Intake & Validation

### Purpose
Perform deterministic data validation before triggering the multi-agent assessment flow. This topic protects the downstream specialists from processing duplicate, corrupted, or inconsistent Excel records.

### Logic Flow Diagram
```
[Ingest Pending Disruption Row]
             │
             ▼
  {Check DisruptionID Exists?} ────(No)───➔ [Set Status: Insufficient Evidence]
             │ (Yes)
             ▼
  {Check Duplicate ID?} ──────────(Yes)──➔ [Set Status: Duplicate In Assessment]
             │ (No)
             ▼
 {SKU & Supplier Exist in Masters?} ─(No)─➔ [Set Status: Manual Review]
             │ (Yes)
             ▼
{PO Exists and matches SKU/Supplier?} ──(No)➔ [Set Status: Insufficient Evidence]
             │ (Yes)
             ▼
      [Validation Passed] ➔ [Update Status: In Assessment] ➔ [Begin Specialists Fan-Out]
```

### Input & Output Variables

| Variable Name | Type | Direction | Validation Criteria / Purpose |
|---|---|---|---|
| `DisruptionID` | String | Input/Output | Must exist in the register, must be unique. |
| `SupplierID` | String | Output | Must match a valid record in `SuppliersTable`. |
| `SKU` | String | Output | Must match a valid record in `SKUMasterTable`. |
| `DisruptionType` | String | Output | Cannot be null or blank. |
| `ReportedDate` | Date | Output | Must be a valid date. |
| `ExpectedRecoveryDate` | Date | Output | Must be after or equal to `ReportedDate`. |
| `AffectedPO` | String | Output | Must exist in `PurchaseOrdersTable`. |
| `AffectedQty` | Decimal | Output | Must be a positive number (>0). |
| `ReportedSeverity` | String | Output | Maps to Low, Medium, High, or Critical. |
| `ValidationStatus` | String | Output | `Valid` / `Invalid` / `Duplicate` |
| `DuplicateDetected` | Boolean | Output | Sets to `True` if ID is already being processed. |

### Invalid Input Handling
* If validation fails (e.g. invalid PO relationship, non-existent SKU), the topic halts further execution.
* The system writes the validation error reason to the disruption log.
* The status is updated to `Insufficient Evidence` or `Manual Review`, preventing child agents from running on corrupted inputs.

---

## Topic 2: Recovery Strategy Resolution

### Purpose
Resolve competing specialist recommendations after the parallel fan-in. It uses a deterministic decision tree based on NovaSphere's policies instead of averaging specialist scores.

### Decision Precedence Logic
1. **Safety or Quality Restrictions**: Quality-held stock is excluded; unapproved suppliers are blocked.
2. **Strategic/SLA commitments**: Prioritize available stock to Strategic/SLA orders.
3. **Supplier Approval Restriction**: Never select unapproved alternate suppliers for autonomous recovery.
4. **Inventory Availability and Timing**: Check if existing stock covers the shortage timeframe.
5. **Commercial Approval**: Flag cost premiums (>15%) or expediting (>10%).
6. **Cost Optimization**: Select the lowest-cost option among remaining approved options.

### Operational Branches

#### Branch A: Existing Inventory Sufficient
* **Condition**: Available to Promise (ATP) stock covers the entire customer demand during the recovery window.
* **Action**: Reallocate existing stock, avoid alternate sourcing or expedited logistics, and verify if safety stock consumption is required.

#### Branch B: Partial Inventory
* **Condition**: ATP stock covers only a portion of the customer demand.
* **Action**: Rank orders by priority, protect Strategic/SLA orders with existing stock, and route remaining standard orders to alternate supplier sourcing or partial fulfillment evaluation.

#### Branch C: Approved Alternate Available
* **Condition**: Stock is short, but an approved alternate supplier has capacity and can meet required delivery dates.
* **Action**: Propose alternate sourcing, calculate unit-cost and expediting premiums, and check for commercial approval.

#### Branch D: Unapproved Alternate Only
* **Condition**: No approved alternates exist, but an unapproved supplier is available.
* **Action**: Do not recommend autonomous sourcing. Transition status to `Awaiting Approval` or `Management Escalation` for manual supplier qualification.

#### Branch E: No Viable Recovery Route
* **Condition**: No inventory, no approved/unapproved alternate capacity, and delivery dates will be missed.
* **Action**: Escalate case, set risk to `Critical`, and transition status to `Management Escalation`.

---

## Topic 3: Approval, Exception & Selective Reassessment

### Purpose
Manage human approval boundaries, retry failed specialist executions, and execute targeted reassessments if data changes.

### Approval Routing Conditions
The topic transitions the disruption to `Awaiting Approval` if any of the following are true:
* Cost premium exceeds **15%** (routes to Finance Business Partner).
* Expediting premium exceeds **10%** (routes to Supply Chain Director).
* Strategic SLA order requires consuming safety stock.
* Sourcing requires manual supplier qualification (unapproved supplier).
* Customer order requires split shipment but partial fulfillment permission is not defined.

### Selective Reassessment Flow
If data changes during assessment (e.g. alternate supplier capacity update):
1. **Identify Stale Output**: Determine which specialist's inputs changed (in this case, Alternate Supplier).
2. **Targeted Re-run**: Re-execute only the Alternate Supplier Specialist and the Commercial Specialist (to recalculate costs).
3. **Preserve State**: Retain the previous output of the Inventory and Customer Impact Specialists to save processing time.
4. **Re-enter Fan-In**: Update the Supervisor variables and rerun the Recovery Planning Specialist.
5. **Loop Limit Safeguard**: Max reassessment loops = **2**. If unresolved after 2 loops, the state is forced to `Manual Review` to prevent infinite execution loops.
