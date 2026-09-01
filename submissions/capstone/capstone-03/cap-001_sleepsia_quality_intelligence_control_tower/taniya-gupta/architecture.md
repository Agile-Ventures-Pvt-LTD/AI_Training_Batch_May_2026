# Architecture & Variable Flow Matrix

## 1. Architectural Topology & Agent Boundaries

```
Recurrence Trigger (Autonomous Scanner)
        │
        ▼
  Quality Supervisor (Parent Orchestrator Agent)
        │
        ├──► Topic 1: Incident Intake & Validation
        │    Input:  Topic.ComplaintID, Topic.OrderID, Topic.SKU, Topic.BatchID
        │    Output: Topic.ValidationResult ("Valid" | "Invalid" | "Insufficient Evidence")
        │
        ├──► Parallel Fan-Out (Specialist Child Agents)
        │    ├── Complaint Pattern Specialist ──► Output: ComplaintFindings
        │    ├── Returns Specialist ───────────► Output: ReturnFindings (ReturnRatePercent)
        │    ├── Product/Batch Specialist ──────► Output: ProductFindings (PreviousIncidents)
        │    ├── Customer Impact Specialist ───► Output: CustomerFindings
        │    └── Safety Specialist ─────────────► Output: SafetyFindings (ConfirmedSafety)
        │
        ├──► Fan-In (Quality Supervisor Consolidates Specialist Outputs)
        │
        ├──► Topic 2: Quality Investigation Decision (8 Priority Rules)
        │    Input:  Consolidated Specialist Findings
        │    Output: Topic.IncidentClassification, Topic.ClassificationRationale
        │
        ├──► CAPA Specialist ──► Topic 3: CAPA Planning & Ownership
        │    Input:  IncidentID, IncidentClassification, SKU, DominantFailureMode
        │    Output: CAPASummary, OwnerRole, Containment, Corrective, Preventive, TargetDate
        │
        ├──► Supervisor Validation & Persistent Tool Execution
        │    ├── Word Online (Business) ──► Product Quality Investigation Report (.docx)
        │    ├── Office 365 Outlook ──► HTML Alert Notification Email
        │    └── Excel Online (Business) ──► Quality_Incidents & CAPA_Register Updates
        │
        └──► Topic 4: Evidence Update & Selective Reassessment
             Input:  IncidentID, ReassessmentCount, NewEvidence
             Output: Rerun Stale Specialists ──► Re-enter Topic 2

M365 Guidance Specialist ──► Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)
```

---

## 2. Agent Responsibility

| Agent Name | Scope & Authority | Primary Tool / Input |
|---|---|---|
| **Quality Supervisor** | SOLE decision owner. Orchestrates fan-out/fan-in, rule precedence, CAPA approval, Word/Outlook/Excel tools. | Excel, Word, Outlook, Custom Topics |
| **Complaint Pattern Specialist** | Analyzes complaint frequency, categories, failure modes, customer impact dates. | `Customer_Complaints` sheet |
| **Returns Specialist** | Calculates return counts, return rates against sales units, refund exposure, 2% threshold. | `Returns`, `Sales_Summary` sheets |
| **Product/Batch Specialist** | Validates SKU/batch relationship, manufacture date, supplier lot, quality holds, incident history. | `Product_Master`, `Batch_Register` |
| **Customer Impact Specialist** | Counts unique affected customers, unresolved cases, fulfilment vs product quality errors. | `Customer_Complaints`, `Returns` | Cannot assign severity. |
| **Safety Specialist** | Checks SafetyIndicator (heat, burning smell, smoke). Triggers Critical Escalation. | `Customer_Complaints` (SafetyIndicator) | Cannot give medical advice or public recall statements. |
| **CAPA Specialist** | Generates containment, corrective, preventive actions, assigns owner role & target dates. | `Owners` sheet, Specialist findings | Cannot claim root cause is confirmed without evidence. |
| **M365 Guidance Specialist** | Operational & technical guidance for Teams/M365 deployment via MCP server. | Microsoft Learn MCP Server | Has ZERO influence on quality severity decisions. |
