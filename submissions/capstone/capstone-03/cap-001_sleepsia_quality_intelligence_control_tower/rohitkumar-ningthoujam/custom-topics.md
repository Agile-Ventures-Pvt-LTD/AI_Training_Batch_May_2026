# Custom Topics

## Topic 1 — Incident Intake & Validation

Validates the complaint/incident before specialist analysis.

Key checks:
- Complaint/Incident ID exists.
- Required fields are present.
- SKU exists in Product Master.
- Batch exists when supplied.
- Complaint date is valid.
- Severity is valid.
- Record is not already processed.

Outputs:
- ValidationStatus
- IncidentStatus
- Validated complaint/incident information

Invalid records do not proceed to specialist analysis.

## Topic 2 — Quality Investigation Decision

Consolidates specialist findings and determines the quality outcome.

Inputs:
- Incident ID
- Complaint pattern findings
- Safety findings
- Product/batch findings
- Customer impact
- Return findings

Decision considers:
- Safety risk
- Repeated failures
- Customer impact
- Product/batch evidence
- Returns
- Previous incidents
- Evidence gaps

Outputs:
- Final classification
- Decision rationale
- Recommended action

## Topic 3 — CAPA Planning & Ownership

Creates CAPA actions when the classification requires them.

Inputs:
- Incident ID
- Classification
- Category
- Batch ID

Actions:
- Create containment action.
- Define corrective/preventive recommendations.
- Assign OwnerRole from Owners table.
- Set target date.
- Define validation method.
- Write CAPA_Register.
- Return CAPA summary.

CAPA is triggered for applicable Investigation Required, High-Priority Quality Incident, or Critical Escalation classifications.

## Topic 4 — Reporting & Notification

Completes the investigation communication process.

Actions:
- Generate the Quality Investigation Report using the Word tool.
- Send the Quality Investigation Notification using the Outlook tool when required.

Outputs:
- Investigation report
- Notification status
- Final investigation summary