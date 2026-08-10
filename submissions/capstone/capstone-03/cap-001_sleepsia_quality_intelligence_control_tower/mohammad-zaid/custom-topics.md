# custom-topics.md

# CAP-001 — Custom Topics

## 1. Overview

The solution uses custom topics to control the major stages of the autonomous product-quality workflow.

The four mandatory custom topics are:

1. Incident Intake & Validation
2. Quality Investigation Decision
3. CAPA & Evidence Follow-Up
4. Reassessment Controller

Each topic has a defined responsibility and returns structured information to the Quality Supervisor.

---

## 2. Topic 1 — Incident Intake & Validation

### Purpose

Validates the complaint record before specialist analysis begins.

### Responsibilities

- Validate required complaint identifiers.
- Validate product and batch information where supplied.
- Validate complaint date.
- Validate category and severity.
- Validate processing status.
- Determine whether sufficient information exists for specialist analysis.
- Prevent invalid records from entering the investigation workflow.

### Inputs

| Input | Type | Description |
|---|---|---|
| ComplaintID | Text | Unique complaint identifier. |
| OrderID | Text | Order associated with the complaint. |
| SKU | Text | Product SKU associated with the complaint. |
| BatchID | Text | Batch identifier when supplied. |
| ComplaintDate | DateTime | Complaint record date. |
| Category | Text | Complaint category. |
| Severity | Text | Recorded complaint severity. |
| Processed | Boolean | Indicates whether the complaint has already been processed. |

### Output

| Output | Type | Description |
|---|---|---|
| ValidationOutcome | Text | Validation result: `Valid`, `Invalid`, or `Insufficient Evidence`. |

### Routing

```text
Complaint Record
      |
      ▼
Required Information Check
      |
 ┌────┼──────────────┐
 ▼    ▼              ▼
Invalid  Insufficient   Valid
         Evidence         |
                          ▼
                  Specialist Analysis
```

---

## 3. Topic 2 — Quality Investigation Decision

### Purpose

Consolidates specialist findings and applies the defined quality-decision precedence.

### Responsibilities

* Receive consolidated specialist findings.
* Evaluate safety indicators.
* Evaluate complaint-pattern thresholds.
* Evaluate return-rate findings.
* Evaluate previous incident history.
* Evaluate missing evidence.
* Evaluate overdue CAPA.
* Assign exactly one final quality classification.

### Inputs

| Input | Type | Description |
|--------|--------|-------------|
| SafetyResult | Text | Safety Specialist finding. |
| ComplaintClusterResult | Text | Complaint Pattern Specialist finding. |
| ReturnRateResult | Number | Return-rate result from the Returns Specialist. |
| PreviousIncidentResult | Text | Product-Batch Specialist finding on previous incidents. |
| EvidenceStatus | Text | Indicates whether required evidence is missing. |
| CAPAStatus | Text | Indicates whether an applicable CAPA is overdue. |

### Output

| Output | Type | Description |
|----------|------|-------------|
| Classification | Text | Final quality classification assigned by the Supervisor workflow. |

### Decision Precedence

```text
Safety Indicator
      ↓
Complaint Cluster Threshold
      ↓
Return Rate ≥ 2%
      ↓
Previous Incident / Repeat Failure
      ↓
Missing Evidence
      ↓
Overdue CAPA
      ↓
Final Classification
```

### Possible Classifications

* Critical
* Investigation Required
* High-Priority
* Insufficient Evidence
* Monitoring

The highest-precedence applicable condition controls the final classification.

---

## 4. Topic 3 — CAPA & Evidence Follow-Up

### Purpose

Coordinates corrective/preventive action and evidence follow-up for incidents requiring additional quality action.

### Responsibilities

* Determine whether CAPA action is required.
* Coordinate containment recommendations.
* Coordinate corrective-action recommendations.
* Coordinate preventive-action recommendations.
* Assign an owner role.
* Assign a target date.
* Define the validation method.
* Request missing evidence where required.
* Escalate overdue CAPA.
* Preserve evidence-based root-cause status.

### Inputs

| Input | Type | Description |
|----------|------|-------------|
| Classification | Text | Quality classification from the decision stage. |
| EvidenceStatus | Text | Current evidence status. |
| CAPAStatus | Text | Current CAPA status. |
| IncidentID | Text | Quality incident identifier. |

### Output

| Output | Type | Description |
|------------|------|-------------|
| FollowUpOutcome | Text | Follow-up result for CAPA or evidence handling. |

### Routing

```text
Quality Classification
        |
        ▼
CAPA / Evidence Required?
        |
   ┌────┴────┐
  No        Yes
   │          │
   ▼          ▼
Continue   CAPA / Evidence
              │
              ▼
       Owner + Target Date
              │
              ▼
       Validation Method
              │
              ▼
       Supervisor Review
```

Critical incidents are not independently closed by the CAPA Specialist.

---

## 5. Topic 4 — Reassessment Controller

### Purpose

Controls reassessment when new evidence changes the inputs used by previous specialist analyses.

### Responsibilities

* Detect whether new evidence has been supplied.
* Identify affected specialist results.
* Mark stale specialist results.
* Rerun only the affected specialist analysis.
* Return updated findings to the Supervisor.
* Track automated reassessment cycles.
* Stop automated reassessment after two cycles.
* Route unresolved incidents to Manual Review.

### Inputs

| Input | Type | Description |
|--------|--------|-------------|
| NewEvidence | Text | Newly supplied evidence or evidence update. |
| PreviousClassification | Text | Classification before reassessment. |
| AffectedDomain | Text | Specialist domain affected by the new evidence. |
| ReassessmentCount | Number | Number of automated reassessment cycles already performed. |

### Output

| Output | Type | Description |
|----------|------|-------------|
| ReassessmentOutcome | Text | Result of the reassessment control process. |

### Routing

```text
New Evidence
     |
     ▼
Evidence Changed?
     |
 ┌───┴────┐
 No      Yes
 │        │
 ▼        ▼
Continue  Identify Stale Result
              |
              ▼
       Re-run Affected Specialist
              |
              ▼
        Supervisor Fan-In
              |
              ▼
        Recalculate Decision
              |
              ▼
      Reassessment Count < 2?
           │          │
          Yes        No
           │          │
           ▼          ▼
      Continue      Manual Review
```

---

## 6. Topic Integration

The four topics form the controlled workflow of the Quality Supervisor.

```text
Recurrence Trigger
       |
       ▼
Incident Intake & Validation
       |
       ▼
Specialist Analysis
       |
       ▼
Quality Investigation Decision
       |
       ▼
CAPA & Evidence Follow-Up
       |
       ▼
Reassessment Controller
       |
       ▼
Supervisor Validation
       |
       ▼
Reporting / State Update / Notification
```

Topics are used to make workflow control explicit, deterministic, and traceable.

---

## 7. Topic Governance

All custom topics follow these rules:

1. The Quality Supervisor controls topic invocation.
2. Topics perform only their defined responsibility.
3. Topic outputs are returned as structured values.
4. Specialist findings are not treated as final decisions without Supervisor consolidation.
5. Safety-related findings receive the highest decision precedence.
6. Missing evidence is explicitly represented.
7. Reassessment is selective rather than a complete workflow restart.
8. Automated reassessment is limited to two cycles.
9. Failures are surfaced rather than hidden.
10. No topic may claim an external action succeeded unless the underlying operation succeeded.