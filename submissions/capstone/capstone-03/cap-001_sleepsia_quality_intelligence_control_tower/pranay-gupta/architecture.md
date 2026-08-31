# Architecture

## 1. Architectural Model
The solution follows a hierarchical multi-agent pattern with the **Quality Supervisor** as the parent orchestrator and specialist child agents performing focused analysis.

The Supervisor is the sole owner of the final internal quality classification and final workflow state.

## 2. Supervisor
The Quality Supervisor:
- Receives the autonomous trigger.
- Performs or coordinates intake validation.
- Selects the appropriate specialist agents.
- Coordinates parallel analysis.
- Waits for required findings.
- Handles specialist retry/fallback.
- Applies policy precedence.
- Controls reassessment.
- Coordinates CAPA.
- Authorizes final reporting and notification.
- Preserves uncertainty and missing evidence.

## 3. Child Agents

| Agent | Primary Responsibility | Main Evidence |
|---|---|---|
| Complaint Pattern Specialist | Complaint counts, clusters, repeated categories and failure modes | Customer_Complaints |
| Returns Specialist | Return count, rate, reasons and exposure | Returns, Sales_Summary |
| Product/Batch Specialist | SKU, batch, supplier lot and prior incident relationships | Product_Master, Batch_Register, Quality_Incidents |
| Customer Impact Specialist | Customer exposure and unresolved impact | Customer_Complaints, Returns |
| Safety Specialist | Safety indicators and safety escalation | Customer_Complaints, policy sources |
| CAPA Specialist | Containment, corrective/preventive action, owner and validation | Owners, Quality_Incidents, CAPA_Register |
| M365 Guidance Specialist | Microsoft operational guidance | Microsoft Learn MCP |

## 4. Data and Tool Boundaries
Excel access is scoped to the specialist that needs the relevant data. The Supervisor's recurrence check remains minimal and is used to identify `Processed = No` records.

Word and Outlook are controlled finalization tools and are not specialist-analysis tools.

## 5. High-Level Flow
```text
Recurrence Trigger
      ↓
Processed = No
      ↓
Incident Intake & Validation
      ↓
Parallel Specialist Analysis
      ↓
Supervisor Fan-In
      ↓
Quality Investigation Decision
      ↓
CAPA Planning, if required
      ↓
Supervisor Validation
      ↓
Word Report
      ↓
Excel Final State
      ↓
Outlook Notification
```

## 6. M365 Guidance Boundary
Microsoft Learn MCP is attached only to the M365 Guidance Specialist. Its output is operational guidance and cannot override internal Sleepsia quality rules.

## 7. Failure Philosophy
The architecture favors explicit failure states over fabricated success. Failed specialist/tool operations are recorded, retried only where permitted, and escalated to manual review or insufficient evidence when required.
