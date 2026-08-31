# Tool Implementation

## 1. Excel Online (Business)

Excel is the primary operational data source/state store.

### Supervisor
The recurrence mechanism uses only the minimum required check to identify eligible `Processed = No` records.

### Complaint Pattern Specialist
Uses complaint records for counts, clusters, categories and repeated failure patterns.

### Returns Specialist
Uses return and sales information for return-rate and exposure analysis.

### Product/Batch Specialist
Uses product, batch and incident records to establish SKU/batch relationships and previous incidents.

### Customer Impact Specialist
Uses complaint/return information to assess affected customer exposure.

### Safety Specialist
Uses relevant complaint evidence and approved policy sources for safety indicators.

### CAPA Specialist
Uses owners, incident and CAPA registers to plan and record remediation.

### State Updates
State changes must occur only at the appropriate successful workflow stage. Source evidence must not be silently overwritten.

## 2. Word Online (Business)

Creates the Product Quality Investigation Report after Supervisor validation.

Expected report content includes:
- Incident/reference information.
- Complaint/cluster summary.
- Specialist findings.
- Safety findings.
- Final classification.
- Decision rationale.
- Evidence summary.
- CAPA details where applicable.
- Reassessment details where applicable.
- Final action/status.

If creation fails, record the failure and never claim that the report exists.

## 3. Office 365 Outlook

Sends the internal quality notification after final Supervisor validation.

The notification should communicate:
- Incident/reference.
- SKU/batch.
- Final classification.
- Key rationale.
- CAPA status when applicable.
- Required internal action.
- Report status.
- Any unresolved evidence or tool failure.

If sending fails, record the notification failure and preserve the quality decision.

## 4. Tool Governance
No tool success should be inferred from an attempted call. The workflow must use explicit success/failure outputs.

## 5. Testing
Formal tool-success and tool-failure scenarios remain reserved for the final testing phase.
