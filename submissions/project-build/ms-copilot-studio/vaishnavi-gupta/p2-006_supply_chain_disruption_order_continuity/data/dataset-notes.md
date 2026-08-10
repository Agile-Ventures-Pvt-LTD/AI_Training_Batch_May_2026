# Dataset Notes

## Overview

The project uses a synthetic supply chain dataset provided for the P2-006 build. The dataset is designed to simulate common supply disruption scenarios and support testing of autonomous orchestration, specialist assessments, conflict resolution, approval routing, reporting, and exception handling workflows. 

---

# Dataset Summary

| Dataset Component | Records |
|------------------|---------|
| Disruption Requests | 6 |
| Suppliers | 5 |
| SKUs | 8 |
| Inventory Records | 8 |
| Purchase Orders | 10 |
| Customer Orders | 10 |
| Alternate Supplier Mappings | 8 |
| Recovery Rules | 12 |
| Stakeholders | 7 |


---

# Primary Data Tables

The solution uses the following Excel tables:

- DisruptionRequestsTable
- SuppliersTable
- SKUMasterTable
- InventoryTable
- PurchaseOrdersTable
- CustomerOrdersTable
- AlternateSuppliersTable
- RecoveryRulesTable
- StakeholdersTable

These tables are stored in OneDrive for Business or SharePoint and accessed through Excel Online (Business) connectors. 

---

# Covered Business Scenarios

The dataset includes sample cases for:

- Supplier delays
- Shipment delays
- Partial shipments
- Supplier cancellations
- Material shortages
- Quality holds
- Inventory shortages
- Strategic customer exposure
- Approved alternate suppliers
- Unapproved alternate suppliers
- Commercial approval requirements
- No viable recovery route


---

# Purpose of the Dataset

The dataset is used to:

- Validate disruption intake processing
- Test specialist agent assessments
- Demonstrate fan-out and fan-in orchestration
- Validate conflict resolution logic
- Test approval and escalation workflows
- Generate reports and notifications
- Verify end-to-end autonomous execution


---

# Assumptions

- All data is synthetic and provided for training purposes.
- No real customer, supplier, or financial information is used.
- Recommendations are generated solely from the supplied dataset and policy rules.
- The dataset is intentionally small to focus on orchestration patterns rather than data volume processing.

