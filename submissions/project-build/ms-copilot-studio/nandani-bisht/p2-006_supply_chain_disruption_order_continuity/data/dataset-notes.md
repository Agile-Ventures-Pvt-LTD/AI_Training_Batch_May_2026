# dataset-notes.md

# Dataset Notes

## P2-006 – Supply Chain Disruption Order Continuity

---

# Overview

The **Supply Chain Disruption Order Continuity** solution uses a synthetic dataset designed for training, demonstration, and evaluation purposes.

The datasets simulate enterprise supply chain operations and provide sufficient information for the Supervisor Agent and specialist child agents to perform disruption assessment, recovery planning, approval routing, reporting, and stakeholder notification.

All data contained within this project is fictional and must not be interpreted as real business information. :contentReference[oaicite:2]{index=2}

---

# Dataset Package

The project contains the following datasets.

| File | Purpose |
|------|---------|
| P2-006_Supply_Chain_Continuity_Lab_Data.xlsx | Primary operational workbook |
| Disruption_Requests.csv | Lightweight trigger dataset |
| NovaSphere_Supply_Continuity_Policy.docx | Business policies and decision rules |
| P2-006_Dataset_Manifest.md | Dataset documentation |

The policy document provides the authoritative business rules used by the Supervisor Agent and specialist agents, while the workbook contains the operational data required for workflow execution. :contentReference[oaicite:3]{index=3}

---

# Primary Workbook

The solution primarily uses the Excel workbook:

```text
P2-006_Supply_Chain_Continuity_Lab_Data.xlsx
```

This workbook serves as the operational data source for the Microsoft Copilot Studio solution.

---

# Workbook Structure

The workbook contains the following worksheets.

| Worksheet | Purpose |
|------------|---------|
| README | Workbook documentation |
| Disruption_Requests | Incoming disruption requests |
| Suppliers | Supplier master data |
| SKU_Master | Product master data |
| Inventory | Inventory availability |
| Purchase_Orders | Purchase order information |
| Customer_Orders | Customer demand |
| Alternate_Suppliers | Approved alternate suppliers |
| Recovery_Rules | Recovery strategy rules |
| Stakeholders | Notification recipients |
| Test_Scenarios | Sample evaluation scenarios |

These worksheets provide the information required by the Supervisor Agent and specialist agents during workflow execution. :contentReference[oaicite:4]{index=4}

---

# Dataset Relationships

```text
Disruption Requests
          │
          ▼
Purchase Orders
          │
          ▼
SKU Master
          │
          ▼
Inventory
          │
          ▼
Alternate Suppliers
          │
          ▼
Customer Orders
          │
          ▼
Recovery Rules
          │
          ▼
Stakeholders
```

---

# Data Used by Each Specialist

## Inventory Impact Specialist

Reads:

- Inventory
- SKU_Master
- Purchase_Orders

Purpose

- Determine Available-to-Promise (ATP)
- Identify shortages
- Assess inventory availability

---

## Alternate Supplier Specialist

Reads:

- Alternate_Suppliers
- Suppliers
- Recovery_Rules

Purpose

- Identify approved suppliers
- Compare lead times
- Evaluate supplier capacity

---

## Customer & Order Impact Specialist

Reads:

- Customer_Orders
- Inventory
- Purchase_Orders

Purpose

- Identify affected customers
- Prioritize strategic customers
- Evaluate SLA commitments

---

## Commercial Impact Specialist

Reads:

- Recovery_Rules
- Alternate_Suppliers
- Purchase_Orders

Purpose

- Calculate commercial impact
- Determine approval requirements

---

## Recovery Planning Specialist

Consumes outputs from all specialist agents.

Produces

- Recovery Strategy
- Residual Risk
- Required Approvals

---

## Reporting & Communication Specialist

Uses

- Final Recovery Strategy
- Stakeholders

Produces

- Word Report
- Outlook Notification

---

# Primary Trigger Dataset

The solution begins processing using the:

```text
Disruption_Requests
```

table.

Each disruption request represents an individual supply chain event requiring autonomous assessment.

Typical fields include:

- Disruption ID
- Supplier ID
- SKU
- Purchase Order
- Status
- Recovery Date

---

# Business Policy Dataset

The **NovaSphere Supply Continuity Policy** defines the business rules governing the solution.

Examples include:

- Customer priority rules
- Inventory allocation rules
- Alternate supplier selection
- Commercial approval thresholds
- Recovery strategies
- Risk classifications
- Reporting requirements

These rules are referenced by the Supervisor Agent during workflow execution. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

---

# Synthetic Data Notice

All project datasets are synthetic.

They are intended exclusively for:

- Training
- Demonstration
- Evaluation
- Proof-of-concept implementations

No real suppliers, customers, purchase orders, financial values, or email addresses are included. :contentReference[oaicite:7]{index=7}

---

# Data Flow

```text
Excel Workbook
        │
        ▼
Disruption Request
        │
        ▼
Supervisor Agent
        │
        ▼
Specialist Agents
        │
        ▼
Recovery Strategy
        │
        ▼
Word Report
        │
        ▼
Excel Update
        │
        ▼
Outlook Notification
```

---

# Data Governance

The solution follows these principles:

- Read-only access during assessment
- Controlled updates after approval
- Synthetic data only
- Policy-driven decision making
- Full workflow traceability

---

# Assumptions

The project assumes that:

- All workbook sheets are populated.
- Data relationships are valid.
- Supplier and SKU identifiers are consistent.
- Recovery rules reflect current business policies.
- Stakeholder contact information is available for notifications.

---

# Limitations

Current dataset limitations include:

- Static workbook data
- Synthetic business scenarios
- No live ERP integration
- No real-time inventory updates
- No external supplier APIs

These limitations are acceptable for demonstration and evaluation purposes.

---

# Summary

The dataset package provides a realistic but synthetic representation of a supply chain environment. Combined with the NovaSphere policy document, it enables the Supervisor Agent and specialist agents to demonstrate autonomous disruption assessment, recovery planning, approval management, reporting, and stakeholder communication in a controlled evaluation environment.

---

# Version

**Version:** 1.0

**Status:** Completed