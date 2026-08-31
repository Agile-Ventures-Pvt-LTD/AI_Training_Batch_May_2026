# Custom Topics

## Topic 1 — Incident Intake & Validation
Validate ComplaintID, OrderID, SKU, BatchID when supplied, ComplaintDate, Category, Severity, SKU/Batch mapping and duplicate processing.

Outputs: ValidationStatus, IncidentID, ComplaintID, SKU, BatchID, ValidationReason.

Valid -> specialist analysis. Invalid/insufficient -> evidence/review path.

## Topic 2 — Quality Investigation Decision
Apply deterministic precedence:
1. SafetyIndicator = Yes -> Critical Escalation.
2. >=2 potential safety complaints for same SKU/batch -> High-Priority Quality Incident.
3. >=5 similar complaints for same SKU/batch within 7 days -> Investigation Required.
4. ReturnRate >=2% -> Investigation Required.
5. Previous incident + repeated failure -> High-Priority Quality Incident.
6. Missing required batch evidence -> Insufficient Evidence.
7. Overdue CAPA -> escalation.
8. Isolated low-severity complaint with no higher rule -> Informational.

Outputs: FinalClassification, DecisionPriority, DecisionRationale.

## Topic 3 — CAPA Planning & Ownership
Invoke for Investigation Required, High-Priority Quality Incident and Critical Escalation.

Create containment, corrective and preventive actions; resolve OwnerRole; set target date; define validation method; update CAPA_Register; return CAPA summary.

## Topic 4 — Evidence Update & Selective Reassessment
Inputs: IncidentID, SKU, BatchID, NewEvidenceType, NewEvidence, ReassessmentCount.

Check reassessment limit; identify stale domain; rerun only stale specialist; preserve unaffected findings; increment count; re-enter Topic 2.

## Screenshot Evidence
Use these relative GitHub paths. Replace filenames only if your actual PNG names differ.

- Supervisor: `screenshots/supervisor_agent/supervisor_agent.png`
- Child agents: `screenshots/child_agent/child_agents.png`
- Excel tool: `screenshots/excel_tool/excel_tool.png`
- Excel tool 1: `screenshots/excel_tool/excel_tool1.png`
- Knowledge Base: `screenshots/knowledge_base/knowledge_base.png`
- MCP Server: `screenshots/mcp_server/mcp_server.png`
- Topics: `screenshots/topics/topics.png`
- Word/Outlook: `screenshots/word_outlook_tool/word_outlook_tool.png`

Markdown image syntax:
`![Description](screenshots/<folder>/<file>.png)`

