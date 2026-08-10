# Architecture

## Agent roster

| Agent | Type | Owns | Tools (scoped) |
|---|---|---|---|
| Quality Supervisor | Main agent | Orchestration lifecycle, final classification, report/notification authorisation | Excel Online (Business), Word Online (Business), Office 365 Outlook |
| Safety Specialist | Child agent | Safety-indicator detection | Excel (Customer_Complaints, read-only) |
| Complaint Pattern Specialist | Child agent | Complaint counting/clustering | Excel (Customer_Complaints, read-only) |
| Returns Specialist | Child agent | Return rate calculation | Excel (Returns, Sales_Summary, read-only) |
| Product/Batch Specialist | Child agent | SKU/batch confirmation, incident history, overdue CAPA check | Excel (Product_Master, Batch_Register, Quality_Incidents, CAPA_Register, read-only) |
| Customer Impact Specialist | Child agent | Customer/order impact, fulfilment vs. quality distinction | Excel (Customer_Complaints, Returns, read-only) |
| CAPA Specialist | Child agent | CAPA creation and ownership assignment | Excel (Owners, Quality_Incidents read-only; CAPA_Register read/write) |
| M365 Guidance Specialist | Child agent | Operational Microsoft 365/Teams/Copilot Studio guidance | Microsoft Learn MCP server |

## Hierarchy

The Quality Supervisor is the sole parent orchestrator. All six domain specialists and the M365 Guidance Specialist are child agents invoked by the Supervisor. No specialist independently assigns a final quality classification, escalation decision, or authorises reporting/notification — these remain exclusively with the Supervisor, per the PRD's responsibility-boundary requirement (Section 3).

## Tool boundary rationale

Each specialist is scoped to only the Excel tables its domain requires (PRD Section 25 equivalent / Section 19), reducing tool ambiguity and reinforcing the "no overlapping ownership" rule in PRD Section 3. Word, Excel (write), and Outlook are held only by the Supervisor, since only the Supervisor is authorised to generate reports, update incident state, and send notifications.

## High-level flow

```
Recurrence Trigger
  -> Quality Supervisor
      -> Incident Intake & Validation (Topic 1)
          -> [existing open incident found?]
              NO  -> fan-out: Safety, Complaint Pattern, Returns,
                     Product/Batch, Customer Impact Specialists
                     -> Supervisor fan-in
                     -> Quality Investigation Decision (Topic 2)
              YES -> Evidence Update & Selective Reassessment (Topic 4)
                     -> re-enters Topic 2
      -> CAPA Planning & Ownership (Topic 3), if classification warrants it
      -> Supervisor: Word report -> Excel update -> Outlook notification
```

Interactive employee queries (Teams / Microsoft 365 Copilot) are handled by the same Supervisor using knowledge sources and read-only lookups, without re-entering the autonomous pipeline (see orchestration-patterns.md, Section: Interactive Mode Boundary).