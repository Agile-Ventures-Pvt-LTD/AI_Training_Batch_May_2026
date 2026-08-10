# Custom Topics

## Topic 1 — Incident Intake & Validation

### Purpose
Deterministic validation before specialist analysis.

### Checks
- ComplaintID exists
- OrderID exists
- SKU exists
- SKU exists in Product_Master
- supplied BatchID exists and maps to SKU
- ComplaintDate is valid
- Category exists
- Severity is valid
- complaint has not already been processed

### Outputs
`Valid`, `Invalid`, or `Insufficient Evidence`

Invalid and Insufficient Evidence records must not launch specialist analysis.

## Topic 2 — Specialist Investigation
**Implementation details:** `[Complete with final canvas variables/branches after build]`

Expected behavior:
- accept only Valid intake;
- fan out to five evidence specialists;
- collect outputs;
- preserve missing/unverified evidence;
- pass consolidated evidence to Supervisor decision logic.

## Topic 3 — Quality Decision, CAPA, Reporting & Notification
**Implementation details:** `[Complete with final canvas variables/branches after build]`

Expected behavior:
- apply decision priority;
- invoke CAPA when required;
- prevent duplicate CAPA;
- update incident;
- generate Word report;
- send applicable Outlook notification.

## Topic 4 — Reassessment
**Implementation details:** `[Complete with final canvas variables/branches after build]`

Expected behavior:
- identify IncidentID and changed evidence domain;
- rerun only affected specialist when appropriate;
- preserve unaffected findings;
- recalculate classification;
- update/report/notify when required.

> Final variable names and exact branches must be updated after the four topic canvases are fully tested.
