## Overview

The solution implements four mandatory custom topics to ensure a governed, deterministic, and traceable quality investigation workflow. Each topic performs a specific responsibility and passes structured outputs to the next stage of the investigation.

---

# Topic 1 – Incident Intake & Validation

## Purpose

Validate mandatory complaint information before any specialist analysis begins.

## Input Variables

- ComplaintID
- OrderID
- SKU
- BatchID
- ComplaintDate
- Category
- Severity
- SafetyIndicator

## Validation Rules

- ComplaintID exists
- OrderID exists
- SKU exists
- BatchID matches SKU (if provided)
- ComplaintDate is valid
- Category is valid
- Severity is valid
- Duplicate complaint not already processed

## Outputs

- Valid
- Invalid
- Insufficient Evidence

---

# Topic 2 – Quality Investigation Decision

## Purpose

Consolidate specialist findings and assign a single investigation classification using deterministic policy precedence.

## Inputs

- Complaint Pattern Specialist findings
- Returns Specialist findings
- Product/Batch Specialist findings
- Customer Impact Specialist findings
- Safety Specialist findings

## Decision Rules

1. Safety Override
2. Complaint Cluster Threshold
3. Return Rate Threshold
4. Previous Incident History
5. Missing Evidence
6. Overdue CAPA

## Outputs

- No Investigation Required
- Investigation Required
- High-Priority Quality Incident
- Critical Escalation
- Decision Rationale

---

# Topic 3 – CAPA Planning & Ownership

## Purpose

Generate containment, corrective, and preventive actions for investigations requiring CAPA.

## Inputs

- Investigation Classification
- Investigation Findings
- Root Cause
- Evidence Summary

## Activities

- Create CAPA
- Assign Owner
- Set Due Date
- Define Corrective Actions
- Define Preventive Actions
- Update CAPA Register

## Outputs

- CAPA ID
- CAPA Owner
- Action Plan
- Due Date
- CAPA Status

---

# Topic 4 – Evidence Update & Selective Reassessment

## Purpose

Reassess only the affected specialist when new evidence is submitted.

## Inputs

- Complaint ID
- New Evidence
- Updated Documents
- Updated Investigation Data

## Activities

- Identify affected specialist
- Re-execute only that specialist
- Preserve previous valid findings
- Update investigation decision if required

## Outputs

- Updated Findings
- Updated Classification
- Updated Evidence Summary
- Reassessment Status

---

# Topic Flow

```text
Incident Intake & Validation
          │
          ▼
Specialist Investigation
          │
          ▼
Quality Investigation Decision
          │
          ▼
CAPA Planning & Ownership
          │
          ▼
Evidence Update & Selective Reassessment
```

---

# Topic Dependencies

| Topic | Invoked By | Next Step |
|--------|------------|-----------|
| Incident Intake & Validation | Quality Supervisor | Specialist Investigation |
| Quality Investigation Decision | Quality Supervisor | CAPA Planning / Report Generation |
| CAPA Planning & Ownership | Quality Supervisor | Report Generation |
| Evidence Update & Selective Reassessment | Quality Supervisor | Quality Investigation Decision |

---

# Benefits

- Deterministic workflow execution
- Modular topic design
- Reusable business logic
- Clear decision traceability
- Easy maintenance and testing
- Controlled orchestration by the Quality Supervisor