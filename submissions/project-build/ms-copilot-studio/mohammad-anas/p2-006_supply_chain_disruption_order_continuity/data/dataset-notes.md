# Dataset Notes

## Overview

The **P2-006 Supply Chain Disruption Order Continuity** solution uses a Microsoft Excel workbook as its operational datastore.

The workbook contains multiple structured tables representing different business entities involved in supply chain continuity management. These tables are accessed through Microsoft Excel Online (Business) connectors configured within Microsoft Copilot Studio.

The dataset supports autonomous disruption assessment, recovery planning, reporting, and lifecycle management.

---

# Dataset Summary

| Table | Purpose |
|--------|---------|
| Disruption Requests | Stores reported supply chain disruptions awaiting assessment. |
| Suppliers | Contains supplier master information. |
| SKU Master | Stores product master data and SKU attributes. |
| Inventory | Contains inventory balances and stock availability. |
| Purchase Orders | Stores inbound purchase order information. |
| Customer Orders | Contains customer demand and fulfilment information. |
| Alternate Suppliers | Stores approved alternate sourcing options. |
| Recovery Rules | Defines business continuity and recovery policies. |
| Stakeholders | Contains stakeholder contact information for notifications. |

---

# Table Descriptions

## 1. Disruption Requests

### Purpose

Acts as the primary operational table for the workflow.

The Supervisor retrieves pending disruption requests from this table and initiates the assessment workflow.

### Key Fields

- DisruptionID
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- SeverityReported
- Reason
- Status
- Notes

### Used By

- Supervisor Agent
- Disruption Intake & Validation Topic
- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

---

## 2. Suppliers

### Purpose

Stores supplier master information required for supplier continuity assessments.

### Typical Information

- Supplier ID
- Supplier Name
- Region
- Country
- Operational Status
- Capacity
- Risk Rating

### Used By

- Alternate Supplier Specialist
- Commercial Impact Specialist

---

## 3. SKU Master

### Purpose

Maintains product master information.

### Typical Information

- SKU
- Product Name
- Product Category
- Criticality
- Preferred Supplier
- Safety Stock

### Used By

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist

---

## 4. Inventory

### Purpose

Tracks available inventory and stock coverage.

### Typical Information

- SKU
- Warehouse
- Available Quantity
- Reserved Quantity
- Safety Stock
- Reorder Point

### Used By

- Inventory Impact Specialist
- Customer & Order Impact Specialist

---

## 5. Purchase Orders

### Purpose

Stores inbound purchase orders that may reduce disruption impact.

### Typical Information

- Purchase Order Number
- Supplier
- SKU
- Quantity
- Expected Delivery Date
- Status

### Used By

- Inventory Impact Specialist

---

## 6. Customer Orders

### Purpose

Stores customer demand and delivery commitments.

### Typical Information

- Customer ID
- Customer Name
- Order Number
- SKU
- Quantity
- Delivery Date
- Priority

### Used By

- Customer & Order Impact Specialist

---

## 7. Alternate Suppliers

### Purpose

Stores approved alternate sourcing options for business continuity.

### Typical Information

- Supplier ID
- Alternate Supplier
- Approved Status
- Capacity
- Lead Time
- Region

### Used By

- Alternate Supplier Specialist
- Commercial Impact Specialist

---

## 8. Recovery Rules

### Purpose

Defines organizational recovery policies and approval thresholds.

### Typical Information

- Recovery Strategy
- Approval Threshold
- Business Priority
- Recovery Timeline
- Escalation Rule

### Used By

- Commercial Impact Specialist
- Recovery Planning Specialist

---

## 9. Stakeholders

### Purpose

Stores notification recipients used during reporting.

### Typical Information

- Name
- Role
- Department
- Email Address
- Approval Level

### Used By

- Reporting & Communication Specialist

---

# Dataset Relationships

```text
Disruption Requests
        │
        ├────────► Suppliers
        │
        ├────────► SKU Master
        │
        ├────────► Inventory
        │
        ├────────► Purchase Orders
        │
        ├────────► Customer Orders
        │
        ├────────► Alternate Suppliers
        │
        ├────────► Recovery Rules
        │
        └────────► Stakeholders
```

---

# Data Usage by Workflow

| Workflow Stage | Dataset Used |
|----------------|--------------|
| Disruption Intake | Disruption Requests |
| Inventory Assessment | Inventory, SKU Master, Purchase Orders |
| Supplier Assessment | Suppliers, Alternate Suppliers, SKU Master |
| Customer Assessment | Customer Orders, Inventory |
| Commercial Assessment | Recovery Rules, Suppliers, Alternate Suppliers |
| Recovery Planning | Specialist outputs + NovaSphere Supply Continuity Policy |
| Reporting | Disruption Requests + Specialist findings + Stakeholders |

---

# Data Access Pattern

The solution follows a controlled data access model.

1. The Supervisor retrieves the oldest pending disruption.
2. The disruption record is validated.
3. Specialist agents retrieve only the data required for their assigned responsibility.
4. The Recovery Planning Specialist consumes structured specialist outputs rather than querying Excel directly.
5. The Reporting & Communication Specialist generates reports and notifications using the validated assessment results.
6. The Supervisor updates the disruption lifecycle status upon workflow completion.

---

# Assumptions

The dataset assumes:

- All tables are stored in a single Microsoft Excel workbook.
- Primary keys are unique.
- Relationships between tables are maintained.
- Required connector permissions are configured.
- Data quality is sufficient for autonomous assessment.
- The workbook is accessible through Microsoft Excel Online (Business).

---

# Limitations

- Excel is used as a demonstration datastore and is not intended for high-volume transactional workloads.
- The dataset represents predefined laboratory scenarios rather than live enterprise data.
- Referential integrity depends on workbook maintenance and is not enforced automatically.
- Simultaneous edits may affect concurrency in collaborative environments.

---

# Conclusion

The supplied dataset provides the operational foundation for the Supply Chain Disruption Order Continuity solution. By organizing disruption requests, inventory, suppliers, customer orders, recovery rules, and stakeholder information into structured Excel tables, the solution enables autonomous assessment, policy-driven recovery planning, lifecycle management, and stakeholder communication within Microsoft Copilot Studio.