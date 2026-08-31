# Custom Topics

The PRD defines four mandatory custom topics. These topics are orchestration/control points rather than replacements for the child specialist agents.

## 1. Incident Intake & Validation

### Trigger
Invoked by the Supervisor after the recurrence mechanism identifies an eligible unprocessed record.

### Purpose
Validate the minimum information required before specialist analysis begins.

### Checks
- ComplaintID
- OrderID
- SKU
- BatchID where applicable
- ComplaintDate
- Category
- Severity
- Duplicate/processed state
- Required source-data relationships

### Outcome
`Valid`, `Invalid`, or `Insufficient Evidence`.

An invalid incident must not launch unnecessary specialist analysis.

## 2. Quality Investigation Decision

### Trigger
Invoked after the required specialist findings are available.

### Purpose
Apply the defined quality-policy precedence and produce exactly one internal classification.

### Decision Factors
- Safety override
- Complaint cluster threshold
- Return-rate threshold
- Previous incident history
- Evidence completeness
- CAPA status/overdue condition

### Output
Final classification, supporting rationale, evidence references and next action.

## 3. CAPA Planning & Ownership

### Trigger
Invoked when the final classification requires CAPA.

### Purpose
Translate the quality decision into controlled remediation.

### Actions
- Define containment.
- Define corrective/preventive actions.
- Assign an approved OwnerRole.
- Set target date.
- Define validation method.
- Update CAPA_Register.
- Return the CAPA summary to the Supervisor.

## 4. Evidence Update & Selective Reassessment

### Trigger
Invoked when new evidence materially changes an existing assessment.

### Purpose
Avoid unnecessary full reruns.

### Actions
- Compare new evidence with previous evidence.
- Mark affected specialist findings stale.
- Rerun only affected specialists.
- Preserve unaffected findings.
- Increment ReassessmentCount.
- Re-enter Quality Investigation Decision.

Repeated unresolved reassessment must ultimately move to Manual Review rather than looping indefinitely.
