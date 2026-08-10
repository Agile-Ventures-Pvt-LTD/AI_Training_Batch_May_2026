# Dataset Notes

## Project

**NovaSphere Supply Chain Continuity Management System using Microsoft Copilot Studio**

---

# Overview

The solution uses the provided synthetic supply chain dataset to simulate disruption management scenarios.

The dataset supports testing of inventory impact, supplier availability, customer risk, commercial analysis, and recovery planning.

---

# Data Source

Workbook:

`P2-006_Supply_Chain_Continuity_Lab_Data.xlsx`

Platform:

**Excel Online (Business)**

---

# Tables Used

| Table                   | Purpose                         |
| ----------------------- | ------------------------------- |
| DisruptionRequestsTable | Supply disruption records       |
| SuppliersTable          | Supplier information            |
| SKUMasterTable          | Product master data             |
| InventoryTable          | Stock availability              |
| PurchaseOrdersTable     | Open purchase orders            |
| CustomerOrdersTable     | Customer demand and commitments |
| AlternateSuppliersTable | Alternate supplier options      |
| RecoveryRulesTable      | Decision and approval rules     |
| StakeholdersTable       | Notification recipients         |

---

# Dataset Size

The dataset contains:

* 6 disruption requests
* 5 suppliers
* 8 SKUs
* 8 inventory records
* 10 purchase orders
* 10 customer orders
* 8 alternate supplier mappings
* 12 recovery rules
* 7 stakeholders

---

# Supported Scenarios

The dataset includes examples for:

* Supplier delays
* Shipment delays
* Quality holds
* Supplier cancellations
* Partial shipments
* Material shortages
* Strategic customer impact
* Inventory shortages
* Approved alternate suppliers
* Unapproved alternate suppliers
* Cost approval requirements
* No viable recovery options

---

# Data Usage Rules

The solution uses the dataset only for:

* Disruption validation.
* Specialist assessments.
* Recovery planning.
* Decision rule evaluation.
* Testing and demonstration.

The system must not:

* Modify source data incorrectly.
* Create unsupported values.
* Assume missing approvals.
* Fabricate business information.

---

# Data Limitations

* Dataset is synthetic and small-scale.
* No live ERP integration is included.
* Results depend on data accuracy.
* Enterprise deployment would require larger data sources and governance controls.

---

# Purpose

The dataset provides a controlled environment to demonstrate autonomous multi-agent supply disruption response using Microsoft Copilot Studio.
