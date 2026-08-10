# tool-implementation.md

# CAP-001 — Tool Implementation

## 1. Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses Microsoft 365 connectors and operational tools to provide controlled access to quality data, update workflow state, generate reports, and communicate validated outcomes.

Tools are assigned to agents according to their responsibilities. Tool access is intentionally separated so that each specialist receives only the operational data required for its domain.

---

## 2. Excel Online (Business) Tools

Excel Online (Business) is the primary operational data connector.

The workbook contains the operational tables required for complaint analysis, investigation, CAPA management, and workflow state updates.

### Complaint Pattern Specialist

#### Tool: Customer Complaints Data Reader

**Purpose:** Reads customer complaint records required to identify complaint patterns and clusters.

**Connector:** Excel Online (Business)

**Table:** Customer Complaints

---

### Returns Specialist

#### Tool: Returns Data Reader

**Purpose:** Reads return records required to calculate return counts and return-rate findings.

**Connector:** Excel Online (Business)

**Table:** Returns

#### Tool: Sales Data Reader

**Purpose:** Reads sales-summary records required to determine units sold for return-rate calculation.

**Connector:** Excel Online (Business)

**Table:** Sales_Summary

---

### Product-Batch Specialist

#### Tool: Product Master Data Reader

**Purpose:** Reads product information required to validate the affected SKU.

**Connector:** Excel Online (Business)

**Table:** Product_Master

#### Tool: Batch Register Data Reader

**Purpose:** Reads batch information required to validate and analyze the affected batch.

**Connector:** Excel Online (Business)

**Table:** Batch_Register

---

### Customer Impact Specialist

#### Tool: Customer Complaints Impact Reader

**Purpose:** Reads complaint information required to assess customer impact.

**Connector:** Excel Online (Business)

**Table:** Customer_Complaints

---

### Safety Specialist

#### Tool: Safety Complaint Reader

**Purpose:** Reads complaint safety indicators required to identify potential safety concerns.

**Connector:** Excel Online (Business)

**Table:** Customer_Complaints

---

### CAPA Specialist

#### Tool: CAPA Register Manager

**Purpose:** Reads and updates CAPA records for corrective and preventive action management.

**Connector:** Excel Online (Business)

**Table:** CAPA_Register

---

### Quality Supervisor

#### Tool: Quality Rules Reader

**Purpose:** Reads the configured quality rules and thresholds used for deterministic decision-making.

**Connector:** Excel Online (Business)

**Table:** Quality_Rules

#### Tool: Quality Incident Register Manager

**Purpose:** Reads and updates quality incident records and workflow status.

**Connector:** Excel Online (Business)

**Table:** Quality_Incidents

---

## 3. Word Online (Business) Tools

Word Online is used to generate the formal Product Quality Investigation Report after the Quality Supervisor has validated the final decision.

### Tool: Create Product Quality Investigation Report

**Purpose:** Creates the formal quality investigation report containing the incident findings, classification, CAPA information, evidence status, and final decision.

**Connector:** Word Online (Business)

**Agent:** Quality Supervisor / Reporting Workflow

---

## 4. Outlook Tools

Two Outlook tools are used to separate email preparation from email transmission.

### Tool: Draft Quality Notification Email

**Purpose:** Creates a draft internal quality notification based on the validated incident outcome.

**Connector:** Office 365 Outlook

**Agent:** Quality Supervisor / Reporting & Communication Workflow

### Tool: Send Draft Quality Notification Email

**Purpose:** Sends the previously prepared quality notification after Supervisor validation.

**Connector:** Office 365 Outlook

**Agent:** Quality Supervisor / Reporting & Communication Workflow

---

## 5. Tool Access Model

```text
Quality Supervisor
       │
       ├── Quality Rules Reader
       ├── Quality Incident Register Manager
       ├── Word Report Tool
       └── Outlook Draft / Send Tools
       │
       ├───────────────┬────────────────┬─────────────────┐
       ▼               ▼                ▼                 ▼
Complaint Pattern   Returns       Product-Batch     Customer Impact
       │               │                │                 │
       ▼               ▼                ▼                 ▼
Complaints       Returns + Sales   Product + Batch   Complaint Data
       │
       └──────────────────────────────────────────────────────┐
                                                              ▼
                                                        Safety Specialist
                                                              │
                                                              ▼
                                                        Safety Data

CAPA Specialist
       │
       ▼
CAPA Register
```

---

## 6. Tool Governance

The tool implementation follows these principles:

1. Each specialist receives only the tools required for its responsibility.
2. Excel is used as the operational source of record.
3. Read operations are separated from update operations where appropriate.
4. The Quality Supervisor controls final incident-state updates.
5. Word report generation occurs only after final Supervisor validation.
6. Outlook email sending occurs only after the notification has been prepared and authorized.
7. A failed tool operation must not be represented as successful.
8. Missing operational data must not be fabricated.
9. Tool results are treated as evidence for the appropriate specialist domain.
10. Final quality classification remains under Quality Supervisor control.

---

## 7. Connector Summary

| Connector | Primary Use |
|-----------|-------------|
| Excel Online (Business) | Operational quality data and state management |
| Word Online (Business) | Quality investigation report generation |
| Office 365 Outlook | Quality notification drafting and sending |
| Microsoft Learn MCP | Microsoft 365 guidance |

---

## 8. Operational Data Flow

```text
Excel Operational Data
        │
        ▼
Specialist Data Readers
        │
        ▼
Specialist Findings
        │
        ▼
Quality Supervisor
        │
        ├── Quality Incident Update
        │
        ├── CAPA Workflow
        │
        ├── Word Investigation Report
        │
        └── Outlook Notification
```

The tool layer provides the operational evidence and execution capabilities required by the multi-agent quality-governance workflow while keeping decision authority with the Quality Supervisor.