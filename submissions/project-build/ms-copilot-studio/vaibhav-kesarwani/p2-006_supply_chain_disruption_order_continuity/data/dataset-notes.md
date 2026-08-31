# Dataset notes

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

This document describes the Excel dataset used by the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The dataset provides the operational data required for disruption detection, inventory assessment, supplier evaluation, customer impact analysis, commercial assessment, and reporting.

The Excel workbook acts as the primary data source for all Copilot Studio child agents.

## Dataset overview

| Dataset        | Value                                        |
| -------------- | -------------------------------------------- |
| File name      | P2-006_Supply_Chain_Continuity_Lab_Data.xlsx |
| Storage        | OneDrive for Business                        |
| Data source    | Excel Online (Business)                      |
| Primary access | Microsoft Copilot Studio                     |
| Integration    | Power Automate                               |

## Workbook structure

| Table               | Purpose                                  |
| ------------------- | ---------------------------------------- |
| Disruption_Requests | Disruption trigger and workflow tracking |
| Suppliers           | Supplier master data                     |
| SKU_Master          | Product master data                      |
| Inventory           | Current inventory position               |
| Purchase_Orders     | Inbound supply commitments               |
| Customer_Orders     | Customer demand and commitments          |
| Alternate_Suppliers | Approved alternate sourcing options      |
| Recovery_Rules      | Policy thresholds and business rules     |
| Stakeholders        | Notification and approval routing        |

## Table summary

### Disruption_Requests

Primary trigger table.

| Key fields           |
| -------------------- |
| DisruptionID         |
| SupplierID           |
| SKU                  |
| AffectedPO           |
| AffectedQty          |
| ReportedSeverity     |
| ExpectedRecoveryDate |
| Status               |

Used by:

* Autonomous Trigger
* Validation Specialist
* Supervisor Agent

### Suppliers

Supplier master data.

| Key fields     |
| -------------- |
| SupplierID     |
| SupplierName   |
| Region         |
| SupplierStatus |

Used by:

* Validation Specialist
* Alternate Supplier Specialist

### SKU_Master

Product master data.

| Key fields        |
| ----------------- |
| SKU               |
| SKUDescription    |
| Category          |
| StandardLeadTime  |
| PrimarySupplierID |

Used by:

* Validation Specialist
* Scope Specialist
* Inventory Specialist
* Supplier Specialist

### Inventory

Current inventory position.

| Key fields     |
| -------------- |
| SKU            |
| OnHandQty      |
| ReservedQty    |
| SafetyStock    |
| QualityHoldQty |

Used by:

* Inventory Impact Specialist

### Purchase_Orders

Inbound supply commitments.

| Key fields          |
| ------------------- |
| POID                |
| SupplierID          |
| SKU                 |
| ExpectedReceiptDate |
| Quantity            |

Used by:

* Validation Specialist
* Inventory Impact Specialist
* Scope Specialist

### Customer_Orders

Customer demand and commitments.

| Key fields   |
| ------------ |
| OrderID      |
| Customer     |
| CustomerTier |
| SLAProtected |
| Priority     |
| RequiredDate |
| Quantity     |
| Revenue      |

Used by:

* Scope Specialist
* Customer & Order Impact Specialist

### Alternate_Suppliers

Alternate sourcing options.

| Key fields          |
| ------------------- |
| SKU                 |
| AlternateSupplierID |
| ApprovedStatus      |
| AvailableCapacity   |
| LeadTime            |
| UnitCost            |

Used by:

* Alternate Supplier Specialist

### Recovery_Rules

Business rules and approval thresholds.

| Key fields               |
| ------------------------ |
| CostPremiumThreshold     |
| ExpeditePremiumThreshold |
| ReassessmentLimit        |

Used by:

* Commercial Impact Specialist

### Stakeholders

Notification and approval routing.

| Key fields      |
| --------------- |
| Role            |
| Email           |
| EscalationLevel |

Used by:

* Reporting & Communication Specialist
* Power Automate notification flow

## Data relationships

| Relationship                          | Description                           |
| ------------------------------------- | ------------------------------------- |
| Suppliers → Purchase_Orders           | Supplier ownership of purchase orders |
| Suppliers → SKU_Master                | Primary supplier relationship         |
| SKU_Master → Inventory                | Inventory by SKU                      |
| SKU_Master → Customer_Orders          | Customer demand by SKU                |
| SKU_Master → Alternate_Suppliers      | Alternate sourcing by SKU             |
| Disruption_Requests → Purchase_Orders | Affected purchase-order relationship  |

## Data usage by specialist agents

| Specialist              | Tables used                                                 |
| ----------------------- | ----------------------------------------------------------- |
| Validation              | Disruption_Requests, Suppliers, SKU_Master, Purchase_Orders |
| Scope                   | SKU_Master, Inventory, Purchase_Orders, Customer_Orders     |
| Inventory               | Inventory, SKU_Master, Purchase_Orders                      |
| Supplier                | Alternate_Suppliers, Suppliers, SKU_Master                  |
| Customer                | Customer_Orders, SKU_Master                                 |
| Commercial              | Recovery_Rules                                              |
| Recovery Planning       | Supervisor context only                                     |
| Strategy Resolution     | Supervisor context only                                     |
| Approval & Reassessment | Supervisor context only                                     |
| Reporting               | Supervisor context only                                     |

## Data assumptions

The dataset assumes:

* one primary supplier per SKU,
* approved alternate suppliers are pre-qualified,
* inventory values represent current operational inventory,
* customer priorities are maintained in Customer_Orders,
* approval thresholds are stored in Recovery_Rules,
* stakeholder email addresses are maintained in Stakeholders.

## Data quality requirements

Mandatory fields:

* SupplierID
* SKU
* AffectedPO
* AffectedQty
* ReportedSeverity
* ExpectedRecoveryDate

Validation checks:

* supplier existence,
* SKU existence,
* purchase-order existence,
* supplier and PO relationship,
* duplicate disruption status.

## Operational limitations

| Limitation                       | Impact                                            |
| -------------------------------- | ------------------------------------------------- |
| Excel-based storage              | Limited concurrent write scalability              |
| Static supplier capacity         | Capacity changes require reassessment             |
| Manual master-data maintenance   | Data freshness depends on updates                 |
| No real-time ERP synchronization | Inventory and PO data may lag operational systems |

## Future enhancements

Recommended migration path:

* Excel → Dataverse
* SharePoint document integration
* SAP inventory integration
* Dynamics 365 customer integration
* Automated supplier-capacity synchronization
* Real-time disruption event ingestion

## Dataset governance

The dataset should be treated as the authoritative operational source for:

* disruption identification,
* inventory assessment,
* supplier evaluation,
* customer exposure analysis,
* approval determination,
* reporting generation.

Any changes to table structure, column names, or business-rule values should be reflected in the corresponding Copilot Studio child-agent configurations and Power Automate flows.

## Summary

The Excel dataset provides a structured operational foundation for the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The workbook supports autonomous disruption detection, parallel specialist assessment, deterministic recovery planning, approval governance, and executive reporting while maintaining clear data ownership and traceable operational relationships.
