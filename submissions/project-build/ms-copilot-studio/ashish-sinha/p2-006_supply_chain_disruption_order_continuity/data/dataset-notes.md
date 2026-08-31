# Dataset Notes

## Operational data source
The supplied workbook must be stored in:
- OneDrive for Business, or
- SharePoint

and accessed through Excel Online (Business).

## Required tables

### DisruptionRequestsTable
Used to identify reported disruptions and manage disruption state.

Key concepts:
- Disruption ID
- Supplier ID
- SKU
- Disruption type
- Reported date
- Expected recovery date
- Affected PO
- Affected quantity
- Reported severity
- Status

### SuppliersTable
Supplier master/reference information.

### SKUMasterTable
SKU master/reference information.

### InventoryTable
Inventory availability and related inventory constraints.

### PurchaseOrdersTable
Open purchase-order information and supplier/SKU relationship.

### CustomerOrdersTable
Affected customer demand, priorities, SLA commitments, required dates, and order impact.

### AlternateSuppliersTable
Alternate supplier candidates, approval/qualification, capacity, lead time, and cost information.

### RecoveryRulesTable
Deterministic recovery and approval rules where supplied.

### StakeholdersTable
Authorized stakeholder roles and communication routing.

## Data validation
Topic 1 must verify:
- required IDs exist
- disruption is unique
- status is Pending
- supplier exists
- SKU exists
- disruption type exists
- reported date is valid
- PO exists and matches supplier/SKU
- affected quantity is positive

## Data integrity
Do not create unrelated replacement data when the supplied workbook is available. Do not invent missing supplier approval, customer agreement, costs, quantities, or stakeholder recipients.

## Knowledge source
Add **NovaSphere Supply Continuity Policy** as the authoritative knowledge source. It defines customer priority, inventory rules, alternate supplier rules, commercial approval, recovery strategies, decision precedence, risk classification, reassessment, failure handling, and final status definitions.

## Tool allocation
- Supervisor → state/orchestration
- Inventory Specialist → inventory/SKU/PO
- Alternate Supplier Specialist → supplier/alternate supplier
- Customer & Order Specialist → customer orders and relevant inventory/order data
- Commercial Specialist → cost and approval data
- Recovery Planning Specialist → consolidated specialist outputs + policy
- Reporting Specialist → Word + Outlook
