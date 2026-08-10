# Dataset Notes

## Overview

The solution uses a structured Microsoft Excel workbook as the primary business data source. The dataset simulates supply chain disruption scenarios and provides the information required by the Supervisor Agent and specialist child agents to perform autonomous disruption assessment and recovery planning.

The workbook is organized into multiple tables, each representing a specific business domain. Together, these datasets enable end-to-end orchestration without requiring external systems.

---

# Dataset Structure

| Table | Purpose | Used By |
|--------|---------|---------|
| Disruption_Requests | Stores disruption requests awaiting assessment | Supervisor, Inventory, Alternate Supplier, Customer, Commercial |
| Inventory | Stores inventory availability and ATP information | Inventory, Customer |
| SKU_Master | Stores SKU planning information | Inventory, Alternate Supplier, Customer |
| Purchase_Orders | Stores inbound purchase order details | Inventory |
| Alternate_Suppliers | Stores alternate supplier information | Alternate Supplier, Commercial |
| Suppliers | Stores supplier profile and performance | Alternate Supplier |
| Customer_Orders | Stores customer demand and commitments | Customer, Commercial |
| Recovery_Rules | Stores commercial approval thresholds and business rules | Commercial |

---

# Table Descriptions

## 1. Disruption_Requests

### Purpose

Acts as the primary entry point for the workflow.

The Supervisor retrieves the oldest disruption whose status is **Pending** and initiates the assessment.

### Example Fields

- DisruptionID
- SupplierID
- SKU
- PurchaseOrder
- AffectedQuantity
- Status
- ExpectedRecoveryDate
- DisruptionType

### Used By

- Supply Continuity Supervisor
- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

---

## 2. Inventory

### Purpose

Provides inventory availability required for inventory assessment.

### Example Fields

- SKU
- OnHandQty
- ReservedQty
- AvailableToPromiseQty
- InboundWithin7DaysQty
- QualityHoldQty

### Used By

- Inventory Impact Specialist
- Customer & Order Impact Specialist

---

## 3. SKU_Master

### Purpose

Stores planning information for each product.

### Example Fields

- SKU
- ProductName
- DailyConsumption
- SafetyStockQty

### Used By

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist

---

## 4. Purchase_Orders

### Purpose

Stores inbound purchase order information.

Used to determine future inventory availability.

### Example Fields

- PurchaseOrder
- SKU
- SupplierID
- ExpectedDeliveryDate
- Quantity

### Used By

- Inventory Impact Specialist

---

## 5. Alternate_Suppliers

### Purpose

Stores approved alternate supplier options.

### Example Fields

- AlternateSupplierID
- SKU
- Approved
- AvailableCapacityQty
- LeadTimeDays
- ExpediteLeadTimeDays
- ExpeditePremiumPct
- UnitCost_INR

### Used By

- Alternate Supplier Specialist
- Commercial Impact Specialist

---

## 6. Suppliers

### Purpose

Stores supplier profile and performance information.

### Example Fields

- SupplierID
- SupplierName
- RiskRating
- OnTimeDeliveryPct
- QualityScore
- StandardLeadTimeDays

### Used By

- Alternate Supplier Specialist

---

## 7. Customer_Orders

### Purpose

Stores customer demand and order commitments.

### Example Fields

- OrderID
- CustomerID
- CustomerName
- SKU
- OrderedQty
- Revenue
- CustomerTier
- StrategicCustomer
- SLAProtected
- PartialFulfillmentAllowed
- RequiredDate

### Used By

- Customer & Order Impact Specialist
- Commercial Impact Specialist

---

## 8. Recovery_Rules

### Purpose

Stores business rules used during commercial assessment.

### Example Fields

- RuleName
- ThresholdValue
- RequiredApproval
- Description

### Used By

- Commercial Impact Specialist

---

# Dataset Relationships

```
Disruption_Requests
        │
        ├─────────────► Inventory
        │
        ├─────────────► SKU_Master
        │
        ├─────────────► Purchase_Orders
        │
        ├─────────────► Alternate_Suppliers
        │                     │
        │                     ▼
        │                 Suppliers
        │
        └─────────────► Customer_Orders

Commercial Impact Specialist
        │
        ▼
Recovery_Rules
```

---

# Dataset Usage by Agent

| Agent | Tables Used |
|--------|-------------|
| Supply Continuity Supervisor | Disruption_Requests |
| Inventory Impact Specialist | Disruption_Requests, Inventory, SKU_Master, Purchase_Orders |
| Alternate Supplier Specialist | Disruption_Requests, Alternate_Suppliers, Suppliers, SKU_Master |
| Customer & Order Impact Specialist | Disruption_Requests, Customer_Orders, Inventory, SKU_Master |
| Commercial Impact Specialist | Disruption_Requests, Alternate_Suppliers, Customer_Orders, Recovery_Rules |
| Recovery Planning Specialist | Receives consolidated specialist assessments (no direct dataset access) |
| Reporting & Communication Specialist | Uses approved Supervisor outputs (no direct dataset access) |

---

# Assumptions

The dataset assumes that:

- Each disruption has a unique **DisruptionID**.
- Every SKU exists in the SKU Master table.
- Inventory records exist for all affected SKUs.
- Customer orders reference valid SKUs.
- Alternate suppliers reference valid SKUs.
- Supplier records are complete.
- Business rule thresholds are maintained in the Recovery_Rules table.

---

# Limitations

- The dataset is intended for demonstration purposes.
- Data is static and does not update in real time.
- Relationships are maintained manually within the workbook.
- Historical disruption records are limited.
- Live ERP synchronization is not implemented.

---

# Future Improvements

The dataset can be enhanced by integrating with enterprise systems such as:

- Microsoft Dataverse
- SQL Server
- Azure SQL Database
- SAP S/4HANA
- Microsoft Dynamics 365

These integrations would enable real-time disruption monitoring, inventory updates, supplier management, and customer order synchronization.