# Operational Dataset & Relationships

This document details the structure, schemas, and relationships of the Microsoft Excel workbook used as the primary data store for the multi-agent system.

---

## 1. Overview of Excel Workbook
The data is stored in a single workbook hosted in **OneDrive for Business** or **SharePoint**, enabling access via the **Excel Online (Business)** connector. The workbook contains nine structured tables.

---

## 2. Table Schemas & Key Columns

### Table 1: `DisruptionRequestsTable`
Tracks disruption requests.
* **Key Columns**:
  * `DisruptionID` (String, Primary Key)
  * `SupplierID` (String, Foreign Key)
  * `SKU` (String, Foreign Key)
  * `DisruptionType` (String) - *e.g., Delay, Cancellation, Quality Hold*
  * `ReportedDate` (Date)
  * `ExpectedRecoveryDate` (Date)
  * `AffectedPO` (String, Foreign Key)
  * `AffectedQty` (Decimal)
  * `ReportedSeverity` (String) - *Low, Medium, High, Critical*
  * `Status` (String) - *Pending, In Assessment, Awaiting Approval, Recovery Plan Proposed, Completed, etc.*
  * `ResolutionNotes` (String)

### Table 2: `SuppliersTable`
Master list of primary component suppliers.
* **Key Columns**:
  * `SupplierID` (String, Primary Key)
  * `SupplierName` (String)
  * `SupplierRiskRating` (String) - *Low, Medium, High*
  * `ActiveStatus` (Boolean)

### Table 3: `SKUMasterTable`
Product master data.
* **Key Columns**:
  * `SKU` (String, Primary Key)
  * `Description` (String)
  * `CriticalClass` (String) - *Yes/No (indicates if the SKU is critical)*
  * `SafetyStockLevel` (Decimal)
  * `UnitOfMeasure` (String)

### Table 4: `InventoryTable`
Current warehouse stock levels.
* **Key Columns**:
  * `SKU` (String, Primary Key/Foreign Key)
  * `QtyOnHand` (Decimal)
  * `QtyReserved` (Decimal)
  * `SafetyStock` (Decimal)
  * `QualityHoldQty` (Decimal) - *Stock on hold; excluded from Available to Promise (ATP)*

### Table 5: `PurchaseOrdersTable`
Inbound shipments from suppliers.
* **Key Columns**:
  * `PurchaseOrderID` (String, Primary Key)
  * `SupplierID` (String, Foreign Key)
  * `SKU` (String, Foreign Key)
  * `OrderQty` (Decimal)
  * `ExpectedDeliveryDate` (Date)
  * `QualityHold` (Boolean) - *Yes/No (indicates if inbound stock is held)*

### Table 6: `CustomerOrdersTable`
Outbound sales orders and customer commitments.
* **Key Columns**:
  * `CustomerOrderID` (String, Primary Key)
  * `CustomerName` (String)
  * `SKU` (String, Foreign Key)
  * `OrderQty` (Decimal)
  * `RequiredDeliveryDate` (Date)
  * `CustomerTier` (String) - *Strategic, Priority, Standard*
  * `SLAProtected` (Boolean)
  * `PartialFulfillment` (Boolean) - *Yes/No (permission to split order)*
  * `OrderValue` (Decimal)

### Table 7: `AlternateSuppliersTable`
Approved alternate sourcing mappings.
* **Key Columns**:
  * `SKU` (String, Composite Key)
  * `AlternateSupplierID` (String, Composite Key)
  * `Approved` (Boolean) - *Yes/No (unapproved suppliers trigger manual workflows)*
  * `StandardLeadTime` (Integer) - *in days*
  * `ExpediteLeadTime` (Integer) - *in days*
  * `AlternateUnitCost` (Decimal)
  * `AvailableCapacity` (Decimal)

### Table 8: `RecoveryRulesTable`
Policy and precedence rules used by the Strategy Resolution topic.
* **Key Columns**:
  * `RuleID` (String, Primary Key)
  * `DisruptionType` (String)
  * `PriorityRank` (Integer)
  * `ApprovedStrategy` (String)

### Table 9: `StakeholdersTable`
Distribution lists for conditional notifications.
* **Key Columns**:
  * `Role` (String, Primary Key) - *e.g., Finance Business Partner, Supply Chain Director*
  * `EmailAddress` (String)
  * `Name` (String)

---

## 3. Seed Dataset Summary
The database includes the following records for validation testing:
* **6 Disruption Requests**: Covering delays, cancellations, and quality holds.
* **5 Suppliers**: Standard suppliers.
* **8 SKUs**: Component item master.
* **8 Inventory Records**: Inventory balances.
* **10 Purchase Orders**: Open inbound orders.
* **10 Customer Orders**: Strategic, priority, and standard demand.
* **8 Alternate-Supplier Mappings**: Alternate sourcing options.
* **12 Recovery Rules**: Resolution rules.
* **7 Stakeholders**: Roles and emails.
