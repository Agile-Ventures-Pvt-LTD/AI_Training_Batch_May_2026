# Custom Topics

## Overview

The Sleepsia Quality & Customer Experience Intelligence Control Tower implements **four mandatory custom topics** that standardize investigation workflows. Each topic performs a specific business function and returns structured outputs that are consumed by the Quality Supervisor.

---

# Topic 1 – Incident Intake & Validation

## Purpose

Validates incoming incidents before investigation begins by ensuring all mandatory information is available.

## Trigger

- New investigation request
- New customer complaint
- Manual incident submission

## Input Variables

| Variable | Type | Description |
|----------|------|-------------|
| IncidentID | String | Investigation identifier |
| ComplaintID | String | Complaint identifier |
| SKU | String | Product SKU |
| BatchID | String | Manufacturing batch |
| Severity | String | Complaint severity |
| Description | String | Complaint description |

## Decision Branches

| Branch | Action |
|---------|--------|
| Valid | Continue investigation |
| Invalid | Stop workflow |
| Insufficient Evidence | Request missing information |

## Output Variables

| Variable | Type |
|----------|------|
| ValidationStatus | String |
| MissingFields | String |
| CanProceed | Boolean |
| ValidationMessage | String |

---

# Topic 2 – Quality Investigation Decision

## Purpose

Applies deterministic quality rules to classify the investigation based on specialist findings and business rules.

## Trigger

After Topic 1 returns **Valid** and specialist analyses are complete.

## Input Variables

| Variable | Type |
|----------|------|
| ComplaintSeverity | String |
| ComplaintCount | Number |
| ReturnRate | Number |
| SafetyIndicator | Boolean |
| CustomerImpact | String |
| BatchIssueDetected | Boolean |

## Decision Branches

| Branch | Result |
|---------|--------|
| Informational | Close investigation |
| Investigation Required | Continue investigation |
| High-Priority Quality Incident | Escalate and create CAPA |
| Critical Escalation | Immediate escalation and CAPA |

## Output Variables

| Variable | Type |
|----------|------|
| FinalClassification | String |
| EscalationRequired | Boolean |
| CAPARequired | Boolean |
| DecisionReason | String |

---

# Topic 3 – CAPA Planning & Ownership

## Purpose

Generates a Corrective and Preventive Action (CAPA) plan for qualifying investigations.

## Trigger

When Topic 2 indicates:

- Investigation Required
- High-Priority Quality Incident
- Critical Escalation

## Input Variables

| Variable | Type |
|----------|------|
| IncidentID | String |
| FinalClassification | String |
| RootCause | String |
| ProductCategory | String |

## Decision Branches

| Branch | Action |
|---------|--------|
| CAPA Required | Generate CAPA plan |
| CAPA Not Required | Return without action |

## Output Variables

| Variable | Type |
|----------|------|
| CAPAID | String |
| ContainmentAction | String |
| CorrectiveAction | String |
| PreventiveAction | String |
| OwnerRole | String |
| TargetCompletionDate | Date |
| ValidationMethod | String |

---

# Topic 4 – Evidence Update & Selective Reassessment

## Purpose

Processes newly received evidence and determines whether selective reassessment is required.

## Trigger

When additional evidence is submitted after the initial investigation.

## Input Variables

| Variable | Type |
|----------|------|
| IncidentID | String |
| ReassessmentCount | Number |
| HasNewComplaintEvidence | Boolean |
| HasNewReturnsEvidence | Boolean |
| HasNewBatchEvidence | Boolean |
| HasNewCustomerImpactEvidence | Boolean |
| HasNewSafetyEvidence | Boolean |

## Decision Branches

| Branch | Action |
|---------|--------|
| Reassessment Limit Exceeded | Manual Review |
| No New Evidence | Preserve current findings |
| New Evidence Detected | Selective rerun of affected specialists |

## Output Variables

| Variable | Type |
|----------|------|
| ReassessmentCount | Number |
| ShouldRerunSpecialists | Boolean |
| IsMaxReassessmentExceeded | Boolean |
| FinalState | String |
| NextAction | String |
| StaleSpecialists | String |
| PreservedSpecialists | String |
| StatusReason | String |

---

# Topic Integration

| Topic | Invoked By | Next Step |
|--------|------------|-----------|
| Topic 1 – Incident Intake & Validation | Quality Supervisor | Specialist agents |
| Topic 2 – Quality Investigation Decision | Quality Supervisor | Close investigation or Topic 3 |
| Topic 3 – CAPA Planning & Ownership | Quality Supervisor | CAPA approval and record updates |
| Topic 4 – Evidence Update & Selective Reassessment | Quality Supervisor | Selective rerun or Manual Review |

---

# Topic Execution Flow

```text
New Investigation
        │
        ▼
Topic 1
Incident Intake & Validation
        │
        ▼
Specialist Child Agents
        │
        ▼
Topic 2
Quality Investigation Decision
        │
        ├── Informational
        │       │
        │       ▼
        │   Close Investigation
        │
        └── Investigation Required /
            High Priority /
            Critical
                │
                ▼
Topic 3
CAPA Planning & Ownership
                │
                ▼
Update Records
                │
                ▼
New Evidence?
                │
           Yes  ▼
Topic 4
Evidence Update &
Selective Reassessment
                │
                ├── Preserve Findings
                ├── Selective Specialist Rerun
                └── Manual Review
```

## Summary

The four custom topics provide a standardized and reusable investigation framework:

- **Topic 1:** Validates incident data before investigation.
- **Topic 2:** Applies quality decision rules to classify incidents.
- **Topic 3:** Generates CAPA plans for qualifying investigations.
- **Topic 4:** Handles new evidence through selective reassessment with bounded reassessment cycles.