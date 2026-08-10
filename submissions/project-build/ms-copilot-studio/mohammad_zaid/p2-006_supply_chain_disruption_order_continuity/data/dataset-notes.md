
# Dataset Notes

# Overview

The Autonomous Supply Chain Disruption & Order Continuity Response System uses a structured Microsoft Excel workbook as its operational datastore. The workbook contains multiple normalized tables representing disruptions, inventory, suppliers, customer orders, recovery policies, and stakeholder information.

Each table is accessed through Microsoft Excel Online (Business) connectors configured in Microsoft Copilot Studio.

---

# Workbook Information

| Property         | Value                             |
| ---------------- | --------------------------------- |
| Storage          | OneDrive for Business             |
| Format           | Microsoft Excel (.xlsx)           |
| Access Method    | Excel Online (Business) Connector |
| Primary Consumer | Supply Continuity Supervisor      |
| Child Consumers  | Specialist Agents                 |

---

# Dataset Architecture

```
                    DisruptionRequestsTable
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
 InventoryTable        PurchaseOrdersTable   CustomerOrdersTable
         │
         ▼
   SKUMasterTable
         │
         ▼
 AlternateSuppliersTable
         │
         ▼
    SuppliersTable

RecoveryRulesTable
StakeholdersTable
```

---

# Table 1 — DisruptionRequestsTable

## Purpose

Stores all incoming supply disruption requests.

This table acts as the entry point for the complete orchestration workflow.

---

## Primary Key

```
DisruptionID
```

---

## Accessed By

- Supply Continuity Supervisor

---

## Tools

- SUP - Get Pending Disruptions
- SUP - Update Disruption Status

---

## Important Columns

- DisruptionID
- Status
- SupplierID
- SKU
- DisruptionType
- ReportedDate
- ExpectedRecoveryDate
- AffectedPO
- AffectedQty
- ReportedSeverity

---

## Usage

- Detect pending disruptions
- Validate disruption requests
- Track workflow status
- Update disruption lifecycle

---

# Table 2 — InventoryTable

## Purpose

Stores current inventory availability and stock information for each SKU.

---

## Primary Key

```
SKU
```

---

## Accessed By

- Inventory Impact Specialist
- Customer & Order Impact Specialist

---

## Tools

- INV - Get Inventory Data
- CUS - Get Inventory Data

---

## Important Columns

- SKU
- Warehouse
- AvailableInventory
- ReservedInventory
- SafetyStock
- QualityHold
- LastUpdated

---

## Usage

- Inventory availability
- Safety stock analysis
- Shortage calculation
- Customer allocation

---

# Table 3 — PurchaseOrdersTable

## Purpose

Stores inbound purchase orders and expected replenishment information.

---

## Primary Key

```
PurchaseOrderID
```

---

## Accessed By

- Inventory Impact Specialist

---

## Tool

- INV - Get Purchase Order Data

---

## Important Columns

- PurchaseOrderID
- SupplierID
- SKU
- Quantity
- ExpectedDeliveryDate
- Status

---

## Usage

- Incoming inventory evaluation
- Replenishment analysis
- Recovery planning

---

# Table 4 — CustomerOrdersTable

## Purpose

Stores customer demand and delivery commitments.

---

## Primary Key

```
CustomerOrderID
```

---

## Accessed By

- Customer & Order Impact Specialist

---

## Tool

- CUS - Get Customer Order Data

---

## Important Columns

- CustomerOrderID
- CustomerID
- SKU
- OrderQuantity
- RequiredDate
- CustomerPriority
- SLA
- Revenue

---

## Usage

- Customer impact analysis
- Revenue calculation
- SLA protection
- Order prioritization

---

# Table 5 — AlternateSuppliersTable

## Purpose

Contains approved alternate suppliers for supported SKUs.

---

## Primary Key

```
AlternateSupplierID
```

---

## Accessed By

- Alternate Supplier Specialist

---

## Tool

- ALT - Get Alternate Supplier Data

---

## Important Columns

- AlternateSupplierID
- SupplierID
- SKU
- LeadTime
- Capacity
- ApprovalStatus

---

## Usage

- Alternate supplier selection
- Capacity validation
- Lead time comparison

---

# Table 6 — SuppliersTable

## Purpose

Contains supplier master information.

---

## Primary Key

```
SupplierID
```

---

## Accessed By

- Alternate Supplier Specialist

---

## Tool

- ALT - Get Supplier Data

---

## Important Columns

- SupplierID
- SupplierName
- SupplierRisk
- Region
- ContactInformation

---

## Usage

- Supplier verification
- Supplier risk evaluation
- Supplier profile lookup

---

# Table 7 — SKUMasterTable

## Purpose

Maintains master data for all products.

---

## Primary Key

```
SKU
```

---

## Accessed By

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist

---

## Tools

- INV - Get SKU Master Data
- ALT - Get SKU Master Data
- CUS - Get SKU Master Data

---

## Important Columns

- SKU
- ProductName
- ProductCategory
- UnitOfMeasure
- SafetyStockTarget

---

## Usage

- Product validation
- SKU lookup
- Product metadata

---

# Table 8 — RecoveryRulesTable

## Purpose

Stores business recovery policies and commercial approval thresholds.

---

## Primary Key

```
RuleID
```

---

## Accessed By

- Commercial Impact Specialist

---

## Tool

- COM - Get Recovery Rules

---

## Important Columns

- RuleID
- RuleName
- ThresholdValue
- ApprovalRole
- RuleDescription

---

## Usage

- Approval evaluation
- Cost thresholds
- Commercial policies

---

# Table 9 — StakeholdersTable

## Purpose

Stores notification recipients and reporting contacts.

---

## Accessed By

- Reporting & Communication Specialist

---

## Current Usage

Prepared for future enhancement.

The current implementation uses Outlook recipients configured during report generation.

---

# Table Relationships

| Parent Table            | Related Table       | Relationship |
| ----------------------- | ------------------- | ------------ |
| DisruptionRequestsTable | SuppliersTable      | SupplierID   |
| DisruptionRequestsTable | SKUMasterTable      | SKU          |
| DisruptionRequestsTable | PurchaseOrdersTable | AffectedPO   |
| InventoryTable          | SKUMasterTable      | SKU          |
| PurchaseOrdersTable     | SuppliersTable      | SupplierID   |
| PurchaseOrdersTable     | SKUMasterTable      | SKU          |
| CustomerOrdersTable     | SKUMasterTable      | SKU          |
| AlternateSuppliersTable | SuppliersTable      | SupplierID   |
| AlternateSuppliersTable | SKUMasterTable      | SKU          |

---

# Dataset Access Pattern

The implementation intentionally avoids OData filtering within Excel connectors to improve connector stability and reduce runtime issues observed during testing.

Instead:

- Required tables are retrieved.
- Business filtering and decision-making are performed by the respective Copilot Studio agents.

This approach simplifies connector configuration and improves maintainability.

---

# Dataset Validation

Before orchestration begins, the Supervisor validates:

- Disruption ID
- Pending status
- Supplier ID
- SKU
- Purchase Order
- Affected Quantity
- Reported Date

Only validated records proceed to specialist assessment.

---

# Data Ownership

| Table                   | Primary Owner           |
| ----------------------- | ----------------------- |
| DisruptionRequestsTable | Supply Chain Operations |
| InventoryTable          | Inventory Management    |
| PurchaseOrdersTable     | Procurement             |
| CustomerOrdersTable     | Customer Service        |
| SuppliersTable          | Supplier Management     |
| AlternateSuppliersTable | Procurement             |
| SKUMasterTable          | Master Data Management  |
| RecoveryRulesTable      | Commercial Operations   |
| StakeholdersTable       | Business Operations     |

---

# Implementation Notes

- Microsoft Excel Online (Business) is used as the operational datastore.
- Each specialist agent accesses only the tables required for its domain.
- The Supervisor coordinates all data flow between agents.
- Business policy is maintained separately within the Supervisor knowledge base.
- Dataset updates occur only through controlled Supervisor tools.
- The design minimizes coupling by keeping datasets domain-specific and avoiding unnecessary cross-table dependencies.

---

# Summary

The Excel workbook serves as the operational backbone of the solution, providing structured business data for disruption management, inventory analysis, supplier evaluation, customer impact assessment, commercial decision-making, and reporting. The normalized table design, combined with dedicated agent ownership and Microsoft Excel Online connectors, enables a modular, maintainable, and scalable data architecture aligned with the overall multi-agent orchestration strategy.
