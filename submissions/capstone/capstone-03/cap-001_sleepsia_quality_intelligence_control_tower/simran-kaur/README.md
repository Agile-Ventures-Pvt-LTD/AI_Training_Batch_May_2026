# CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower

# Agent Name : Sleepsia Quality Supervisor

## Project
- **Project ID:** CAP-001
- **Platform:** Microsoft Copilot Studio
- **Participant:** Simran Kaur
- **Purpose:** Autonomous product-quality complaint validation, specialist investigation, quality decision, CAPA, reporting, notification, and reassessment.

## Architecture
The system uses a central **Sleepsia Quality Supervisor** with specialist child agents.

### Agents
1. Complaint Pattern Specialist — complaint counts, categories, clusters, repeated patterns.
2. Returns Specialist — returns, sales, and return-rate calculation.
3. Product/Batch Specialist — SKU, BatchID, product/batch validation and historical quality information.
4. Customer Impact Specialist — affected customers, repeat customers, unresolved cases, customer impact.
5. Safety Specialist — explicit safety indicators.
6. CAPA Specialist — containment, corrective and preventive actions.
7. M365 Guidance Specialist — Microsoft operational guidance through **Microsoft Learn MCP**; does not influence quality decisions.

## Intake Validation
`Incident Intake & Validation` is a deterministic gate. It validates:
- ComplaintID
- OrderID
- SKU
- SKU against Product_Master
- supplied BatchID against SKU
- ComplaintDate
- Category
- Severity
- duplicate processing status

Outputs are exactly:
- `Valid`
- `Invalid`
- `Insufficient Evidence`

Only `Valid` records may start specialist analysis.

## Decision Rules
Priority:
1. Confirmed credible safety evidence → **Critical Escalation**
2. Previous incident + repeated failure → **High-Priority Quality Incident**
3. Return Rate = `(Return Count / Sales Volume) × 100`; return rate >= 2% → **Investigation Required**
4. At least 5 complaints for the same SKU within 7 days → **Investigation Required**
5. Otherwise → **Monitoring or Informational**

## Supervisor Tools
- `Get Quality Incident`
- `Check Existing Incidents`
- `Update Quality Incident`
- `Check Existing CAPA Records`
- `Generate Quality Incident Report`
- `Send Quality Notification`

## Publishing
- **Agent URL:** `https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/a574e6ed-7d94-f111-b8dc-000d3af21e08/overview`
- **Channel:** Was not able to use channel due to publishig issue
- **Publishing status:** Showing billing issue while publishing

## Completion
- Supervisor: Complete
- Specialist agents: Complete
- Supervisor tools: Completed
- Mandatory topics: Completed
- MCP/knowledge validation: Completed
- Publishing: Pending
