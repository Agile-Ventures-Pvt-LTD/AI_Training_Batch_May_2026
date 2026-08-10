# Knowledge sources

## Sleepsia product quality & customer experience intelligence control tower

This document defines the knowledge architecture used by the Sleepsia Product Quality & Customer Experience Intelligence Control Tower.

The system uses a combination of **structured operational data**, **quality policy documents**, and **Microsoft Learn MCP** to support autonomous quality investigations, deterministic decision making, and enterprise operational guidance.

The Quality Supervisor and all child agents operate using **retrieval-based evidence** rather than inferred or fabricated information.

---

# Knowledge architecture

The system uses three categories of knowledge.

| Source type                      | Purpose                       |
| -------------------------------- | ----------------------------- |
| Structured operational data      | Quality investigations        |
| Policy and operational documents | Business rules and procedures |
| Microsoft Learn MCP              | Microsoft platform guidance   |

---

# Structured operational data

## Primary operational workbook

**File**

Sleepsia_CAP001_Quality_Capstone_Data.xlsx

This workbook contains all operational data required for autonomous investigations.

---

# Table inventory

## tblCustomerComplaints

### Purpose

Primary complaint intake and investigation source.

### Used by

* Incident Intake & Validation Specialist
* Complaint Pattern Specialist
* Customer Impact Specialist
* Safety Specialist
* Quality Supervisor

### Key fields

* ComplaintID
* OrderID
* CustomerID
* SKU
* BatchID
* ComplaintDate
* Category
* Severity
* SafetyIndicator
* Status
* Processed

### Access

Read/write

The Quality Supervisor updates:

* Processed
* Status
* Incident linkage

---

## tblProductMaster

### Purpose

Product validation and product metadata.

### Used by

* Incident Intake & Validation Specialist
* Product/Batch Specialist

### Key fields

* SKU
* ProductName
* Category
* ProductStatus

### Access

Read-only

---

## tblBatchRegister

### Purpose

Manufacturing batch validation.

### Used by

* Incident Intake & Validation Specialist
* Product/Batch Specialist

### Key fields

* BatchID
* SKU
* ManufactureDate
* SupplierLot
* QualityHoldStatus

### Access

Read-only

---

## tblSalesSummary

### Purpose

Return-rate calculations.

### Used by

* Returns Specialist

### Key fields

* SKU
* UnitsSold
* SalesPeriod

### Access

Read-only

---

## tblReturns

### Purpose

Return analysis and customer impact.

### Used by

* Returns Specialist
* Customer Impact Specialist

### Key fields

* ReturnID
* SKU
* BatchID
* ReturnReason
* RefundAmount
* ReturnDate

### Access

Read-only

---

## tblQualityIncidents

### Purpose

Incident history and operational incident management.

### Used by

* Product/Batch Specialist
* Quality Supervisor

### Key fields

* IncidentID
* ComplaintID
* SKU
* BatchID
* Classification
* Status
* CreatedDate
* DecisionRationale
* AppliedRule
* ReassessmentCount

### Access

Read/write

Created and updated by the Quality Supervisor.

---

## tblCAPARegister

### Purpose

Corrective and preventive action management.

### Used by

* CAPA Planning & Ownership Specialist
* Evidence Update & Selective Reassessment Specialist
* Quality Supervisor

### Key fields

* CAPAID
* IncidentID
* Owner
* ActionType
* TargetDate
* Status
* ValidationMethod

### Access

Read/write

Updated only after supervisor authorization.

---

## tblOwners

### Purpose

Owner resolution and notification routing.

### Used by

* CAPA Planning & Ownership Specialist
* Quality Supervisor

### Key fields

* Role
* OwnerName
* Email
* Department

### Access

Read-only

---

## tblQualityRules

### Purpose

Deterministic quality policy reference.

### Used by

* Quality Investigation Decision Specialist
* Quality Supervisor

### Key fields

* RuleName
* Threshold
* Classification
* Priority

### Access

Read-only

---

## tblTestScenarios

### Purpose

System validation and testing.

### Used by

* testing activities,
* demonstration scenarios,
* validation verification.

### Access

Read-only

---

# Knowledge ownership

## Operational ownership

| Table               | Owner               |
| ------------------- | ------------------- |
| Customer Complaints | Customer Experience |
| Product Master      | Product Management  |
| Batch Register      | Manufacturing       |
| Sales Summary       | Finance / Sales     |
| Returns             | Operations          |
| Quality Incidents   | Quality             |
| CAPA Register       | Quality             |
| Owners              | HR / Operations     |
| Quality Rules       | Quality Governance  |

---

# Child-agent knowledge mapping

## Incident Intake & Validation Specialist

### Reads

* tblCustomerComplaints
* tblProductMaster
* tblBatchRegister

### Produces

Validation evidence.

---

## Complaint Pattern Specialist

### Reads

* tblCustomerComplaints

### Produces

Complaint cluster evidence.

---

## Returns Specialist

### Reads

* tblReturns
* tblSalesSummary

### Produces

Return-rate evidence.

---

## Product/Batch Specialist

### Reads

* tblProductMaster
* tblBatchRegister
* tblQualityIncidents

### Produces

Manufacturing evidence.

---

## Customer Impact Specialist

### Reads

* tblCustomerComplaints
* tblReturns

### Produces

Customer exposure evidence.

---

## Safety Specialist

### Reads

* tblCustomerComplaints

### Produces

Safety evidence.

---

## Quality Investigation Decision Specialist

### Reads

Structured outputs from all specialists.

### Produces

Classification recommendation.

---

## CAPA Planning & Ownership Specialist

### Reads

* tblOwners
* tblCAPARegister

### Writes

CAPA recommendations.

---

## Evidence Update & Selective Reassessment Specialist

### Reads

* specialist findings,
* operational tables,
* CAPA status.

### Produces

Reassessment plans.

---

# Policy document knowledge

The system also uses business policy documents stored in **OneDrive for Business**.

## Sleepsia Product Quality Policy

### Purpose

Quality thresholds and investigation policies.

### Used by

* Quality Supervisor
* Quality Investigation Decision Specialist

---

## Sleepsia Product Care and Usage Guide

### Purpose

Product usage guidance and expected behavior.

### Used by

* interactive employee assistance,
* product clarification,
* customer issue interpretation.

---

## Sleepsia Customer Resolution Policy

### Purpose

Internal customer handling guidance.

### Used by

* Customer Impact Specialist
* Quality Supervisor

This document does not determine quality severity.

---

# Microsoft Learn MCP

## Purpose

Microsoft operational guidance.

## Used by

**M365 Guidance Specialist**

## Server

https://learn.microsoft.com/api/mcp

## Knowledge domains

* Copilot Studio
* Microsoft 365 Copilot
* Teams
* connectors
* authentication
* deployment
* governance
* best practices

## Isolation rule

MCP knowledge must never influence:

* quality severity,
* safety classification,
* CAPA decisions,
* incident classification.

---

# Retrieval strategy

## Validation retrieval

Exact record lookup.

## Complaint retrieval

SKU and BatchID filtering.

## Return retrieval

SKU aggregation.

## Batch retrieval

BatchID mapping.

## Incident retrieval

Historical matching.

## CAPA retrieval

Incident linkage.

---

# Evidence hierarchy

The system prioritizes evidence in this order.

## Level 1

Safety evidence

## Level 2

Complaint evidence

## Level 3

Return evidence

## Level 4

Manufacturing evidence

## Level 5

Customer impact evidence

## Level 6

Historical CAPA evidence

Higher-priority evidence overrides lower-priority evidence during decision evaluation.

---

# Data freshness

## Complaint data

Near real-time

## Return data

Operational

## Batch data

Master data

## Incident data

Persistent operational state

## CAPA data

Persistent operational state

## Microsoft MCP

Live documentation retrieval

---

# Update policy

## Read-only sources

* tblProductMaster
* tblBatchRegister
* tblSalesSummary
* tblReturns
* tblOwners
* tblQualityRules
* policy documents
* Microsoft Learn MCP

## Write-enabled sources

* tblCustomerComplaints
* tblQualityIncidents
* tblCAPARegister

Only the **Quality Supervisor** performs operational writes.

Child agents return structured findings only.

---

# Knowledge integrity rules

All agents must follow these rules.

* Never invent evidence.
* Never fabricate records.
* Never assume missing values.
* Never claim a tool operation succeeded unless confirmed.
* Distinguish retrieved evidence from analytical inference.
* Preserve source attribution for all findings.
* Preserve confidence levels.

If required data is unavailable, return **Insufficient Evidence**.
